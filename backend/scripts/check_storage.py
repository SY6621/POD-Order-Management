# -*- coding: utf-8 -*-
"""检查 Storage bucket 和图片访问权限"""

from supabase import create_client
import os

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars

env = load_env()
supabase = create_client(env['SUPABASE_URL'], env['SUPABASE_KEY'])

print('=' * 70)
print('检查 Storage 配置')
print('=' * 70)

# 检查 buckets
try:
    buckets = supabase.storage.list_buckets()
    print('\nBuckets:')
    for b in buckets:
        print(f'  {b.name} (public: {b.public})')
except Exception as e:
    print(f'\n获取 buckets 失败: {e}')

# 检查 B-G01B.jpg 的公开URL
print('\n检查 B-G01B.jpg 公开URL:')
try:
    url = supabase.storage.from_('assets').get_public_url('photos/large/B-G01B.jpg')
    print(f'  {url}')
except Exception as e:
    print(f'  错误: {e}')

# 检查是否有 photos 文件夹
print('\n检查 assets bucket 根目录:')
try:
    files = supabase.storage.from_('assets').list()
    for f in files[:10]:
        print(f'  {f["name"]}')
except Exception as e:
    print(f'  错误: {e}')
