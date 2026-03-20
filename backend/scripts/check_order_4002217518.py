# -*- coding: utf-8 -*-
"""检查订单 4002217518 的完整数据"""

from supabase import create_client
import os

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars

env = load_env()
supabase = create_client(env['SUPABASE_URL'], env['SUPABASE_KEY'])

print("=" * 70)
print("检查订单 4002217518 数据")
print("=" * 70)

# 查询 orders 表
order = supabase.table('orders').select('*').eq('etsy_order_id', '4002217518').execute()

if not order.data:
    print("❌ 订单不存在")
else:
    print("\n【orders 表】")
    print("-" * 50)
    for k, v in order.data[0].items():
        print(f"  {k}: {v}")
    
    # 查询 logistics 表
    order_id = order.data[0]['id']
    logistics = supabase.table('logistics').select('*').eq('order_id', order_id).execute()
    
    print("\n【logistics 表】")
    print("-" * 50)
    if logistics.data:
        for k, v in logistics.data[0].items():
            print(f"  {k}: {v}")
    else:
        print("  无物流记录")

print("\n" + "=" * 70)
