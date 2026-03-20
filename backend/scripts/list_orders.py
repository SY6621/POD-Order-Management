# -*- coding: utf-8 -*-
"""
查看并清理测试订单
"""

from supabase import create_client
import os

def load_env_from_file():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars

env_vars = load_env_from_file()
url = env_vars.get('SUPABASE_URL')
key = env_vars.get('SUPABASE_KEY')
supabase = create_client(url, key)

print("=" * 70)
print("当前数据库订单列表")
print("=" * 70)

result = supabase.table('orders').select('id, etsy_order_id, customer_name, status, created_at').order('created_at', desc=True).execute()

print(f"\n共 {len(result.data)} 条订单:\n")
print(f"{'序号':^4} | {'Etsy订单号':<15} | {'客户':<20} | {'状态':<12} | {'创建日期':<12}")
print("-" * 80)

for i, order in enumerate(result.data, 1):
    etsy_id = order.get('etsy_order_id') or 'N/A'
    customer = order.get('customer_name') or 'N/A'
    status = order.get('status') or 'N/A'
    created = order.get('created_at', '')[:10] if order.get('created_at') else 'N/A'
    
    # 标记测试订单
    is_test = etsy_id.startswith('PO-') or etsy_id == 'N/A'
    marker = '[测试]' if is_test else ''
    
    print(f"{i:^4} | {etsy_id:<15} | {customer:<20} | {status:<12} | {created:<12} {marker}")

print("\n" + "=" * 70)
print("说明：[测试] 标记的订单是测试数据，可以删除")
print("=" * 70)
