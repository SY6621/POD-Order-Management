import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from src.services.database_service import db

rows = db.select('sku_mapping', limit=3)
if rows:
    print('字段名:', list(rows[0].keys()))
    for r in rows:
        print(r)
else:
    print('sku_mapping 表为空')
