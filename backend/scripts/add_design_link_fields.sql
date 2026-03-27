
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
