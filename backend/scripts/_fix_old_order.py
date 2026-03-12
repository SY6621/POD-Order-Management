"""
修复旧订单字段：
  - matched_sku_id: 补填 B-G01B（Heart/Gold/L）
  - product_shape / color / size: 统一改为中文
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from src.services.database_service import db
from src.services.order_service import lookup_sku, _SHAPE_MAP, _COLOR_MAP, _SIZE_MAP

ETSY_ID = '3986891868'

order = db.get_order_by_etsy_id(ETSY_ID)
if not order:
    print('未找到该订单')
    exit()

print(f'修复前：')
print(f'  product_shape  = {order["product_shape"]}')
print(f'  product_color  = {order["product_color"]}')
print(f'  product_size   = {order["product_size"]}')
print(f'  matched_sku_id = {order["matched_sku_id"]}')

# 英文 → 中文转换
shape_en = order['product_shape']
color_en = order['product_color']
size_en  = order['product_size']

cn_shape = _SHAPE_MAP.get(shape_en, shape_en)
cn_color = _COLOR_MAP.get(color_en, color_en)
cn_size  = _SIZE_MAP.get(size_en, size_en)

# 查 SKU（返回完整行，包含 UUID id 和 sku_code）
sku = lookup_sku(shape_en, color_en, size_en)
# matched_sku_id 字段是 UUID 类型，存 sku_mapping.id
skm_uuid  = sku['id']       if sku else None
skm_code  = sku['sku_code'] if sku else ''
print(f'  SKU UUID: {skm_uuid}')
print(f'  SKU Code: {skm_code}')

# 更新数据库（使用通用 update 方法）
result = db.update('orders', {'id': order['id']}, {
    'product_shape':  cn_shape,
    'product_color':  cn_color,
    'product_size':   cn_size,
    'matched_sku_id': skm_uuid,
})

if result:
    print(f'\n修复后：')
    print(f'  product_shape  = {cn_shape}')
    print(f'  product_color  = {cn_color}')
    print(f'  product_size   = {cn_size}')
    print(f'  matched_sku_id = {skm_uuid}  ({skm_code})')
    print('\n✅ 修复完成')
else:
    print('\n❌ 更新失败，请检查 update 方法')
