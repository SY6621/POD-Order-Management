# 多租户系统数据库创建 SQL

请在 Supabase Dashboard 的 SQL Editor 中按顺序执行以下 SQL：

## 1. 创建 shops 表

```sql
CREATE TABLE shops (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    region VARCHAR(50),
    password_hash VARCHAR(255),
    api_key VARCHAR(255),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX idx_shops_code ON shops(code);
CREATE INDEX idx_shops_status ON shops(status);
```

## 2. 创建 users 表

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'store_operator', 'factory')),
    shop_id UUID REFERENCES shops(id) ON DELETE SET NULL,
    email VARCHAR(100),
    status VARCHAR(20) DEFAULT 'active',
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_shop_id ON users(shop_id);
```

## 3. 扩展 orders 表

```sql
-- 添加店铺关联
ALTER TABLE orders ADD COLUMN shop_id UUID REFERENCES shops(id) ON DELETE SET NULL;
ALTER TABLE orders ADD COLUMN shop_order_id VARCHAR(50);

-- 创建索引
CREATE INDEX idx_orders_shop_id ON orders(shop_id);
```

## 4. 初始化默认数据

```sql
-- 插入默认店铺
INSERT INTO shops (name, code, region, status) VALUES
    ('美国店铺', 'us', 'North America', 'active'),
    ('欧洲店铺', 'eu', 'Europe', 'active'),
    ('亚洲店铺', 'asia', 'Asia', 'active')
ON CONFLICT (code) DO NOTHING;

-- 查看创建的店铺
SELECT * FROM shops;
```

## 5. 创建访问日志表（可选）

```sql
-- 店铺访问日志
CREATE TABLE shop_access_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    shop_id UUID REFERENCES shops(id) ON DELETE CASCADE,
    action VARCHAR(50) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_shop_access_logs_shop_id ON shop_access_logs(shop_id);

-- 工厂访问日志
CREATE TABLE factory_access_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    action VARCHAR(50) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 执行后验证

```sql
-- 验证表是否创建成功
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('shops', 'users', 'shop_access_logs', 'factory_access_logs');

-- 验证orders表扩展
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'orders' 
AND column_name IN ('shop_id', 'shop_order_id');

-- 查看默认店铺
SELECT * FROM shops;
```