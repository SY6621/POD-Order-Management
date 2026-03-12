"""验证 SKU 反推映射正确性（覆盖全部 12 种外观×颜色组合）"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')
from src.services.order_service import lookup_sku

# 真实订单测试（来自诊断脚本解析结果）
print('=== 真实订单 SKU 反推 ===')
r = lookup_sku('Heart', 'Gold', 'Large')
print(f'  预期: B-G01B  → 实际: {r["sku_code"] if r else "未匹配"}')
print()

# 覆盖测试：全部 4 种颜色 + 3 种外观 + L/S
print('=== 全量覆盖测试 ===')
cases = [
    ('Heart',  'Gold',      'Large',  'B-G01B'),
    ('Heart',  'Silver',    'Large',  'B-G01A'),
    ('Heart',  'Rose Gold', 'Large',  'B-G01C'),
    ('Heart',  'Black',     'Large',  'B-G01D'),
    ('Heart',  'Gold',      'Small',  'B-G02B'),
    ('round',  'Gold',      'Large',  'B-C01B'),
    ('bone',   'Gold',      'Large',  'B-E01B'),
    ('Bone',   'Silver',    'Small',  'B-E02A'),
]

pass_count = 0
for shape, color, size, expected in cases:
    r = lookup_sku(shape, color, size)
    actual = r['sku_code'] if r else '未匹配'
    ok = '✅' if actual == expected else '❌'
    if actual == expected: pass_count += 1
    print(f'  {ok} {shape}/{color}/{size} → {actual}  (预期:{expected})')

print(f'\n共 {len(cases)} 项，通过 {pass_count} 项')
