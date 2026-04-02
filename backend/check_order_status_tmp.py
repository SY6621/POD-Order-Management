from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()
s = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
r = s.table('orders').select('id,order_id,status,email_sent').order('created_at', {'ascending': False}).execute()

print(f'Total orders: {len(r.data)}')
print("\nStatus values in database:")
status_values = {}
for order in r.data:
    status = order.get('status')
    if status not in status_values:
        status_values[status] = 0
    status_values[status] += 1

for status, count in sorted(status_values.items()):
    print(f"  {status}: {count} orders")

print("\nFirst 30 orders:")
for x in r.data[:30]:
    print(f'{x["order_id"]}: status={x["status"]}, email_sent={x.get("email_sent")}')
