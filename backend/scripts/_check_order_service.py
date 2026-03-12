from pathlib import Path
f = Path('src/services/order_service.py')
t = f.read_text(encoding='utf-8')

# 打印当前颜色映射相关行，确认实际内容
for i, line in enumerate(t.split('\n'), 1):
    if 'Silver' in line or 'Rose' in line or 'RoseGold' in line or 'sku_mapping' in line.lower():
        print(f"L{i}: {repr(line)}")
