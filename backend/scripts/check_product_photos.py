# -*- coding: utf-8 -*-
"""检查产品图片数据"""

from supabase import create_client
import os

def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars

env = load_env()
supabase = create_client(env['SUPABASE_URL'], env['SUPABASE_KEY'])

print('=' * 70)
print('检查产品图片数据')
print('=' * 70)

# 查询所有 product_photos
photos = supabase.table('product_photos').select('sku_id, photo_url, photo_type').execute()
print(f'\n共 {len(photos.data)} 条产品图片记录:')
for p in photos.data:
    print(f'  sku_id: {p["sku_id"]}  photo_url: {p["photo_url"]}')

# 查询订单使用的 sku_id 列表
orders = supabase.table('orders').select('etsy_order_id, sku_id').execute()
print('\n订单 sku_id:')
for o in orders.data:
    print(f'  {o["etsy_order_id"]} -> sku_id: {o["sku_id"]}')

# 检查 Storage 中的图片文件
print('\nStorage assets bucket 根目录:')
try:
    files = supabase.storage.from_('assets').list()
    if isinstance(files, list):
        for f in files[:20]:
            print(f'  {f["name"]} (type: {f.get("id", "folder")})')
    else:
        print(f'  返回类型异常: {type(files)}')
except Exception as e:
    print(f'  错误: {e}')

# 确认 B-G01B.jpg 的公开访问URL
SUPABASE_URL = env['SUPABASE_URL']
target_url = f"{SUPABASE_URL}/storage/v1/object/public/assets/photos/large/B-G01B.jpg"
print(f'\nB-G01B 图片预期 URL:')
print(f'  {target_url}')

# 检查图片是否存在
print('\n尝试获取图片信息...')
try:
    # 使用 getPublicUrl 方式
    url_data = supabase.storage.from_('assets').get_public_url('photos/large/B-G01B.jpg')
    print(f'  get_public_url 返回: {url_data}')
except Exception as e:
    print(f'  获取URL失败: {e}')

