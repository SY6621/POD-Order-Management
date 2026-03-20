# -*- coding: utf-8 -*-
"""检查订单的 sku_id 关联"""

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
print("检查订单 sku_id 关联")
print("=" * 70)

orders = supabase.table('orders').select('etsy_order_id, customer_name, status, sku_id').execute()

print(f"\n共 {len(orders.data)} 条订单:\n")
for o in orders.data:
    print(f"  {o['etsy_order_id']}: {o['customer_name']} ({o['status']})")
    print(f"    sku_id: {o['sku_id']}")
    
    # 检查 sku_mapping
    if o['sku_id']:
        sku = supabase.table('sku_mapping').select('sku_code, shape, color, size').eq('id', o['sku_id']).execute()
        if sku.data:
            print(f"    SKU: {sku.data[0]['sku_code']} ({sku.data[0]['shape']}/{sku.data[0]['color']}/{sku.data[0]['size']})")
        else:
            print(f"    ⚠️ SKU 记录不存在!")
    else:
        print(f"    ⚠️ 未关联 SKU")
    print()
