# -*- coding: utf-8 -*-
"""重置订单状态为 pending，清空效果图和物流数据（用于循环测试）"""

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
print("重置订单状态（清空效果图/物流数据，状态改为 pending）")
print("=" * 70)

# 获取所有真实订单（非PO-开头）
orders = supabase.table('orders').select('id, etsy_order_id, customer_name, status').execute()

real_orders = [o for o in orders.data if not o['etsy_order_id'].startswith('PO-')]

print(f"\n找到 {len(real_orders)} 个真实订单:\n")
for order in real_orders:
    print(f"  - {order['etsy_order_id']}: {order['customer_name']} ({order['status']})")
    
    # 1. 清空 production_documents 表的 effect_svg_url
    docs = supabase.table('production_documents').select('id').eq('order_id', order['id']).execute()
    if docs.data:
        for doc in docs.data:
            supabase.table('production_documents').update({
                'effect_svg_url': None,
                'shipping_label_url': None,
                'updated_at': 'now()'
            }).eq('id', doc['id']).execute()
        print(f"    ✅ 已清空 production_documents 效果图/面单URL")
    
    # 2. 清空 orders 表的 effect_image_url
    supabase.table('orders').update({
        'effect_image_url': None,
        'effect_image_back_url': None,
        'status': 'pending',
        'updated_at': 'now()'
    }).eq('id', order['id']).execute()
    print(f"    ✅ 已清空 orders 效果图，状态改为 pending")
    
    # 3. 清空 logistics 表的 4PX 相关数据
    logistics = supabase.table('logistics').select('id').eq('order_id', order['id']).execute()
    if logistics.data:
        for log in logistics.data:
            supabase.table('logistics').update({
                'tracking_number': '',
                'label_url': None,
                'carrier_api_order_id': None,
                'carrier_api_response': None,
                'shipping_status': 'pending',
                'updated_at': 'now()'
            }).eq('id', log['id']).execute()
        print(f"    ✅ 已清空 logistics 物流数据")

print("\n" + "=" * 70)
print("所有订单已重置为 pending 状态，可以开始测试")
print("=" * 70)

# 显示当前状态
print("\n【当前订单状态】")
orders = supabase.table('orders').select('etsy_order_id, customer_name, status').execute()
for o in orders.data:
    print(f"  - {o['etsy_order_id']}: {o['customer_name']} ({o['status']})")
