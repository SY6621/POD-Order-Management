-- 为shops表添加operator字段
ALTER TABLE shops ADD COLUMN IF NOT EXISTS operator VARCHAR(10);

-- 为澳洲01店设置运营归属
UPDATE shops SET operator = 'A' WHERE code = 'au01';

-- 验证
SELECT id, code, name, operator FROM shops;
