# -*- coding: utf-8 -*-
"""
执行设计链接字段扩展
在 shops 表中新增 design_token 等字段支持双链接体系

使用方法：
1. 在 Supabase Dashboard 中手动执行 SQL（推荐）
2. 或使用 psql 命令行工具执行
"""

import os

# SQL 语句
SQL_STATEMENTS = """
-- ============================================================
-- 双链接体系 - 数据库扩展脚本
-- 为 shops 表新增设计链接(design_link)相关字段
-- ============================================================

-- 1. 新增 design_token 字段 (设计链接Token)
ALTER TABLE shops ADD COLUMN IF NOT EXISTS design_token VARCHAR(64);

-- 2. 新增 design_link_enabled 字段 (设计链接是否启用)
ALTER TABLE shops ADD COLUMN IF NOT EXISTS design_link_enabled BOOLEAN DEFAULT false;

-- 3. 新增 design_link_created_at 字段 (设计链接创建时间)
ALTER TABLE shops ADD COLUMN IF NOT EXISTS design_link_created_at TIMESTAMP WITH TIME ZONE;

-- 4. 新增 design_link_updated_at 字段 (设计链接更新时间)
ALTER TABLE shops ADD COLUMN IF NOT EXISTS design_link_updated_at TIMESTAMP WITH TIME ZONE;

-- 5. 为 design_token 创建唯一索引 (确保Token唯一)
CREATE UNIQUE INDEX IF NOT EXISTS idx_shops_design_token ON shops(design_token) WHERE design_token IS NOT NULL;

-- ============================================================
-- 验证新增字段
-- ============================================================
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'shops' 
AND column_name LIKE 'design%'
ORDER BY ordinal_position;
"""


def print_sql():
    """打印 SQL 语句供手动执行"""
    print("=" * 70)
    print("请在 Supabase Dashboard 中执行以下 SQL：")
    print("=" * 70)
    print()
    print(SQL_STATEMENTS)
    print()
    print("=" * 70)
    print("执行步骤：")
    print("1. 登录 Supabase Dashboard")
    print("2. 进入 SQL Editor")
    print("3. 新建查询，粘贴上述 SQL")
    print("4. 点击 Run 执行")
    print("=" * 70)


def save_sql_file():
    """保存 SQL 到文件"""
    sql_file = os.path.join(os.path.dirname(__file__), 'add_design_link_fields.sql')
    with open(sql_file, 'w', encoding='utf-8') as f:
        f.write(SQL_STATEMENTS)
    print(f"✅ SQL 已保存到: {sql_file}")
    return sql_file


if __name__ == "__main__":
    save_sql_file()
    print()
    print_sql()
