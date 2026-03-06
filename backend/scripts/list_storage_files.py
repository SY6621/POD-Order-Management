# -*- coding: utf-8 -*-
"""
详细检查 Supabase Storage 文件列表
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.database_service import db


def list_all_files(bucket_name: str):
    """递归列出 bucket 中的所有文件"""
    print(f"\n{'='*50}")
    print(f"Bucket: {bucket_name}")
    print(f"{'='*50}")
    
    total_files = 0
    
    try:
        # 列出根目录
        root_items = db._client.storage.from_(bucket_name).list()
        
        for item in root_items:
            name = item.get("name", "unknown")
            
            # 检查是否是文件夹（通过 metadata 判断）
            if item.get("metadata") is None:
                # 是文件夹，递归列出
                sub_items = db._client.storage.from_(bucket_name).list(name)
                print(f"\n📁 {name}/ ({len(sub_items)} 个文件)")
                for sub in sub_items:
                    sub_name = sub.get("name", "")
                    sub_size = sub.get("metadata", {}).get("size", 0)
                    size_kb = sub_size / 1024 if sub_size else 0
                    print(f"   📄 {sub_name} ({size_kb:.1f} KB)")
                    total_files += 1
            else:
                # 是文件
                size = item.get("metadata", {}).get("size", 0)
                size_kb = size / 1024 if size else 0
                print(f"\n📄 {name} ({size_kb:.1f} KB)")
                total_files += 1
        
        print(f"\n总计: {total_files} 个文件")
        return total_files
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return 0


def main():
    print("=" * 60)
    print("Supabase Storage 文件详细清单")
    print("=" * 60)
    
    t = list_all_files("templates")
    p = list_all_files("photos")
    f = list_all_files("fonts")
    
    print(f"\n{'='*60}")
    print(f"总计: templates={t}, photos={p}, fonts={f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
