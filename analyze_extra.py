
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

# Effects.vue
with open(r'D:\ETSY_Order_Automation\frontend\src\views\Effects\Effects.vue', 'rb') as f:
    effects_data = f.read()
print('=== Effects.vue ===')
inv = find_invalid(effects_data)
print(f'{len(inv)} invalid positions')
shown = set()
for p in inv:
    if p in shown: continue
    shown.add(p); shown.add(p+1)
    ctx = effects_data[max(0,p-15):p+15].decode('latin-1')
    hex_ctx = ' '.join(f'{b:02x}' for b in effects_data[max(0,p-3):p+6])
    print(f'  Pos {p}: hex=[{hex_ctx}] ctx={repr(ctx)}')

print()
# Remote.vue
with open(r'D:\ETSY_Order_Automation\frontend\src\views\Remote\Remote.vue', 'rb') as f:
    remote_data = f.read()
print('=== Remote.vue ===')
inv2 = find_invalid(remote_data)
print(f'{len(inv2)} invalid positions')
shown2 = set()
for p in inv2[:20]:
    if p in shown2: continue
    shown2.add(p); shown2.add(p+1)
    ctx = remote_data[max(0,p-15):p+15].decode('latin-1')
    hex_ctx = ' '.join(f'{b:02x}' for b in remote_data[max(0,p-3):p+6])
    print(f'  Pos {p}: hex=[{hex_ctx}] ctx={repr(ctx)}')
print('...')

# Show Remote.vue first 300 chars
print()
print('Remote.vue first 300 chars (errors replaced):')
print(remote_data[:300].decode('utf-8', errors='replace'))
