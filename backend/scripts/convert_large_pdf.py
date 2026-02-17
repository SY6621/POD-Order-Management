# -*- coding: utf-8 -*-
"""
大号PDF转SVG脚本 - 用页码命名方便校对
"""

import fitz
import re
from pathlib import Path


def main():
    pdf_path = Path(r"d:\ETSY_Order_Automation\backend\src\B不锈钢外观模版-正反面-大.pdf")
    output_dir = Path(r"d:\ETSY_Order_Automation\backend\assets\templates\B不锈钢_模版_大号")
    
    # 颜色代码映射
    color_map = {
        "9f9fa0": "Silver",
        "ebcd7b": "Gold", 
        "dabf9b": "RoseGold",
        "231916": "Black",
    }
    
    doc = fitz.open(pdf_path)
    print(f"处理: {pdf_path.name}, 共 {len(doc)} 页")
    print("-" * 60)
    
    for i in range(len(doc)):
        page = doc[i]
        svg = page.get_svg_image()
        
        # 提取颜色
        match = re.search(r'fill="#([0-9a-fA-F]{6})"', svg)
        color_hex = match.group(1).lower() if match else "unknown"
        color_name = color_map.get(color_hex, color_hex)
        
        # 添加白色背景
        viewbox_match = re.search(r'viewBox="([^"]+)"', svg)
        if viewbox_match:
            parts = viewbox_match.group(1).split()
            if len(parts) == 4:
                w, h = parts[2], parts[3]
                white_rect = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#FFFFFF"/>\n'
                svg = re.sub(r'(<svg[^>]*>)', rf'\1\n{white_rect}', svg)
        
        # 用页码命名，包含颜色信息方便识别
        filename = f"page_{i+1:02d}_{color_name}.svg"
        with open(output_dir / filename, 'w', encoding='utf-8') as f:
            f.write(svg)
        
        print(f"页{i+1:2d} -> {filename}")
    
    doc.close()
    print("-" * 60)
    print(f"完成! 共生成 {len(doc)} 个文件")
    print(f"\n请打开目录查看并校对外观类型:")
    print(f"  {output_dir}")


if __name__ == "__main__":
    main()
