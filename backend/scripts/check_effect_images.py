#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查订单效果图字段
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

print("=" * 60)
print("订单效果图字段检查")
print("=" * 60)

result = supabase.table('orders').select('etsy_order_id, customer_name, effect_image_url').execute()

if result.data:
    for r in result.data:
        etsy_id = r.get('etsy_order_id', 'N/A')
        customer = r.get('customer_name', 'N/A')
        effect = r.get('effect_image_url')
        status = '✅ 有' if effect else '❌ 无'
        print(f"  {etsy_id} | {customer[:15]:15} | {status}")
        if effect:
            print(f"     URL: {effect[:60]}...")
else:
    print("  无数据")

print("\n" + "=" * 60)
