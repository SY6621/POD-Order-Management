import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path('.env'))
from src.services.database_service import db

# 查询所有订单
result = db._client.table('orders').select('id, etsy_order_id, customer_name, status, sku_id, matched_sku_id').execute()
print(f'=== orders表共 {len(result.data)} 条 ===\n')

# 状态分布
statuses = {}
for o in result.data:
    s = o.get('status', 'unknown')
    statuses[s] = statuses.get(s, 0) + 1
print(f'状态分布: {statuses}\n')

# 查询logistics表
logistics = db._client.table('logistics').select('*').execute()
print(f'=== logistics表共 {len(logistics.data)} 条 ===\n')

# 为每个logistics记录构建订单关联
logistics_by_order = {}
for l in logistics.data:
    logistics_by_order[l.get('order_id')] = l

# 列出所有订单详情
print('--- 订单列表 ---')
for o in result.data:
    order_id = o.get('id')
    log = logistics_by_order.get(order_id, {})
    country = log.get('country', '')
    has_addr = bool(log.get('street_address'))
    has_name = bool(log.get('recipient_name'))
    has_tracking = bool(log.get('tracking_number'))
    is_au = ' [AU]' if str(country).upper() in ('AU', 'AUSTRALIA') else '     '
    print(f'{is_au} Etsy#{o.get("etsy_order_id","")} | {o.get("customer_name","")[:15]} | status:{o.get("status","")} | country:{country} | addr:{"Y" if has_addr else "N"} | name:{"Y" if has_name else "N"} | tracking:{"Y" if has_tracking else "N"}')

print('\n' + '='*60)
print('\n--- Logistics详情 ---')
for l in logistics.data:
    print(f'  order_id:{str(l.get("order_id",""))[:8]}... | tracking:{l.get("tracking_number","")} | status:{l.get("shipping_status","")} | recipient:{l.get("recipient_name","")} | country:{l.get("country","")} | addr:{l.get("street_address","")[:20] if l.get("street_address") else "无"}')

# 已下单的order_id列表
shipped_order_ids = [l.get('order_id') for l in logistics.data if l.get('tracking_number')]
print(f'\n已有物流单号的订单ID: {len(shipped_order_ids)} 条')
for oid in shipped_order_ids:
    print(f'  - {oid}')

