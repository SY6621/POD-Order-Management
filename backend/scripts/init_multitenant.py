#!/usr/bin/env python3
"""
多租户数据库初始化脚本
创建店铺表、用户表，扩展订单表
"""

import os
import sys
from supabase import create_client
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def init_multitenant():
    """初始化多租户数据库结构"""
    
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_KEY')
    
    if not url or not key:
        print("❌ 错误: 缺少 SUPABASE_URL 或 SUPABASE_SERVICE_KEY")
        sys.exit(1)
    
    supabase = create_client(url, key)
    
    print("🚀 开始初始化多租户数据库...")
    
    # 1. 创建 shops 表
    print("\n1. 创建 shops 表...")
    try:
        # 检查表是否已存在
        result = supabase.table('shops').select('id').limit(1).execute()
        print("   ✅ shops 表已存在")
    except Exception as e:
        if 'relation "shops" does not exist' in str(e):
            # 创建表
            create_shops_sql = """
            CREATE TABLE shops (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                name VARCHAR(100) NOT NULL,
                code VARCHAR(20) UNIQUE NOT NULL,
                region VARCHAR(50),
                password_hash VARCHAR(255),
                api_key VARCHAR(255),
                status VARCHAR(20) DEFAULT 'active',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
            # 使用 supabase 的 SQL 执行功能
            print("   ⏳ 请在 Supabase Dashboard 中执行以下 SQL:")
            print(create_shops_sql)
        else:
            print(f"   ⚠️ 检查表时出错: {e}")
    
    # 2. 创建 users 表
    print("\n2. 创建 users 表...")
    try:
        result = supabase.table('users').select('id').limit(1).execute()
        print("   ✅ users 表已存在")
    except Exception as e:
        if 'relation "users" does not exist' in str(e):
            print("   ⏳ 请在 Supabase Dashboard 中执行创建 users 表的 SQL")
        else:
            print(f"   ⚠️ 检查表时出错: {e}")
    
    # 3. 扩展 orders 表
    print("\n3. 扩展 orders 表...")
    try:
        # 检查列是否存在
        result = supabase.table('orders').select('shop_id').limit(1).execute()
        print("   ✅ shop_id 列已存在")
    except Exception as e:
        if 'column "shop_id" does not exist' in str(e):
            print("   ⏳ 请在 Supabase Dashboard 中执行:")
            print("   ALTER TABLE orders ADD COLUMN shop_id UUID REFERENCES shops(id);")
            print("   ALTER TABLE orders ADD COLUMN shop_order_id VARCHAR(50);")
        else:
            print(f"   ⚠️ 检查列时出错: {e}")
    
    # 4. 初始化默认店铺数据
    print("\n4. 初始化默认店铺数据...")
    try:
        default_shops = [
            {'name': '美国店铺', 'code': 'us', 'region': 'North America', 'status': 'active'},
            {'name': '欧洲店铺', 'code': 'eu', 'region': 'Europe', 'status': 'active'},
            {'name': '亚洲店铺', 'code': 'asia', 'region': 'Asia', 'status': 'active'},
        ]
        
        for shop in default_shops:
            try:
                result = supabase.table('shops').insert(shop).execute()
                print(f"   ✅ 创建店铺: {shop['name']} ({shop['code']})")
            except Exception as e:
                if 'duplicate key value' in str(e):
                    print(f"   ℹ️ 店铺已存在: {shop['name']} ({shop['code']})")
                else:
                    print(f"   ⚠️ 创建店铺失败: {e}")
                    
    except Exception as e:
        print(f"   ❌ 初始化店铺数据失败: {e}")
    
    print("\n" + "="*50)
    print("初始化完成！")
    print("\n下一步:")
    print("1. 在 Supabase Dashboard 中检查表结构")
    print("2. 为店铺设置访问密码")
    print("3. 创建管理员账号")

if __name__ == '__main__':
    init_multitenant()