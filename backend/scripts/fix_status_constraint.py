"""
第1步：移除数据库中的status约束，然后更新status值为中文
"""
from dotenv import load_dotenv
load_dotenv()
import os
from supabase import create_client

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
s = create_client(url, key)

# 使用rpc执行SQL，先删除约束，然后更新数据
# 注意：需要使用 service_role key 才能修改约束
# 尝试通过 rpc 执行

try:
    # 先尝试删除约束
    result = s.rpc('exec_sql', {'sql': '''
        ALTER TABLE orders DROP CONSTRAINT IF EXISTS orders_status_check;
        ALTER TABLE orders ADD CONSTRAINT orders_status_check 
            CHECK (status IN (
                '新订单', '待回复', '待创建', '客户修改', '生产中', '已送达',
                'pending', 'effect_sent', 'confirmed', 'customer_modify', 'producing', 'delivered'
            ));
    '''}).execute()
    print('✅ 约束修改成功:', result)
except Exception as e:
    print(f'❌ RPC方式失败: {e}')
    print('\n需要在Supabase SQL Editor中手动执行以下SQL：')
    print('''
-- 第1步：删除旧约束
ALTER TABLE orders DROP CONSTRAINT IF EXISTS orders_status_check;

-- 第2步：添加新约束（支持中英文）
ALTER TABLE orders ADD CONSTRAINT orders_status_check 
    CHECK (status IN (
        \'新订单\', \'待回复\', \'待创建\', \'客户修改\', \'生产中\', \'已送达\',
        \'pending\', \'effect_sent\', \'confirmed\', \'customer_modify\', \'producing\', \'delivered\'
    ));

-- 第3步：更新现有数据
UPDATE orders SET status = \'新订单\' WHERE status = \'pending\';
UPDATE orders SET status = \'生产中\' WHERE status = \'producing\';
UPDATE orders SET status = \'待回复\' WHERE status = \'effect_sent\';
UPDATE orders SET status = \'待创建\' WHERE status = \'confirmed\';
UPDATE orders SET status = \'客户修改\' WHERE status = \'customer_modify\';
UPDATE orders SET status = \'已送达\' WHERE status = \'delivered\';

-- 第4步：删除旧约束，只保留中文
ALTER TABLE orders DROP CONSTRAINT IF EXISTS orders_status_check;
ALTER TABLE orders ADD CONSTRAINT orders_status_check 
    CHECK (status IN (\'新订单\', \'待回复\', \'待创建\', \'客户修改\', \'生产中\', \'已送达\'));
''')
