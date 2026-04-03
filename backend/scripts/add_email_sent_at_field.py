"""给 orders 表添加 email_sent_at 字段"""
import os
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from supabase import create_client

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_KEY')

if not url or not key:
    print('❌ 缺少 Supabase 配置')
    sys.exit(1)

supabase = create_client(url, key)

# 测试字段是否存在
try:
    result = supabase.table('orders').select('email_sent_at').limit(1).execute()
    print('✅ email_sent_at 字段已存在')
    print(f'   查询结果: {result.data}')
except Exception as e:
    error_msg = str(e)
    if 'column' in error_msg.lower() and 'does not exist' in error_msg.lower():
        print('⚠️ email_sent_at 字段不存在')
        print('')
        print('请在 Supabase Dashboard > SQL Editor 中执行以下 SQL:')
        print('')
        print('ALTER TABLE orders ADD COLUMN IF NOT EXISTS email_sent_at TIMESTAMPTZ;')
        print('')
    else:
        print(f'❌ 检查失败: {e}')
