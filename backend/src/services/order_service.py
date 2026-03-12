# -*- coding: utf-8 -*-
"""订单处理服务

包含：
  1. 邮件解析结果 → 写入 Supabase
  2. SKU 反推：通过 (shape, color, size) 得到唯一产品编号
"""

from typing import Optional, Dict
from src.services.database_service import db
from src.services.email_parser import ParsedOrder


# ============================================================
# SKU 反推：Etsy 邮件英文字段 → sku_mapping 表中文字段映射
#
# 数据库标准（以 sku_mapping 为唯一真相来源）：
#   外观：心形 / 圆形 / 骨头形
#   颜色：金色 / 银色 / 玫瑰金 / 黑色
#   大小：L / S
# ============================================================

# Etsy 邮件外观 → sku_mapping.shape
_SHAPE_MAP = {
    "heart":  "心形",
    "Heart":  "心形",
    "round":  "圆形",
    "Round":  "圆形",
    "circle": "圆形",
    "Circle": "圆形",
    "bone":   "骨头形",   # 注意：数据库是「骨头形」
    "Bone":   "骨头形",
}

# Etsy 邮件颜色 → sku_mapping.color
# 统一标准：客户端用「银色」，工厂原叫「钢本色」已废弃
_COLOR_MAP = {
    "Gold":      "金色",
    "gold":      "金色",
    "Silver":    "银色",
    "silver":    "银色",
    "Rose Gold": "玫瑰金",
    "rose gold": "玫瑰金",
    "RoseGold":  "玫瑰金",
    "Black":     "黑色",
    "black":     "黑色",
}

# Etsy 邮件大小 → sku_mapping.size（统一用 L/S）
_SIZE_MAP = {
    "Large":  "L",
    "large":  "L",
    "Small":  "S",
    "small":  "S",
    "Medium": "L",  # Medium 暂归并到 L，待产品线扩展时单独处理
}


def lookup_sku(shape: str, color: str, size: str) -> Optional[Dict]:
    """
    SKU 反推函数

    入参 shape/color/size 均为邮件解析得到的英文字段。
    内部自动转换为中文匹配 sku_mapping 表，返回匹配到的记录。

    示例：
      lookup_sku("Heart", "Gold", "Large")
      → {"sku_code": "B-G01B", "shape": "心形", "color": "金色", "size": "L", ...}
    """
    cn_shape = _SHAPE_MAP.get(shape, shape)
    cn_color = _COLOR_MAP.get(color, color)
    cn_size  = _SIZE_MAP.get(size, size)

    print(f"  [SKU反推] {shape}/{color}/{size} → {cn_shape}/{cn_color}/{cn_size}")

    # 查询 sku_mapping 表（字段名： shape, color, size）
    result = db.select_one("sku_mapping", {
        "shape": cn_shape,
        "color": cn_color,
        "size":  cn_size,
    })

    if result:
        print(f"  [SKU反推] 找到：{result.get('sku_code')}  (UUID: {result.get('id')})")
    else:
        print(f"  [SKU反推] 未找到匹配的SKU，请检查 sku_mapping 表数据")

    return result


class OrderService:
    def __init__(self):
        self.db = db

    def process_parsed_order(self, parsed: ParsedOrder) -> Optional[Dict]:
        # 检查订单是否已存在（重复不写入，直接跳过）
        existing = self.db.get_order_by_etsy_id(parsed.etsy_order_id)
        if existing:
            print(f"  ℹ️ 订单 {parsed.etsy_order_id} 已存在，跳过（无需重复导入）")
            return None

        item = parsed.items[0] if parsed.items else None

        # SKU 反推：通过 shape + color + size 查 sku_mapping 表
        matched_sku    = None
        matched_sku_id = ""
        sku_code       = ""
        if item and item.shape and item.color and item.size:
            matched_sku = lookup_sku(item.shape, item.color, item.size)
            if matched_sku:
                # matched_sku_id 字段是 UUID 类型，必须存 sku_mapping.id（UUID）
                matched_sku_id = matched_sku.get("id") or ""
                # sku_code 保存备用，供页面展示（如 B-G01B）
                sku_code = matched_sku.get("sku_code") or ""

        order_data = {
            "etsy_order_id":   parsed.etsy_order_id,
            "status":          "pending",
            "customer_name":   parsed.customer_name or parsed.shipping_name or "",
            "customer_email":  "",
            "total_amount":    parsed.order_total,
            "quantity":        item.quantity            if item else 1,
            "front_text":      item.customization_front if item else "",
            "back_text":       item.customization_back  if item else "",
            "font_code":       item.font_code            if item else "",
            # 外观/颜色/大小 存中文，与 sku_mapping 表统一，方便后续查询对比
            "product_shape":   _SHAPE_MAP.get(item.shape, item.shape)  if item else "",
            "product_color":   _COLOR_MAP.get(item.color, item.color)  if item else "",
            "product_size":    _SIZE_MAP.get(item.size,  item.size)   if item else "",
            "matched_sku_id":  matched_sku_id,
            # sku_code 不写入 sku_id（UUID类型字段），页面展示时由 matched_sku_id 反查 sku_mapping.sku_code
        }

        order = self.db.create_order(order_data)

        if order:
            print(f"  ✅ 订单已写入数据库: {parsed.etsy_order_id}")
            if matched_sku_id:
                print(f"  ✅ 匹配 SKU: {matched_sku_id}")
            else:
                print(f"  ⚠️  SKU 未匹配，请手动核对")
        return order


order_service = OrderService()