"""
效果图自动生成测试
流程：从数据库取订单 → 构建配置 → 生成SVG → 上传Storage → 回写URL
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')

from src.services.database_service import db
from src.services.effect_template_service import (
    generate_effect_image_for_order,
    _build_config_from_order,
)

ETSY_ID = '3986891868'

print('=' * 60)
print('  效果图自动生成测试')
print('=' * 60)

# Step 1: 取订单
order = db.get_order_by_etsy_id(ETSY_ID)
if not order:
    print('❌ 未找到订单，退出')
    exit()

print(f'\n[Step 1] 订单数据：')
print(f'  外观: {order["product_shape"]}')
print(f'  颜色: {order["product_color"]}')
print(f'  大小: {order["product_size"]}')
print(f'  正面: {order["front_text"]}  字体: {order["font_code"]}')
print(f'  背面: {order["back_text"]}')

# Step 2: 构建配置（验证解析是否正确）
config = _build_config_from_order(order)
print(f'\n[Step 2] 构建 EffectConfig：')
print(f'  shape={config.shape}, size={config.size}, color={config.color}')
print(f'  front.text="{config.front.text}"  font_family="{config.front.font_family}"')
print(f'  back.text_content="{config.back.text_content}"')
print(f'  back.phone_number="{config.back.phone_number}"')

# Step 3: 生成SVG（先不上传，本地验证）
print(f'\n[Step 3] 生成 SVG（本地保存，不上传）...')
local_path = generate_effect_image_for_order(order, upload=False)
if local_path:
    print(f'  ✅ 本地 SVG: {local_path}')
else:
    print('  ❌ SVG 生成失败')
    exit()

# Step 4: 上传到 Supabase Storage
print(f'\n[Step 4] 上传到 Supabase Storage...')
url = generate_effect_image_for_order(order, upload=True)
if url:
    print(f'  ✅ 效果图 URL: {url}')

    # Step 5: 回写 orders.effect_image_url
    print(f'\n[Step 5] 回写 effect_image_url 到数据库...')
    result = db.update('orders', {'id': order['id']}, {'effect_image_url': url})
    if result:
        print(f'  ✅ 数据库已更新')
    else:
        print(f'  ❌ 数据库更新失败')
else:
    print('  ❌ 上传失败，请检查 Supabase Storage bucket "effect-images" 是否存在')

print('\n' + '=' * 60)
