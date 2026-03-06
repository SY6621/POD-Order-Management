# -*- coding: utf-8 -*-
"""
更新 SVG 模板：将实拍图 base64 替换为占位符
"""

import re
from pathlib import Path

SVG_PATH = Path(__file__).parent.parent / "src" / "模版-设计图-校对文档-快递面单V2.svg"

def update_template():
    """将实拍图 base64 替换为占位符"""
    with open(SVG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 查找第一个 image 元素（实拍图，800x800）
    # 模式：<image width="800" height="800" xlink:href="data:image/jpeg;base64,..." transform="...">
    pattern = r'<image width="800" height="800" xlink:href="data:image/jpeg;base64,[^"]*" transform="([^"]*)">'
    
    match = re.search(pattern, content)
    if match:
        transform = match.group(1)
        placeholder = f'<image width="800" height="800" xlink:href="{{{{PRODUCT_PHOTO_BASE64}}}}" transform="{transform}">'
        content = re.sub(pattern, placeholder, content, count=1)
        print(f"✓ 替换实拍图占位符")
        print(f"  transform: {transform}")
    else:
        print("❌ 未找到实拍图 image 元素")
        return
    
    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✓ SVG 模板更新完成")


if __name__ == "__main__":
    update_template()
