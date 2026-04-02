# -*- coding: utf-8 -*-
"""
FastAPI 后端 API 服务
提供效果图生成、邮件发送、PDF生成等功能接口
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path
from datetime import datetime
import os
import sys
import random

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.services.effect_image_service import effect_image_service
from src.services.email_service import email_service
from src.services.database_service import db
from src.services.shipping_service import FourPXClient
from src.services.translation_service import translation_service
from src.services.ai_service import ai_service
from src.config.settings import settings


# 初始化 4PX 物流客户端
fourpx_client = FourPXClient(
    app_key=settings.FOURPX_APP_KEY,
    app_secret=settings.FOURPX_APP_SECRET,
    sandbox=settings.FOURPX_SANDBOX
)


# 创建 FastAPI 应用
app = FastAPI(
    title="ETSY订单自动化 API",
    description="提供效果图生成、邮件发送、PDF生成等功能",
    version="1.0.0"
)

# 字体目录
FONTS_DIR = Path(__file__).parent.parent.parent / "assets" / "fonts"

# 配置 CORS（允许前端跨域调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册客服外链路由
from src.api.service_link_routes import router as service_link_router
app.include_router(service_link_router)


# ============ 工具函数 ============

def scramble_phone(phone: str) -> str:
    """保留电话前面部分，打乱后6位数字（隐私保护）"""
    if not phone or len(phone) < 6:
        # 生成一个假电话
        return f"+1{random.randint(100, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
    digits = list(phone[-6:])
    random.shuffle(digits)
    return phone[:-6] + ''.join(digits)


# ============ 请求模型定义 ============

class EffectImageRequest(BaseModel):
    """效果图生成请求"""
    order_id: str
    shape: str = "bone"  # bone, heart, circle
    color: str = "G"     # G(金色), S(银色), B(黑色)
    size: str = "large"  # large, small
    text_front: str      # 正面文字
    text_back: Optional[str] = ""  # 背面文字
    font_code: str = "F-01"  # 字体代码


class OrderStatusRequest(BaseModel):
    """订单状态更新请求"""
    order_id: str
    status: str  # pending, effect_sent, producing, delivered


class SendEmailRequest(BaseModel):
    """发送邮件请求"""
    order_id: str
    to_email: str
    customer_name: str
    product_info: str = ""
    effect_image_path: Optional[str] = None


class GenerateAllRequest(BaseModel):
    """一键生成效果图+PDF请求"""
    order_id: str  # Supabase UUID


# ============ 物流相关请求模型 ============

class ShippingCreateOrderRequest(BaseModel):
    """创建物流订单请求"""
    order_id: str  # Supabase orders 表的 id
    logistics_product_code: str  # 物流产品代码，如 "U0107600"
    # 收件人信息
    recipient_name: str
    recipient_phone: str
    recipient_email: Optional[str] = ""
    recipient_street: str
    recipient_city: str
    recipient_state: str
    recipient_postcode: str
    recipient_country: str = "US"
    # 包裹信息
    weight_kg: float = 0.03
    declare_value: float = 10.0
    declare_currency: str = "USD"


class ShippingGetLabelRequest(BaseModel):
    """获取物流面单请求"""
    tracking_number: Optional[str] = None
    order_no: Optional[str] = None


class ShippingGetProductsRequest(BaseModel):
    """查询物流产品请求"""
    country_code: str
    postcode: Optional[str] = ""


class ShippingCancelOrderRequest(BaseModel):
    """取消物流订单请求"""
    order_no: str
    reason: Optional[str] = ""


class ShippingQueryOrderRequest(BaseModel):
    """查询物流订单请求"""
    order_no: str


# ============ 邮件模板相关请求模型 ============

class EmailTemplateCreateRequest(BaseModel):
    """创建邮件模板请求"""
    type: str  # first_confirm, modification, follow_up
    template_key: str  # 模板唯一标识
    name: str  # 模板名称
    content: dict  # JSONB 邮件内容
    icon: Optional[str] = None
    description: Optional[str] = None
    subject_zh: Optional[str] = None
    subject_en: Optional[str] = None
    ai_prompt: Optional[str] = None
    sender_name: Optional[str] = None
    style: Optional[str] = None
    is_active: Optional[bool] = True
    sort_order: Optional[int] = 0


class EmailTemplateUpdateRequest(BaseModel):
    """更新邮件模板请求"""
    name: Optional[str] = None
    description: Optional[str] = None
    subject_zh: Optional[str] = None
    subject_en: Optional[str] = None
    content: Optional[dict] = None
    ai_prompt: Optional[str] = None
    sender_name: Optional[str] = None
    style: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


@app.get("/")
async def root():
    """API 根路径"""
    return {"message": "ETSY订单自动化 API", "status": "running"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}


# ============ 字体服务 API ============

@app.get("/fonts/{font_filename}")
async def get_font(font_filename: str):
    """
    获取字体文件（供前端设计器加载）
    
    支持的字体文件：
    - F-01.ttf ~ F-08.ttf（正面字体）
    - back_standard.ttf（背面字体）
    """
    # 安全检查：只允许 .ttf 或 .otf 文件
    if not (font_filename.endswith(".ttf") or font_filename.endswith(".otf")):
        raise HTTPException(status_code=400, detail="只支持 TTF 或 OTF 字体文件")
    
    font_path = FONTS_DIR / font_filename
    
    if not font_path.exists():
        raise HTTPException(status_code=404, detail=f"字体文件不存在: {font_filename}")
    
    # 根据扩展名设置正确的 media_type
    media_type = "font/otf" if font_filename.endswith(".otf") else "font/ttf"
    
    return FileResponse(
        path=str(font_path),
        media_type=media_type,
        filename=font_filename
    )


@app.get("/api/fonts/list")
async def list_fonts():
    """列出所有可用字体"""
    if not FONTS_DIR.exists():
        return {"fonts": [], "error": "字体目录不存在"}
    
    fonts = []
    for f in FONTS_DIR.glob("*.ttf"):
        fonts.append({
            "filename": f.name,
            "name": f.stem
        })
    
    return {"fonts": fonts}


@app.post("/api/effect-image/generate")
async def generate_effect_image(request: EffectImageRequest):
    """
    生成效果图 SVG
    
    参数:
    - order_id: 订单ID
    - shape: 形状 (bone/heart/circle)
    - color: 颜色 (G/S/B)
    - size: 尺寸 (large/small)
    - text_front: 正面文字
    - text_back: 背面文字(可选)
    - font_code: 字体代码
    
    返回:
    - front_svg: 正面SVG文件路径
    - back_svg: 背面SVG文件路径(如有)
    """
    try:
        result = effect_image_service.generate_effect_svg(
            shape=request.shape,
            color=request.color,
            size=request.size,
            text_front=request.text_front,
            text_back=request.text_back,
            font_code=request.font_code,
            order_id=request.order_id
        )
        
        if not result:
            raise HTTPException(status_code=500, detail="效果图生成失败")
        
        front_path, back_path = result
        
        response = {
            "success": True,
            "order_id": request.order_id,
            "front_svg": str(front_path) if front_path else None,
            "back_svg": str(back_path) if back_path else None
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成效果图出错: {str(e)}")


@app.get("/api/effect-image/view/{filename}")
async def view_effect_image(filename: str):
    """查看效果图 SVG 文件"""
    from src.config.settings import settings
    file_path = settings.OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=str(file_path),
        media_type="image/svg+xml",
        filename=filename
    )


@app.post("/api/order/update-status")
async def update_order_status(request: OrderStatusRequest):
    """
    更新订单状态
    
    状态流转:
    - pending -> effect_sent (效果图已发送)
    - effect_sent -> producing (生产中)
    - producing -> delivered (已送达)
    """
    # TODO: 调用 Supabase 更新订单状态
    return {
        "success": True,
        "order_id": request.order_id,
        "new_status": request.status
    }


@app.post("/api/email/send-confirmation")
async def send_confirmation_email(request: SendEmailRequest):
    """
    发送订单确认邮件
    
    参数:
    - order_id: 订单ID
    - to_email: 客户邮箱
    - customer_name: 客户名称
    - product_info: 产品信息
    - effect_image_path: 效果图路径(可选)
    """
    try:
        result = email_service.send_confirmation_email(
            to_email=request.to_email,
            customer_name=request.customer_name,
            order_id=request.order_id,
            product_info=request.product_info,
            effect_image_path=request.effect_image_path
        )
        
        if result['success']:
            return {
                "success": True,
                "order_id": request.order_id,
                "message": result['message']
            }
        else:
            raise HTTPException(status_code=500, detail=result['message'])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"发送邮件失败: {str(e)}")


@app.post("/api/effect-image/generate-and-upload")
async def generate_and_upload_effect(request: GenerateAllRequest):
    """
    一键生成效果图并上传到 Supabase Storage
    将正面和背面 SVG 所有 URL 写入 orders 表
    """
    try:
        order = db.select_one("orders", {"id": request.order_id})
        if not order:
            raise HTTPException(status_code=404, detail="订单不存在")
        result = effect_image_service.generate_and_upload(order)
        if not result:
            raise HTTPException(status_code=500, detail="效果图生成失败")
        return {
            "success": True,
            "order_id": request.order_id,
            "effect_image_url": result.get("effect_image_url"),
            "effect_image_back_url": result.get("effect_image_back_url")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成效果图出错: {str(e)}")


@app.post("/api/pdf/generate-and-upload")
async def generate_and_upload_pdf(request: GenerateAllRequest):
    """
    一键生成生产文档 PDF 并上传到 Supabase Storage
    将 PDF URL 写入 orders.production_pdf_url
    
    数据流：
    1. 查询 orders 表获取基础订单数据
    2. 关联 sku_mapping 表获取 shape/color/size/craft/sku_code
    3. 关联 logistics 表获取物流信息
    4. 关联 production_documents 表获取效果图链接
    5. 调用 svg_pdf_service 生成 PDF
    6. 上传 PDF 到 Supabase Storage
    7. 更新 orders.production_pdf_url
    """
    try:
        from src.services.svg_pdf_service import svg_pdf_service

        # 1. 查询基础订单数据
        order_data = db.select_one("orders", {"id": request.order_id})
        if not order_data:
            raise HTTPException(status_code=404, detail="订单不存在")

        print(f"[DEBUG] 订单基础数据: {order_data}")

        # 2. 关联查询 sku_mapping 表获取产品属性
        sku_id = order_data.get("sku_id")
        if sku_id:
            sku_data = db.select_one("sku_mapping", {"id": sku_id})
            if sku_data:
                print(f"[DEBUG] SKU数据: {sku_data}")
                order_data.update({
                    "sku": sku_data.get("sku_code", ""),
                    "shape": sku_data.get("shape", ""),
                    "color": sku_data.get("color", ""),
                    "size": sku_data.get("size", ""),
                    "craft": sku_data.get("craft", "抛光"),
                    "material": sku_data.get("material", ""),
                })
            else:
                print(f"[WARN] 未找到SKU数据, sku_id={sku_id}")
        else:
            print(f"[WARN] 订单没有关联SKU")

        # 3. 关联查询 logistics 表获取物流信息
        logistics_list = db.select("logistics", {"order_id": request.order_id})
        if logistics_list:
            logistics = logistics_list[0]
            print(f"[DEBUG] 物流数据: {logistics}")
            order_data.update({
                "recipient_name": logistics.get("recipient_name", ""),
                "street_address": logistics.get("street_address", ""),
                "city": logistics.get("city", ""),
                "state_code": logistics.get("state_code", ""),
                "postal_code": logistics.get("postal_code", ""),
                "country": logistics.get("country", ""),
                "tracking_number": logistics.get("tracking_number", ""),
                "label_url": logistics.get("label_url", ""),  # 4PX面单PNG URL
            })
        else:
            print(f"[WARN] 未找到物流数据")

        # 4. 关联查询 production_documents 表获取效果图链接
        prod_docs = db.select("production_documents", {"order_id": request.order_id})
        if prod_docs:
            doc = prod_docs[0]
            print(f"[DEBUG] 生产文档数据: {doc}")
            order_data.update({
                "effect_image_url": doc.get("effect_jpg_url", ""),
                "effect_svg_url": doc.get("effect_svg_url", ""),
                "real_photo_urls": doc.get("real_photo_urls", ""),
            })
        else:
            print(f"[WARN] 未找到生产文档数据")

        # 5. 打印完整数据供调试
        print(f"[DEBUG] 完整订单数据用于PDF生成:")
        for key, value in order_data.items():
            print(f"  {key}: {value}")

        # 6. 生成 PDF
        pdf_path = svg_pdf_service.generate_from_raw_data(order_data)
        if not pdf_path:
            raise HTTPException(status_code=500, detail="PDF 生成失败")

        # 7. 上传 PDF
        dest_name = f"{order_data.get('etsy_order_id') or request.order_id}.pdf"
        pdf_url = db.upload_file("production-docs", pdf_path, dest_name)
        if pdf_url:
            db.update("orders", {"id": request.order_id}, {"production_pdf_url": pdf_url})

        return {
            "success": True,
            "order_id": request.order_id,
            "production_pdf_url": pdf_url
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"[ERROR] PDF生成出错: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"PDF 生成出错: {str(e)}")


# ============ 物流服务 API ============

@app.post("/api/shipping/create-order")
async def create_shipping_order(request: ShippingCreateOrderRequest):
    """
    创建物流订单（4PX直发）
    
    流程：
    1. 从Supabase查询订单信息
    2. 自动获取SKU重量（从sku_mapping.weight_g）
    3. 自动补充收件人地址（从orders.shipping_*字段）
    4. 构造4PX API参数
    5. 调用4PX创建订单
    6. 更新数据库（logistics + orders）
    """
    try:
        # 1. 查询订单信息
        order = db.select_one("orders", {"id": request.order_id})
        if not order:
            return JSONResponse(
                {"success": False, "message": "订单不存在", "data": None},
                status_code=404
            )
        
        etsy_order_id = order.get("etsy_order_id", request.order_id)
        
        # 2. 查询SKU信息（包含重量weight_g）
        sku_data = {}
        sku_id = order.get("sku_id")
        if sku_id:
            sku_info = db.select_one("sku_mapping", {"id": sku_id})
            if sku_info:
                sku_data = sku_info
        
        # 3. 重量处理：优先使用前端传值，其次使用SKU重量，默认30g
        weight_kg = request.weight_kg
        if weight_kg <= 0 or weight_kg == 0.03:  # 默认值检测
            sku_weight_g = sku_data.get("weight_g", 0)
            if sku_weight_g and sku_weight_g > 0:
                weight_kg = sku_weight_g / 1000.0  # 克转千克
                print(f"[INFO] 使用SKU重量: {sku_weight_g}g -> {weight_kg}kg")
            else:
                weight_kg = 0.03  # 默认30g = 0.03kg
                print(f"[INFO] 使用默认重量: 30g")
        
        # 4. 收件人信息处理：优先使用前端传值，其次从orders表shipping_*字段补充
        recipient_name = request.recipient_name or order.get("shipping_name") or order.get("customer_name") or ""
        recipient_street = request.recipient_street or order.get("shipping_address_line1") or ""
        recipient_city = request.recipient_city or order.get("shipping_city") or ""
        recipient_state = request.recipient_state or order.get("shipping_state") or ""
        recipient_postcode = request.recipient_postcode or order.get("shipping_zip") or ""
        recipient_country = request.recipient_country or order.get("shipping_country") or order.get("country") or "US"
        
        # 5. 电话隐私处理（4PX必填）
        scrambled_phone = scramble_phone(request.recipient_phone)
        
        # 6. 构造4PX订单数据（严格按照官方API文档格式）
        # 重量转换：千克 -> 克（整数）
        weight_g = int(weight_kg * 1000)
        if weight_g < 1:
            weight_g = 27  # 默认27克
        
        fourpx_order_data = {
            "ref_no": etsy_order_id,
            "business_type": "BDS",
            "duty_type": "P",
            "logistics_service_info": {
                "logistics_product_code": request.logistics_product_code
            },
            "parcel_list": [{
                "weight": weight_g,  # 重量单位：克（整数）
                "parcel_value": request.declare_value,  # 申报总价值
                "currency": request.declare_currency,  # 申报币种
                "include_battery": "N",
                "declare_product_info": [{
                    "declare_product_name_cn": "不锈钢宠物牌",
                    "declare_product_name_en": "Stainless Steel Pet Tag",
                    "declare_product_code_qty": str(order.get("quantity", 1)),
                    "declare_unit_price_export": request.declare_value,
                    "currency_export": request.declare_currency,
                    "declare_unit_price_import": request.declare_value,
                    "currency_import": request.declare_currency,
                    "brand_export": "",
                    "brand_import": ""
                }]
            }],
            "is_insure": "N",
            "sender": {
                "first_name": settings.EMAIL_ADDRESS.split("@")[0] if settings.EMAIL_ADDRESS else "Etsy Seller",
                "company": "Etsy Shop",
                "phone": "13800138000",
                "post_code": "518000",
                "country": "CN",
                "state": "GuangDong",
                "city": "Shenzhen",
                "street": "Nanshan District Road 1"
            },
            "recipient_info": {
                "first_name": recipient_name,
                "phone": scrambled_phone,
                "email": request.recipient_email or order.get("customer_email") or "",
                "country": recipient_country,
                "state": recipient_state,
                "city": recipient_city,
                "street": recipient_street,
                "post_code": recipient_postcode
            },
            "deliver_type_info": {
                "deliver_type": "2"  # 快递到仓
            }
        }
        
        # 7. 调用4PX创建订单
        result = fourpx_client.create_order(fourpx_order_data)
        
        if result.get("result") != "1":
            error_msg = result.get("msg") or result.get("error") or "4PX API调用失败"
            return JSONResponse(
                {"success": False, "message": error_msg, "data": result},
                status_code=400
            )
        
        # 8. 提取返回数据
        response_data = result.get("data", {})
        tracking_number = response_data.get("4px_tracking_no") or response_data.get("logistics_order_no", "")
        order_no = response_data.get("order_no", "")
        
        # 9. 获取面单URL
        label_url = ""
        if tracking_number:
            label_result = fourpx_client.get_label(tracking_number)
            if label_result.get("result") == "1":
                label_data = label_result.get("data", {})
                label_url_info = label_data.get("label_url_info", {})
                label_url = label_url_info.get("logistics_label", "")
        
        # 10. 更新logistics表
        logistics_list = db.select("logistics", {"order_id": request.order_id})
        logistics_update = {
            "tracking_number": tracking_number,
            "label_url": label_url,
            "state_code": recipient_state,
            "delivery_status": "shipped",
            "shipped_at": datetime.now().isoformat()
        }
        
        try:
            if logistics_list:
                db.update("logistics", {"order_id": request.order_id}, logistics_update)
            else:
                logistics_insert = {
                    "order_id": request.order_id,
                    "recipient_name": recipient_name,
                    "country": recipient_country,
                    "city": recipient_city,
                    "street_address": recipient_street,
                    "postal_code": recipient_postcode,
                    **logistics_update
                }
                db.insert("logistics", logistics_insert)
        except Exception as logistics_err:
            print(f"[WARN] logistics表更新失败（可忽略）: {logistics_err}")
            # logistics更新失败不阻断主流程，只保存核心字段
            try:
                core_update = {"tracking_number": tracking_number, "label_url": label_url}
                if logistics_list:
                    db.update("logistics", {"order_id": request.order_id}, core_update)
                else:
                    db.insert("logistics", {"order_id": request.order_id, "recipient_name": recipient_name, "tracking_number": tracking_number, "label_url": label_url})
            except Exception as e2:
                print(f"[WARN] logistics核心字段保存也失败: {e2}")
        
        # 11. 更新订单状态（无论logistics是否成功，状态必须更新）
        db.update("orders", {"id": request.order_id}, {"status": "producing"})
        
        # 12. 自动生成生产文档PDF（异步触发，不阻断响应）
        production_pdf_url = ""
        try:
            from src.services.svg_pdf_service import svg_pdf_service
            # 重新查询完整订单数据
            order_full = db.select_one("orders", {"id": request.order_id}) or order
            # 补充SKU数据
            if sku_data:
                order_full.update({
                    "sku": sku_data.get("sku_code", ""),
                    "shape": sku_data.get("shape", ""),
                    "color": sku_data.get("color", ""),
                    "size": sku_data.get("size", ""),
                    "craft": sku_data.get("craft", "抛光"),
                    "material": sku_data.get("material", ""),
                })
            # 补充物流数据（刚写入的）
            order_full.update({
                "recipient_name": recipient_name,
                "street_address": recipient_street,
                "city": recipient_city,
                "state_code": recipient_state,
                "postal_code": recipient_postcode,
                "country": recipient_country,
                "tracking_number": tracking_number,
                "label_url": label_url,
            })
            # 补充效果图数据
            prod_docs = db.select("production_documents", {"order_id": request.order_id})
            if prod_docs:
                doc = prod_docs[0]
                order_full.update({
                    "effect_image_url": doc.get("effect_jpg_url", ""),
                    "effect_svg_url": doc.get("effect_svg_url", ""),
                    "real_photo_urls": doc.get("real_photo_urls", ""),
                })
            # 生成PDF
            pdf_path = svg_pdf_service.generate_from_raw_data(order_full)
            if pdf_path:
                dest_name = f"{order_full.get('etsy_order_id') or request.order_id}.pdf"
                production_pdf_url = db.upload_file("production-docs", pdf_path, dest_name) or ""
                if production_pdf_url:
                    db.update("orders", {"id": request.order_id}, {"production_pdf_url": production_pdf_url})
                    print(f"[INFO] 生产文档PDF自动生成成功: {production_pdf_url}")
        except Exception as pdf_err:
            print(f"[WARN] 生产文档PDF自动生成失败（不影响主流程）: {pdf_err}")
        
        return JSONResponse({
            "success": True,
            "message": "物流订单创建成功",
            "data": {
                "order_no": order_no,
                "tracking_number": tracking_number,
                "label_url": label_url,
                "production_pdf_url": production_pdf_url,
                "weight_used_kg": weight_kg,
                "4px_response": response_data
            }
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"success": False, "message": str(e), "data": None},
            status_code=500
        )


@app.post("/api/shipping/get-label")
async def get_shipping_label(request: ShippingGetLabelRequest):
    """
    获取物流面单
    
    参数：tracking_number 或 order_no
    """
    try:
        request_no = request.tracking_number or request.order_no
        if not request_no:
            return JSONResponse(
                {"success": False, "message": "请提供 tracking_number 或 order_no", "data": None},
                status_code=400
            )
        
        result = fourpx_client.get_label(request_no)
        
        if result.get("result") != "1":
            error_msg = result.get("msg") or "获取面单失败"
            return JSONResponse(
                {"success": False, "message": error_msg, "data": result},
                status_code=400
            )
        
        label_data = result.get("data", {})
        label_url_info = label_data.get("label_url_info", {})
        label_url = label_url_info.get("logistics_label", "")
        
        return JSONResponse({
            "success": True,
            "message": "获取面单成功",
            "data": {
                "label_url": label_url,
                "raw_response": label_data
            }
        })
        
    except Exception as e:
        return JSONResponse(
            {"success": False, "message": str(e), "data": None},
            status_code=500
        )


@app.post("/api/shipping/get-products")
async def get_shipping_products(request: ShippingGetProductsRequest):
    """
    查询可用物流产品
    
    参数：country_code (必填), postcode (可选)
    返回：最多10个物流渠道
    """
    try:
        result = fourpx_client.get_logistics_products(
            country_code=request.country_code,
            postcode=request.postcode or ""
        )
        
        if result.get("result") != "1":
            error_msg = result.get("msg") or "查询物流产品失败"
            return JSONResponse(
                {"success": False, "message": error_msg, "data": result},
                status_code=400
            )
        
        products = result.get("data", [])
        
        # 限制返回最多10个渠道
        if isinstance(products, list):
            products = products[:10]
        
        return JSONResponse({
            "success": True,
            "message": f"查询到 {len(products) if isinstance(products, list) else 0} 个物流渠道",
            "data": {
                "products": products
            }
        })
        
    except Exception as e:
        return JSONResponse(
            {"success": False, "message": str(e), "data": None},
            status_code=500
        )


@app.post("/api/shipping/cancel-order")
async def cancel_shipping_order(request: ShippingCancelOrderRequest):
    """
    取消物流订单
    
    参数：order_no (4PX订单号), reason (取消原因)
    """
    try:
        result = fourpx_client.cancel_order(
            request_no=request.order_no,
            cancel_reason=request.reason or "客户取消订单"
        )
        
        if result.get("result") != "1":
            error_msg = result.get("msg") or "取消订单失败"
            return JSONResponse(
                {"success": False, "message": error_msg, "data": result},
                status_code=400
            )
        
        return JSONResponse({
            "success": True,
            "message": "订单取消成功",
            "data": result.get("data")
        })
        
    except Exception as e:
        return JSONResponse(
            {"success": False, "message": str(e), "data": None},
            status_code=500
        )


@app.post("/api/shipping/query-order")
async def query_shipping_order(request: ShippingQueryOrderRequest):
    """
    查询物流订单状态
    
    参数：order_no (4PX订单号)
    """
    try:
        result = fourpx_client.query_order(order_no=request.order_no)
        
        if result.get("result") != "1":
            error_msg = result.get("msg") or "查询订单失败"
            return JSONResponse(
                {"success": False, "message": error_msg, "data": result},
                status_code=400
            )
        
        return JSONResponse({
            "success": True,
            "message": "查询成功",
            "data": result.get("data")
        })
        
    except Exception as e:
        return JSONResponse(
            {"success": False, "message": str(e), "data": None},
            status_code=500
        )


# ==================== 邮件模板 API ====================

@app.get("/api/email-templates")
async def get_all_email_templates(is_active: Optional[str] = None):
    """
    获取所有邮件模板（按type分组返回）
    
    Query参数:
    - is_active: 可选，过滤是否启用的模板 ("true"/"false")
    
    返回格式:
    {
        "success": true,
        "data": {
            "first_confirm": [...],
            "modification": [...],
            "follow_up": [...]
        }
    }
    """
    try:
        # 构建查询条件
        filters = {}
        if is_active is not None:
            if is_active.lower() == "true":
                filters["is_active"] = True
            elif is_active.lower() == "false":
                filters["is_active"] = False
        
        # 查询所有模板，按 sort_order 排序
        templates = db.supabase.table("email_templates").select("*").order("sort_order").execute()
        
        if not templates.data:
            return {"success": True, "data": {"first_confirm": [], "modification": [], "follow_up": []}}
        
        # 按类型分组
        grouped = {
            "first_confirm": [],
            "modification": [],
            "follow_up": []
        }
        
        for tpl in templates.data:
            tpl_type = tpl.get("type", "")
            # 应用过滤条件
            if is_active is not None:
                if is_active.lower() == "true" and not tpl.get("is_active", True):
                    continue
                if is_active.lower() == "false" and tpl.get("is_active", True):
                    continue
            
            if tpl_type in grouped:
                grouped[tpl_type].append(tpl)
        
        return {"success": True, "data": grouped}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"success": False, "message": f"获取模板列表失败: {str(e)}", "data": None},
            status_code=500
        )


@app.get("/api/email-templates/{template_type}")
async def get_email_templates_by_type(template_type: str):
    """
    获取指定类型的模板列表
    
    路径参数:
    - template_type: 模板类型 (first_confirm / modification / follow_up)
    
    返回格式:
    {
        "success": true,
        "data": [...]
    }
    """
    try:
        valid_types = ["first_confirm", "modification", "follow_up"]
        if template_type not in valid_types:
            return JSONResponse(
                {"success": False, "message": f"无效的模板类型，有效值: {', '.join(valid_types)}", "data": None},
                status_code=400
            )
        
        result = db.supabase.table("email_templates").select("*").eq("type", template_type).order("sort_order").execute()
        
        return {"success": True, "data": result.data or []}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"success": False, "message": f"获取模板列表失败: {str(e)}", "data": None},
            status_code=500
        )


@app.post("/api/email-templates")
async def create_email_template(request: EmailTemplateCreateRequest):
    """
    创建新邮件模板
    
    必填字段: type, template_key, name, content
    
    返回格式:
    {
        "success": true,
        "data": {...}
    }
    """
    try:
        # 检查 (type, template_key) 是否已存在
        existing = db.supabase.table("email_templates").select("id").eq("type", request.type).eq("template_key", request.template_key).execute()
        
        if existing.data:
            return JSONResponse(
                {"success": False, "message": f"模板已存在: type={request.type}, template_key={request.template_key}", "data": None},
                status_code=400
            )
        
        # 构建插入数据
        insert_data = {
            "type": request.type,
            "template_key": request.template_key,
            "name": request.name,
            "content": request.content,
            "icon": request.icon,
            "description": request.description,
            "subject_zh": request.subject_zh,
            "subject_en": request.subject_en,
            "ai_prompt": request.ai_prompt,
            "sender_name": request.sender_name,
            "style": request.style,
            "is_active": request.is_active if request.is_active is not None else True,
            "sort_order": request.sort_order if request.sort_order is not None else 0
        }
        
        result = db.supabase.table("email_templates").insert(insert_data).execute()
        
        if result.data:
            return {"success": True, "data": result.data[0]}
        else:
            return JSONResponse(
                {"success": False, "message": "创建模板失败", "data": None},
                status_code=500
            )
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"success": False, "message": f"创建模板失败: {str(e)}", "data": None},
            status_code=500
        )


@app.put("/api/email-templates/{template_id}")
async def update_email_template(template_id: str, request: EmailTemplateUpdateRequest):
    """
    更新邮件模板内容
    
    自动更新 updated_at 为当前时间
    
    返回格式:
    {
        "success": true,
        "data": {...}
    }
    """
    try:
        # 检查模板是否存在
        existing = db.supabase.table("email_templates").select("*").eq("id", template_id).execute()
        
        if not existing.data:
            return JSONResponse(
                {"success": False, "message": "模板不存在", "data": None},
                status_code=404
            )
        
        # 构建更新数据（只更新非None字段）
        update_data = {"updated_at": datetime.now().isoformat()}
        
        if request.name is not None:
            update_data["name"] = request.name
        if request.description is not None:
            update_data["description"] = request.description
        if request.subject_zh is not None:
            update_data["subject_zh"] = request.subject_zh
        if request.subject_en is not None:
            update_data["subject_en"] = request.subject_en
        if request.content is not None:
            update_data["content"] = request.content
        if request.ai_prompt is not None:
            update_data["ai_prompt"] = request.ai_prompt
        if request.sender_name is not None:
            update_data["sender_name"] = request.sender_name
        if request.style is not None:
            update_data["style"] = request.style
        if request.is_active is not None:
            update_data["is_active"] = request.is_active
        if request.sort_order is not None:
            update_data["sort_order"] = request.sort_order
        
        result = db.supabase.table("email_templates").update(update_data).eq("id", template_id).execute()
        
        if result.data:
            return {"success": True, "data": result.data[0]}
        else:
            return JSONResponse(
                {"success": False, "message": "更新模板失败", "data": None},
                status_code=500
            )
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"success": False, "message": f"更新模板失败: {str(e)}", "data": None},
            status_code=500
        )


@app.delete("/api/email-templates/{template_id}")
async def delete_email_template(template_id: str):
    """
    删除邮件模板
    
    返回格式:
    {
        "success": true,
        "message": "模板已删除"
    }
    """
    try:
        # 检查模板是否存在
        existing = db.supabase.table("email_templates").select("id").eq("id", template_id).execute()
        
        if not existing.data:
            return JSONResponse(
                {"success": False, "message": "模板不存在", "data": None},
                status_code=404
            )
        
        # 执行删除
        db.supabase.table("email_templates").delete().eq("id", template_id).execute()
        
        return {"success": True, "message": "模板已删除"}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"success": False, "message": f"删除模板失败: {str(e)}", "data": None},
            status_code=500
        )


# ==================== 工厂管理 API ====================

class FactoryCreateRequest(BaseModel):
    """创建工厂请求"""
    name: str
    code: str
    password_hash: Optional[str] = ""
    status: Optional[str] = "active"
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    access_url: Optional[str] = None


class FactoryUpdateRequest(BaseModel):
    """更新工厂请求"""
    name: Optional[str] = None
    code: Optional[str] = None
    password_hash: Optional[str] = None
    status: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    access_url: Optional[str] = None


class FactoryVerifyPasswordRequest(BaseModel):
    """验证工厂密码请求"""
    code: str
    password: str


@app.get("/api/factories")
async def get_all_factories():
    """
    获取所有工厂列表
    
    返回格式:
    {
        "success": true,
        "data": [...]
    }
    """
    try:
        result = db.supabase.table("factories").select("*").order("created_at", desc=True).execute()
        
        return {"success": True, "data": result.data or []}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"success": False, "message": f"获取工厂列表失败: {str(e)}", "data": None},
            status_code=500
        )


@app.post("/api/factories")
async def create_factory(request: FactoryCreateRequest):
    """
    创建新工厂
    
    必填字段: name, code
    
    返回格式:
    {
        "success": true,
        "data": {...}
    }
    """
    try:
        # 检查 code 是否已存在
        existing = db.supabase.table("factories").select("id").eq("code", request.code).execute()
        
        if existing.data:
            return JSONResponse(
                {"success": False, "message": f"工厂代码已存在: {request.code}", "data": None},
                status_code=400
            )
        
        # 构建插入数据
        insert_data = {
            "name": request.name,
            "code": request.code,
            "password_hash": request.password_hash or "",
            "status": request.status or "active",
            "contact_name": request.contact_name,
            "contact_phone": request.contact_phone,
            "address": request.address,
            "access_url": request.access_url
        }
        
        result = db.supabase.table("factories").insert(insert_data).execute()
        
        if result.data:
            return {"success": True, "data": result.data[0], "message": "工厂创建成功"}
        else:
            return JSONResponse(
                {"success": False, "message": "创建工厂失败", "data": None},
                status_code=500
            )
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"success": False, "message": f"创建工厂失败: {str(e)}", "data": None},
            status_code=500
        )


@app.put("/api/factories/{factory_id}")
async def update_factory(factory_id: str, request: FactoryUpdateRequest):
    """
    更新工厂信息
    
    自动更新 updated_at 为当前时间
    
    返回格式:
    {
        "success": true,
        "data": {...}
    }
    """
    try:
        # 检查工厂是否存在
        existing = db.supabase.table("factories").select("*").eq("id", factory_id).execute()
        
        if not existing.data:
            return JSONResponse(
                {"success": False, "message": "工厂不存在", "data": None},
                status_code=404
            )
        
        # 构建更新数据（只更新非None字段）
        update_data = {}
        
        if request.name is not None:
            update_data["name"] = request.name
        if request.code is not None:
            # 检查新code是否已被其他工厂使用
            code_check = db.supabase.table("factories").select("id").eq("code", request.code).neq("id", factory_id).execute()
            if code_check.data:
                return JSONResponse(
                    {"success": False, "message": f"工厂代码已被使用: {request.code}", "data": None},
                    status_code=400
                )
            update_data["code"] = request.code
        if request.password_hash is not None:
            update_data["password_hash"] = request.password_hash
        if request.status is not None:
            update_data["status"] = request.status
        if request.contact_name is not None:
            update_data["contact_name"] = request.contact_name
        if request.contact_phone is not None:
            update_data["contact_phone"] = request.contact_phone
        if request.address is not None:
            update_data["address"] = request.address
        if request.access_url is not None:
            update_data["access_url"] = request.access_url
        
        if not update_data:
            return JSONResponse(
                {"success": False, "message": "没有需要更新的字段", "data": None},
                status_code=400
            )
        
        result = db.supabase.table("factories").update(update_data).eq("id", factory_id).execute()
        
        if result.data:
            return {"success": True, "data": result.data[0], "message": "工厂更新成功"}
        else:
            return JSONResponse(
                {"success": False, "message": "更新工厂失败", "data": None},
                status_code=500
            )
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"success": False, "message": f"更新工厂失败: {str(e)}", "data": None},
            status_code=500
        )


@app.delete("/api/factories/{factory_id}")
async def delete_factory(factory_id: str):
    """
    删除工厂
    
    返回格式:
    {
        "success": true,
        "message": "工厂已删除"
    }
    """
    try:
        # 检查工厂是否存在
        existing = db.supabase.table("factories").select("id").eq("id", factory_id).execute()
        
        if not existing.data:
            return JSONResponse(
                {"success": False, "message": "工厂不存在", "data": None},
                status_code=404
            )
        
        # 执行删除
        db.supabase.table("factories").delete().eq("id", factory_id).execute()
        
        return {"success": True, "message": "工厂已删除"}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"success": False, "message": f"删除工厂失败: {str(e)}", "data": None},
            status_code=500
        )


@app.post("/api/factories/verify-password")
async def verify_factory_password(request: FactoryVerifyPasswordRequest):
    """
    验证工厂密码（用于工厂协作平台登录）
    
    参数:
    - code: 工厂代码
    - password: 访问密码
    
    返回格式:
    {
        "success": true,
        "data": {
            "valid": true/false,
            "factory": {...}
        }
    }
    """
    try:
        # 查询工厂
        result = db.supabase.table("factories").select("*").eq("code", request.code).execute()
        
        if not result.data:
            return {
                "success": True,
                "data": {
                    "valid": False,
                    "message": "工厂不存在"
                }
            }
        
        factory = result.data[0]
        
        # 检查状态
        if factory.get("status") != "active":
            return {
                "success": True,
                "data": {
                    "valid": False,
                    "message": "工厂已停用"
                }
            }
        
        # 验证密码
        if factory.get("password_hash") == request.password:
            return {
                "success": True,
                "data": {
                    "valid": True,
                    "factory": {
                        "id": factory["id"],
                        "name": factory["name"],
                        "code": factory["code"]
                    }
                }
            }
        else:
            return {
                "success": True,
                "data": {
                    "valid": False,
                    "message": "密码错误"
                }
            }
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"success": False, "message": f"验证失败: {str(e)}", "data": None},
            status_code=500
        )


# ==================== 翻译 API ====================

class TranslateRequest(BaseModel):
    """翻译请求模型"""
    text: str
    source_lang: str = "zh"
    target_lang: str = "en"


class TranslateEmailRequest(BaseModel):
    """邮件翻译请求模型"""
    chinese_content: str


class AIGenerateEmailRequest(BaseModel):
    """AI生成邮件请求模型"""
    scene: str  # first_confirm / modify_confirm / review_request
    customer_name: str
    product_name: str = "Custom Pet Tag"
    front_text: Optional[str] = ""
    back_text: Optional[str] = ""
    shape: str = "Heart"
    color: str = "Gold"
    size: str = "Small"
    tone: str = "friendly"  # friendly / professional / warm
    length: str = "standard"  # short / standard / detailed
    sender_name: str = "Customer Support Team"
    modify_reason: Optional[str] = None  # 仅 modify_confirm 场景需要
    customer_request: Optional[str] = None  # 客户修改要求原始文本
    operator_note: Optional[str] = None  # 运营填写的修改完成说明
    effect_image_url: Optional[str] = None


@app.post("/api/translate")
async def translate_text(request: TranslateRequest):
    """
    通用翻译接口
    
    请求示例:
    {
        "text": "你好世界",
        "source_lang": "zh",
        "target_lang": "en"
    }
    """
    try:
        if not request.text.strip():
            return JSONResponse(
                {"success": False, "message": "翻译文本不能为空", "data": None},
                status_code=400
            )
        
        result = translation_service.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        if result:
            return {
                "success": True,
                "message": "翻译成功",
                "data": {
                    "translated_text": result,
                    "source_lang": request.source_lang,
                    "target_lang": request.target_lang
                }
            }
        else:
            return JSONResponse(
                {"success": False, "message": "翻译失败，请检查API配置", "data": None},
                status_code=500
            )
            
    except Exception as e:
        return JSONResponse(
            {"success": False, "message": f"翻译服务异常: {str(e)}", "data": None},
            status_code=500
        )


@app.post("/api/translate/email")
async def translate_email(request: TranslateEmailRequest):
    """
    邮件专用翻译接口（中文 -> 英文）
    
    请求示例:
    {
        "chinese_content": "亲爱的客户，感谢您的订单..."
    }
    """
    try:
        if not request.chinese_content.strip():
            return JSONResponse(
                {"success": False, "message": "邮件内容不能为空", "data": None},
                status_code=400
            )
        
        result = translation_service.translate_email(
            chinese_content=request.chinese_content
        )
        
        if result:
            return {
                "success": True,
                "message": "邮件翻译成功",
                "data": {
                    "english_content": result
                }
            }
        else:
            return JSONResponse(
                {"success": False, "message": "翻译失败，请检查API配置", "data": None},
                status_code=500
            )
            
    except Exception as e:
        return JSONResponse(
            {"success": False, "message": f"翻译服务异常: {str(e)}", "data": None},
            status_code=500
        )


# ==================== AI 邮件生成 API ====================

@app.get("/api/ai/status")
async def get_ai_status():
    """
    获取AI服务状态
    
    返回格式:
    {
        "success": true,
        "data": {
            "ai_available": true/false,
            "provider": "zhipu"/null,
            "model": "glm-4-flash",
            "supported_scenes": {...},
            "supported_tones": {...}
        }
    }
    """
    try:
        return {
            "success": True,
            "data": {
                "ai_available": ai_service.is_ai_available(),
                "provider": ai_service.available_provider,
                "model": ai_service.model if ai_service.is_ai_available() else None,
                "supported_scenes": ai_service.get_supported_scenes(),
                "supported_tones": ai_service.get_supported_tones()
            }
        }
    except Exception as e:
        return JSONResponse(
            {"success": False, "message": f"获取AI状态失败: {str(e)}", "data": None},
            status_code=500
        )


@app.post("/api/ai/generate-email")
async def ai_generate_email(request: AIGenerateEmailRequest):
    """
    AI生成邮件内容
    
    三种场景:
    - first_confirm: 首封确认邮件 - 效果图制作完成，请客户确认设计
    - modify_confirm: 修改确认邮件 - 按客户要求修改后，请再次确认
    - review_request: 追评邮件 - 订单完成后邀请客户留下好评
    
    请求示例:
    {
        "scene": "first_confirm",
        "customer_name": "Ellie Boon",
        "product_name": "Custom Heart Pet ID Tag",
        "front_text": "Dolly",
        "back_text": "07957 183676",
        "shape": "Heart",
        "color": "Gold",
        "size": "Small",
        "tone": "friendly",
        "sender_name": "HeritageHound Team",
        "effect_image_url": "https://xxx.supabase.co/xxx.svg"
    }
    
    返回格式:
    {
        "success": true,
        "data": {
            "subject": "Your Custom Heart Pet ID Tag is Ready! 🐾",
            "body": "Dear Ellie,\n\nThank you for your order...",
            "scene": "first_confirm",
            "generated_by": "ai" / "template"
        }
    }
    """
    try:
        # 参数校验
        valid_scenes = ["first_confirm", "modify_confirm", "review_request"]
        if request.scene not in valid_scenes:
            return JSONResponse(
                {"success": False, "message": f"无效的场景类型，有效值: {', '.join(valid_scenes)}", "data": None},
                status_code=400
            )
        
        valid_tones = ["friendly", "professional", "warm"]
        if request.tone not in valid_tones:
            return JSONResponse(
                {"success": False, "message": f"无效的语气风格，有效值: {', '.join(valid_tones)}", "data": None},
                status_code=400
            )
        
        valid_lengths = ["short", "standard", "detailed"]
        if request.length not in valid_lengths:
            return JSONResponse(
                {"success": False, "message": f"无效的长度类型，有效值: {', '.join(valid_lengths)}", "data": None},
                status_code=400
            )
        
        # modify_confirm 场景需要 modify_reason
        if request.scene == "modify_confirm" and not request.modify_reason:
            return JSONResponse(
                {"success": False, "message": "modify_confirm 场景需要提供 modify_reason 参数", "data": None},
                status_code=400
            )
        
        # 构建参数
        params = {
            "scene": request.scene,
            "customer_name": request.customer_name,
            "product_name": request.product_name,
            "front_text": request.front_text or "",
            "back_text": request.back_text or "",
            "shape": request.shape,
            "color": request.color,
            "size": request.size,
            "tone": request.tone,
            "length": request.length,
            "sender_name": request.sender_name,
            "effect_image_url": request.effect_image_url
        }
        
        # modify_confirm 场景添加修改相关信息
        if request.scene == "modify_confirm":
            if request.modify_reason:
                params["modify_reason"] = request.modify_reason
            if request.customer_request:
                params["customer_request"] = request.customer_request
            if request.operator_note:
                params["operator_note"] = request.operator_note
        
        # 调用AI服务生成邮件
        result = ai_service.generate_email(params)
        
        # 构建返回格式，包含中英文内容
        response_data = {
            "subject": result.get("subject", ""),
            "body": result.get("body", ""),
            "chinese_content": result.get("body", ""),  # AI生成的是英文，但按接口规范提供字段
            "english_content": result.get("body", ""),
            "scene": result.get("scene", request.scene),
            "generated_by": result.get("generated_by", "template")
        }
        
        return {
            "success": True,
            "data": response_data
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"success": False, "message": f"邮件生成失败: {str(e)}", "data": None},
            status_code=500
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
