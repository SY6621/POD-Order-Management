# -*- coding: utf-8 -*-
"""
上传本地资源到 Supabase Storage
包括：模板、实拍图、字体
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.database_service import db

# 资源目录
ASSETS_DIR = Path(__file__).parent.parent / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
PHOTOS_DIR = ASSETS_DIR / "photos"
FONTS_DIR = ASSETS_DIR / "fonts"


def create_bucket_if_not_exists(bucket_name: str, public: bool = True):
    """创建 bucket（如果不存在）"""
    try:
        # 尝试获取 bucket
        db._client.storage.get_bucket(bucket_name)
        print(f"    Bucket '{bucket_name}' 已存在")
        return True
    except Exception:
        # 不存在，创建新的
        try:
            db._client.storage.create_bucket(bucket_name, options={"public": public})
            print(f"    ✓ 创建 Bucket '{bucket_name}'")
            return True
        except Exception as e:
            print(f"    ✗ 创建 Bucket 失败: {e}")
            return False


def upload_file_to_bucket(bucket: str, local_path: Path, remote_path: str):
    """上传单个文件到 bucket"""
    try:
        with open(local_path, "rb") as f:
            file_bytes = f.read()
        
        # 确定 MIME 类型
        suffix = local_path.suffix.lower()
        mime_map = {
            ".svg": "image/svg+xml",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".ttf": "font/ttf",
            ".otf": "font/otf",
        }
        mime = mime_map.get(suffix, "application/octet-stream")
        
        # 上传（使用 upsert 覆盖已存在的文件）
        db._client.storage.from_(bucket).upload(
            remote_path, 
            file_bytes,
            file_options={"content-type": mime, "upsert": "true"}
        )
        return True
    except Exception as e:
        print(f"      ✗ 上传失败 {remote_path}: {e}")
        return False


# 中文目录名 → 英文目录名映射
DIR_NAME_MAP = {
    "B不锈钢_模版_大号": "large",
    "B不锈钢_模版_小号": "small",
    "B不锈钢_实拍图_大": "large",
    "B不锈钢_实拍图_小": "small",
    "阿里巴巴普惠体": "alibaba",
}


def sanitize_filename(filename: str) -> str:
    """清理文件名，移除空格和特殊字符"""
    # 移除空格，替换为下划线
    return filename.replace(" ", "_").replace(" - ", "-")


def upload_templates():
    """上传 SVG 模板"""
    print("\n[2] 上传 SVG 模板...")
    
    success_count = 0
    total_count = 0
    
    # 遍历模板目录
    for size_dir in TEMPLATES_DIR.iterdir():
        if size_dir.is_dir():
            # 将中文目录名转为英文
            remote_dir = DIR_NAME_MAP.get(size_dir.name, size_dir.name)
            print(f"    目录: {size_dir.name} → {remote_dir}")
            for svg_file in size_dir.glob("*.svg"):
                total_count += 1
                # 清理文件名并构建远程路径
                clean_name = sanitize_filename(svg_file.name)
                remote_path = f"{remote_dir}/{clean_name}"
                if upload_file_to_bucket("templates", svg_file, remote_path):
                    success_count += 1
                    print(f"      ✓ {svg_file.name}")
    
    print(f"    模板上传完成: {success_count}/{total_count}")
    return success_count, total_count


def upload_photos():
    """上传产品实拍图"""
    print("\n[3] 上传产品实拍图...")
    
    success_count = 0
    total_count = 0
    
    # 遍历实拍图目录
    for size_dir in PHOTOS_DIR.iterdir():
        if size_dir.is_dir():
            # 将中文目录名转为英文
            remote_dir = DIR_NAME_MAP.get(size_dir.name, size_dir.name)
            print(f"    目录: {size_dir.name} → {remote_dir}")
            for photo_file in size_dir.glob("*.jpg"):
                total_count += 1
                remote_path = f"{remote_dir}/{photo_file.name}"
                if upload_file_to_bucket("photos", photo_file, remote_path):
                    success_count += 1
                    print(f"      ✓ {photo_file.name}")
    
    print(f"    实拍图上传完成: {success_count}/{total_count}")
    return success_count, total_count


def upload_fonts():
    """上传字体文件"""
    print("\n[4] 上传字体文件...")
    
    success_count = 0
    total_count = 0
    
    # 上传产品字体（F-01~F-08 + back_standard）
    print("    产品字体:")
    for font_file in FONTS_DIR.glob("*.ttf"):
        total_count += 1
        if upload_file_to_bucket("fonts", font_file, font_file.name):
            success_count += 1
            print(f"      ✓ {font_file.name}")
    
    for font_file in FONTS_DIR.glob("*.otf"):
        total_count += 1
        if upload_file_to_bucket("fonts", font_file, font_file.name):
            success_count += 1
            print(f"      ✓ {font_file.name}")
    
    # 上传阿里巴巴普惠体（使用英文目录名）
    alibaba_dir = FONTS_DIR / "阿里巴巴普惠体"
    if alibaba_dir.exists():
        print("    阿里巴巴普惠体 → alibaba:")
        for font_file in alibaba_dir.glob("*.TTF"):
            total_count += 1
            remote_path = f"alibaba/{font_file.name}"
            if upload_file_to_bucket("fonts", font_file, remote_path):
                success_count += 1
                print(f"      ✓ {font_file.name}")
    
    print(f"    字体上传完成: {success_count}/{total_count}")
    return success_count, total_count


def main():
    """主函数"""
    print("=" * 60)
    print("上传本地资源到 Supabase Storage")
    print("=" * 60)
    
    # 1. 创建 buckets
    print("\n[1] 创建 Storage Buckets...")
    create_bucket_if_not_exists("templates", public=True)
    create_bucket_if_not_exists("photos", public=True)
    create_bucket_if_not_exists("fonts", public=True)
    
    # 2. 上传模板
    t_success, t_total = upload_templates()
    
    # 3. 上传实拍图
    p_success, p_total = upload_photos()
    
    # 4. 上传字体
    f_success, f_total = upload_fonts()
    
    # 汇总
    print("\n" + "=" * 60)
    print("上传完成汇总")
    print("=" * 60)
    print(f"  模板:   {t_success}/{t_total}")
    print(f"  实拍图: {p_success}/{p_total}")
    print(f"  字体:   {f_success}/{f_total}")
    total = t_success + p_success + f_success
    total_all = t_total + p_total + f_total
    print(f"  总计:   {total}/{total_all}")
    print("=" * 60)


if __name__ == "__main__":
    main()
