"""
Supabase 连接测试脚本
验证 .env 配置是否正确
"""
import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from supabase import create_client, Client

# 加载 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

def test_connection():
    """测试 Supabase 连接"""
    print("=" * 50)
    print("Supabase 连接测试")
    print("=" * 50)
    
    # 读取配置
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ 错误: .env 文件中缺少 SUPABASE_URL 或 SUPABASE_KEY")
        return False
    
    print(f"✅ SUPABASE_URL: {url[:30]}...")
    print(f"✅ SUPABASE_KEY: {key[:20]}...")
    
    try:
        # 创建客户端
        supabase: Client = create_client(url, key)
        print("✅ Supabase 客户端创建成功")
        
        # 测试查询 - 读取 fonts 表
        print("\n测试查询 fonts 表...")
        response = supabase.table("fonts").select("*").limit(3).execute()
        
        print(f"✅ 查询成功！fonts 表共有 {len(response.data)} 条记录（显示前3条）")
        for font in response.data:
            print(f"   - {font['name']}: {font['file_path']}")
        
        # 测试查询 - 读取 sku_mapping 表
        print("\n测试查询 sku_mapping 表...")
        response = supabase.table("sku_mapping").select("*").limit(3).execute()
        
        print(f"✅ 查询成功！sku_mapping 表共有 {len(response.data)} 条记录（显示前3条）")
        for sku in response.data:
            print(f"   - {sku['sku_code']}: {sku['shape']} {sku['color']} {sku['size']}")
        
        print("\n" + "=" * 50)
        print("🎉 所有测试通过！Supabase 连接正常")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

if __name__ == "__main__":
    test_connection()