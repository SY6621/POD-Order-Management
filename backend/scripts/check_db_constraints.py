#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 orders 表的约束信息
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv(project_root / ".env")

from supabase import create_client
import os

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# 查询约束信息
print("=" * 60)
print("orders 表约束信息")
print("=" * 60)

result = supabase.from_('information_schema.table_constraints').select('*').eq('table_name', 'orders').execute()

if result.data:
    for r in result.data:
        print(f"  - {r.get('constraint_name')}: {r.get('constraint_type')}")
else:
    print("  无约束信息")

# 查询 check 约束详情
print("\n" + "=" * 60)
print("orders 表 CHECK 约束详情")
print("=" * 60)

result = supabase.from_('information_schema.check_constraints').select('*').execute()

if result.data:
    for r in result.data:
        if 'orders' in str(r.get('constraint_name', '')).lower():
            print(f"  - {r.get('constraint_name')}: {r.get('check_clause')}")
else:
    print("  无 CHECK 约束")

# 查询所有不同的 status 值
print("\n" + "=" * 60)
print("orders 表现有 status 值")
print("=" * 60)

result = supabase.table('orders').select('status').execute()
if result.data:
    statuses = {}
    for r in result.data:
        s = r.get('status')
        if s:
            statuses[s] = statuses.get(s, 0) + 1
    for s, count in sorted(statuses.items()):
        print(f"  - {s}: {count} 条")
else:
    print("  无数据")
