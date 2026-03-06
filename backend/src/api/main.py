# -*- coding: utf-8 -*-
"""
FastAPI 后端 API 服务
提供效果图生成、邮件发送、PDF生成等功能接口
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.services.effect_image_service import effect_image_service
from src.services.email_service import email_service
from src.services.database_service import db


# 创建 FastAPI 应用
app = FastAPI(
    title="ETSY订单自动化 API",
    description="提供效果图生成、邮件发送、PDF生成等功能",
    version="1.0.0"
)

# 配置 CORS（允许前端跨域调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/")
async def root():
    """API 根路径"""
    return {"message": "ETSY订单自动化 API", "status": "running"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}


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
    """
    try:
        from src.services.svg_pdf_service import svg_pdf_service

        order_data = db.select_one("orders", {"id": request.order_id})
        if not order_data:
            raise HTTPException(status_code=404, detail="订单不存在")

        # 关联查询 logistics 表获取收件人地址信息
        logistics_list = db.select("logistics", {"order_id": request.order_id})
        if logistics_list:
            logistics = logistics_list[0]
            # 将 logistics 字段平铺到 order_data 字典中
            order_data.update({
                "recipient_name": logistics.get("recipient_name", ""),
                "street_address": logistics.get("street_address", ""),
                "city": logistics.get("city", ""),
                "state_code": logistics.get("state_code", ""),
                "postal_code": logistics.get("postal_code", ""),
                "country": logistics.get("country", ""),
                "tracking_number": logistics.get("tracking_number", ""),
            })

        # 直接用字典数据生成 PDF，避免触发 SQLAlchemy Database 类初始化
        pdf_path = svg_pdf_service.generate_from_raw_data(order_data)
        if not pdf_path:
            raise HTTPException(status_code=500, detail="PDF 生成失败")

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
        raise HTTPException(status_code=500, detail=f"PDF 生成出错: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
