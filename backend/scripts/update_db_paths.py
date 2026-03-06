# -*- coding: utf-8 -*-
"""
更新 Supabase 数据库中的文件路径，指向 Storage 的新路径
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.database_service import db

# 路径映射规则
PATH_MAPPING = {
    # 模板路径
    "templates/B不锈钢_模版_大号/": "templates/large/",
    "templates/B不锈钢_模版_小号/": "templates/small/",
    # 实拍图路径
    "photos/B不锈钢_实拍图_大/": "photos/large/",
    "photos/B不锈钢_实拍图_小/": "photos/small/",
    # 字体路径
    "/fonts/": "fonts/",
}


def update_templates_table():
    """更新 templates 表中的路径"""
    print("\n[1] 更新 templates 表...")
    
    templates = db.select("templates")
    updated = 0
    
    for t in templates:
        changes = {}
        
        # 更新正面 SVG 路径
        if t.get("front_svg_path"):
            old_path = t["front_svg_path"]
            new_path = old_path
            for old, new in PATH_MAPPING.items():
                new_path = new_path.replace(old, new)
            # 清理文件名中的空格
            new_path = new_path.replace(" ", "_").replace("_-_", "-")
            if old_path != new_path:
                changes["front_svg_path"] = new_path
        
        # 更新背面 SVG 路径
        if t.get("back_svg_path"):
            old_path = t["back_svg_path"]
            new_path = old_path
            for old, new in PATH_MAPPING.items():
                new_path = new_path.replace(old, new)
            # 清理文件名中的空格
            new_path = new_path.replace(" ", "_").replace("_-_", "-")
            if old_path != new_path:
                changes["back_svg_path"] = new_path
        
        if changes:
            db.update("templates", {"id": t["id"]}, changes)
            updated += 1
            print(f"    ✓ {t['name']}")
    
    print(f"    更新完成: {updated} 条")
    return updated


def update_product_photos_table():
    """更新 product_photos 表中的路径"""
    print("\n[2] 更新 product_photos 表...")
    
    photos = db.select("product_photos")
    updated = 0
    
    for p in photos:
        if p.get("photo_url"):
            old_path = p["photo_url"]
            new_path = old_path
            for old, new in PATH_MAPPING.items():
                new_path = new_path.replace(old, new)
            
            if old_path != new_path:
                db.update("product_photos", {"id": p["id"]}, {"photo_url": new_path})
                updated += 1
                print(f"    ✓ {old_path} → {new_path}")
    
    print(f"    更新完成: {updated} 条")
    return updated


def update_fonts_table():
    """更新 fonts 表中的路径"""
    print("\n[3] 更新 fonts 表...")
    
    fonts = db.select("fonts")
    updated = 0
    
    for f in fonts:
        if f.get("file_path"):
            old_path = f["file_path"]
            new_path = old_path
            
            # 移除开头的斜杠
            if new_path.startswith("/fonts/"):
                new_path = "fonts/" + new_path[7:]
            elif new_path.startswith("/"):
                new_path = new_path[1:]
            
            if old_path != new_path:
                db.update("fonts", {"id": f["id"]}, {"file_path": new_path})
                updated += 1
                print(f"    ✓ {old_path} → {new_path}")
    
    print(f"    更新完成: {updated} 条")
    return updated


def verify_paths():
    """验证更新后的路径"""
    print("\n[4] 验证更新后的路径...")
    
    # 检查模板
    templates = db.select("templates")
    print(f"    templates 示例: {templates[0]['front_svg_path']}")
    
    # 检查实拍图
    photos = db.select("product_photos")
    print(f"    photos 示例: {photos[0]['photo_url']}")
    
    # 检查字体
    fonts = db.select("fonts")
    print(f"    fonts 示例: {fonts[0]['file_path']}")


def main():
    print("=" * 60)
    print("更新 Supabase 数据库路径")
    print("=" * 60)
    
    t = update_templates_table()
    p = update_product_photos_table()
    f = update_fonts_table()
    
    verify_paths()
    
    print("\n" + "=" * 60)
    print(f"更新汇总: templates={t}, photos={p}, fonts={f}")
    print("=" * 60)


if __name__ == "__main__":
    main()
