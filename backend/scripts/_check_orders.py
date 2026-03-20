# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from services.database import db

# 查询已完成订单
orders = db.select('orders', {'status': 'delivered'}, limit=5)
print('已完成订单列表:')
for o in orders:
    print(f"  ID: {o['id']}, 订单号: {o.get('etsy_order_id', 'N/A')}, 客户: {o.get('customer_name', 'N/A')}")
