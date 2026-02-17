# -*- coding: utf-8 -*-
"""
SVG模板重命名脚本
功能：将template_page_X.svg按工厂SKU编码规则重命名
"""

import os
from pathlib import Path


def rename_svg_templates():
    """
    重命名SVG模板文件，按工厂SKU编码规则
    
    PDF结构（B不锈钢外观模版-正反面-大.pdf，共24页）：
    - 页面1-8：圆形（C）外观，4色 × 正反面
    - 页面9-16：骨形（E）外观，4色 × 正反面
    - 页面17-24：心形（G）外观，4色 × 正反面
    
    颜色代码：A=银色, B=金色, C=玫瑰金, D=黑色
    规格：01=大尺寸（此PDF为大尺寸）
    工艺：B=抛光/亮光
    """
    
    templates_dir = Path(r"d:\ETSY_Order_Automation\backend\assets\templates")
    
    # 页面到SKU的映射
    # 格式：{页码: (SKU编号, 描述)}
    # 每种外观：正面银、反面银、正面金、反面金、正面玫瑰金、反面玫瑰金、正面黑、反面黑
    page_mapping = {
        # 圆形（C）- 页面1-8
        1: ("B-C01A-front", "圆形 大 银色 正面"),
        2: ("B-C01A-back", "圆形 大 银色 反面"),
        3: ("B-C01B-front", "圆形 大 金色 正面"),
        4: ("B-C01B-back", "圆形 大 金色 反面"),
        5: ("B-C01C-front", "圆形 大 玫瑰金 正面"),
        6: ("B-C01C-back", "圆形 大 玫瑰金 反面"),
        7: ("B-C01D-front", "圆形 大 黑色 正面"),
        8: ("B-C01D-back", "圆形 大 黑色 反面"),
        
        # 骨形（E）- 页面9-16
        9: ("B-E01A-front", "骨形 大 银色 正面"),
        10: ("B-E01A-back", "骨形 大 银色 反面"),
        11: ("B-E01B-front", "骨形 大 金色 正面"),
        12: ("B-E01B-back", "骨形 大 金色 反面"),
        13: ("B-E01C-front", "骨形 大 玫瑰金 正面"),
        14: ("B-E01C-back", "骨形 大 玫瑰金 反面"),
        15: ("B-E01D-front", "骨形 大 黑色 正面"),
        16: ("B-E01D-back", "骨形 大 黑色 反面"),
        
        # 心形（G）- 页面17-24
        17: ("B-G01A-front", "心形 大 银色 正面"),
        18: ("B-G01A-back", "心形 大 银色 反面"),
        19: ("B-G01B-front", "心形 大 金色 正面"),
        20: ("B-G01B-back", "心形 大 金色 反面"),
        21: ("B-G01C-front", "心形 大 玫瑰金 正面"),
        22: ("B-G01C-back", "心形 大 玫瑰金 反面"),
        23: ("B-G01D-front", "心形 大 黑色 正面"),
        24: ("B-G01D-back", "心形 大 黑色 反面"),
    }
    
    print("=" * 70)
    print("SVG模板文件重命名")
    print("=" * 70)
    print(f"\n目录: {templates_dir}\n")
    
    renamed_count = 0
    errors = []
    
    print("-" * 70)
    print(f"{'原文件名':<30} -> {'新文件名':<25} {'描述'}")
    print("-" * 70)
    
    for page_num, (sku, desc) in page_mapping.items():
        old_name = f"template_page_{page_num}.svg"
        new_name = f"{sku}.svg"
        
        old_path = templates_dir / old_name
        new_path = templates_dir / new_name
        
        if old_path.exists():
            try:
                # 如果目标文件已存在，先删除
                if new_path.exists():
                    new_path.unlink()
                
                old_path.rename(new_path)
                print(f"✅ {old_name:<30} -> {new_name:<25} {desc}")
                renamed_count += 1
            except Exception as e:
                error_msg = f"重命名失败 {old_name}: {e}"
                print(f"❌ {error_msg}")
                errors.append(error_msg)
        else:
            print(f"⚠️  {old_name:<30} 文件不存在，跳过")
    
    print("-" * 70)
    print(f"\n完成！成功重命名: {renamed_count} 个文件")
    
    if errors:
        print(f"错误: {len(errors)} 个")
        for err in errors:
            print(f"   - {err}")
    
    # 显示最终文件列表
    print("\n" + "=" * 70)
    print("当前模板目录中的SKU文件：")
    print("-" * 70)
    
    sku_files = sorted([f.name for f in templates_dir.glob("B-*.svg")])
    for f in sku_files:
        print(f"   {f}")
    
    print(f"\n共 {len(sku_files)} 个SKU模板文件")
    print("=" * 70)


if __name__ == "__main__":
    rename_svg_templates()
