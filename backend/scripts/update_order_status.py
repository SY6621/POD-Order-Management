import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path('.env'))
from src.services.database_service import db

# 找到Etsy#3986891868订单
result = db._client.table('orders').select('id, etsy_order_id, status, customer_name').eq('etsy_order_id', '3986891868').execute()

if not result.data:
    print('❌ 未找到订单 Etsy#3986891868')
else:
    order = result.data[0]
    print(f'找到订单: {order["etsy_order_id"]} | {order["customer_name"]} | 当前状态: {order["status"]}')
    
    # 更新为confirmed
    update_result = db._client.table('orders').update({'status': 'confirmed'}).eq('id', order['id']).execute()
    print(f'✅ 已更新 Etsy#{order["etsy_order_id"]} → confirmed')
    
    # 验证更新
    verify = db._client.table('orders').select('id, etsy_order_id, status').eq('id', order['id']).execute()
    print(f'验证: {verify.data[0]["etsy_order_id"]} 状态为 {verify.data[0]["status"]}')

# 再查询一下还有没有其他有地址但非confirmed的订单
print('\n--- 检查其他候选订单 ---')
orders = db._client.table('orders').select('id, etsy_order_id, customer_name, status').execute()
logistics = db._client.table('logistics').select('order_id, street_address, tracking_number').execute()

logistics_map = {l['order_id']: l for l in logistics.data}

for o in orders.data:
    log = logistics_map.get(o['id'], {})
    has_addr = bool(log.get('street_address'))
    has_tracking = bool(log.get('tracking_number'))
    if has_addr and not has_tracking and o['status'] != 'confirmed':
        print(f'  候选: Etsy#{o["etsy_order_id"]} | {o["customer_name"]} | 状态:{o["status"]} (有地址无tracking)')
