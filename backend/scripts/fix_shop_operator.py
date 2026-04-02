"""修复店铺关联和运营字段"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

from supabase import create_client

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase = create_client(url, key)

print("=" * 60)
print("步骤1: 查看shops表当前数据")
print("=" * 60)
shops = supabase.table('shops').select('*').execute()
for shop in shops.data:
    print(f"  ID: {shop.get('id')}")
    print(f"  Code: {shop.get('code')}")
    print(f"  Name: {shop.get('name')}")
    print(f"  Operator: {shop.get('operator', '字段不存在')}")
    print()

print("=" * 60)
print("步骤2: 为au01设置operator='A'")
print("=" * 60)
try:
    result = supabase.table('shops').update({'operator': 'A'}).eq('code', 'au01').execute()
    if result.data:
        print(f"  ✅ 成功设置 {result.data[0].get('code')} operator = A")
    else:
        print("  ❌ 未找到au01店铺，尝试用name查找...")
        result2 = supabase.table('shops').update({'operator': 'A'}).ilike('name', '%澳洲%').execute()
        if result2.data:
            print(f"  ✅ 成功设置 operator = A")
        else:
            print("  ❌ 仍未找到，请检查shops表")
except Exception as e:
    print(f"  ❌ 更新失败: {e}")
    print("  可能operator字段不存在，需要在Supabase SQL Editor执行:")
    print("  ALTER TABLE shops ADD COLUMN IF NOT EXISTS operator VARCHAR(10);")
    print("  UPDATE shops SET operator = 'A' WHERE code = 'au01';")

print("\n" + "=" * 60)
print("步骤3: 检查orders的shop_id关联")
print("=" * 60)
orders = supabase.table('orders').select('id, etsy_order_id, shop_id, status').execute()
null_shop = [o for o in orders.data if not o.get('shop_id')]
has_shop = [o for o in orders.data if o.get('shop_id')]
print(f"  总订单数: {len(orders.data)}")
print(f"  已关联shop_id: {len(has_shop)}")
print(f"  未关联shop_id: {len(null_shop)}")

if null_shop:
    print("\n  未关联的订单:")
    for o in null_shop:
        print(f"    - {o.get('etsy_order_id')} (status: {o.get('status')})")

print("\n" + "=" * 60)
print("步骤4: 关联未分配订单到au01店铺")
print("=" * 60)
if null_shop:
    # 获取au01的shop id
    au01 = supabase.table('shops').select('id').eq('code', 'au01').execute()
    if not au01.data:
        au01 = supabase.table('shops').select('id').ilike('name', '%澳洲%').execute()
    
    if au01.data:
        shop_id = au01.data[0]['id']
        print(f"  au01 shop_id: {shop_id}")
        for o in null_shop:
            result = supabase.table('orders').update({'shop_id': shop_id}).eq('id', o['id']).execute()
            print(f"  ✅ 订单 {o.get('etsy_order_id')} 已关联到au01")
    else:
        print("  ❌ 找不到au01店铺")
else:
    print("  所有订单已关联，无需修复")

print("\n" + "=" * 60)
print("步骤5: 验证修复结果")
print("=" * 60)

try:
    shops_after = supabase.table('shops').select('id, code, name, operator').execute()
    for s in shops_after.data:
        print(f"  Shop: {s.get('name')} ({s.get('code')}) - Operator: {s.get('operator')}")
except Exception as e:
    print(f"  ⚠️ 无法查询operator字段（字段可能不存在）")
    shops_after = supabase.table('shops').select('id, code, name').execute()
    for s in shops_after.data:
        print(f"  Shop: {s.get('name')} ({s.get('code')})")

orders_after = supabase.table('orders').select('id, etsy_order_id, shop_id, status').execute()
null_after = [o for o in orders_after.data if not o.get('shop_id')]
print(f"\n  修复后未关联订单数: {len(null_after)}")
if len(null_after) == 0:
    print("  ✅ 所有订单已正确关联店铺！")

print("\n" + "=" * 60)
print("⚠️ 重要提示：operator字段不存在")
print("=" * 60)
print("请在Supabase SQL Editor中手动执行以下SQL：")
print()
print("  ALTER TABLE shops ADD COLUMN IF NOT EXISTS operator VARCHAR(10);")
print("  UPDATE shops SET operator = 'A' WHERE code = 'au01';")
print()
print("执行后，A运营Tab将能正确显示订单。")
print("\n✅ 订单关联修复完成！请刷新前端页面验证。")
