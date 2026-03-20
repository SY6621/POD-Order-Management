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
    2. 构造4PX API参数
    3. 调用4PX创建订单
    4. 更新数据库（logistics + orders）
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
        
        # 2. 查询SKU信息
        sku_data = {}
        sku_id = order.get("sku_id")
        if sku_id:
            sku_info = db.select_one("sku_mapping", {"id": sku_id})
            if sku_info:
                sku_data = sku_info
        
        # 3. 电话隐私处理
        scrambled_phone = scramble_phone(request.recipient_phone)
        
        # 4. 构造4PX订单数据
        fourpx_order_data = {
            "ref_no": etsy_order_id,
            "business_type": "BDS",
            "logistics_product_code": request.logistics_product_code,
            "parcel_list": [{
                "weight": request.weight_kg,
                "declare_product_info": [{
                    "declare_product_name_cn": "不锈钢宠物牌",
                    "declare_product_name_en": "Stainless Steel Pet ID Tag",
                    "declare_product_code": sku_data.get("sku_code", "B-E01B"),
                    "declare_unit_price_export": request.declare_value,
                    "currency_export": request.declare_currency,
                    "qty": order.get("quantity", 1)
                }]
            }],
            "deliver_type": "2",
            "duty_type": "P",
            "include_battery": "N",
            "recipient_info": {
                "recipient_name": request.recipient_name,
                "recipient_phone": scrambled_phone,
                "recipient_email": request.recipient_email or "",
                "recipient_country": request.recipient_country,
                "recipient_state": request.recipient_state,
                "recipient_city": request.recipient_city,
                "recipient_district": "",
                "recipient_street": request.recipient_street,
                "recipient_post_code": request.recipient_postcode
            },
            "sender_info": {
                "sender_name": settings.EMAIL_ADDRESS.split("@")[0] if settings.EMAIL_ADDRESS else "Etsy Seller",
                "sender_phone": "+86 13800138000",
                "sender_country": "CN",
                "sender_state": "广东省",
                "sender_city": "深圳市",
                "sender_district": "福田区",
                "sender_street": "深南大道1号",
                "sender_post_code": "518000"
            }
        }
        
        # 5. 调用4PX创建订单
        result = fourpx_client.create_order(fourpx_order_data)
        
        if result.get("result") != "1":
            error_msg = result.get("msg") or result.get("error") or "4PX API调用失败"
            return JSONResponse(
                {"success": False, "message": error_msg, "data": result},
                status_code=400
            )
        
        # 6. 提取返回数据
        response_data = result.get("data", {})
        tracking_number = response_data.get("4px_tracking_no") or response_data.get("logistics_order_no", "")
        order_no = response_data.get("order_no", "")
        
        # 7. 获取面单URL
        label_url = ""
        if tracking_number:
            label_result = fourpx_client.get_label(tracking_number)
            if label_result.get("result") == "1":
                label_data = label_result.get("data", {})
                label_url_info = label_data.get("label_url_info", {})
                label_url = label_url_info.get("logistics_label", "")
        
        # 8. 更新logistics表
        logistics_list = db.select("logistics", {"order_id": request.order_id})
        logistics_update = {
            "tracking_number": tracking_number,
            "label_url": label_url,
            "state_code": request.recipient_state,
            "delivery_status": "shipped",
            "shipped_at": datetime.now().isoformat()
        }
        
        if logistics_list:
            db.update("logistics", {"order_id": request.order_id}, logistics_update)
        else:
            logistics_insert = {
                "order_id": request.order_id,
                "recipient_name": request.recipient_name,
                "country": request.recipient_country,
                "city": request.recipient_city,
                "street_address": request.recipient_street,
                "postal_code": request.recipient_postcode,
                **logistics_update
            }
            db.insert("logistics", logistics_insert)
        
        # 9. 更新订单状态
        db.update("orders", {"id": request.order_id}, {"status": "producing"})
        
        return JSONResponse({
            "success": True,
            "message": "物流订单创建成功",
            "data": {
                "order_no": order_no,
                "tracking_number": tracking_number,
                "label_url": label_url,
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
