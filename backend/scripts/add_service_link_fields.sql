-- 扩展 shops 表，添加客服外链相关字段
-- 执行时间: 2025-03-25

-- 1. 添加 service_token 字段（客服外链Token）
ALTER TABLE shops 
ADD COLUMN IF NOT EXISTS service_token VARCHAR(64) UNIQUE;

-- 2. 添加 service_link_enabled 字段（外链是否启用）
ALTER TABLE shops 
ADD COLUMN IF NOT EXISTS service_link_enabled BOOLEAN DEFAULT false;

-- 3. 添加 service_link_created_at 字段（外链生成时间）
ALTER TABLE shops 
ADD COLUMN IF NOT EXISTS service_link_created_at TIMESTAMP;

-- 4. 添加 service_link_updated_at 字段（外链更新时间）
ALTER TABLE shops 
ADD COLUMN IF NOT EXISTS service_link_updated_at TIMESTAMP;

-- 5. 为现有店铺生成初始Token（可选）
-- UPDATE shops 
-- SET service_token = encode(gen_random_bytes(32), 'hex'),
--     service_link_enabled = false
-- WHERE service_token IS NULL;

-- 验证字段添加成功
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'shops' 
AND column_name IN ('service_token', 'service_link_enabled', 'service_link_created_at', 'service_link_updated_at')
ORDER BY ordinal_position;
