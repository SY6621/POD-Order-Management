"""
Final comprehensive encoding fix for Dashboard.vue, PendingOrders.vue, Production.vue
Each fix: (old_bytes, new_bytes, description)
Order matters - more specific patterns first
"""

def find_invalid(data):
    positions = []
    i = 0
    while i < len(data):
        b = data[i]
        if b < 0x80:
            i += 1
        elif b < 0xC0:
            positions.append(i)
            i += 1
        elif b < 0xE0:
            if i+1 < len(data) and 0x80 <= data[i+1] <= 0xBF:
                i += 2
            else:
                positions.append(i)
                i += 1
        elif b < 0xF0:
            if i+2 < len(data) and 0x80 <= data[i+1] <= 0xBF and 0x80 <= data[i+2] <= 0xBF:
                i += 3
            else:
                positions.append(i)
                i += 1
        else:
            i += 1
    return positions

# ======== DASHBOARD FIXES ========
dashboard_fixes = [
    # 须24 小时内回复 (须=E9A1BB, '2'=32 was consumed)
    (bytes.fromhex('e9a13f34'), bytes.fromhex('e9a1bb3234'), '须24'),
    # 回复</ (复=E5A48D, < consumed)
    (bytes.fromhex('e5a43f2f'), bytes.fromhex('e5a48d3c2f'), '复</'),
    # 已完成</ (成=E6 88 90, < consumed)
    (bytes.fromhex('e6883f2f'), bytes.fromhex('e688903c2f'), '成</'),
    # 订单状态分布 --> (布=E5B883, space consumed)
    (bytes.fromhex('e5b83f2d2d3e'), bytes.fromhex('e5b88320' + '2d2d3e'), '布 -->'),
    # 订单状态分布</h3> (布=E5B883, < consumed)
    (bytes.fromhex('e5b83f2f6833'), bytes.fromhex('e5b8833c2f6833'), '布</h3>'),
    # 查看全部 →</button> (→=E28692, < consumed)
    (bytes.fromhex('e2863f2f6275'), bytes.fromhex('e286923c2f6275'), '→</button>'),
    # 状态</th> (态=E68081, < consumed)
    (bytes.fromhex('e6803f2f7468'), bytes.fromhex('e680813c2f7468'), '态</th>'),
    # 交货期</th> (期=E69C9F, < consumed)
    (bytes.fromhex('e69c3f2f7468'), bytes.fromhex('e69c9f3c2f7468'), '期</th>'),
    # 须跟进' : ' (进=E8BF9B, quote consumed)
    (bytes.fromhex('e8bf3f203a2027'), bytes.fromhex('e8bf9b27203a2027'), "进' : '"),
    # XX前', timeColor: (前=E5898D, quote consumed) - appears 4x
    (bytes.fromhex('e5893f2c'), bytes.fromhex('e5898d272c'), "前',"),
    # { day: '二', val: 18
    (bytes.fromhex('e4ba3f2c2076616c3a2031382c'), bytes.fromhex('e4ba8c272c2076616c3a2031382c'), "二', val:18"),
    # { day: '四', val: 22
    (bytes.fromhex('e59b3f2c2076616c3a2032322c'), bytes.fromhex('e59b9b272c2076616c3a2032322c'), "四', val:22"),
    # { day: '五', val: 30
    (bytes.fromhex('e4ba3f2c2076616c3a2033302c'), bytes.fromhex('e4ba94272c2076616c3a2033302c'), "五', val:30"),
    # { day: '中, val: 15 -> 三', val: 15 (fix erroneous e4b83f->e4b8ad from previous run)
    (bytes.fromhex('e4b8ad2c2076616c3a2031352c'), bytes.fromhex('e4b889272c2076616c3a2031352c'), "三', val:15 (fix中->三)"),
    # 六', (六=E585AD, quote consumed)
    (bytes.fromhex('e5853f2c'), bytes.fromhex('e585ad272c'), "六',"),
    # 日', (日=E697A5, quote consumed)
    (bytes.fromhex('e6973f2c'), bytes.fromhex('e697a5272c'), "日',"),
    # 确认', (认=E8AEA4, quote consumed)
    (bytes.fromhex('e8ae3f2c'), bytes.fromhex('e8aea4272c'), "认',"),
    # 待上传', (传=E4BCA0, quote consumed)
    (bytes.fromhex('e4bc3f2c'), bytes.fromhex('e4bca0272c'), "传',"),
    # ⚠', (⚠=E29AA0, quote consumed)
    (bytes.fromhex('e29a3f2c'), bytes.fromhex('e29aa0272c'), "⚠',"),
    # 件）</h3> (）=EFBC89, < consumed)
    (bytes.fromhex('efbc3f2f6833'), bytes.fromhex('efbc893c2f6833'), "）</h3>"),
]

# ======== PENDINGORDERS FIXES ========
pending_fixes = [
    # 须24小时内回复 (须=E9A1BB, '2' consumed)
    (bytes.fromhex('e9a13f34'), bytes.fromhex('e9a1bb3234'), '须24'),
    # 回复\r\n (复=E5A48D, 0D kept)
    (bytes.fromhex('e5a43f0d0a'), bytes.fromhex('e5a48d0d0a'), '复\\r\\n'),
    # 新到未处理< (理=E79086, 3C kept)
    (bytes.fromhex('e7903f3c'), bytes.fromhex('e790863c'), '理<'),
    # 状态</th>
    (bytes.fromhex('e6803f2f7468'), bytes.fromhex('e680813c2f7468'), '态</th>'),
    # 效果图预览 --> (览=E8A788, space consumed)
    (bytes.fromhex('e8a73f2d2d3e'), bytes.fromhex('e8a78820' + '2d2d3e'), '览 -->'),
    # 自定义图形 SVG (形=E5BDA2, space consumed)
    (bytes.fromhex('e5bd3f535647'), bytes.fromhex('e5bda220535647'), '形 SVG'),
    # 效果图预览</h3> (览=E8A788, < consumed)
    (bytes.fromhex('e8a73f2f6833'), bytes.fromhex('e8a7883c2f6833'), '览</h3>'),
    # 亲爱的{{ (的=E79A84, { kept)
    (bytes.fromhex('e79a3f7b7b'), bytes.fromhex('e79a847b7b'), '的{{'),
    # 预计4小时内 (计=E8AEA1, '4' kept, only A1 consumed)
    (bytes.fromhex('e8ae3f34'), bytes.fromhex('e8aea134'), '计4'),
    # 确认。</p> (。=E38082, < consumed)
    (bytes.fromhex('e3803f2f703e'), bytes.fromhex('e380823c2f703e'), '。</p>'),
    # 诚挚问候<br/> (候=E58099, 3C kept)
    (bytes.fromhex('e5803f3c6272'), bytes.fromhex('e580993c6272'), '候<br/>'),
    # 客户需求 --> (求=E6B182, space consumed)
    (bytes.fromhex('e6b13f2d2d3e'), bytes.fromhex('e6b18220' + '2d2d3e'), '求 -->'),
    # 客户需求</h4> (求=E6B182, < consumed)
    (bytes.fromhex('e6b13f2f6834'), bytes.fromhex('e6b1823c2f6834'), '求</h4>'),
    # 确认', (认=E8AEA4)
    (bytes.fromhex('e8ae3f2c'), bytes.fromhex('e8aea4272c'), "认',"),
    # 待上传', (传=E4BCA0)
    (bytes.fromhex('e4bc3f2c'), bytes.fromhex('e4bca0272c'), "传',"),
    # 待发送', (送=E98081)
    (bytes.fromhex('e9803f2c'), bytes.fromhex('e98081272c'), "送',"),
]

# ======== PRODUCTION FIXES ========
production_fixes = [
    # 须跟进</span> (进=E8BF9B, < consumed)
    (bytes.fromhex('e8bf3f2f'), bytes.fromhex('e8bf9b3c2f'), '进</'),
    # ⚠2 单须跟进 (⚠=E29AA0, only A0 consumed, '2' kept)
    (bytes.fromhex('e29a3f32'), bytes.fromhex('e29aa032'), '⚠2'),
    # 优先级</th> (级=E7BAA7, < consumed)
    (bytes.fromhex('e7ba3f2f7468'), bytes.fromhex('e7baa73c2f7468'), '级</th>'),
    # 状态</th>
    (bytes.fromhex('e6803f2f7468'), bytes.fromhex('e680813c2f7468'), '态</th>'),
    # ⚠</span> (⚠=E29AA0, < consumed)
    (bytes.fromhex('e29a3f2f'), bytes.fromhex('e29aa03c2f'), '⚠</'),
    # —</span> (—=E28094, < consumed)
    (bytes.fromhex('e2803f2f'), bytes.fromhex('e280943c2f'), '—</'),
    # （点击表格行展开） --> (）=EFBC89, space consumed)
    (bytes.fromhex('efbc3f2d2d3e'), bytes.fromhex('efbc8920' + '2d2d3e'), '） -->'),
    # ⚠ 已逾期 (⚠=E29AA0, space consumed before 已)
    (bytes.fromhex('e29a3fe5b7b2'), bytes.fromhex('e29aa020e5b7b2'), '⚠ 已'),
    # 须跟进' : ' (进=E8BF9B, quote consumed)
    (bytes.fromhex('e8bf3f203a2027'), bytes.fromhex('e8bf9b27203a2027'), "进' : '"),
    # 生产进度条 --> (条=E69DA1, space consumed)
    (bytes.fromhex('e69d3f2d2d3e'), bytes.fromhex('e69da120' + '2d2d3e'), '条 -->'),
    # 已完成</span> (成=E68890, < consumed)
    (bytes.fromhex('e6883f2f'), bytes.fromhex('e688903c2f'), '成</'),
    # 已逾期</span> — 请立即联系 (—=E28094, space consumed)
    (bytes.fromhex('e2803fe8afb7'), bytes.fromhex('e28094' + '20' + 'e8afb7'), '— 请'),
    # 跟进进度</span> (度=E5BAA6, < consumed)
    (bytes.fromhex('e5ba3f2f'), bytes.fromhex('e5baa63c2f'), '度</'),
    # 在新标签页查看</button> (看=E79C8B, < consumed)
    (bytes.fromhex('e79c3f2f'), bytes.fromhex('e79c8b3c2f'), '看</'),
    # 查看详情</p> (情=E68385, < consumed)
    (bytes.fromhex('e6833f2f'), bytes.fromhex('e683853c2f'), '情</'),
    # ⚠须跟进 (⚠=E29AA0, E9 kept, only A0 consumed with E9 as pair trail)
    (bytes.fromhex('e29a3fe9a1bb'), bytes.fromhex('e29aa0e9a1bb'), '⚠须'),
]

files = [
    (r'D:\ETSY_Order_Automation\frontend\src\views\Dashboard\Dashboard.vue', dashboard_fixes, 'Dashboard'),
    (r'D:\ETSY_Order_Automation\frontend\src\views\PendingOrders\PendingOrders.vue', pending_fixes, 'PendingOrders'),
    (r'D:\ETSY_Order_Automation\frontend\src\views\Production\Production.vue', production_fixes, 'Production'),
]

import os

for filepath, fixes, name in files:
    with open(filepath, 'rb') as f:
        data = f.read()
    
    original = data
    print(f'\n=== {name} ===')
    
    invalid_before = find_invalid(data)
    print(f'Before: {len(invalid_before)} invalid positions')
    
    for old, new, desc in fixes:
        count = data.count(old)
        if count > 0:
            data = data.replace(old, new)
            print(f'  Fixed {count}x: {desc}')
    
    if data != original:
        with open(filepath, 'wb') as f:
            f.write(data)
        
        invalid_after = find_invalid(data)
        if not invalid_after:
            print(f'  => FULLY FIXED!')
        else:
            print(f'  => Still {len(invalid_after)} errors remaining')
            shown = set()
            for pos in invalid_after:
                if pos in shown: continue
                shown.add(pos); shown.add(pos+1)
                ctx = data[max(0,pos-15):pos+15].decode('latin-1')
                print(f'     Pos {pos}: {repr(ctx)}')
    else:
        print(f'  No changes applied')

print('\nDone!')
