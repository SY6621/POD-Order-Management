
with open(r'D:\ETSY_Order_Automation\frontend\src\views\Production\Production.vue', 'rb') as f:
    data = f.read()

# Wider context around pos 14589 
chunk = data[14300:14800]
text = chunk.decode('utf-8', errors='replace')
print('==Production pos14589 wider==')
print(text[:400])
print()

# Also PendingOrders around 21600-21900
with open(r'D:\ETSY_Order_Automation\frontend\src\views\PendingOrders\PendingOrders.vue', 'rb') as f:
    data2 = f.read()
chunk2 = data2[21580:22000]
text2 = chunk2.decode('utf-8', errors='replace')
print('==PendingOrders 21580-22000==')
print(text2[:350])
