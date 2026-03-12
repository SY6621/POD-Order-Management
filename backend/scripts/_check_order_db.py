"""查看数据库中订单 3986891868 的完整字段"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from src.services.database_service import db

order = db.get_order_by_etsy_id('3986891868')
if order:
    print('订单已存在，字段如下：')
    for k, v in order.items():
        print(f'  {k:25} = {v}')
else:
    print('未找到该订单')
