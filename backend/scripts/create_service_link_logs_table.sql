-- 创建客服外链访问日志表
-- 用于记录客服通过外链访问和操作的历史

CREATE TABLE IF NOT EXISTS service_link_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shop_id UUID NOT NULL REFERENCES shops(id) ON DELETE CASCADE,
    order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
    
    -- 访问信息
    ip_address INET,
    user_agent TEXT,
    
    -- 操作类型
    action VARCHAR(50) NOT NULL, -- 'view':查看, 'send_email':发送邮件, 'confirm':客户确认, 'request_modify':请求修改
    
    -- 操作详情（JSON格式，可选）
    action_details JSONB,
    
    -- 时间戳
    created_at TIMESTAMP DEFAULT NOW()
);

-- 创建索引优化查询
CREATE INDEX IF NOT EXISTS idx_service_link_logs_shop_id ON service_link_logs(shop_id);
CREATE INDEX IF NOT EXISTS idx_service_link_logs_order_id ON service_link_logs(order_id);
CREATE INDEX IF NOT EXISTS idx_service_link_logs_action ON service_link_logs(action);
CREATE INDEX IF NOT EXISTS idx_service_link_logs_created_at ON service_link_logs(created_at);

-- 添加表注释
COMMENT ON TABLE service_link_logs IS '客服外链访问日志表';
COMMENT ON COLUMN service_link_logs.action IS '操作类型: view(查看), send_email(发送邮件), confirm(客户确认), request_modify(请求修改)';

-- 验证表创建成功
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'service_link_logs'
ORDER BY ordinal_position;
