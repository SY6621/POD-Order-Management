# -*- coding: utf-8 -*-
"""
小号PDF转SVG并按SKU命名
"""

import fitz
import re
from pathlib import Path


def main():
    pdf_path = Path(r"d:\ETSY_Order_Automation\backend\src\B不锈钢外观模版-正反面-小.pdf")
    output_dir = Path(r"d:\ETSY_Order_Automation\backend\assets\templates\B不锈钢_模版_小号")
    
    # 页码到SKU文件名的映射（小号用02和S）
    # 页1-8: 圆形(C), 页9-16: 骨形(E), 页17-24: 心形(G)
    page_to_filename = {
        # 圆形(Circle) 页1-8
        1: "B-C02A_Circle_Silver - S-F.svg",
        2: "B-C02A_Circle_Silver - S-B.svg",
        3: "B-C02B_Circle_Gold - S-F.svg",
        4: "B-C02B_Circle_Gold - S-B.svg",
        5: "B-C02C_Circle_RoseGold - S-F.svg",
        6: "B-C02C_Circle_RoseGold - S-B.svg",
        7: "B-C02D_Circle_Black - S-F.svg",
        8: "B-C02D_Circle_Black - S-B.svg",
        # 骨形(Bone) 页9-16
        9: "B-E02A_Bone_Silver - S-F.svg",
        10: "B-E02A_Bone_Silver - S-B.svg",
        11: "B-E02B_Bone_Gold - S-F.svg",
        12: "B-E02B_Bone_Gold - S-B.svg",
        13: "B-E02C_Bone_RoseGold - S-F.svg",
        14: "B-E02C_Bone_RoseGold - S-B.svg",
        15: "B-E02D_Bone_Black - S-F.svg",
        16: "B-E02D_Bone_Black - S-B.svg",
        # 心形(Heart) 页17-24
        17: "B-G02A_Heart_Silver - S-F.svg",
        18: "B-G02A_Heart_Silver - S-B.svg",
        19: "B-G02B_Heart_Gold - S-F.svg",
        20: "B-G02B_Heart_Gold - S-B.svg",
        21: "B-G02C_Heart_RoseGold - S-F.svg",
        22: "B-G02C_Heart_RoseGold - S-B.svg",
        23: "B-G02D_Heart_Black - S-F.svg",
        24: "B-G02D_Heart_Black - S-B.svg",
    }
    
    doc = fitz.open(pdf_path)
    print("=" * 70)
    print("小号PDF转SVG并命名")
    print("=" * 70)
    print(f"源文件: {pdf_path.name}, 共 {len(doc)} 页")
    print(f"输出目录: {output_dir}")
    print("-" * 70)
    
    page_count = len(doc)
    
    for i in range(page_count):
        page = doc[i]
        svg = page.get_svg_image()
        
        # 添加白色背景
        viewbox_match = re.search(r'viewBox="([^"]+)"', svg)
        if viewbox_match:
            parts = viewbox_match.group(1).split()
            if len(parts) == 4:
                w, h = parts[2], parts[3]
                white_rect = f'<rect x="0" y="0" width="{w}" height="{h}" fill="#FFFFFF"/>\n'
                svg = re.sub(r'(<svg[^>]*>)', rf'\1\n{white_rect}', svg)
        
        # 获取文件名
        filename = page_to_filename.get(i + 1, f"page_{i+1:02d}.svg")
        
        # 保存文件
        with open(output_dir / filename, 'w', encoding='utf-8') as f:
            f.write(svg)
        
        print(f"✅ 页{i+1:2d} -> {filename}")
    
    doc.close()
    
    print("-" * 70)
    print(f"完成！共生成 {page_count} 个SVG文件")
    print("=" * 70)


if __name__ == "__main__":
    main()
