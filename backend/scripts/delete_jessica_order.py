# -*- coding: utf-8 -*-
"""删除 Jessica Head 订单以便重新抓取测试"""

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

print("=" * 60)
print("删除 Jessica Head 订单 (4002217518)")
print("=" * 60)

# 查找订单
order = supabase.table('orders').select('id, etsy_order_id, customer_name').eq('etsy_order_id', '4002217518').execute()

if order.data:
    order_id = order.data[0]['id']
    print(f"\n找到订单: {order.data[0]}")
    
    # 删除关联的 production_documents
    supabase.table('production_documents').delete().eq('order_id', order_id).execute()
    print("✅ 已删除 production_documents")
    
    # 删除关联的 logistics
    supabase.table('logistics').delete().eq('order_id', order_id).execute()
    print("✅ 已删除 logistics")
    
    # 删除订单
    supabase.table('orders').delete().eq('id', order_id).execute()
    print("✅ 已删除订单 4002217518 (Jessica Head)")
else:
    print("⚠️ 订单不存在或已删除")

print("\n" + "=" * 60)
print("现在可以重新抓取邮件了")
print("=" * 60)
