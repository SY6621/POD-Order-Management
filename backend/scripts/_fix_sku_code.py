import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8',errors='replace')
sys.path.insert(0,'.')
from src.services.database_service import db

order = db.get_order_by_etsy_id('3986891868')
print('补填前 sku_id =', repr(order.get('sku_id')))

sku = db.select_one('sku_mapping', {'id': order['matched_sku_id']})
sku_code = sku['sku_code']
print('从 sku_mapping 取到 sku_code =', repr(sku_code))

result = db.update('orders', {'id': order['id']}, {'sku_id': sku_code})
if result:
    print('✅ 补填成功，sku_id =', result.get('sku_id'))
else:
    print('❌ 补填失败')

# 再次验证
order2 = db.get_order_by_etsy_id('3986891868')
print('补填后 sku_id =', repr(order2.get('sku_id')))
