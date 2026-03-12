from pathlib import Path
f = Path('src/services/order_service.py')
t = f.read_text(encoding='utf-8')

# 修正：Silver → 银色（不是钢本色）
t = t.replace('"钢本色"', '"银色"')

# 修正：大小用 L/S（不是大/小）
t = t.replace('"Large":  "大"', '"Large":  "L"')
t = t.replace('"large":  "大"', '"large":  "L"')
t = t.replace('"Small":  "小"', '"Small":  "S"')
t = t.replace('"small":  "小"', '"small":  "S"')
t = t.replace('"Medium": "大"', '"Medium": "L"')

# 修正：主键字段用 sku_code 而不是 sku_id
t = t.replace('matched_sku.get("sku_id")', 'matched_sku.get("sku_code")')

f.write_text(t, encoding='utf-8')
print('done')

# 验证关键行
for i, line in enumerate(t.split('\n'), 1):
    if any(k in line for k in ['Silver', 'Large', 'Small', 'Medium', 'sku_code', 'sku_id']):
        print(f"L{i}: {repr(line)}")
