-- ============================================================
-- 修复 email_logs 表：添加缺失的 content 字段
-- 执行时间：2026-03-13
-- 问题原因：email_logs 表创建时可能遗漏了 content 字段
-- ============================================================

-- 1. 添加 content 字段（如果不存在）
ALTER TABLE email_logs 
ADD COLUMN IF NOT EXISTS content TEXT;

-- 2. 验证表结构
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'email_logs'
ORDER BY ordinal_position;
