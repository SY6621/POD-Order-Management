# -*- coding: utf-8 -*-
"""订单处理服务"""

from typing import Optional, Dict
from src.services.database_service import db
from src.services.email_parser import ParsedOrder


class OrderService:
    def __init__(self):
        self.db = db
    
    def process_parsed_order(self, parsed: ParsedOrder) -> Optional[Dict]:
        # 检查订单是否已存在（重复不写入，直接跳过）
        existing = self.db.get_order_by_etsy_id(parsed.etsy_order_id)
        if existing:
            print(f"  ℹ️ 订单 {parsed.etsy_order_id} 已存在，跳过（无需重复导入）")
            return None  # 返回 None 表示“跳过”，区别于新建成功返回的字典
        
        # 提取第一个商品信息
        item = parsed.items[0] if parsed.items else None
        
        # 仅传入 Supabase orders 表实际存在的列
        # 实际列名： id, etsy_order_id, etsy_receipt_id, product_shape, product_color,
        # product_size, product_craft, quantity, front_text, front_font_id, back_text,
        # matched_sku_id, customer_name, customer_email, status, created_at, confirmed_at,
        # due_date, shipped_at, completed_at, sku_id, total_amount, progress, priority,
        # estimated_delivery, updated_at, operator_email, remote_status, font_code
        order_data = {
            "etsy_order_id":   parsed.etsy_order_id,
            "status":          "pending",
            "customer_name":   parsed.customer_name or parsed.shipping_name or "",
            "customer_email":  "",          # NOT NULL 列，邮件中通常不含客户邮箱，用空字符串占位
            "total_amount":    parsed.order_total,
            "quantity":        item.quantity            if item else 1,
            "front_text":      item.customization_front if item else "",
            "back_text":       item.customization_back  if item else "",
            "font_code":       item.font_code            if item else "",
            "product_shape":   item.shape               if item else "",
            "product_color":   item.color               if item else "",
            "product_size":    item.size                if item else "",
        }
        
        order = self.db.create_order(order_data)
        
        if order:
            print(f"  ✅ 订单已写入数据库: {parsed.etsy_order_id}")
        return order


order_service = OrderService()