
with open(r'D:\ETSY_Order_Automation\frontend\src\views\Production\Production.vue', 'rb') as f:
    data = f.read()

old = bytes.fromhex('e8bf3f207d2c')
new = bytes.fromhex('e8bf9b27207d2c')
count = data.count(old)
print(f'Pattern count: {count}')
if count > 0:
    data = data.replace(old, new)
    with open(r'D:\ETSY_Order_Automation\frontend\src\views\Production\Production.vue', 'wb') as f:
        f.write(data)
    print('Fixed!')

def find_invalid(data):
    positions = []
    i = 0
    while i < len(data):
        b = data[i]
        if b < 0x80: i += 1
        elif b < 0xC0: positions.append(i); i += 1
        elif b < 0xE0:
            if i+1 < len(data) and 0x80 <= data[i+1] <= 0xBF: i += 2
            else: positions.append(i); i += 1
        elif b < 0xF0:
            if i+2 < len(data) and 0x80 <= data[i+1] <= 0xBF and 0x80 <= data[i+2] <= 0xBF: i += 3
            else: positions.append(i); i += 1
        else: i += 1
    return positions

inv = find_invalid(data)
if not inv:
    print('Production.vue: FULLY FIXED!')
else:
    print(f'Still {len(inv)} errors:')
    for p in inv[:5]:
        ctx = data[max(0,p-10):p+10].decode('latin-1')
        print(f'  Pos {p}: {repr(ctx)}')
