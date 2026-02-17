# -*- coding: utf-8 -*-
"""
小号SVG模板重命名脚本
根据用户校对的外观映射关系重命名
"""

from pathlib import Path


def main():
    templates_dir = Path(r"d:\ETSY_Order_Automation\backend\assets\templates\B不锈钢_模版_小号")
    
    # 用户校对的页码到外观的映射
    # 格式: "原文件名": "新文件名"
    # 每个外观+颜色组合的第一个页码为正面(F)，第二个为反面(B)
    rename_map = {
        # Circle (圆形) - C02
        "page_12_Silver.svg": "B-C02A_Circle_Silver - S-F.svg",      # Silver第一个
        "page_24_Silver.svg": "B-C02A_Circle_Silver - S-B.svg",      # Silver第二个
        "page_03_Gold.svg": "B-C02B_Circle_Gold - S-F.svg",          # Gold第一个
        "page_15_Gold.svg": "B-C02B_Circle_Gold - S-B.svg",          # Gold第二个
        "page_05_RoseGold.svg": "B-C02C_Circle_RoseGold - S-F.svg",  # RoseGold第一个
        "page_17_RoseGold.svg": "B-C02C_Circle_RoseGold - S-B.svg",  # RoseGold第二个
        "page_07_Black.svg": "B-C02D_Circle_Black - S-F.svg",        # Black第一个
        "page_19_Black.svg": "B-C02D_Circle_Black - S-B.svg",        # Black第二个
        
        # Bone (骨形) - E02
        "page_01_Silver.svg": "B-E02A_Bone_Silver - S-F.svg",        # Silver第一个
        "page_13_Silver.svg": "B-E02A_Bone_Silver - S-B.svg",        # Silver第二个
        "page_04_Gold.svg": "B-E02B_Bone_Gold - S-F.svg",            # Gold第一个
        "page_16_Gold.svg": "B-E02B_Bone_Gold - S-B.svg",            # Gold第二个
        "page_06_RoseGold.svg": "B-E02C_Bone_RoseGold - S-F.svg",    # RoseGold第一个
        "page_18_RoseGold.svg": "B-E02C_Bone_RoseGold - S-B.svg",    # RoseGold第二个
        "page_08_Black.svg": "B-E02D_Bone_Black - S-F.svg",          # Black第一个
        "page_20_Black.svg": "B-E02D_Bone_Black - S-B.svg",          # Black第二个
        
        # Heart (心形) - G02
        "page_02_Silver.svg": "B-G02A_Heart_Silver - S-F.svg",       # Silver第一个
        "page_14_Silver.svg": "B-G02A_Heart_Silver - S-B.svg",       # Silver第二个
        "page_09_Gold.svg": "B-G02B_Heart_Gold - S-F.svg",           # Gold第一个
        "page_21_Gold.svg": "B-G02B_Heart_Gold - S-B.svg",           # Gold第二个
        "page_10_RoseGold.svg": "B-G02C_Heart_RoseGold - S-F.svg",   # RoseGold第一个
        "page_22_RoseGold.svg": "B-G02C_Heart_RoseGold - S-B.svg",   # RoseGold第二个
        "page_11_Black.svg": "B-G02D_Heart_Black - S-F.svg",         # Black第一个
        "page_23_Black.svg": "B-G02D_Heart_Black - S-B.svg",         # Black第二个
    }
    
    print("=" * 70)
    print("小号SVG模板重命名")
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
