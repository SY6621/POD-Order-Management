# -*- coding: utf-8 -*-
"""验证 email_parser 解析结果"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from src.services.email_parser import email_parser

# 格式一：标准 Front/Back + 字体代码
body1 = """Your order number is: 3794236690

* Delivery address *
Marinella Nesso
1 Shaw St.
501
Toronto ON M6K 0A1
Canada
* Dispatching internationally? *

Personalization: Front: Luna (F-04) Back: 416.456.3524
Color + Size:: Gold Large
Quantity: 1
Order total: AU$45.00
"""

# 格式二：不分面，带备注 + 字体代码
body2 = """Your order number is: 3794236691

* Delivery address *
Ocean Melanson
105 Bridge St
Sackville NB E4L 3P4
Canada
* Dispatching internationally? *

Personalization: Chloe (F-04) (with a heart below the name) 5062290282
Color + Size:: Silver Small
Quantity: 1
Order total: AU$30.00
"""

# 格式三：无字体代码（ID=4120 这封）
body3 = """---------- Forwarded message ---------
From: Etsy Transactions <transaction@etsy.com>

Your order number is: 3891559803

* Delivery address *
Demi Brooker
3/1A Salisbury Rd
ROSE BAY NSW 2029
Australia
* Dispatching internationally? *

Custom Heart Pet ID Tag
Color + Size:: Gold Large
Personalization: Spirit 0402 830 481
Quantity: 1
Order total: AU$34.46
"""

for i, (label, body) in enumerate([
    ("格式一：标准Front/Back+字体", body1),
    ("格式二：不分面+备注+字体", body2),
    ("格式三：无字体代码（ID=4120）", body3),
], 1):
    print(f"\n{'='*50}")
    print(f"【{label}】")
    r = email_parser.parse_forwarded_email(body)
    if not r:
        print("  ❌ 解析失败")
        continue
    print(f"  订单号: {r.etsy_order_id}")
    print(f"  客户名: {r.customer_name}")
    print(f"  城市:   {r.shipping_city} {r.shipping_state} {r.shipping_zip}")
    print(f"  国家:   {r.shipping_country}")
    if r.items:
        item = r.items[0]
        print(f"  正面刻字: [{item.customization_front}]")
        print(f"  背面刻字: [{item.customization_back}]")
        print(f"  字体代码: [{item.font_code}]")
        print(f"  颜色/尺寸: {item.color} / {item.size}")
    status = "✅ OK" if r.customer_name and r.customer_name != "*" else "❌ 客户名异常"
    print(f"  {status}")
