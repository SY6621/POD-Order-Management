# -*- coding: utf-8 -*-
"""
测试查询 delivered 状态的订单
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
print("测试查询 delivered 状态的订单")
print("=" * 70)

# 查询 delivered 状态的订单
result = supabase.table('orders').select('*').eq('status', 'delivered').execute()

print(f"\n查询结果: {len(result.data)} 条订单")

if result.data:
    for order in result.data:
        print(f"\n订单ID: {order['id']}")
        print(f"Etsy订单号: {order.get('etsy_order_id', 'N/A')}")
        print(f"客户: {order.get('customer_name', 'N/A')}")
        print(f"状态: {order['status']}")
else:
    print("没有 delivered 状态的订单")
    
    # 检查所有订单状态
    print("\n" + "=" * 70)
    print("检查所有订单状态:")
    print("=" * 70)
    all_orders = supabase.table('orders').select('etsy_order_id, customer_name, status').execute()
    for o in all_orders.data:
        print(f"  {o.get('etsy_order_id', 'N/A')}: {o.get('customer_name', 'N/A')} - {o['status']}")
