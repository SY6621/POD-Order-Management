# -*- coding: utf-8 -*-
"""检查设计器SVG结构"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
import re

url = "https://rtuzqnoztrdvhfnndqjv.supabase.co/storage/v1/object/public/effect-images/effect_fd8455c4-1a2d-4b37-a8bf-e385cad993fd_1774406705582.svg"

r = requests.get(url, timeout=15)
print(f"状态: {r.status_code}")
content = r.text
print(f"总长度: {len(content)} 字符")
print(f"\n--- 前500字符 ---")
print(content[:500])

# 解析 viewBox
vb = re.search(r'viewBox=["\']([^"\']+)["\']', content)
if vb:
    print(f"\nviewBox: {vb.group(1)}")
    parts = vb.group(1).split()
    print(f"  宽: {parts[2] if len(parts)>=4 else '?'}")
    print(f"  高: {parts[3] if len(parts)>=4 else '?'}")

# 解析 width/height
w = re.search(r'\bwidth=["\']([^"\']+)["\']', content)
h = re.search(r'\bheight=["\']([^"\']+)["\']', content)
print(f"\nwidth属性: {w.group(1) if w else '无'}")
print(f"height属性: {h.group(1) if h else '无'}")
