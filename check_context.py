
with open(r'D:\ETSY_Order_Automation\frontend\src\views\Production\Production.vue', 'rb') as f:
    data = f.read()

for pos, label in [(14500, 'pos14589'), (19200, 'pos19356'), (10700, 'pos10788'), (23700, 'pos23853')]:
    chunk = data[pos:pos+200]
    text = chunk.decode('utf-8', errors='replace')
    print(f'=={label}==')
    print(text[:180])
    print()

# Also check PendingOrders around pos 21650
with open(r'D:\ETSY_Order_Automation\frontend\src\views\PendingOrders\PendingOrders.vue', 'rb') as f:
    data2 = f.read()
for pos, label in [(21500, 'pend21653'), (21700, 'pend21743')]:
    chunk = data2[pos:pos+200]
    text = chunk.decode('utf-8', errors='replace')
    print(f'=={label}==')
    print(text[:180])
    print()
