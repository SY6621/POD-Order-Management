# -*- coding: utf-8 -*-
"""
Shipping label service for logistics integration
Supports Postlink and 4PX carriers
"""

import hashlib
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field

import requests

from src.config.settings import settings


@dataclass
class ShippingLabel:
    """Shipping label data structure"""
    tracking_number: str = ""
    carrier: str = "Postlink"
    label_image_path: Optional[Path] = None
    
    recipient_name: str = ""
    recipient_address: str = ""
    recipient_city: str = ""
    recipient_state: str = ""
    recipient_postal_code: str = ""
    recipient_country: str = ""
    recipient_country_code: str = ""
    
    weight: float = 0.03
    ref_no: str = ""
    product_name: str = "pet ID tag"


@dataclass
class OrderData:
    """Complete order data structure for production"""
    order_id: str = ""
    customer_name: str = ""
    order_date: str = ""
    ship_date: str = ""
    
    sku: str = ""
    shape: str = ""
    shape_en: str = ""
    color: str = ""
    color_en: str = ""
    size: str = ""
    size_en: str = ""
    craft: str = "抛光"
    
    front_text: str = ""
    front_font: str = ""
    back_text: str = ""
    
    shipping: ShippingLabel = field(default_factory=ShippingLabel)
    
    product_photo_path: Optional[Path] = None
    effect_image_front_path: Optional[Path] = None
    effect_image_back_path: Optional[Path] = None
    
    width_mm: float = 45.0
    height_mm: float = 26.0


class ShippingService:
    """Shipping label generation and logistics API service"""
    
    COUNTRY_CODES = {
        "australia": "AU", "united states": "US", "usa": "US",
        "united kingdom": "GB", "uk": "GB", "canada": "CA",
        "germany": "DE", "france": "FR", "japan": "JP",
        "new zealand": "NZ", "singapore": "SG",
    }
    
    SHAPE_MAP = {
        "bone": ("骨头形", "Bone"),
        "heart": ("心形", "Heart"),
        "circle": ("圆形", "Circle"),
    }
    
    COLOR_MAP = {
        "gold": ("金色", "Gold"),
        "silver": ("银色", "Silver"),
        "rose gold": ("玫瑰金", "Rose Gold"),
        "rosegold": ("玫瑰金", "Rose Gold"),
        "black": ("黑色", "Black"),
    }
    
    SIZE_MAP = {
        "large": ("大", "Large", 45.0, 26.0),
        "small": ("小", "Small", 38.0, 22.0),
    }
    
    def __init__(self):
        self.output_dir = settings.OUTPUT_DIR
        settings.ensure_output_dir()
    
    def get_country_code(self, country: str) -> str:
        country_lower = country.lower().strip()
        return self.COUNTRY_CODES.get(country_lower, country_lower[:2].upper())
    
    def translate_product_info(self, shape: str, color: str, size: str) -> Dict[str, Any]:
        shape_lower = shape.lower().strip()
        color_lower = color.lower().strip()
        size_lower = size.lower().strip()
        
        shape_info = self.SHAPE_MAP.get(shape_lower, (shape, shape))
        color_info = self.COLOR_MAP.get(color_lower, (color, color))
        size_info = self.SIZE_MAP.get(size_lower, ("", "", 45.0, 26.0))
        
        return {
            "shape_cn": shape_info[0], "shape_en": shape_info[1],
            "color_cn": color_info[0], "color_en": color_info[1],
            "size_cn": size_info[0], "size_en": size_info[1],
            "width_mm": size_info[2], "height_mm": size_info[3],
        }
    
    def generate_sku(self, shape: str, color: str, size: str) -> str:
        shape_codes = {"bone": "E", "heart": "G", "circle": "C"}
        color_codes = {"silver": "A", "gold": "B", "rose gold": "C", "rosegold": "C", "black": "D"}
        size_codes = {"large": "01", "small": "02"}
        
        # 调试输出
        print(f"[DEBUG] generate_sku: shape='{shape}' -> lower='{shape.lower()}'")
        print(f"[DEBUG] shape_codes lookup: {shape_codes.get(shape.lower(), 'NOT FOUND')}")
        
        shape_code = shape_codes.get(shape.lower(), "E")
        color_code = color_codes.get(color.lower(), "A")
        size_code = size_codes.get(size.lower(), "01")
        
        sku = f"B-{shape_code}{size_code}{color_code}"
        print(f"[DEBUG] Generated SKU: {sku}")
        return sku
    
    def create_order_data(self, raw_data: Dict[str, Any]) -> OrderData:
        # ===== 真实数据库字段名对齐 =====
        # orders 表: product_shape / product_color / product_size / product_craft
        # 收件人信息: recipient_name / street_address / city / state_code / postal_code / country
        # 字体: font_code
        # 订单号: etsy_order_id
        
        shape = raw_data.get("product_shape") or raw_data.get("shape", "Bone")
        color = raw_data.get("product_color") or raw_data.get("color", "Gold")
        size  = raw_data.get("product_size")  or raw_data.get("size", "Large")
        craft = raw_data.get("product_craft") or raw_data.get("craft", "抛光")
        
        product_trans = self.translate_product_info(shape, color, size)
        # 必须用英文原始值生成 SKU，翻译后的中文无法匹配 SKU 字典
        sku = self.generate_sku(shape, color, size)
        
        # 订单号
        order_id = raw_data.get("etsy_order_id") or raw_data.get("order_id", "")
        
        # 字体：数据库字段 font_code
        front_font = raw_data.get("font_code") or raw_data.get("font", "F-01")
        if not front_font:
            front_font = "F-01"
        
        # 收件人：数据库字段 recipient_name / street_address / city / state_code / postal_code / country
        shipping_name = (
            raw_data.get("recipient_name") or
            raw_data.get("shipping_name") or
            raw_data.get("customer_name", "")
        )
        shipping_address = (
            raw_data.get("street_address") or
            raw_data.get("shipping_address_line1") or
            raw_data.get("shipping_address", "")
        )
        shipping_city = (
            raw_data.get("city") or
            raw_data.get("shipping_city", "")
        )
        shipping_state = (
            raw_data.get("state_code") or
            raw_data.get("state") or
            raw_data.get("shipping_state", "")
        )
        shipping_postal = (
            raw_data.get("postal_code") or
            raw_data.get("shipping_postal_code", "")
        )
        country = (
            raw_data.get("country") or
            raw_data.get("shipping_country", "")
        )
        tracking_number = (
            raw_data.get("tracking_number") or ""
        )
        
        shipping = ShippingLabel(
            tracking_number=tracking_number,
            recipient_name=shipping_name,
            recipient_address=shipping_address,
            recipient_city=shipping_city,
            recipient_state=shipping_state,
            recipient_postal_code=shipping_postal,
            recipient_country=country,
            recipient_country_code=self.get_country_code(country),
            ref_no=order_id,
        )
        
        # 订单日期：兼容 created_at（带时区 ISO 格式）
        raw_date = raw_data.get("order_date") or raw_data.get("created_at", "")
        if raw_date and "T" in str(raw_date):
            raw_date = str(raw_date).split("T")[0]
        order_date = raw_date or datetime.now().strftime("%Y-%m-%d")
        try:
            order_dt = datetime.strptime(str(order_date)[:10], "%Y-%m-%d")
            ship_dt = order_dt + timedelta(days=2)
            ship_date = ship_dt.strftime("%Y-%m-%d")
        except:
            ship_date = order_date
        
        return OrderData(
            order_id=order_id,
            customer_name=raw_data.get("customer_name", ""),
            order_date=order_date,
            ship_date=ship_date,
            sku=sku,
            shape=product_trans["shape_cn"],
            shape_en=product_trans["shape_en"],
            color=product_trans["color_cn"],
            color_en=product_trans["color_en"],
            size=product_trans["size_cn"],
            size_en=product_trans["size_en"],
            front_text=raw_data.get("front_text", ""),
            front_font=front_font,
            back_text=raw_data.get("back_text", ""),
            shipping=shipping,
            width_mm=product_trans["width_mm"],
            height_mm=product_trans["height_mm"],
        )
    
    def generate_tracking_number(self, order_id: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"PL{timestamp}{order_id[-4:]}"
    
    def create_shipping_label(self, order_data: OrderData) -> ShippingLabel:
        if not order_data.shipping.tracking_number:
            order_data.shipping.tracking_number = self.generate_tracking_number(order_data.order_id)
        order_data.shipping.ref_no = order_data.order_id
        print(f"[OK] Shipping label created: {order_data.shipping.tracking_number}")
        return order_data.shipping


class FourPXClient:
    """4PX 物流 API 客户端"""
    
    def __init__(self, app_key: str = None, app_secret: str = None, sandbox: bool = True):
        self.app_key = app_key or settings.FOURPX_APP_KEY
        self.app_secret = app_secret or settings.FOURPX_APP_SECRET
        self.sandbox = sandbox
        self.base_url = (
            "https://open-test.4px.com/router/api/service" if sandbox
            else "https://open.4px.com/router/api/service"
        )
    
    def generate_sign(self, method: str, v: str, body: Dict[Any, Any], timestamp: str = None) -> tuple:
        """
        生成 4PX API 签名
        
        签名规则：
        sign = app_key{AppKey}formatjsonmethod{method}timestamp{timestamp}v{v}{body}{AppSecret}
        MD5 加密（32位小写）
        """
        if timestamp is None:
            timestamp = str(int(time.time() * 1000))
        
        # 压缩 JSON body（无空格、无换行）
        body_str = json.dumps(body, ensure_ascii=False, separators=(',', ':'))
        
        # 拼接签名字符串
        sign_string = f"app_key{self.app_key}formatjsonmethod{method}timestamp{timestamp}v{v}{body_str}{self.app_secret}"
        
        # MD5 加密（32位小写）
        md5_sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest().lower()
        
        return sign_string, md5_sign, timestamp
    
    def call_api(self, method: str, v: str, body: Dict[Any, Any]) -> Dict[Any, Any]:
        """调用 4PX API"""
        sign_string, sign, timestamp = self.generate_sign(method, v, body)
        
        url = f"{self.base_url}?method={method}&app_key={self.app_key}&v={v}&timestamp={timestamp}&format=json&sign={sign}"
        body_str = json.dumps(body, ensure_ascii=False, separators=(',', ':'))
        
        try:
            response = requests.post(
                url,
                data=body_str,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            return response.json()
        except Exception as e:
            return {"error": str(e), "result": "0"}
    
    def create_order(self, order_data: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        创建直发委托单
        API: ds.xms.order.create v1.1.0
        """
        method = "ds.xms.order.create"
        v = "1.1.0"
        return self.call_api(method, v, order_data)
    
    def get_label(self, request_no: str, label_type: str = "1", label_size: str = "10x10") -> Dict[Any, Any]:
        """
        获取标签
        API: ds.xms.label.get v1.1.0
        
        Args:
            request_no: 4PX 请求单号（不是 ETSY order_no）
            label_type: 标签类型，1-地址标签
            label_size: 标签尺寸，如 "10x10"
        """
        method = "ds.xms.label.get"
        v = "1.1.0"
        body = {
            "request_no": request_no,  # 4PX API 要求用 request_no
            "label_type": label_type,
            "label_size": label_size
        }
        return self.call_api(method, v, body)
    
    def cancel_order(self, request_no: str, cancel_reason: str = "") -> Dict[Any, Any]:
        """
        取消直发委托单
        API: ds.xms.order.cancel v1.0.0
        
        Args:
            request_no: 4PX 请求单号
            cancel_reason: 取消原因
        """
        method = "ds.xms.order.cancel"
        v = "1.0.0"
        body = {
            "request_no": request_no,
            "cancel_reason": cancel_reason or "客户取消订单"
        }
        return self.call_api(method, v, body)
    
    def get_logistics_products(self, country_code: str, postcode: str = "") -> Dict[Any, Any]:
        """
        查询物流产品
        API: ds.xms.logistics_product.getlist v1.0.0
        """
        method = "ds.xms.logistics_product.getlist"
        v = "1.0.0"
        body = {
            "country_code": country_code,
            "postcode": postcode,
            "transport_mode": "A"
        }
        return self.call_api(method, v, body)
    
    def query_order(self, order_no: str) -> Dict[Any, Any]:
        """
        查询直发委托单
        API: ds.xms.order.get v1.1.0
        """
        method = "ds.xms.order.get"
        v = "1.1.0"
        body = {"order_no": order_no}
        return self.call_api(method, v, body)


shipping_service = ShippingService()