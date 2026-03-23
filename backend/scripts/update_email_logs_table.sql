-- ============================================================
-- 更新 email_logs 表，添加落款人和确认截止时间字段
-- 执行时间：2026-03-13
-- ============================================================

-- 1. 添加 sender_name 字段（落款人）
ALTER TABLE email_logs 
ADD COLUMN IF NOT EXISTS sender_name VARCHAR(100) DEFAULT 'Customer Support Team';

-- 2. 添加 confirmation_deadline 字段（确认截止时间）
ALTER TABLE email_logs 
ADD COLUMN IF NOT EXISTS confirmation_deadline VARCHAR(100);

-- 3. 为 email_type 字段添加注释说明
COMMENT ON COLUMN email_logs.email_type IS '邮件类型：first_confirm(首封确认邮件)、modification(修改确认邮件)、follow_up(追评邮件)';

-- 4. 查看更新后的表结构
SELECT column_name, data_type, column_default 
FROM information_schema.columns 
WHERE table_name = 'email_logs'
ORDER BY ordinal_position;
