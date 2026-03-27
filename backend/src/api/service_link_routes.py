# -*- coding: utf-8 -*-
"""
客服外链 API 路由
提供生成Token、验证Token、获取pending订单、记录操作日志等功能
"""

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import secrets
import hashlib

# 导入数据库服务
from src.services.database_service import db

router = APIRouter(prefix="/service-link", tags=["客服外链"])


# ============ 数据模型 ============

class GenerateTokenRequest(BaseModel):
    """生成Token请求"""
    shop_id: str
    enabled: bool = True


class TokenResponse(BaseModel):
    """Token响应"""
    shop_id: str
    shop_code: str
    shop_name: str
    service_token: str
    service_link_enabled: bool
    service_link_url: str
    created_at: Optional[datetime] = None


class ValidateTokenRequest(BaseModel):
    """验证Token请求"""
    shop_code: str
    token: str


class ValidateTokenResponse(BaseModel):
    """验证Token响应"""
    valid: bool
    shop_id: Optional[str] = None
    shop_name: Optional[str] = None
    message: str


class OrderResponse(BaseModel):
    """订单响应"""
    id: str
    etsy_order_id: str
    customer_name: str
    product_shape: str
    product_color: str
    front_text: str
    back_text: str
    effect_image_url: Optional[str] = None
    email_status: Optional[str] = None
    created_at: datetime


class LogActionRequest(BaseModel):
    """记录操作请求"""
    shop_id: str
    order_id: Optional[str] = None
    action: str  # 'view', 'send_email', 'confirm', 'request_modify'
    action_details: Optional[dict] = None


# ============ 辅助函数 ============

def generate_secure_token() -> str:
    """生成安全的随机Token"""
    # 生成32字节随机数据，转为16进制字符串（64位）
    return secrets.token_hex(32)


def build_service_link_url(shop_code: str, token: str, base_url: str = "http://localhost:5173") -> str:
    """构建客服外链URL"""
    return f"{base_url}/service/{shop_code}?token={token}"


# ============ API 路由 ============

@router.post("/generate-token", response_model=TokenResponse)
async def generate_token(request: GenerateTokenRequest):
    """
    生成或刷新店铺的客服外链Token
    
    - 如果店铺已有Token，会重新生成并覆盖
    - 返回完整的客服外链URL
    """
    try:
        # 1. 获取店铺信息
        shop_result = db.supabase.table("shops").select("*").eq("id", request.shop_id).single().execute()
        
        if not shop_result.data:
            raise HTTPException(status_code=404, detail="店铺不存在")
        
        shop = shop_result.data
        
        # 2. 生成新Token
        new_token = generate_secure_token()
        now = datetime.utcnow().isoformat()
        
        # 3. 更新店铺信息
        update_data = {
            "service_token": new_token,
            "service_link_enabled": request.enabled,
            "service_link_created_at": now,
            "service_link_updated_at": now
        }
        
        update_result = db.supabase.table("shops").update(update_data).eq("id", request.shop_id).execute()
        
        if not update_result.data:
            raise HTTPException(status_code=500, detail="更新店铺Token失败")
        
        updated_shop = update_result.data[0]
        
        # 4. 返回结果
        return TokenResponse(
            shop_id=updated_shop["id"],
            shop_code=updated_shop["code"],
            shop_name=updated_shop["name"],
            service_token=updated_shop["service_token"],
            service_link_enabled=updated_shop["service_link_enabled"],
            service_link_url=build_service_link_url(updated_shop["code"], updated_shop["service_token"]),
            created_at=updated_shop.get("service_link_created_at")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成Token失败: {str(e)}")


@router.get("/shops/{shop_id}/token", response_model=TokenResponse)
async def get_shop_token(shop_id: str):
    """
    获取店铺的客服外链信息
    
    - 如果店铺还没有Token，返回空token
    """
    try:
        result = db.supabase.table("shops").select("*").eq("id", shop_id).single().execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="店铺不存在")
        
        shop = result.data
        
        return TokenResponse(
            shop_id=shop["id"],
            shop_code=shop["code"],
            shop_name=shop["name"],
            service_token=shop.get("service_token", ""),
            service_link_enabled=shop.get("service_link_enabled", False),
            service_link_url=build_service_link_url(shop["code"], shop.get("service_token", "")) if shop.get("service_token") else "",
            created_at=shop.get("service_link_created_at")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取Token失败: {str(e)}")


@router.post("/shops/{shop_id}/toggle", response_model=TokenResponse)
async def toggle_service_link(shop_id: str, enabled: bool):
    """
    启用或禁用店铺的客服外链
    """
    try:
        now = datetime.utcnow().isoformat()
        
        update_result = db.supabase.table("shops").update({
            "service_link_enabled": enabled,
            "service_link_updated_at": now
        }).eq("id", shop_id).execute()
        
        if not update_result.data:
            raise HTTPException(status_code=404, detail="店铺不存在")
        
        shop = update_result.data[0]
        
        return TokenResponse(
            shop_id=shop["id"],
            shop_code=shop["code"],
            shop_name=shop["name"],
            service_token=shop.get("service_token", ""),
            service_link_enabled=shop["service_link_enabled"],
            service_link_url=build_service_link_url(shop["code"], shop.get("service_token", "")) if shop.get("service_token") else "",
            created_at=shop.get("service_link_created_at")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"切换外链状态失败: {str(e)}")


@router.post("/validate", response_model=ValidateTokenResponse)
async def validate_token(request: ValidateTokenRequest):
    """
    验证客服外链Token是否有效
    
    - 检查Token是否匹配
    - 检查外链是否已启用
    """
    try:
        # 1. 获取店铺信息
        result = db.supabase.table("shops").select("*").eq("code", request.shop_code).single().execute()
        
        if not result.data:
            return ValidateTokenResponse(valid=False, message="店铺不存在")
        
        shop = result.data
        
        # 2. 检查是否有Token
        if not shop.get("service_token"):
            return ValidateTokenResponse(valid=False, message="店铺未生成客服外链")
        
        # 3. 检查Token是否匹配
        if shop["service_token"] != request.token:
            return ValidateTokenResponse(valid=False, message="Token无效")
        
        # 4. 检查外链是否启用
        if not shop.get("service_link_enabled", False):
            return ValidateTokenResponse(valid=False, message="客服外链已禁用")
        
        # 5. 验证成功
        return ValidateTokenResponse(
            valid=True,
            shop_id=shop["id"],
            shop_name=shop["name"],
            message="验证成功"
        )
        
    except Exception as e:
        return ValidateTokenResponse(valid=False, message=f"验证失败: {str(e)}")


@router.get("/shops/{shop_id}/pending-orders", response_model=List[OrderResponse])
async def get_pending_orders(shop_id: str):
    """
    获取店铺的待确认订单（pending状态）
    
    - 客服外链只能看到待确认的订单
    """
    try:
        result = db.supabase.table("orders").select("*").eq("shop_id", shop_id).eq("status", "pending").order("created_at", desc=True).execute()
        
        orders = []
        for order in result.data or []:
            orders.append(OrderResponse(
                id=order["id"],
                etsy_order_id=order["etsy_order_id"],
                customer_name=order.get("customer_name", ""),
                product_shape=order.get("product_shape", ""),
                product_color=order.get("product_color", ""),
                front_text=order.get("front_text", ""),
                back_text=order.get("back_text", ""),
                effect_image_url=order.get("effect_image_url"),
                email_status=order.get("email_status"),
                created_at=order["created_at"]
            ))
        
        return orders
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取订单失败: {str(e)}")


@router.post("/log-action")
async def log_action(request: LogActionRequest, http_request: Request):
    """
    记录客服操作日志
    
    - 自动记录IP地址和User-Agent
    - 只记录操作时间，不记录客服身份
    """
    try:
        # 获取客户端信息
        client_ip = http_request.client.host if http_request.client else None
        user_agent = http_request.headers.get("user-agent")
        
        log_data = {
            "shop_id": request.shop_id,
            "order_id": request.order_id,
            "ip_address": client_ip,
            "user_agent": user_agent,
            "action": request.action,
            "action_details": request.action_details,
            "created_at": datetime.utcnow().isoformat()
        }
        
        result = db.supabase.table("service_link_logs").insert(log_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="记录日志失败")
        
        return {"success": True, "log_id": result.data[0]["id"]}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"记录日志失败: {str(e)}")


@router.get("/shops/{shop_id}/logs")
async def get_shop_logs(shop_id: str, limit: int = 50):
    """
    获取店铺的操作日志
    
    - 用于Admin查看客服操作历史
    """
    try:
        result = db.supabase.table("service_link_logs").select("*").eq("shop_id", shop_id).order("created_at", desc=True).limit(limit).execute()
        
        return result.data or []
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取日志失败: {str(e)}")


# ============================================================
# 设计链接 API (Design Link)
# 客服可直接修改设计、生成效果图、发邮件
# ============================================================

class DesignTokenResponse(BaseModel):
    """设计链接Token响应"""
    shop_id: str
    shop_code: str
    shop_name: str
    design_token: str
    design_link_enabled: bool
    design_link_url: str
    created_at: Optional[datetime] = None


class ValidateDesignTokenRequest(BaseModel):
    """验证设计链接Token请求"""
    shop_code: str
    token: str


def build_design_link_url(shop_code: str, token: str, base_url: str = "http://localhost:5173") -> str:
    """构建设计链接URL"""
    return f"{base_url}/design/{shop_code}?token={token}"


@router.post("/design-link/generate-token", response_model=DesignTokenResponse)
async def generate_design_token(request: GenerateTokenRequest):
    """
    生成或刷新店铺的设计链接Token
    
    - 设计链接允许客服直接修改设计、生成效果图
    - 与沟通链接(service_link)独立，互不影响
    """
    try:
        # 1. 获取店铺信息
        shop_result = db.supabase.table("shops").select("*").eq("id", request.shop_id).single().execute()
        
        if not shop_result.data:
            raise HTTPException(status_code=404, detail="店铺不存在")
        
        shop = shop_result.data
        
        # 2. 生成新Token
        new_token = generate_secure_token()
        now = datetime.utcnow().isoformat()
        
        # 3. 更新店铺信息
        update_data = {
            "design_token": new_token,
            "design_link_enabled": request.enabled,
            "design_link_created_at": now,
            "design_link_updated_at": now
        }
        
        update_result = db.supabase.table("shops").update(update_data).eq("id", request.shop_id).execute()
        
        if not update_result.data:
            raise HTTPException(status_code=500, detail="更新店铺设计链接Token失败")
        
        updated_shop = update_result.data[0]
        
        # 4. 返回结果
        return DesignTokenResponse(
            shop_id=updated_shop["id"],
            shop_code=updated_shop["code"],
            shop_name=updated_shop["name"],
            design_token=updated_shop["design_token"],
            design_link_enabled=updated_shop["design_link_enabled"],
            design_link_url=build_design_link_url(updated_shop["code"], updated_shop["design_token"]),
            created_at=updated_shop.get("design_link_created_at")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成设计链接Token失败: {str(e)}")


@router.get("/design-link/shops/{shop_id}/token", response_model=DesignTokenResponse)
async def get_design_token(shop_id: str):
    """
    获取店铺的设计链接信息
    
    - 如果店铺还没有设计链接Token，返回空token
    """
    try:
        result = db.supabase.table("shops").select("*").eq("id", shop_id).single().execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="店铺不存在")
        
        shop = result.data
        
        return DesignTokenResponse(
            shop_id=shop["id"],
            shop_code=shop["code"],
            shop_name=shop["name"],
            design_token=shop.get("design_token", ""),
            design_link_enabled=shop.get("design_link_enabled", False),
            design_link_url=build_design_link_url(shop["code"], shop.get("design_token", "")) if shop.get("design_token") else "",
            created_at=shop.get("design_link_created_at")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取设计链接Token失败: {str(e)}")


@router.post("/design-link/shops/{shop_id}/toggle", response_model=DesignTokenResponse)
async def toggle_design_link(shop_id: str, enabled: bool):
    """
    启用或禁用店铺的设计链接
    """
    try:
        now = datetime.utcnow().isoformat()
        
        update_result = db.supabase.table("shops").update({
            "design_link_enabled": enabled,
            "design_link_updated_at": now
        }).eq("id", shop_id).execute()
        
        if not update_result.data:
            raise HTTPException(status_code=404, detail="店铺不存在")
        
        shop = update_result.data[0]
        
        return DesignTokenResponse(
            shop_id=shop["id"],
            shop_code=shop["code"],
            shop_name=shop["name"],
            design_token=shop.get("design_token", ""),
            design_link_enabled=shop["design_link_enabled"],
            design_link_url=build_design_link_url(shop["code"], shop.get("design_token", "")) if shop.get("design_token") else "",
            created_at=shop.get("design_link_created_at")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"切换设计链接状态失败: {str(e)}")


@router.post("/design-link/validate", response_model=ValidateTokenResponse)
async def validate_design_token(request: ValidateDesignTokenRequest):
    """
    验证设计链接Token是否有效
    
    - 检查Token是否匹配
    - 检查设计链接是否已启用
    """
    try:
        # 1. 获取店铺信息
        result = db.supabase.table("shops").select("*").eq("code", request.shop_code).single().execute()
        
        if not result.data:
            return ValidateTokenResponse(valid=False, message="店铺不存在")
        
        shop = result.data
        
        # 2. 检查是否有设计链接Token
        if not shop.get("design_token"):
            return ValidateTokenResponse(valid=False, message="店铺未生成设计链接")
        
        # 3. 检查Token是否匹配
        if shop["design_token"] != request.token:
            return ValidateTokenResponse(valid=False, message="设计链接Token无效")
        
        # 4. 检查设计链接是否启用
        if not shop.get("design_link_enabled", False):
            return ValidateTokenResponse(valid=False, message="设计链接已禁用")
        
        # 5. 验证成功
        return ValidateTokenResponse(
            valid=True,
            shop_id=shop["id"],
            shop_name=shop["name"],
            message="设计链接验证成功"
        )
        
    except Exception as e:
        return ValidateTokenResponse(valid=False, message=f"验证失败: {str(e)}")
