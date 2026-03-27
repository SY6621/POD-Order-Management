# -*- coding: utf-8 -*-
"""
插入测试店铺数据
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.database_service import db

def seed_test_shops():
    """插入测试店铺"""
    
    test_shops = [
        {
            'code': 'us',
            'name': '美国店铺',
            'region': 'North America',
            'status': 'active',
            'service_token': 'abc123xyz789',
            'service_link_enabled': True,
            'design_token': 'dsg_us_001',
            'design_link_enabled': True
        },
        {
            'code': 'eu',
            'name': '欧洲店铺',
            'region': 'Europe',
            'status': 'active',
            'service_token': 'def456uvw012',
            'service_link_enabled': True,
            'design_token': None,
            'design_link_enabled': False
        },
        {
            'code': 'asia',
            'name': '亚洲店铺',
            'region': 'Asia',
            'status': 'active',
            'service_token': None,
            'service_link_enabled': False,
            'design_token': None,
            'design_link_enabled': False
        }
    ]
    
    print("=" * 60)
    print("插入测试店铺数据")
    print("=" * 60)
    
    for shop in test_shops:
        try:
            # 检查是否已存在
            existing = db.supabase.table('shops').select('id').eq('code', shop['code']).execute()
            if existing.data:
                print(f"⚠️  店铺 {shop['code']} 已存在，跳过")
                continue
            
            # 插入店铺
            result = db.supabase.table('shops').insert(shop).execute()
            if result.data:
                print(f"✅ 店铺 {shop['code']} 插入成功，ID: {result.data[0]['id']}")
            else:
                print(f"❌ 店铺 {shop['code']} 插入失败")
        except Exception as e:
            print(f"❌ 店铺 {shop['code']} 插入失败: {e}")
    
    print("=" * 60)
    
    # 显示所有店铺
    print("\n当前店铺列表：")
    result = db.supabase.table('shops').select('id,code,name,design_link_enabled').execute()
    for shop in result.data or []:
        print(f"  - {shop['code']}: {shop['name']} (设计链接: {'已启用' if shop.get('design_link_enabled') else '未启用'})")

if __name__ == '__main__':
    seed_test_shops()
