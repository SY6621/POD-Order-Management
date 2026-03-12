from pathlib import Path
f = Path('src/services/order_service.py')
t = f.read_text(encoding='utf-8')

# 修正颜色映射错别字
t = t.replace('"钔本色"', '"钢本色"')
t = t.replace('"珫瑞金"', '"玫瑰金"')

f.write_text(t, encoding='utf-8')
print('done')

# 验证
for i, line in enumerate(t.split('\n'), 1):
    if 'Silver' in line or 'Rose' in line or 'RoseGold' in line:
        print(f"L{i}: {repr(line)}")
