"""
Supabase 保活脚本
每天自动执行一次简单查询，防止项目被暂停
"""
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from supabase import create_client, Client

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

def ping_database():
    """向数据库发送心跳请求"""
    print("=" * 50)
    print("开始 Supabase 保活检查...")
    print("=" * 50)
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ 错误: .env 文件中缺少 SUPABASE_URL 或 SUPABASE_KEY")
        return False
    
    try:
        supabase: Client = create_client(url, key)
        
        response = supabase.table("orders").select("id").limit(1).execute()
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] ✅ Supabase 保活成功 - 数据库响应正常")
        print(f"✅ 查询到 {len(response.data)} 条数据")
        print("✅ 保活成功 - 项目将保持活跃状态")
        print("=" * 50)
        return True
        
    except Exception as e:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] ❌ Supabase 保活失败: {e}")
        print("❌ 保活失败 - 请检查 Supabase 配置")
        print("=" * 50)
        return False

if __name__ == "__main__":
    ping_database()