-- 工厂管理表
-- 用于管理工厂账户和访问权限

-- 删除已存在的表（注意：会删除数据）
DROP TABLE IF EXISTS factories;

-- 创建工厂表
CREATE TABLE factories (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name VARCHAR(200) NOT NULL,              -- 工厂名称
  code VARCHAR(50) NOT NULL UNIQUE,        -- 工厂代码（唯一标识，用于生成访问链接）
  password_hash VARCHAR(200),              -- 访问密码（工厂协作平台登录用）
  status VARCHAR(20) DEFAULT 'active',     -- 状态：active/inactive
  contact_name VARCHAR(100),               -- 联系人姓名
  contact_phone VARCHAR(50),               -- 联系电话
  address TEXT,                            -- 工厂地址
  access_url TEXT,                         -- 自定义访问URL（可选）
  created_at TIMESTAMPTZ DEFAULT NOW(),    -- 创建时间
  updated_at TIMESTAMPTZ DEFAULT NOW()     -- 更新时间
);

-- 启用行级安全策略
ALTER TABLE factories ENABLE ROW LEVEL SECURITY;

-- 允许匿名读取（工厂协作平台需要）
CREATE POLICY "Allow anonymous read" ON factories FOR SELECT USING (true);

-- 允许匿名写入（Admin后台管理需要）
CREATE POLICY "Allow anonymous write" ON factories FOR ALL USING (true);

-- 创建更新时间触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_factories_updated_at
    BEFORE UPDATE ON factories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 插入默认工厂数据
INSERT INTO factories (name, code, password_hash, status, contact_name)
VALUES 
  ('主工厂', 'main-factory', 'factory123', 'active', '工厂负责人A'),
  ('分工厂A', 'sub-factory-a', 'factory456', 'active', '工厂负责人B')
ON CONFLICT (code) DO NOTHING;

-- 验证插入结果
SELECT * FROM factories;
