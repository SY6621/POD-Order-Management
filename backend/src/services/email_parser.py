# -*- coding: utf-8 -*-
"""
Etsy 订单邮件解析器

支持两种格式：
  1. 直接收到的 Etsy 订单通知邮件
  2. 转发的 Etsy 订单邮件（含 Forwarded message 标志）

刻字格式支持：
  - 标准格式： Personalization: Front: Luna (F-04) Back: 416.456.3524
  - 带备注格式： Personalization: Chloe (f-04) (with a heart below the name) 5062290282
"""

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
        
        # ────────────────────────────────
        # 1. 解析订单号
        # 格式1： Your order number is: 3794236690
        # 格式2： Your order number is 3986891868.
        # 格式3： Order #3794236690（邮件主题中也有）
        # ────────────────────────────────
        m = re.search(r"Your order number is:?\s*(\d+)", body)
        if not m:
            m = re.search(r"Order\s*#(\d+)", body)
        order.etsy_order_id = m.group(1) if m else ""
        if not order.etsy_order_id:
            return None
        
        # ────────────────────────────────
        # 2. 解析收货地址
        # 格式A（带星号装饰）：
        #   * Delivery address *
        #   Demi Brooker
        #   3/1A Salisbury Rd
        #   ROSE BAY NSW 2029
        #   Australia
        # 格式B（无星号）：
        #   Delivery address
        #   OCEAN MELANSON
        #   105 BRIDGE ST
        #   SACKVILLE NB E4L 3P4
        #   Canada
        # 终止词：Dispatching / We're applying / Sell with confidence
        # ────────────────────────────────
        m = re.search(
            r"\*?\s*Delivery address\s*\*?\s*\n([\s\S]*?)(?:\* Dispatching|Dispatching|We're applying|Sell with confidence)",
            body, re.I
        )
        if m:
            lines = [l.strip() for l in m.group(1).split('\n') if l.strip()]
            # 过滤掉只含 * 或空内容的行
            lines = [l for l in lines if l not in ('*', '') and not re.fullmatch(r'\*+', l)]
            if lines:
                order.shipping_name = order.customer_name = lines[0]   # 真实姓名
            if len(lines) > 1:
                order.shipping_address_line1 = lines[1]
            # 地址可能有两行（如建筑号 + 街道名）
            if len(lines) > 3:
                order.shipping_address_line2 = lines[2]
                city_line = lines[3]
            else:
                city_line = lines[2] if len(lines) > 2 else ""
            
            # 解析城市行：格式 "SACKVILLE NB E4L 3P4" 或 "ROSE BAY NSW 2029"
            # 最后一个单词为邮编，倒数第二个为州编，剩余为城市
            if city_line:
                parts = city_line.split()
                if len(parts) >= 3:
                    # 加拿大邮编格式： A1B 2C3（两段，第二段为纯数字+字母6位）
                    # 澳大利亚/美国邮编：纯数字（如 2029 或 90210）
                    last = parts[-1]
                    second_last = parts[-2] if len(parts) >= 2 else ""
                    if re.match(r'^[A-Z]\d[A-Z]$', second_last):   # 加拿大前半段 E4L
                        order.shipping_zip = second_last + " " + last
                        order.shipping_state = parts[-3]
                        order.shipping_city = ' '.join(parts[:-3])
                    else:
                        order.shipping_zip = last
                        order.shipping_state = second_last
                        order.shipping_city = ' '.join(parts[:-2])
            
            # 最后一行为国家
            if lines:
                order.shipping_country = lines[-1]
        
        # ────────────────────────────────
        # 3. 解析订单金额
        # 格式： Order total: AU$34.46
        # ────────────────────────────────
        m = re.search(r"Order total[:\s]*(AU?\$?)(\d+\.\d+)", body)
        if m:
            order.order_total = float(m.group(2))
            order.currency = "AUD" if "AU" in m.group(1) else "USD"
        
        # ────────────────────────────────
        # 4. 解析客户用户名
        # 格式： contact the buyer directly\nCatsbyGatsby
        # ────────────────────────────────
        m = re.search(r"contact the buyer directly\s*([a-zA-Z0-9_]+)", body, re.I)
        order.customer_username = m.group(1) if m else ""
        
        # ────────────────────────────────
        # 5. 解析商品信息
        # ────────────────────────────────
        item = ParsedOrderItem()
        
        # 商品名：匹配 "Custom Heart Pet ID Tag: ..." 到 Color 或 Engraving 或 Quantity 前
        m = re.search(r"((?:Engraved|Custom)\s+\w+.*?Pet ID Tag[^\n]*)\n", body, re.I)
        if m:
            item.product_name = m.group(1).strip()[:200]
        for k, v in self.SHAPES.items():
            if k in item.product_name.lower():
                item.shape = v
                break
        
        # 颜色+尺寸： Color + Size:: Gold Large
        m = re.search(r"Color\s*\+\s*Size[:\s:]+([^\n]+)", body, re.I)
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
        
        # 刷刻面： Engraving Side:: Double-sided
        m = re.search(r"Engraving Side[:\s:]+([^\n]+)", body, re.I)
        if m:
            item.engraving_side = m.group(1).strip()
        
        # Transaction ID
        m = re.search(r"Transaction ID[:\s]+(\d+)", body, re.I)
        if m:
            item.transaction_id = m.group(1).strip()
        
        # ────────────────────────────────
        # 6. 解析 Personalization（刻字内容 + 字体代码）
        #
        # 规则：字体代码必须以 F- 开头（如 F-04），其他括号内容忽略
        #
        # 格式一（标准 Front/Back）：
        #   Personalization: Front: Luna (F-04) Back: 416.456.3524
        #   → front="Luna", font="F-04", back="416.456.3524"
        #
        # 格式二（不分面，带备注）：
        #   Personalization: Chloe (F-04) (with a heart below the name) 5062290282
        #   → front="Chloe", font="F-04", back="5062290282"
        #
        # 格式三（无字体代码，纯内容）：
        #   Personalization: Spirit 0402 830 481
        #   → front="Spirit 0402 830 481", font="", back=""
        # ────────────────────────────────
        m = re.search(r"Personalization[:\s]+([^\n]+(?:\n(?!Shop:|Transaction|Quantity|Price)[^\n]+)*)", body, re.I)
        if m:
            pers_raw = m.group(1).strip()
            
            # 字体代码：必须以 F- 开头，格式如 (F-04)
            FONT_RE = re.compile(r"\((F-\d{2})\)", re.I)
            
            # 格式一：明确包含 "Front:" 关键词
            front_m = re.search(r"Front[:\s]+(.+?)(?:\s+Back[:\s]+|$)", pers_raw, re.I)
            back_m  = re.search(r"Back[:\s]+(.+)", pers_raw, re.I)
            
            if front_m:
                front_raw = front_m.group(1).strip()
                font_m = FONT_RE.search(front_raw)
                if font_m:
                    item.font_code = font_m.group(1).upper()           # 统一大写：F-04
                    item.customization_front = FONT_RE.sub("", front_raw).strip()
                else:
                    item.customization_front = front_raw
                
                if back_m:
                    item.customization_back = back_m.group(1).strip()
            else:
                # 格式二/三：没有 Front: 关键词
                font_m = FONT_RE.search(pers_raw)
                if font_m:
                    item.font_code = font_m.group(1).upper()
                    # 字体括号前面的内容为刻字名
                    item.customization_front = pers_raw[:font_m.start()].strip()
                    # 字体括号后面的内容（备注/电话等）存入 back 避免丢失
                    remainder = FONT_RE.sub("", pers_raw[font_m.start():]).strip()
                    if remainder:
                        item.customization_back = remainder
                else:
                    # 格式三：无字体代码，全部内容作为 front_text
                    item.customization_front = pers_raw
        
        # 数量和单价
        m = re.search(r"Quantity[:\s]*(\d+)", body)
        if m:
            item.quantity = int(m.group(1))
        m = re.search(r"Price[:\s]*(AU?\$?)([\d.]+)", body)
        if m:
            item.price = float(m.group(2))
        
        order.items.append(item)
        return order
    
    def parse_forwarded_email(self, body: str) -> Optional[ParsedOrder]:
        """
        处理转发邮件格式：
        先尝试提取 Forwarded message 内容，如果没有则直接解析整封邮件
        """
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