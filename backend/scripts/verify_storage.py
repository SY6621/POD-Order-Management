# -*- coding: utf-8 -*-
"""
验证 Supabase Storage 中的文件
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.database_service import db


def list_bucket_files(bucket_name: str):
    """列出 bucket 中的文件"""
    try:
        # 列出根目录
        files = db._client.storage.from_(bucket_name).list()
        print(f"\n[{bucket_name}] 根目录:")
        for f in files:
            name = f.get("name", "unknown")
            if f.get("id"):  # 是文件夹
                # 列出子目录
                sub_files = db._client.storage.from_(bucket_name).list(name)
                print(f"  📁 {name}/ ({len(sub_files)} 个文件)")
                for sf in sub_files[:3]:  # 只显示前3个
                    print(f"      - {sf.get('name')}")
                if len(sub_files) > 3:
                    print(f"      ... 还有 {len(sub_files)-3} 个文件")
            else:
                print(f"  📄 {name}")
        return True
    except Exception as e:
        print(f"  ❌ 无法访问: {e}")
        return False


def main():
    print("=" * 60)
    print("验证 Supabase Storage 文件")
    print("=" * 60)
    
    # 列出所有 buckets
    try:
        buckets = db._client.storage.list_buckets()
        print(f"\n发现 {len(buckets)} 个 Buckets:")
        for b in buckets:
            print(f"  - {b.name} ({'PUBLIC' if b.public else 'PRIVATE'})")
    except Exception as e:
        print(f"❌ 无法获取 buckets: {e}")
        return
    
    # 检查每个资源 bucket
    list_bucket_files("templates")
    list_bucket_files("photos")
    list_bucket_files("fonts")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
