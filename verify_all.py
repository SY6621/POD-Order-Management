
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

files = [
    r'D:\ETSY_Order_Automation\frontend\src\views\Dashboard\Dashboard.vue',
    r'D:\ETSY_Order_Automation\frontend\src\views\PendingOrders\PendingOrders.vue',
    r'D:\ETSY_Order_Automation\frontend\src\views\Production\Production.vue',
    r'D:\ETSY_Order_Automation\frontend\src\views\CompletedOrders\CompletedOrders.vue',
    r'D:\ETSY_Order_Automation\frontend\src\views\Logistics\Logistics.vue',
    r'D:\ETSY_Order_Automation\frontend\src\views\EmailTemplates\EmailTemplates.vue',
]

all_ok = True
for fp in files:
    import os
    name = os.path.basename(fp)
    with open(fp, 'rb') as f:
        data = f.read()
    inv = find_invalid(data)
    status = 'OK' if not inv else f'ERRORS: {len(inv)}'
    print(f'{name}: {status}')
    if inv:
        all_ok = False
        for p in inv[:3]:
            enc = data[max(0,p-10):p+10]
            ctx = enc.decode('latin-1')
            print(f'  Pos {p}: {repr(ctx)}')

if all_ok:
    print('\nAll 6 Vue files are valid UTF-8!')
