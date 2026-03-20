# -*- coding: utf-8 -*-
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_SERVICE_KEY')
supabase = create_client(url, key)

# 查询已完成订单
result = supabase.table('orders').select('*').eq('status', 'delivered').limit(5).execute()
print('已完成订单列表:')
for o in result.data:
    print(f"  ID: {o['id']}, 订单号: {o.get('etsy_order_id')}, 客户: {o.get('customer_name')}")
