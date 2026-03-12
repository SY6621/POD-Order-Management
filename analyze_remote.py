#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""详细分析 Remote.vue 的所有损坏位置"""

import os

def find_invalid(data):
    """找出所有无效UTF-8字节的位置"""
    invalid = []
    i = 0
    while i < len(data):
        b = data[i]
        if b < 0x80:
            i += 1
        elif b < 0xC0:
            # unexpected continuation
            invalid.append(i)
            i += 1
        elif b < 0xE0:
            # 2-byte
            if i+1 < len(data) and 0x80 <= data[i+1] <= 0xBF:
                i += 2
            else:
                invalid.append(i)
                i += 1
        elif b < 0xF0:
            # 3-byte
            if (i+2 < len(data) and 0x80 <= data[i+1] <= 0xBF 
                    and 0x80 <= data[i+2] <= 0xBF):
                i += 3
            else:
                invalid.append(i)
                i += 1
        elif b < 0xF8:
            # 4-byte
            if (i+3 < len(data) and 0x80 <= data[i+1] <= 0xBF 
                    and 0x80 <= data[i+2] <= 0xBF 
                    and 0x80 <= data[i+3] <= 0xBF):
                i += 4
            else:
                invalid.append(i)
                i += 1
        else:
            invalid.append(i)
            i += 1
    return invalid

path = r'd:\ETSY_Order_Automation\frontend\src\views\Remote\Remote.vue'
with open(path, 'rb') as f:
    data = f.read()

invalids = find_invalid(data)
print(f"Remote.vue: {len(invalids)} invalid positions")
print()

# 打印每个损坏位置的上下文
for pos in invalids:
    start = max(0, pos - 8)
    end = min(len(data), pos + 12)
    chunk = data[start:end]
    hex_str = ' '.join(f'{b:02x}' for b in chunk)
    try:
        ctx = data[start:end].decode('utf-8', errors='replace')
        ctx = ctx.replace('\n', '\\n').replace('\r', '\\r')
    except:
        ctx = '?'
    print(f"  Pos {pos}: hex=[{hex_str}] ctx='{ctx}'")

print()
print("=== 唯一损坏模式分析（以损坏字节开头的4字节） ===")
patterns = {}
for pos in invalids:
    key = bytes(data[pos:pos+4]).hex()
    if key not in patterns:
        patterns[key] = []
    patterns[key].append(pos)

for k, v in sorted(patterns.items()):
    start = v[0]
    s = max(0, start-4)
    e = min(len(data), start+8)
    ctx = data[s:e].decode('utf-8', errors='replace').replace('\n','\\n').replace('\r','\\r')
    print(f"  Pattern {k} ({len(v)} times): example ctx='{ctx}'")
