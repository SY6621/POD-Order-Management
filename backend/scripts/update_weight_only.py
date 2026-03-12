#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
更新 SKU 重量数据（假设 weight_g 字段已存在）
"""
import sys
sys.path.insert(0, 'd:\\ETSY_Order_Automation\\backend')

from src.services.database_service import db

# 产品重量数据（单位：克）
WEIGHT_DATA = {
    ("骨头形", "大"): 33,
    ("骨头形", "小"): 20,
    ("心形", "大"): 27,
    ("心形", "小"): 20,
    ("圆形", "大"): 30,
    ("圆形", "小"): 20,
}


def update_weights():
    """更新重量数据"""
    print("=" * 60)
    print("更新 SKU 重量数据")
    print("=" * 60)
    
    # 获取所有 SKU 数据
    sku_list = db.select("sku_mapping")
    
    updated_count = 0
    for sku in sku_list:
        sku_code = sku.get("sku_code", "")
        shape = sku.get("shape", "")
        size = sku.get("size", "")
        
        # 标准化大小字段
        size_std = "大" if size in ["大", "L", "Large", "large"] else "小"
        
        # 查找对应的重量
        key = (shape, size_std)
        weight = WEIGHT_DATA.get(key)
        
        if weight:
            # 更新数据库
            try:
                db.update("sku_mapping", 
                         {"id": sku["id"]}, 
                         {"weight_g": weight})
                print(f"✅ {sku_code}: {shape} {size_std} → {weight}g")
                updated_count += 1
            except Exception as e:
                print(f"❌ {sku_code} 更新失败: {e}")
        else:
            print(f"⚠️  {sku_code}: {shape} {size_std} 未找到对应重量")
    
    print(f"\n共更新 {updated_count} 条记录")
    return updated_count


def verify_updates():
    """验证更新结果"""
    print("\n" + "=" * 60)
    print("验证更新结果")
    print("=" * 60)
    
    sku_list = db.select("sku_mapping")
    
    print("\nSKU 重量数据:")
    print("-" * 60)
    for sku in sku_list:
        sku_code = sku.get("sku_code", "")
        shape = sku.get("shape", "")
        size = sku.get("size", "")
        weight = sku.get("weight_g", 0)
        print(f"  {sku_code:10} | {shape:6} | {size:4} | {weight:3}g")
    
    print("-" * 60)


if __name__ == "__main__":
    print("SKU 重量数据更新")
    print("=" * 60)
    
    # 更新重量数据
    update_weights()
    
    # 验证结果
    verify_updates()
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)
