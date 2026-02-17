# -*- coding: utf-8 -*-
"""Etsy 邮件解析器"""

import re
from typing import Optional, List
from dataclasses import dataclass, field


@dataclass
class ParsedOrderItem:
    product_name: str = ""
    shape: str = ""
    color: str = ""
    size: str = ""
    engraving_side: str = ""
    customization_front: str = ""
    customization_back: str = ""
    font_code: str = ""
    transaction_id: str = ""
    quantity: int = 1
    price: float = 0.0
    currency: str = "AUD"


@dataclass
class ParsedOrder:
    etsy_order_id: str = ""
    order_date: str = ""
    customer_name: str = ""
    customer_username: str = ""
    shipping_name: str = ""
    shipping_address_line1: str = ""
    shipping_address_line2: str = ""
    shipping_city: str = ""
    shipping_state: str = ""
    shipping_zip: str = ""
    shipping_country: str = ""
    item_total: float = 0.0
    shipping_cost: float = 0.0
    order_total: float = 0.0
    currency: str = "AUD"
    items: List[ParsedOrderItem] = field(default_factory=list)
    raw_email_content: str = ""


class EtsyEmailParser:
    SHAPES = {"bone": "Bone", "heart": "Heart", "round": "Round", "rectangle": "Rectangle"}
    COLORS = {"silver": "Silver", "gold": "Gold", "rose gold": "Rose Gold", "black": "Black"}
    SIZES = {"small": "Small", "medium": "Medium", "large": "Large"}
    
    def parse(self, body: str) -> Optional[ParsedOrder]:
        if not body:
            return None
        order = ParsedOrder(raw_email_content=body)
        
        m = re.search(r"Your order number is:\s*(\d+)", body)
        if not m:
            m = re.search(r"Order\s*#(\d+)", body)
        order.etsy_order_id = m.group(1) if m else ""
        if not order.etsy_order_id:
            return None
        
        m = re.search(r"Delivery address\s*([\s\S]*?)(?:Dispatching|We're applying)", body, re.I)
        if m:
            lines = [l.strip() for l in m.group(1).split('\n') if l.strip()]
            if lines:
                order.shipping_name = order.customer_name = lines[0]
            if len(lines) > 1:
                order.shipping_address_line1 = lines[1]
            if len(lines) > 2:
                order.shipping_address_line2 = lines[2]
            if len(lines) > 3:
                parts = lines[-2].split() if len(lines) > 4 else lines[3].split()
                if len(parts) >= 3:
                    order.shipping_zip, order.shipping_state = parts[-1], parts[-2]
                    order.shipping_city = ' '.join(parts[:-2])
            order.shipping_country = lines[-1] if lines and lines[-1].isalpha() else "Australia"
        
        m = re.search(r"Order total[:\s]*(AU?\$?)([\d.]+)", body)
        if m:
            order.order_total = float(m.group(2))
            order.currency = "AUD" if "AU" in m.group(1) else "USD"
        
        m = re.search(r"contact the buyer directly\s*([a-zA-Z0-9_]+)", body, re.I)
        order.customer_username = m.group(1) if m else ""
        
        item = ParsedOrderItem()
        m = re.search(r"((?:Engraved|Custom)\s+\w+\s+Pet ID Tag[^Q]*?)(?:Quantity|Shop)", body, re.I|re.S)
        if m:
            item.product_name = m.group(1).strip()[:200]
        for k, v in self.SHAPES.items():
            if k in item.product_name.lower():
                item.shape = v
                break
        m = re.search(r"Color\s*\+\s*Size[:\s]*([^\n]+)", body, re.I)
        if m:
            cs = m.group(1).lower()
            for k, v in self.COLORS.items():
                if k in cs:
                    item.color = v
                    break
            for k, v in self.SIZES.items():
                if k in cs:
                    item.size = v
                    break
        m = re.search(r"Engraving Side[:\s]*([^\n]+)", body, re.I)
        if m:
            item.engraving_side = m.group(1).strip()
        m = re.search(r"Personalization[:\s]*Front[:\s]*([^\n]+)", body, re.I)
        if m:
            pers = m.group(1)
            fm = re.match(r"([^(]+)\s*\((?:font\s*)?([^)]+)\)", pers)
            if fm:
                item.customization_front = fm.group(1).strip()
                item.font_code = fm.group(2).strip().upper()
            else:
                item.customization_front = pers.split("Back")[0].strip()
            bm = re.search(r"Back[:\s]*(\S+)", pers)
            if bm:
                item.customization_back = bm.group(1)
        m = re.search(r"Quantity[:\s]*(\d+)", body)
        if m:
            item.quantity = int(m.group(1))
        m = re.search(r"Price[:\s]*(AU?\$?)([\d.]+)", body)
        if m:
            item.price = float(m.group(2))
        
        order.items.append(item)
        return order
    
    def parse_forwarded_email(self, body: str) -> Optional[ParsedOrder]:
        m = re.search(r"-+\s*Forwarded message\s*-+\s*([\s\S]+)", body, re.I)
        if m:
            content = m.group(1)
            dm = re.search(r"Date[:\s]*([^\n]+)", content)
            order = self.parse(content)
            if order and dm:
                order.order_date = dm.group(1).strip()
            return order
        return self.parse(body)


email_parser = EtsyEmailParser()