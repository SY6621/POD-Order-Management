# -*- coding: utf-8 -*-
"""
删除测试订单（PO-开头）
保留真实订单
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
print("删除测试订单（PO-开头）")
print("=" * 70)

# 1. 查找所有测试订单
result = supabase.table('orders').select('id, etsy_order_id, customer_name').like('etsy_order_id', 'PO-%').execute()

if not result.data:
    print("✅ 没有测试订单需要删除")
else:
    print(f"\n找到 {len(result.data)} 条测试订单:")
    for order in result.data:
        print(f"  - {order['etsy_order_id']}: {order['customer_name']}")
    
    # 2. 删除关联的 production_documents
    order_ids = [order['id'] for order in result.data]
    for order_id in order_ids:
        supabase.table('production_documents').delete().eq('order_id', order_id).execute()
    print(f"\n✅ 已删除 production_documents 关联记录")
    
    # 3. 删除关联的 logistics
    for order_id in order_ids:
        supabase.table('logistics').delete().eq('order_id', order_id).execute()
    print(f"✅ 已删除 logistics 关联记录")
    
    # 4. 删除订单
    delete_result = supabase.table('orders').delete().like('etsy_order_id', 'PO-%').execute()
    print(f"✅ 已删除 {len(result.data)} 条测试订单")

# 5. 显示剩余订单
print("\n" + "=" * 70)
print("剩余订单列表")
print("=" * 70)

remaining = supabase.table('orders').select('etsy_order_id, customer_name, status').order('created_at', desc=True).execute()
print(f"\n共 {len(remaining.data)} 条订单:\n")
for order in remaining.data:
    print(f"  - {order['etsy_order_id']}: {order['customer_name']} ({order['status']})")

print("\n✅ 清理完成！测试环境已准备就绪")
