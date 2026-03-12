"""查询 sku_mapping 表中颜色和大小的全部实际值"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from src.services.database_service import db

rows = db.select('sku_mapping')
print(f'共 {len(rows)} 条记录\n')

colors = sorted(set(r['color'] for r in rows))
sizes  = sorted(set(r['size']  for r in rows))
shapes = sorted(set(r['shape'] for r in rows))

print('颜色全部值:', colors)
print('大小全部值:', sizes)
print('外观全部值:', shapes)
print()
print('--- 详细列表 ---')
for r in rows:
    print(f"  {r['sku_code']:8} | 外观:{r['shape']:4} | 颜色:{r['color']:6} | 大小:{r['size']}")
