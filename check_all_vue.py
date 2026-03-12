
import os
import glob

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

# Find ALL Vue files in the frontend/src directory
base = r'D:\ETSY_Order_Automation\frontend\src'
for root, dirs, files in os.walk(base):
    for fname in files:
        if fname.endswith('.vue') or fname.endswith('.js') or fname.endswith('.css'):
            fp = os.path.join(root, fname)
            with open(fp, 'rb') as f:
                data = f.read()
            inv = find_invalid(data)
            if inv:
                rel = fp.replace(base, '').lstrip('\\/')
                print(f'ERRORS in {rel}: {len(inv)} invalid positions')
                for p in inv[:3]:
                    ctx = data[max(0,p-10):p+10].decode('latin-1')
                    print(f'  Pos {p}: {repr(ctx)}')
            else:
                rel = fp.replace(base, '').lstrip('\\/')
                print(f'OK: {rel}')
