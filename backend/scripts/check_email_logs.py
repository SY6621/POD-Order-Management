"""
检查 email_logs 表数据状态
用于诊断 ServiceLink 页面邮件内容空白问题
"""
import os
from dotenv import load_dotenv
from supabase import create_client

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')

if not url or not key:
    print("错误: SUPABASE_URL 或 SUPABASE_KEY 未配置")
    exit(1)

supabase = create_client(url, key)

print("=" * 60)
print("阶段1: 验证数据库层 - email_logs 表")
print("=" * 60)

# 1. 查看email_logs表中所有记录
print("\n【email_logs 表所有记录】")
result = supabase.table('email_logs').select('*').execute()
print(f"记录总数: {len(result.data)}")

for row in result.data:
    print(f"\n--- 记录 ---")
    print(f"  id: {row.get('id')}")
    print(f"  order_id: {row.get('order_id')}")
    print(f"  email_type: {row.get('email_type')}")
    content = row.get('content', '')
    print(f"  content长度: {len(content)} 字符")
    if content:
        print(f"  content前100字: {content[:100]}...")
    print(f"  sent_at: {row.get('sent_at')}")
    print(f"  sender_name: {row.get('sender_name')}")

# 2. 查看特定订单的状态
print("\n" + "=" * 60)
print("阶段1.2: 检查订单 4018102033 的状态")
print("=" * 60)

result2 = supabase.table('orders').select('id, etsy_order_id, email_sent, status').eq('etsy_order_id', '4018102033').execute()
print(f"\n订单 4018102033 查询结果:")
if result2.data:
    for order in result2.data:
        print(f"  UUID id: {order.get('id')}")
        print(f"  etsy_order_id: {order.get('etsy_order_id')}")
        print(f"  email_sent: {order.get('email_sent')}")
        print(f"  status: {order.get('status')}")
        
        # 用这个UUID去查email_logs
        order_uuid = order.get('id')
        print(f"\n  用UUID {order_uuid} 查询 email_logs:")
        result3 = supabase.table('email_logs').select('*').eq('order_id', order_uuid).execute()
        print(f"  找到 {len(result3.data)} 条邮件记录")
        for log in result3.data:
            print(f"    - email_type: {log.get('email_type')}, sent_at: {log.get('sent_at')}")
else:
    print("  未找到该订单")

# 3. 查看最近的订单
print("\n" + "=" * 60)
print("阶段1.3: 最近5个订单的email_sent状态")
print("=" * 60)

result4 = supabase.table('orders').select('id, etsy_order_id, email_sent, status').order('created_at', desc=True).limit(5).execute()
for order in result4.data:
    print(f"  {order.get('etsy_order_id')} | email_sent={order.get('email_sent')} | status={order.get('status')}")
    # 查这个订单有没有email_log
    logs = supabase.table('email_logs').select('id').eq('order_id', order.get('id')).execute()
    print(f"    └─ email_logs记录数: {len(logs.data)}")

print("\n" + "=" * 60)
print("诊断完成")
print("=" * 60)
