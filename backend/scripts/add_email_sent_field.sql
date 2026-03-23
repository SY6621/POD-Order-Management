-- 给 orders 表添加 email_sent 字段（标记是否已发送确认邮件）
ALTER TABLE orders 
ADD COLUMN IF NOT EXISTS email_sent BOOLEAN DEFAULT false;

-- 添加注释
COMMENT ON COLUMN orders.email_sent IS '是否已发送确认邮件';

-- 查看字段是否添加成功
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'orders' 
AND column_name = 'email_sent';
