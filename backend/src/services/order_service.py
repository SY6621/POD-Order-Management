# -*- coding: utf-8 -*-
"""订单处理服务"""

from typing import Optional, Dict
from src.services.database_service import db
from src.services.email_parser import ParsedOrder


class OrderService:
    def __init__(self):
        self.db = db
    
    def process_parsed_order(self, parsed: ParsedOrder) -> Optional[Dict]:
        existing = self.db.get_order_by_etsy_id(parsed.etsy_order_id)
        if existing:
            print(f"⚠️ 订单已存在: {parsed.etsy_order_id}")
            return existing
        
        order = self.db.create_order({
            "etsy_order_id": parsed.etsy_order_id,
            "status": "pending",
            "customer_name": parsed.customer_name,
            "shipping_address": f"{parsed.shipping_address_line1}, {parsed.shipping_city}, {parsed.shipping_country}",
            "total_amount": parsed.order_total,
            "currency": parsed.currency,
        })
        
        if order:
            print(f"✅ 订单创建: {parsed.etsy_order_id}")
        return order


order_service = OrderService()