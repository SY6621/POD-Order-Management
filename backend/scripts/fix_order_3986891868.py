# -*- coding: utf-8 -*-
"""修复订单 3986891868 的 SKU 关联"""

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
print("修复订单 3986891868 的 SKU 关联")
print("=" * 70)

# 获取订单当前数据
order = supabase.table('orders').select('*').eq('etsy_order_id', '3986891868').execute()

if not order.data:
    print("❌ 订单不存在")
else:
    o = order.data[0]
    print(f"\n当前订单数据:")
    print(f"  形状: {o.get('product_shape')}")
    print(f"  颜色: {o.get('product_color')}")
    print(f"  尺寸: {o.get('product_size')}")
    print(f"  sku_id: {o.get('sku_id')}")
    
    # 根据 shape/color/size 查找 SKU
    shape = o.get('product_shape', '')
    color = o.get('product_color', '')
    size = o.get('product_size', '')
    
    # 转换中英文
    shape_map = {'Heart': '心形', 'Round': '圆形', 'Bone': '骨头形'}
    color_map = {'Gold': '金色', 'Silver': '银色', 'Rose Gold': '玫瑰金', 'Black': '黑色'}
    size_map = {'Large': 'L', 'Small': 'S'}
    
    cn_shape = shape_map.get(shape, shape)
    cn_color = color_map.get(color, color)
    cn_size = size_map.get(size, size)
    
    print(f"\n查找 SKU: {cn_shape}/{cn_color}/{cn_size}")
    
    sku = supabase.table('sku_mapping').select('id, sku_code').eq('shape', cn_shape).eq('color', cn_color).eq('size', cn_size).execute()
    
    if sku.data:
        sku_id = sku.data[0]['id']
        sku_code = sku.data[0]['sku_code']
        print(f"✅ 找到 SKU: {sku_code} ({sku_id})")
        
        # 更新订单
        supabase.table('orders').update({'sku_id': sku_id}).eq('id', o['id']).execute()
        print(f"✅ 订单已更新 sku_id")
    else:
        print(f"❌ 未找到匹配的 SKU")

print("\n" + "=" * 70)
