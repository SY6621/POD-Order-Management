# -*- coding: utf-8 -*-
"""验证后端是否能正确加载字体数据"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from src.services.database_service import DatabaseService

def main():
    print("=" * 60)
    print("🔍 开始验证后端字体加载功能")
    print("=" * 60)
    
    try:
        # 初始化数据库服务
        db = DatabaseService()
        print("✅ 数据库连接成功")
        
        # 获取所有字体
        fonts = db.get_all_fonts()
        print(f"\n📦 从 Supabase 找到 {len(fonts)} 个字体:\n")
        
        if not fonts:
            print("❌ 未找到任何字体数据！")
            return
        
        # 打印字体详情
        for idx, font in enumerate(fonts, 1):
            print(f"{idx}. [{font['font_code']}]")
            print(f"   名称: {font['font_name']}")
            print(f"   文件: {font['font_file_name']}")
            print(f"   缩放: {font.get('scaling_offset', 'N/A')}")
            print()
        
        print("=" * 60)
        print("✅ 字体加载验证成功！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
