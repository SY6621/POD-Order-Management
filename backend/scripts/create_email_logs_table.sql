-- 创建邮件记录表
CREATE TABLE IF NOT EXISTS email_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    email_type VARCHAR(50) NOT NULL DEFAULT 'confirmation', -- confirmation: 确认邮件, modification: 修改邮件, followup: 追评邮件
    subject TEXT NOT NULL,
    content TEXT NOT NULL,
    effect_image_url TEXT, -- 发送时的效果图URL
    recipient_email VARCHAR(255),
    sent_by UUID REFERENCES users(id) ON DELETE SET NULL, -- 发送人
    status VARCHAR(50) DEFAULT 'sent', -- sent: 已发送, read: 客户已读, replied: 客户已回复, needs_revision: 客户要求修改
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_email_logs_order_id ON email_logs(order_id);
CREATE INDEX IF NOT EXISTS idx_email_logs_sent_at ON email_logs(sent_at);
CREATE INDEX IF NOT EXISTS idx_email_logs_status ON email_logs(status);

-- 添加注释
COMMENT ON TABLE email_logs IS '邮件发送记录表';
COMMENT ON COLUMN email_logs.email_type IS '邮件类型：confirmation=确认邮件, modification=修改邮件, followup=追评邮件';
COMMENT ON COLUMN email_logs.status IS '邮件状态：sent=已发送, read=客户已读, replied=客户已回复, needs_revision=客户要求修改';

-- 查看创建的表结构
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'email_logs'
ORDER BY ordinal_position;
