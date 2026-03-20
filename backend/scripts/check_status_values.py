# -*- coding: utf-8 -*-
"""
检查 orders 表所有不同的 status 值
"""

from supabase import create_client
import os

def load_env_from_file():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars

env_vars = load_env_from_file()
url = env_vars.get('SUPABASE_URL')
key = env_vars.get('SUPABASE_KEY')
supabase = create_client(url, key)

# 查询所有不同的 status 值
result = supabase.table('orders').select('status').execute()

if result.data:
    statuses = set([r['status'] for r in result.data if r['status']])
    print("数据库中存在的 status 值:")
    for s in sorted(statuses):
        count = len([r for r in result.data if r['status'] == s])
        print(f"  - {s}: {count} 条")
else:
    print("无数据")
