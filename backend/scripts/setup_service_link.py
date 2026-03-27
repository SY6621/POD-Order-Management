#!/usr/bin/env python3
"""
客服外链数据库初始化脚本
执行 shops 表扩展和日志表创建
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from supabase import create_client
from config.config import SUPABASE_URL, SUPABASE_KEY

def setup_service_link_tables():
    """设置客服外链相关表结构"""
    
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # SQL 1: 扩展 shops 表
    sql1 = """
    ALTER TABLE shops 
    ADD COLUMN IF NOT EXISTS service_token VARCHAR(64) UNIQUE;
    
    ALTER TABLE shops 
    ADD COLUMN IF NOT EXISTS service_link_enabled BOOLEAN DEFAULT false;
    
    ALTER TABLE shops 
    ADD COLUMN IF NOT EXISTS service_link_created_at TIMESTAMP;
    
    ALTER TABLE shops 
    ADD COLUMN IF NOT EXISTS service_link_updated_at TIMESTAMP;
    """
    
    # SQL 2: 创建日志表
    sql2 = """
    CREATE TABLE IF NOT EXISTS service_link_logs (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        shop_id UUID NOT NULL REFERENCES shops(id) ON DELETE CASCADE,
        order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
        ip_address INET,
        user_agent TEXT,
        action VARCHAR(50) NOT NULL,
        action_details JSONB,
        created_at TIMESTAMP DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_service_link_logs_shop_id ON service_link_logs(shop_id);
    CREATE INDEX IF NOT EXISTS idx_service_link_logs_order_id ON service_link_logs(order_id);
    CREATE INDEX IF NOT EXISTS idx_service_link_logs_action ON service_link_logs(action);
    CREATE INDEX IF NOT EXISTS idx_service_link_logs_created_at ON service_link_logs(created_at);
    """
    
    try:
        # 执行 SQL 1
        result = client.rpc('exec_sql', {'sql': sql1}).execute()
        print("✅ shops 表扩展成功")
        print("   - service_token: 客服外链Token")
        print("   - service_link_enabled: 外链启用状态")
        print("   - service_link_created_at: 外链创建时间")
        print("   - service_link_updated_at: 外链更新时间")
    except Exception as e:
        print(f"❌ shops 表扩展失败: {e}")
        # 尝试直接执行
        try:
            client.table('shops').select('*').limit(1).execute()
            print("ℹ️  字段可能已存在，跳过")
        except Exception as e2:
            print(f"❌ 错误: {e2}")
            return False
    
    try:
        # 执行 SQL 2
        result = client.rpc('exec_sql', {'sql': sql2}).execute()
        print("✅ service_link_logs 表创建成功")
    except Exception as e:
        print(f"⚠️  service_link_logs 表创建: {e}")
        # 表可能已存在
        try:
            client.table('service_link_logs').select('*').limit(1).execute()
            print("ℹ️  表已存在，跳过")
        except:
            print(f"❌ 创建表失败: {e}")
            return False
    
    print("\n🎉 客服外链数据库初始化完成")
    return True

if __name__ == '__main__':
    setup_service_link_tables()
