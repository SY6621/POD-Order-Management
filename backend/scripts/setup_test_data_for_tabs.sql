-- 设置测试数据，让每个Tab都有订单显示
-- 假设有3个订单，分别设置不同的状态

-- 订单1: 新订单状态（无效果图）
UPDATE orders 
SET effect_image_url = NULL, 
    email_sent = false,
    updated_at = NOW()
WHERE etsy_order_id = '4002217518';

-- 订单2: 邮件撰写状态（有效果图，未发送邮件）
UPDATE orders 
SET effect_image_url = 'https://your-supabase-url/storage/v1/object/public/effect-images/test-order-2.png',
    email_sent = false,
    updated_at = NOW()
WHERE etsy_order_id = '3891559803';

-- 订单3: 待创建状态（有效果图，已发送邮件）
UPDATE orders 
SET effect_image_url = 'https://your-supabase-url/storage/v1/object/public/effect-images/test-order-3.png',
    email_sent = true,
    updated_at = NOW()
WHERE etsy_order_id = '3986891868';

-- 查看设置结果
SELECT etsy_order_id, status, effect_image_url IS NOT NULL as has_effect, email_sent
FROM orders 
WHERE etsy_order_id IN ('4002217518', '3891559803', '3986891868')
ORDER BY etsy_order_id;
