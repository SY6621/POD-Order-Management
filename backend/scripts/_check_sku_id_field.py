import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8',errors='replace')
sys.path.insert(0,'.')
from src.services.database_service import db
order = db.get_order_by_etsy_id('3986891868')
print('sku_id       =', repr(order.get('sku_id')))
print('matched_sku_id=', repr(order.get('matched_sku_id')))

# 同时查 sku_mapping 表，确认 sku_code 字段
sku = db.select_one('sku_mapping', {'id': order.get('matched_sku_id')})
if sku:
    print('sku_code     =', repr(sku.get('sku_code')))
    print('sku_mapping全部字段:', list(sku.keys()))
