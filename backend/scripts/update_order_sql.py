# -*- coding: utf-8 -*-
"""
使用Supabase直接更新订单数据（绕过Python模块导入问题）
"""

from supabase import create_client
import os

def load_env_from_file():
    """从.env文件加载环境变量"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip().strip('"').strip("'")
    return env_vars

# 加载环境变量
env_vars = load_env_from_file()
url = env_vars.get('SUPABASE_URL') or os.getenv('SUPABASE_URL')
key = env_vars.get('SUPABASE_KEY') or os.getenv('SUPABASE_KEY') or env_vars.get('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_SERVICE_KEY')
supabase = create_client(url, key)

def update_order():
    """更新订单数据"""
    
    print("=" * 60)
    print("更新订单数据为真实订单")
    print("=" * 60)
    
    # 先检查真实订单 3891559803 是否已存在
    print("\n【步骤0】检查真实订单是否已存在...")
    real_order_result = supabase.table('orders').select('*').eq('etsy_order_id', '3891559803').execute()
    
    if real_order_result.data:
        print(f"✅ 真实订单 3891559803 已存在!")
        order = real_order_result.data[0]
        order_id = order['id']
        print(f"  订单ID: {order_id}")
        print(f"  当前状态: {order.get('status')}")
        use_existing = True
    else:
        print("真实订单不存在，将更新测试订单 PO-202602-103")
        use_existing = False
        # 查找订单 PO-202602-103
        print("\n【步骤1】查找测试订单...")
        result = supabase.table('orders').select('*').ilike('etsy_order_id', '%PO-202602-103%').execute()
        
        if not result.data:
            print("❌ 未找到订单 PO-202602-103")
            return
        
        order = result.data[0]
        order_id = order['id']
        print(f"✅ 找到测试订单 ID: {order_id}")
    
    # 2. 更新订单基础数据（仅当使用测试订单时才更新基础信息）
    if not use_existing:
        print("\n【步骤2】更新订单基础数据...")
        order_update = {
            "etsy_order_id": "3891559803",
            "customer_name": "Demi Brooker",
            "front_text": "Spirit",
            "back_text": "0402 830 481",
            "font_code": "F-04",
            "quantity": 1,
            "total_amount": 34.46,
        }
        
        result = supabase.table('orders').update(order_update).eq('id', order_id).execute()
        if result.data:
            print("✅ 订单基础数据更新成功")
        else:
            print("❌ 订单更新失败")
            return
    else:
        print("\n【步骤2】跳过基础数据更新（使用已存在的真实订单）")
    
    # 3. 查找SKU映射 (心形/金色/L)
    print("\n【步骤3】查找SKU映射...")
    sku_result = supabase.table('sku_mapping').select('*').eq('shape', '心形').eq('color', '金色').eq('size', 'L').execute()
    
    if sku_result.data:
        sku = sku_result.data[0]
        print(f"✅ 找到SKU: {sku['sku_code']} (ID: {sku['id']})")
        
        # 更新订单的sku_id
        supabase.table('orders').update({"sku_id": sku['id']}).eq('id', order_id).execute()
        print("✅ 已关联SKU到订单")
    else:
        print("⚠️ 未找到匹配的SKU (Heart/Gold/Large)")
        # 显示所有SKU
        all_skus = supabase.table('sku_mapping').select('sku_code, shape, color, size').limit(10).execute()
        print("\n可用SKU列表:")
        for s in all_skus.data:
            print(f"  - {s['sku_code']}: {s['shape']}/{s['color']}/{s['size']}")
    
    # 4. 创建/更新物流记录
    print("\n【步骤4】创建物流记录...")
    logistics_data = {
        "order_id": order_id,
        "recipient_name": "Demi Brooker",
        "street_address": "3/1A Salisbury Rd",
        "city": "ROSE BAY",
        "state_code": "NSW",
        "postal_code": "2029",
        "country": "Australia",
        "tracking_number": "TEST3891559803",
    }
    
    # 检查是否已有物流记录
    existing = supabase.table('logistics').select('*').eq('order_id', order_id).execute()
    if existing.data:
        supabase.table('logistics').update(logistics_data).eq('order_id', order_id).execute()
        print("✅ 物流记录已更新")
    else:
        supabase.table('logistics').insert(logistics_data).execute()
        print("✅ 物流记录已创建")
    
    # 5. 创建/更新生产文档记录
    print("\n【步骤5】创建生产文档记录...")
    prod_doc_data = {
        "order_id": order_id,
        "effect_svg_url": "https://rtuzqnoztrdvhfnndqjv.supabase.co/storage/v1/object/public/effects/3891559803.svg",
        "effect_jpg_url": "https://rtuzqnoztrdvhfnndqjv.supabase.co/storage/v1/object/public/effects/3891559803.jpg",
        "real_photo_urls": "https://rtuzqnoztrdvhfnndqjv.supabase.co/storage/v1/object/public/photos/heart_gold_large_01.jpg",
    }
    
    existing_doc = supabase.table('production_documents').select('*').eq('order_id', order_id).execute()
    if existing_doc.data:
        supabase.table('production_documents').update(prod_doc_data).eq('order_id', order_id).execute()
        print("✅ 生产文档记录已更新")
    else:
        supabase.table('production_documents').insert(prod_doc_data).execute()
        print("✅ 生产文档记录已创建")
    
    print("\n" + "=" * 60)
    print("订单数据更新完成!")
    print("=" * 60)
    print(f"订单ID: {order_id}")
    print(f"Etsy订单号: 3891559803")
    print(f"客户: Demi Brooker")
    print(f"正面文字: Spirit (F-04)")
    print(f"背面文字: 0402 830 481")
    print(f"产品: Heart/Gold/Large")
    print(f"物流: 3/1A Salisbury Rd, ROSE BAY NSW 2029, Australia")
    print("\n请刷新页面并重新生成PDF测试!")

if __name__ == "__main__":
    update_order()
