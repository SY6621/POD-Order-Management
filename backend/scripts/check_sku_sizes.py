# -*- coding: utf-8 -*-
"""
查询各形状的尺寸数据
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.database_service import db


def check_sku_sizes():
    """检查 sku_mapping 中各形状的尺寸"""
    print("=" * 60)
    print("各形状尺寸数据")
    print("=" * 60)
    
    sku_data = db.select("sku_mapping")
    
    # 按形状分组
    shapes = {}
    for sku in sku_data:
        shape = sku.get("shape", "未知")
        size = sku.get("size", "?")
        width = sku.get("width_mm", "?")
        height = sku.get("height_mm", "?")
        
        key = f"{shape}-{size}"
        if key not in shapes:
            shapes[key] = {
                "shape": shape,
                "size": size,
                "width_mm": width,
                "height_mm": height,
                "sku_code": sku.get("sku_code", "?"),
            }
    
    for key, data in sorted(shapes.items()):
        print(f"  {data['sku_code']}: {data['shape']} {data['size']} → {data['width_mm']}mm × {data['height_mm']}mm")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    check_sku_sizes()
