# -*- coding: utf-8 -*-
"""
大号SVG模板重命名脚本
按SKU命名规范重命名
"""

from pathlib import Path


def main():
    templates_dir = Path(r"d:\ETSY_Order_Automation\backend\assets\templates\B不锈钢_模版_大号")
    
    # 页码到SKU的映射
    # 页1-8: 圆形(C), 页9-16: 骨形(E), 页17-24: 心形(G)
    # 奇数页=正面(F), 偶数页=反面(B)
    rename_map = {
        # 圆形(Circle) 页1-8
        "page_01_Silver.svg": "B-C01A_Circle_Silver - L-F.svg",
        "page_02_Silver.svg": "B-C01A_Circle_Silver - L-B.svg",
        "page_03_Gold.svg": "B-C01B_Circle_Gold - L-F.svg",
        "page_04_Gold.svg": "B-C01B_Circle_Gold - L-B.svg",
        "page_05_RoseGold.svg": "B-C01C_Circle_RoseGold - L-F.svg",
        "page_06_RoseGold.svg": "B-C01C_Circle_RoseGold - L-B.svg",
        "page_07_Black.svg": "B-C01D_Circle_Black - L-F.svg",
        "page_08_Black.svg": "B-C01D_Circle_Black - L-B.svg",
        # 骨形(Bone) 页9-16
        "page_09_Silver.svg": "B-E01A_Bone_Silver - L-F.svg",
        "page_10_Silver.svg": "B-E01A_Bone_Silver - L-B.svg",
        "page_11_Gold.svg": "B-E01B_Bone_Gold - L-F.svg",
        "page_12_Gold.svg": "B-E01B_Bone_Gold - L-B.svg",
        "page_13_RoseGold.svg": "B-E01C_Bone_RoseGold - L-F.svg",
        "page_14_RoseGold.svg": "B-E01C_Bone_RoseGold - L-B.svg",
        "page_15_Black.svg": "B-E01D_Bone_Black - L-F.svg",
        "page_16_Black.svg": "B-E01D_Bone_Black - L-B.svg",
        # 心形(Heart) 页17-24
        "page_17_Silver.svg": "B-G01A_Heart_Silver - L-F.svg",
        "page_18_Silver.svg": "B-G01A_Heart_Silver - L-B.svg",
        "page_19_Gold.svg": "B-G01B_Heart_Gold - L-F.svg",
        "page_20_Gold.svg": "B-G01B_Heart_Gold - L-B.svg",
        "page_21_RoseGold.svg": "B-G01C_Heart_RoseGold - L-F.svg",
        "page_22_RoseGold.svg": "B-G01C_Heart_RoseGold - L-B.svg",
        "page_23_Black.svg": "B-G01D_Heart_Black - L-F.svg",
        "page_24_Black.svg": "B-G01D_Heart_Black - L-B.svg",
    }
    
    print("=" * 70)
    print("大号SVG模板重命名")
    print("=" * 70)
    print(f"目录: {templates_dir}\n")
    
    success_count = 0
    
    for old_name, new_name in rename_map.items():
        old_path = templates_dir / old_name
        new_path = templates_dir / new_name
        
        if old_path.exists():
            old_path.rename(new_path)
            print(f"✅ {old_name} -> {new_name}")
            success_count += 1
        else:
            print(f"⚠️  {old_name} 不存在，跳过")
    
    print("-" * 70)
    print(f"完成！成功重命名: {success_count} 个文件")
    print("=" * 70)


if __name__ == "__main__":
    main()
