# -*- coding: utf-8 -*-
"""
检查 Supabase 数据库中的资源表数据
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.database_service import db


def check_supabase_data():
    """检查 Supabase 中的资源数据"""
    print("=" * 60)
    print("检查 Supabase 数据库资源数据")
    print("=" * 60)
    
    # 1. 检查 templates 表
    print("\n[1] templates 表（模板信息）:")
    templates = db.select("templates")
    print(f"    记录数: {len(templates)}")
    if templates:
        print(f"    示例: {templates[0]}")
    
    # 2. 检查 product_photos 表
    print("\n[2] product_photos 表（产品实拍图）:")
    photos = db.select("product_photos")
    print(f"    记录数: {len(photos)}")
    if photos:
        print(f"    示例: {photos[0]}")
    
    # 3. 检查 sku_mapping 表
    print("\n[3] sku_mapping 表（SKU对照）:")
    sku_mapping = db.select("sku_mapping")
    print(f"    记录数: {len(sku_mapping)}")
    if sku_mapping:
        print(f"    示例: {sku_mapping[0]}")
    
    # 4. 检查 fonts 表
    print("\n[4] fonts 表（字体信息）:")
    fonts = db.select("fonts")
    print(f"    记录数: {len(fonts)}")
    if fonts:
        print(f"    示例: {fonts[0]}")
    
    # 5. 检查 Storage buckets
    print("\n[5] 检查 Supabase Storage buckets...")
    try:
        # 列出 buckets
        buckets = db._client.storage.list_buckets()
        print(f"    Buckets: {[b.name for b in buckets]}")
    except Exception as e:
        print(f"    无法获取 buckets: {e}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    check_supabase_data()
