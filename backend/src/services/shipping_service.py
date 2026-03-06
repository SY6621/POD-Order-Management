# -*- coding: utf-8 -*-
"""
Shipping label service for logistics integration
Supports Postlink and other carriers
"""

from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field

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


shipping_service = ShippingService()