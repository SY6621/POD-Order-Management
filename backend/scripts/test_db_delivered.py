# -*- coding: utf-8 -*-
"""
使用 database.py 测试查询 delivered 订单
"""
import sys
sys.path.insert(0, 'd:\\ETSY_Order_Automation\\backend')

from src.utils.database import db

orders = db.select('orders', {'status': 'delivered'})
print(f'找到 {len(orders)} 条 delivered 订单')
for o in orders[:3]:
    print(f'  - {o.get("etsy_order_id")}: {o.get("customer_name")}')
