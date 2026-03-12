-- =====================================================
-- 多租户系统数据库初始化脚本
-- 创建店铺表、用户权限表，扩展订单表
-- =====================================================

-- 1. 创建店铺表 (shops)
CREATE TABLE IF NOT EXISTS shops (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,           -- 店铺名称
    code VARCHAR(20) UNIQUE NOT NULL,     -- 店铺代码 (us/eu/asia等)
    region VARCHAR(50),                   -- 地区
    password_hash VARCHAR(255),           -- 访问密码 (bcrypt加密)
    api_key VARCHAR(255),                 -- API密钥 (用于ETSY接口)
    status VARCHAR(20) DEFAULT 'active',  -- active/inactive
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_shops_code ON shops(code);
CREATE INDEX IF NOT EXISTS idx_shops_status ON shops(status);

-- 2. 创建用户权限表 (users)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,  -- bcrypt加密
    role VARCHAR(20) NOT NULL,            -- admin/store_operator/factory
    shop_id UUID REFERENCES shops(id) ON DELETE SET NULL,  -- 店铺运营关联店铺
    email VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- 约束
    CONSTRAINT valid_role CHECK (role IN ('admin', 'store_operator', 'factory'))
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_shop_id ON users(shop_id);

-- 3. 扩展订单表 - 添加店铺关联
ALTER TABLE orders 
ADD COLUMN IF NOT EXISTS shop_id UUID REFERENCES shops(id) ON DELETE SET NULL;

ALTER TABLE orders 
ADD COLUMN IF NOT EXISTS shop_order_id VARCHAR(50);  -- 店铺内部订单号

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_orders_shop_id ON orders(shop_id);

-- 4. 创建更新时间触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为shops表添加更新时间触发器
DROP TRIGGER IF EXISTS update_shops_updated_at ON shops;
CREATE TRIGGER update_shops_updated_at
    BEFORE UPDATE ON shops
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 为users表添加更新时间触发器
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 5. 初始化默认店铺数据
INSERT INTO shops (name, code, region, password_hash, status) VALUES
    ('美国店铺', 'us', 'North America', '$2b$10$YourHashedPasswordHere', 'active'),
    ('欧洲店铺', 'eu', 'Europe', '$2b$10$YourHashedPasswordHere', 'active'),
    ('亚洲店铺', 'asia', 'Asia', '$2b$10$YourHashedPasswordHere', 'active')
ON CONFLICT (code) DO NOTHING;

-- 6. 初始化默认管理员账号
-- 密码: admin123 (实际使用时需要替换为bcrypt加密后的密码)
INSERT INTO users (username, password_hash, role, email, status) VALUES
    ('admin', '$2b$10$YourHashedPasswordHere', 'admin', 'admin@example.com', 'active')
ON CONFLICT (username) DO NOTHING;

-- 7. 创建店铺访问日志表 (用于审计)
CREATE TABLE IF NOT EXISTS shop_access_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    shop_id UUID REFERENCES shops(id) ON DELETE CASCADE,
    action VARCHAR(50) NOT NULL,          -- login/download/view等
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_shop_access_logs_shop_id ON shop_access_logs(shop_id);
CREATE INDEX IF NOT EXISTS idx_shop_access_logs_created_at ON shop_access_logs(created_at);

-- 8. 创建工厂访问日志表
CREATE TABLE IF NOT EXISTS factory_access_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    action VARCHAR(50) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 输出完成信息
SELECT '多租户数据库初始化完成' as status;
SELECT * FROM shops;
SELECT * FROM users;