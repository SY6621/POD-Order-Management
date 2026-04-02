"""
更新数据库orders表的status值从英文改为中文
pending -> 新订单
producing -> 生产中
"""
from dotenv import load_dotenv
load_dotenv()
import os
from supabase import create_client

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
s = create_client(url, key)

# 1. 查看当前所有订单状态
print('=== 更新前状态 ===')
r = s.table('orders').select('etsy_order_id,status').execute()
for x in r.data:
    print(f'  {x.get("etsy_order_id")}: status={x["status"]}')

# 2. pending -> 新订单
r1 = s.table('orders').update({'status': '新订单'}).eq('status', 'pending').execute()
print(f'\npending -> 新订单: {len(r1.data)} 条')

# 3. producing -> 生产中
r2 = s.table('orders').update({'status': '生产中'}).eq('status', 'producing').execute()
print(f'producing -> 生产中: {len(r2.data)} 条')

# 4. 查看更新后
print('\n=== 更新后状态 ===')
r = s.table('orders').select('etsy_order_id,status').execute()
for x in r.data:
    print(f'  {x.get("etsy_order_id")}: status={x["status"]}')

print('\n✅ 数据库status更新完成')
