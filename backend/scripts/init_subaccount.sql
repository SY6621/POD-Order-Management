-- =====================================================
-- 子账号功能数据库扩展脚本
-- 在现有多租户基础上添加主账号-子账号权限体系
-- =====================================================

-- 1. 扩展 users 表 - 添加角色类型和父账号关联
ALTER TABLE users ADD COLUMN IF NOT EXISTS role_type VARCHAR(20) DEFAULT 'sub';
-- role_type: 'main' = 主账号, 'sub' = 子账号

ALTER TABLE users ADD COLUMN IF NOT EXISTS parent_id UUID REFERENCES users(id) ON DELETE SET NULL;
-- parent_id: 子账号关联的主账号ID

ALTER TABLE users ADD COLUMN IF NOT EXISTS display_name VARCHAR(100);
-- display_name: 显示名称

ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(20);
-- phone: 联系电话

-- 更新约束
ALTER TABLE users DROP CONSTRAINT IF EXISTS valid_role;
ALTER TABLE users ADD CONSTRAINT valid_role CHECK (role IN ('admin', 'store_operator', 'factory', 'main', 'sub'));

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_users_role_type ON users(role_type);
CREATE INDEX IF NOT EXISTS idx_users_parent_id ON users(parent_id);

-- 2. 创建用户-店铺权限关联表
CREATE TABLE IF NOT EXISTS user_shop_permissions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    shop_id UUID NOT NULL REFERENCES shops(id) ON DELETE CASCADE,
    granted_by UUID REFERENCES users(id) ON DELETE SET NULL,  -- 哪个主账号授权的
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    permissions JSONB DEFAULT '{"read": true, "write": true}'::jsonb,
    
    -- 唯一约束：一个用户对一个店铺只有一条权限记录
    CONSTRAINT unique_user_shop UNIQUE(user_id, shop_id)
);

CREATE INDEX IF NOT EXISTS idx_user_shop_permissions_user_id ON user_shop_permissions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_shop_permissions_shop_id ON user_shop_permissions(shop_id);

-- 3. 创建操作日志表（用于监控和审计）
CREATE TABLE IF NOT EXISTS operation_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    shop_id UUID REFERENCES shops(id) ON DELETE SET NULL,
    action_type VARCHAR(50) NOT NULL,  -- email_sent, effect_generated, order_confirmed, order_shipped
    action_detail JSONB,
    ip_address INET,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_operation_logs_user_id ON operation_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_operation_logs_shop_id ON operation_logs(shop_id);
CREATE INDEX IF NOT EXISTS idx_operation_logs_action_type ON operation_logs(action_type);
CREATE INDEX IF NOT EXISTS idx_operation_logs_created_at ON operation_logs(created_at);

-- 4. 更新现有管理员为主账号
UPDATE users SET role_type = 'main', role = 'admin' WHERE role = 'admin';

-- 5. 为 shops 表添加密码字段（明文，用于简化访问）
ALTER TABLE shops ADD COLUMN IF NOT EXISTS password VARCHAR(50) DEFAULT 'shop123';

-- 更新现有店铺的默认密码
UPDATE shops SET password = LOWER(code) || '123' WHERE password = 'shop123';

-- 6. 创建子账号绩效统计视图
CREATE OR REPLACE VIEW subaccount_stats AS
SELECT 
    u.id as user_id,
    u.username,
    u.display_name,
    u.parent_id,
    u.status,
    COUNT(DISTINCT usp.shop_id) as managed_shops_count,
    COUNT(DISTINCT o.id) as total_orders,
    COUNT(DISTINCT CASE WHEN o.status = 'shipped' THEN o.id END) as shipped_orders,
    COUNT(DISTINCT CASE WHEN ol.action_type = 'email_sent' THEN ol.id END) as emails_sent,
    MAX(ol.created_at) as last_activity_at
FROM users u
LEFT JOIN user_shop_permissions usp ON u.id = usp.user_id
LEFT JOIN orders o ON usp.shop_id = o.shop_id
LEFT JOIN operation_logs ol ON u.id = ol.user_id
WHERE u.role_type = 'sub'
GROUP BY u.id, u.username, u.display_name, u.parent_id, u.status;

-- 输出完成信息
SELECT '子账号功能数据库扩展完成' as status;
