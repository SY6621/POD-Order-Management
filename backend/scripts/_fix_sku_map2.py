from pathlib import Path
f = Path('src/services/order_service.py')
t = f.read_text(encoding='utf-8')

# 修正debug输出里的字段名
t = t.replace("result.get('sku_id') or result.get('id')", "result.get('sku_code') or result.get('id')")
# 修正注释
t = t.replace('"Medium": "L",   # Medium 暂映射到 大', '"Medium": "L",   # Medium 暂映射到 L')

f.write_text(t, encoding='utf-8')
print('done')
