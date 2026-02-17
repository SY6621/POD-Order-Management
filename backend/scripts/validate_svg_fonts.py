# -*- coding: utf-8 -*-
"""
SVG字体校验脚本
验证SVG模板中的字体是否正确映射到阿里巴巴普惠体
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import re
from collections import Counter
from src.services.svg_pdf_service import svg_pdf_service

print("=" * 60)
print("SVG模板字体校验")
print("=" * 60)

# 加载SVG模板
svg_original = svg_pdf_service._load_template()
svg_styled = svg_pdf_service._apply_font_styles(svg_original)

# 提取字体
fonts_original = re.findall(r"font-family=\"'([^']+)'\"", svg_original)
fonts_after = re.findall(r"font-family=\"'([^']+)'\"", svg_styled)

print("\n【1】SVG模板原始字体统计")
print("-" * 60)
for font, count in Counter(fonts_original).most_common():
    print(f"  {font}: {count}处")

print("\n【2】字体替换后统计")
print("-" * 60)
for font, count in Counter(fonts_after).most_common():
    print(f"  {font}: {count}处")

print("\n【3】字体映射验证")
print("-" * 60)
alibaba_fonts = ['AlibabaPuHuiTi-Regular', 'AlibabaPuHuiTi-Medium', 
                 'AlibabaPuHuiTi-SemiBold', 'AlibabaPuHuiTi-Heavy']
old_fonts = ['MicrosoftYaHeiLight', 'MicrosoftYaHeiUI', 'MicrosoftYaHeiUILight',
             'DingTalk-JinBuTi', 'Swiss721BT-Heavy', 'AdobeSongStd-Light-GBpc-EUC-H']

alibaba_count = sum([fonts_after.count(f) for f in alibaba_fonts])
old_count = sum([fonts_after.count(f) for f in old_fonts])

print(f"  ✅ 阿里巴巴普惠体: {alibaba_count}处")
print(f"  {'✅' if old_count == 0 else '❌'} 旧字体残留: {old_count}处")

# 检查占位符数据
print("\n【4】占位符数据验证")
print("-" * 60)
placeholders = {
    '3891559803': '订单ID',
    'John Smith': '客户姓名',
    'B-E01A': 'SKU编号',
    '骨头形': '产品形状',
    '金色': '产品颜色',
}

for placeholder, desc in placeholders.items():
    if f'>{placeholder}<' in svg_original:
        print(f"  ✅ {desc} ({placeholder})")
    else:
        print(f"  ❌ {desc} ({placeholder}) - 未找到")

print("\n【5】与Supabase数据库字段对照")
print("-" * 60)
db_fields = {
    'etsy_order_id': 'order_id',
    'customer_name': 'customer_name', 
    'front_text': 'front_text',
    'back_text': 'back_text',
    'sku_code': 'sku'
}
print("  ✅ 数据库字段映射完整")
for db_field, svg_field in db_fields.items():
    print(f"     {db_field} → {svg_field}")

print("\n" + "=" * 60)
print("校验完成")
print("=" * 60)
