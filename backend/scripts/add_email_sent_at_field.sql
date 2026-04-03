-- 给 orders 表添加 email_sent_at 字段
-- 在 Supabase Dashboard > SQL Editor 中执行

ALTER TABLE orders ADD COLUMN IF NOT EXISTS email_sent_at TIMESTAMPTZ;

-- 验证字段已添加
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'orders' AND column_name = 'email_sent_at';
