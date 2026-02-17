-- 新增 operator_email 字段（负责人邮箱）
-- 新增 remote_status 字段（远程协作状态）

-- 1. 添加 operator_email 字段
ALTER TABLE orders 
ADD COLUMN IF NOT EXISTS operator_email TEXT;

COMMENT ON COLUMN orders.operator_email IS '负责人邮箱（从转发邮件提取）';

-- 2. 添加 remote_status 字段
ALTER TABLE orders 
ADD COLUMN IF NOT EXISTS remote_status TEXT DEFAULT 'pending';

COMMENT ON COLUMN orders.remote_status IS '远程协作状态：pending=待处理, sent=已发送, confirmed=已确认';

-- 3. 添加 CHECK 约束
ALTER TABLE orders 
ADD CONSTRAINT orders_remote_status_check 
CHECK (remote_status IN ('pending', 'sent', 'confirmed'));

-- 4. 创建索引
CREATE INDEX IF NOT EXISTS idx_orders_operator_email ON orders(operator_email);
CREATE INDEX IF NOT EXISTS idx_orders_remote_status ON orders(remote_status);

-- 5. 验证字段添加
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'orders' 
AND column_name IN ('operator_email', 'remote_status');
