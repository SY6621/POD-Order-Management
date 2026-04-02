# -*- coding: utf-8 -*-
"""
店铺初始化脚本 - 澳洲01店
创建店铺、生成Token、关联订单、验证连通性

注意：如果需要 shop_email 和 account_holder 字段，需先执行以下SQL：
    ALTER TABLE shops ADD COLUMN shop_email VARCHAR(255);
    ALTER TABLE shops ADD COLUMN account_holder VARCHAR(100);
"""
import os
import sys
import secrets
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.database_service import db


def init_shop_au01():
    """初始化澳洲01店"""
    
    print("=" * 60)
    print("🏪 店铺初始化 - 澳洲01店")
    print("=" * 60)
    
    # 1. 查看shops表结构
    print("\n📋 Step 1: 查看shops表结构...")
    try:
        existing_shop = db.supabase.table('shops').select('*').limit(1).execute()
        if existing_shop.data:
            sample_fields = list(existing_shop.data[0].keys())
            print(f"   当前字段: {', '.join(sample_fields)}")
            
            # 检查是否有 shop_email 和 account_holder 字段
            has_shop_email = 'shop_email' in sample_fields
            has_account_holder = 'account_holder' in sample_fields
            print(f"   shop_email字段: {'✅ 存在' if has_shop_email else '❌ 不存在'}")
            print(f"   account_holder字段: {'✅ 存在' if has_account_holder else '❌ 不存在'}")
        else:
            print("   shops表为空，将创建新记录")
            has_shop_email = False
            has_account_holder = False
    except Exception as e:
        print(f"   ⚠️ 查询失败: {e}")
        has_shop_email = False
        has_account_holder = False
    
    # 2. 检查店铺是否已存在
    print("\n📋 Step 2: 检查店铺是否已存在...")
    shop_code = 'au01'
    existing = db.supabase.table('shops').select('*').eq('code', shop_code).execute()
    
    if existing.data:
        shop = existing.data[0]
        shop_id = shop['id']
        is_new = False
        print(f"   ⚠️ 店铺已存在: {shop['name']} (ID: {shop_id})")
        
        # 检查是否已有Token，有则复用
        service_token = shop.get('service_token')
        design_token = shop.get('design_token')
        
        if service_token and design_token:
            print(f"   ✅ 已有Token，将复用（防止旧链接失效）")
        else:
            print(f"   ⚠️ Token缺失，将生成新Token")
            service_token = secrets.token_urlsafe(32)
            design_token = secrets.token_urlsafe(32)
        
        # 更新店铺信息（如果新字段存在）
        print("\n📋 Step 3: 更新店铺信息...")
        update_data = {}
        
        # 只有字段存在时才更新
        if has_shop_email:
            update_data['shop_email'] = 'yangqingssheng@gmail.com'
        if has_account_holder:
            update_data['account_holder'] = 'qingsheng yang'
        
        # 补充缺失的Token
        if not shop.get('service_token'):
            update_data['service_token'] = service_token
            update_data['service_link_enabled'] = True
            update_data['service_link_created_at'] = datetime.utcnow().isoformat()
        if not shop.get('design_token'):
            update_data['design_token'] = design_token
            update_data['design_link_enabled'] = True
            update_data['design_link_created_at'] = datetime.utcnow().isoformat()
        
        if update_data:
            update_data['service_link_updated_at'] = datetime.utcnow().isoformat()
            update_data['design_link_updated_at'] = datetime.utcnow().isoformat()
            
            try:
                result = db.supabase.table('shops').update(update_data).eq('id', shop_id).execute()
                if result.data:
                    print(f"   ✅ 店铺信息更新成功")
                    shop = result.data[0]
                else:
                    print(f"   ⚠️ 更新无返回数据")
            except Exception as e:
                print(f"   ⚠️ 更新失败（可能字段不存在）: {e}")
        else:
            print("   ℹ️ 无需更新")
    else:
        # 3. 创建新店铺
        print("\n📋 Step 3: 创建新店铺...")
        
        # 生成安全Token
        service_token = secrets.token_urlsafe(32)
        design_token = secrets.token_urlsafe(32)
        now = datetime.utcnow().isoformat()
        
        new_shop = {
            'name': '澳洲01店',
            'code': shop_code,
            'region': 'AU',
            'status': 'active',
            'operator': 'A',
            'service_token': service_token,
            'service_link_enabled': True,
            'service_link_created_at': now,
            'service_link_updated_at': now,
            'design_token': design_token,
            'design_link_enabled': True,
            'design_link_created_at': now,
            'design_link_updated_at': now,
        }
        
        # 如果字段存在则添加
        if has_shop_email:
            new_shop['shop_email'] = 'yangqingssheng@gmail.com'
        if has_account_holder:
            new_shop['account_holder'] = 'qingsheng yang'
        
        try:
            result = db.supabase.table('shops').insert(new_shop).execute()
            if result.data:
                shop = result.data[0]
                shop_id = shop['id']
                is_new = True
                print(f"   ✅ 店铺创建成功!")
                print(f"      ID: {shop_id}")
                print(f"      名称: {shop['name']}")
                print(f"      代码: {shop['code']}")
            else:
                print("   ❌ 店铺创建失败：无返回数据")
                return
        except Exception as e:
            print(f"   ❌ 店铺创建失败: {e}")
            return
    
    # 4. 获取Token信息
    print("\n📋 Step 4: 获取Token信息...")
    shop_full = db.supabase.table('shops').select('*').eq('id', shop_id).single().execute()
    
    if not shop_full.data:
        print("   ❌ 无法获取店铺完整信息")
        return
    
    shop_data = shop_full.data
    service_token = shop_data.get('service_token')
    design_token = shop_data.get('design_token')
    
    print(f"   service_token: {service_token}")
    print(f"   design_token: {design_token}")
    
    # 5. 关联pending订单
    print("\n📋 Step 5: 关联pending状态订单...")
    pending_orders = db.supabase.table('orders').select('id, etsy_order_id, shop_id').eq('status', 'pending').execute()
    
    orders_to_update = []
    already_linked = []
    
    if pending_orders.data:
        for order in pending_orders.data:
            if order.get('shop_id') is None:
                orders_to_update.append(order)
            elif order.get('shop_id') == shop_id:
                already_linked.append(order)
            # 其他店铺的订单不处理
        
        if orders_to_update:
            order_ids = [o['id'] for o in orders_to_update]
            # 批量更新
            update_result = db.supabase.table('orders').update({'shop_id': shop_id}).in_('id', order_ids).execute()
            print(f"   ✅ 已关联 {len(orders_to_update)} 个订单到澳洲01店")
            for o in orders_to_update:
                print(f"      - 订单号: {o.get('etsy_order_id', o['id'])}")
        else:
            print("   ℹ️ 没有待关联的pending订单")
        
        if already_linked:
            print(f"   ℹ️ 已有 {len(already_linked)} 个订单关联到此店铺")
    else:
        print("   ℹ️ 当前没有pending状态的订单")
    
    # 6. 验证连通性
    print("\n📋 Step 6: 验证连通性...")
    verify_shop = db.supabase.table('shops').select('id, code, service_token, design_token').eq('id', shop_id).single().execute()
    if verify_shop.data:
        print("   ✅ 数据库连接正常")
        print("   ✅ 店铺数据验证通过")
    else:
        print("   ❌ 验证失败")
        return
    
    # 7. 打印最终结果
    print("\n" + "=" * 60)
    print("📊 初始化完成 - 结果汇总")
    print("=" * 60)
    
    print(f"\n🏪 店铺完整信息:")
    print(f"   ID: {shop_id}")
    print(f"   名称: {shop_data.get('name')}")
    print(f"   代码: {shop_data.get('code')}")
    print(f"   区域: {shop_data.get('region')}")
    print(f"   状态: {shop_data.get('status')}")
    print(f"   店铺邮箱: {shop_data.get('shop_email', '(字段不存在)')}")
    print(f"   账号持有人: {shop_data.get('account_holder', '(字段不存在)')}")
    print(f"   国旗: {shop_data.get('flag_emoji', 'N/A')}")
    print(f"   创建时间: {shop_data.get('created_at', 'N/A')}")
    
    print(f"\n🔑 Token值:")
    print(f"   service_token: {service_token}")
    print(f"   design_token: {design_token}")
    
    print(f"\n🌐 外链完整URL:")
    print(f"   沟通链接: /service/{shop_code}?token={service_token}")
    print(f"   设计链接: /design/{shop_code}?token={design_token}")
    
    # 统计关联订单
    linked_orders = db.supabase.table('orders').select('id, etsy_order_id, status').eq('shop_id', shop_id).execute()
    print(f"\n📦 已关联订单列表:")
    if linked_orders.data:
        print(f"   总数: {len(linked_orders.data)} 个")
        for o in linked_orders.data:
            print(f"   - 订单号: {o.get('etsy_order_id', o['id'])} (状态: {o.get('status', 'N/A')})")
    else:
        print("   总数: 0 个")
    
    # 提示需要添加字段
    if not has_shop_email or not has_account_holder:
        print(f"\n⚠️ 提示: 需要添加以下字段才能存储店铺邮箱和账号持有人:")
        if not has_shop_email:
            print("   ALTER TABLE shops ADD COLUMN shop_email VARCHAR(255);")
        if not has_account_holder:
            print("   ALTER TABLE shops ADD COLUMN account_holder VARCHAR(100);")
    
    print("\n" + "=" * 60)
    print("✅ 店铺初始化完成!")
    print("=" * 60)
    
    return shop_data


if __name__ == '__main__':
    init_shop_au01()
