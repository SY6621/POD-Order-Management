# -*- coding: utf-8 -*-
"""
检查当前订单状态并重置三个真实订单到"新订单"状态
目标：将订单分配到"待确认订单页面"的"新订单"Tab
"""

from supabase import create_client
import os

def load_env():
    """加载环境变量"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars

# 初始化 Supabase 客户端
env = load_env()
supabase = create_client(env['SUPABASE_URL'], env['SUPABASE_KEY'])

print("=" * 70)
print("检查并重置订单状态")
print("=" * 70)

# 1. 查询所有订单
print("\n【步骤 1: 查询当前所有订单】")
orders = supabase.table('orders').select('''
    id, 
    etsy_order_id, 
    customer_name, 
    status,
    effect_image_url,
    email_sent,
    created_at
''').order('created_at', desc=True).execute()

print(f"\n共找到 {len(orders.data)} 个订单:\n")
for i, order in enumerate(orders.data, 1):
    status_display = order['status']
    effect_status = "✓" if order.get('effect_image_url') else "✗"
    email_status = "✓" if order.get('email_sent') else "✗"
    print(f"{i}. {order['etsy_order_id']}: {order['customer_name']}")
    print(f"   状态：{status_display} | 效果图：{effect_status} | 邮件已发送：{email_status}")
    print(f"   创建时间：{order['created_at']}")
    print()

# 2. 筛选真实订单（非 PO-开头的测试订单）
real_orders = [o for o in orders.data if not o['etsy_order_id'].startswith('PO-')]

print(f"\n真实订单数量：{len(real_orders)}")

# 3. 选择前三个真实订单进行重置
if len(real_orders) < 3:
    print(f"\n❌ 真实订单不足 3 个（当前：{len(real_orders)}个）")
    print("请确保数据库中至少有 3 个真实订单")
    exit(1)

orders_to_reset = real_orders[:3]

print(f"\n【步骤 2: 准备重置以下 3 个订单为'新订单'状态】\n")
for order in orders_to_reset:
    print(f"  - {order['etsy_order_id']}: {order['customer_name']} (当前状态：{order['status']})")

print("\n" + "=" * 70)
confirm = input("\n是否继续执行重置？(y/n): ").strip().lower()
if confirm != 'y':
    print("\n❌ 操作已取消")
    exit(0)

# 4. 执行重置操作
print("\n【步骤 3: 执行重置操作】\n")

for order in orders_to_reset:
    order_id = order['id']
    etsy_id = order['etsy_order_id']
    
    print(f"处理订单：{etsy_id}")
    
    # 1. 清空 production_documents 表的 effect_svg_url
    docs = supabase.table('production_documents').select('id').eq('order_id', order_id).execute()
    if docs.data:
        for doc in docs.data:
            supabase.table('production_documents').update({
                'effect_svg_url': None,
                'shipping_label_url': None,
                'updated_at': 'now()'
            }).eq('id', doc['id']).execute()
        print(f"  ✅ 已清空 production_documents 效果图/面单 URL")
    else:
        print(f"  ℹ️  production_documents 无记录")
    
    # 2. 清空 orders 表的 effect_image_url 和 email_sent，状态改为 'pending'
    # 注意：前端"新订单"Tab 的筛选条件是：status === 'pending' && !effect_image_url
    update_data = {
        'effect_image_url': None,
        'effect_image_back_url': None,
        'email_sent': False,  # 确保邮件发送标志为 False
        'status': 'pending',  # 保持 pending 状态（前端会显示为"新订单"）
        'updated_at': 'now()'
    }
    
    supabase.table('orders').update(update_data).eq('id', order_id).execute()
    print(f"  ✅ 已清空 orders 效果图和邮件标志，状态设为 pending")
    
    # 3. 清空 logistics 表的 4PX 相关数据
    logistics = supabase.table('logistics').select('id').eq('order_id', order_id).execute()
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
        print(f"  ✅ 已清空 logistics 物流数据")
    else:
        print(f"  ℹ️  logistics 无记录")
    
    print()

# 5. 验证重置结果
print("\n【步骤 4: 验证重置结果】\n")

reset_orders = supabase.table('orders').select('''
    id, 
    etsy_order_id, 
    customer_name, 
    status,
    effect_image_url,
    email_sent
''').in_('id', [o['id'] for o in orders_to_reset]).execute()

print("重置后的订单状态：\n")
all_correct = True
for order in reset_orders.data:
    status_ok = order['status'] == 'pending'
    effect_ok = order.get('effect_image_url') is None
    email_ok = order.get('email_sent') == False
    
    status_symbol = "✅" if (status_ok and effect_ok and email_ok) else "❌"
    
    print(f"{status_symbol} {order['etsy_order_id']}: {order['customer_name']}")
    print(f"   状态：{order['status']} ({'✓' if status_ok else '✗'})")
    print(f"   效果图：{'None' if effect_ok else 'Has URL'} ({'✓' if effect_ok else '✗'})")
    print(f"   邮件已发送：{order.get('email_sent')} ({'✓' if email_ok else '✗'})")
    print()
    
    if not (status_ok and effect_ok and email_ok):
        all_correct = False

print("=" * 70)
if all_correct:
    print("✅ 所有订单重置成功！")
    print("\n现在可以在前端访问：http://localhost:5173/admin/orders/pending")
    print("这 3 个订单将显示在【新订单】Tab 中")
else:
    print("❌ 部分订单重置失败，请检查上方标记为 ❌ 的订单")
print("=" * 70)
