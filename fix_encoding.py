"""
Comprehensive fix for encoding corruption in Vue files.
Strategy: Find ALL invalid UTF-8 sequences, examine context, apply targeted fixes.
"""
import os

files = [
    r'D:\ETSY_Order_Automation\frontend\src\views\Dashboard\Dashboard.vue',
    r'D:\ETSY_Order_Automation\frontend\src\views\PendingOrders\PendingOrders.vue',
    r'D:\ETSY_Order_Automation\frontend\src\views\Production\Production.vue',
]

def find_invalid_positions(data):
    """Find all positions with invalid UTF-8 bytes."""
    positions = []
    i = 0
    while i < len(data):
        b = data[i]
        if b < 0x80:
            i += 1
        elif b < 0xC0:
            # Unexpected continuation byte
            positions.append((i, 'unexpected continuation'))
            i += 1
        elif b < 0xE0:
            # 2-byte sequence
            if i+1 < len(data) and 0x80 <= data[i+1] <= 0xBF:
                i += 2
            else:
                positions.append((i, '2-byte invalid'))
                i += 1
        elif b < 0xF0:
            # 3-byte sequence
            if i+2 < len(data) and 0x80 <= data[i+1] <= 0xBF and 0x80 <= data[i+2] <= 0xBF:
                i += 3
            else:
                positions.append((i, f'3-byte invalid: {[hex(x) for x in data[i:i+4]]}'))
                i += 1
        else:
            i += 1
    return positions

# Context-aware byte replacements
# Format: (bytes_to_find, bytes_to_replace_with)
# Order matters - more specific patterns first
context_fixes = [
    # 认</span> -> 认 was followed by < (3C), which together with A4 became 3F 2F
    (bytes.fromhex('e8ae3f2f'), bytes.fromhex('e8aea43c2f')),   # 认</  (认=E8 AE A4, < = 3C)
    
    # 条</span> -> 条 last byte A1 + < (3C) = A1 3C -> 3F 2F
    (bytes.fromhex('e69d3f2f'), bytes.fromhex('e69da13c2f')),   # 条</  (条=E6 9D A1)
    
    # ：2026 -> ：last byte 9A + '2'(32) = 9A 32 -> 3F
    (bytes.fromhex('efbc3f30'), bytes.fromhex('efbc9a3230')),   # ：20 (full-width colon then 2 then 0)

    # 栏 ══ -> 栏 last byte 8F + space(20) = 8F 20 -> 3F (space eaten)
    (bytes.fromhex('e6a03fe295'), bytes.fromhex('e6a08f20e295')),  # 栏 ══ (E2 95 90 is ═)
    
    # 容 ══ -> 容 last byte B9 + space(20) = B9 20 -> 3F (from earlier fix, now B9 is there but space missing)
    # After previous fix, E5 AE B9 E2 95 90 -> add space
    (bytes.fromhex('e5aeb9e295'), bytes.fromhex('e5aeb920e295')),  # 容 ══
    
    # 表</span> -> 表 last byte A8 + < (3C) = A8 3C -> 3F 2F
    (bytes.fromhex('e8a13f2f'), bytes.fromhex('e8a1a83c2f')),   # 表</  (表=E8 A1 A8)
    
    # 单</span> -> (should already be fixed by context fix, but check for standalone)
    (bytes.fromhex('e58d3f2f'), bytes.fromhex('e58d953c2f')),   # 单</  (单=E5 8D 95)
    
    # 单\n (newline) -> 单 last byte 95 + \n = 95 0A -> ?
    # (95 in GBK lead range, 0A < 0x40 invalid second byte -> 95 0A -> 3F)
    # But \n is important - would appear in text content
    
    # 中 --> (comment close) -> 中 last byte AD + space(20) = AD 20 -> 3F  
    # After previous fix 中 is E4 B8 AD, but need to check if space was eaten
    # Check: E4 B8 3F 2D 2D 3E -> should be E4 B8 AD 20 2D 2D 3E (中 -->)
    (bytes.fromhex('e4b83f2d'), bytes.fromhex('e4b8ad202d')),   # 中 --> (中 before --)
    
    # 付</span> -> (should already be fixed by context fix E4 BA A4 E4 BB 3F)
    (bytes.fromhex('e4bb3f2f'), bytes.fromhex('e4bb983c2f')),   # 付</  (付=E4 BB 98)
    
    # 件</span> -> (should already be fixed for 邮件 context)
    (bytes.fromhex('e4bbb63f2f'), None),  # skip - 件 already fixed via context
    
    # 单 after SPACE (in 数据) - but these are fixed
    # 卡</div> -> 卡 last byte A1 + < (3C) = A1 3C -> 3F 2F  
    (bytes.fromhex('e58d3f2f'), bytes.fromhex('e58da13c2f')),   # 卡</  (卡=E5 8D A1)
]

for filepath in files:
    with open(filepath, 'rb') as f:
        data = f.read()
    
    # First, check for remaining invalid positions
    invalid = find_invalid_positions(data)
    if not invalid:
        print(f'Already valid UTF-8: {os.path.basename(filepath)}')
        continue
    
    print(f'\n{os.path.basename(filepath)}: {len(invalid)} invalid positions')
    for pos, reason in invalid[:5]:  # Show first 5
        chunk = data[pos-5:pos+10]
        try:
            ctx = data[pos-10:pos+15].decode('latin-1')
        except:
            ctx = ''
        print(f'  Position {pos}: {reason} | context: {repr(ctx)}')
    
    original = data
    
    for old, new in context_fixes:
        if new is not None and old in data:
            count = data.count(old)
            data = data.replace(old, new)
            print(f'  Fixed {count}x: {old.hex()} -> {new.hex()}')
    
    if data != original:
        with open(filepath, 'wb') as f:
            f.write(data)
        
        invalid_after = find_invalid_positions(data)
        if not invalid_after:
            print(f'  => FULLY FIXED: {os.path.basename(filepath)}')
        else:
            print(f'  => Still {len(invalid_after)} errors remaining')
            for pos, reason in invalid_after[:5]:
                try:
                    ctx = data[pos-10:pos+15].decode('latin-1')
                except:
                    ctx = ''
                print(f'     Position {pos}: {repr(ctx)}')
    else:
        print(f'  No context fixes applied')

print('\nDone!')
