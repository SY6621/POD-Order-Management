# -*- coding: utf-8 -*-
"""
手动插入订单 4002217518 到数据库
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
url = env_vars.get('SUPABASE_URL')
key = env_vars.get('SUPABASE_KEY')
supabase = create_client(url, key)

def insert_order():
    """插入订单 4002217518"""
    
    print("=" * 70)
    print("插入订单 4002217518")
    print("=" * 70)
    
    # 检查订单是否已存在
    existing = supabase.table('orders').select('*').eq('etsy_order_id', '4002217518').execute()
    if existing.data:
        print(f"⚠️ 订单 4002217518 已存在!")
        order_id = existing.data[0]['id']
        print(f"  订单ID: {order_id}")
    else:
        # 查找匹配的SKU (心形/金色/L)
        print("\n查找SKU映射...")
        sku_result = supabase.table('sku_mapping').select('*').eq('shape', '心形').eq('color', '金色').eq('size', 'L').execute()
        
        sku_id = None
        if sku_result.data:
            sku_id = sku_result.data[0]['id']
            print(f"✅ 找到SKU: {sku_result.data[0]['sku_code']} (ID: {sku_id})")
        else:
            print("⚠️ 未找到匹配的SKU，将使用第一个可用SKU")
            first_sku = supabase.table('sku_mapping').select('*').limit(1).execute()
            if first_sku.data:
                sku_id = first_sku.data[0]['id']
                print(f"  使用SKU: {first_sku.data[0]['sku_code']}")
        
        # 插入订单
        print("\n插入订单数据...")
        order_data = {
            "etsy_order_id": "4002217518",
            "customer_name": "Jessica Head",
            "customer_email": "",
            "front_text": "",  # 需要在待确认订单页面使用设计器生成
            "back_text": "",
            "font_code": "",
            "quantity": 1,
            "total_amount": 34.46,
            "status": "pending",  # 待处理状态
            "sku_id": sku_id,
            "created_at": "2026-03-16T00:00:00",
        }
        
        result = supabase.table('orders').insert(order_data).execute()
        if result.data:
            order_id = result.data[0]['id']
            print(f"✅ 订单插入成功!")
            print(f"  订单ID: {order_id}")
        else:
            print("❌ 订单插入失败")
            return
    
    # 插入物流记录
    print("\n插入物流记录...")
    logistics_data = {
        "order_id": order_id,
        "recipient_name": "Jessica Head",
        "street_address": "26 Yodalla Ave",
        "city": "EMU PLAINS",
        "state_code": "NSW",
        "postal_code": "2750",
        "country": "Australia",
        "tracking_number": "",  # 等待手动创建物流后更新
    }
    
    existing_logistics = supabase.table('logistics').select('*').eq('order_id', order_id).execute()
    if existing_logistics.data:
        supabase.table('logistics').update(logistics_data).eq('order_id', order_id).execute()
        print("✅ 物流记录已更新")
    else:
        supabase.table('logistics').insert(logistics_data).execute()
        print("✅ 物流记录已创建")
    
    print("\n" + "=" * 70)
    print("订单 4002217518 数据准备完成!")
    print("=" * 70)
    print(f"订单ID: {order_id}")
    print(f"Etsy订单号: 4002217518")
    print(f"客户: Jessica Head")
    print(f"地址: 26 Yodalla Ave, EMU PLAINS NSW 2750, Australia")
    print(f"状态: pending_review (待确认)")
    print("\n下一步:")
    print("1. 在【待确认订单】页面找到此订单")
    print("2. 使用设计器生成效果图")
    print("3. 手动创建物流运单（渠道: 美国联邮通优先挂号-普货(PX), 重量: 0.03kg）")
    print("4. 将面单PDF和快递单号提供给我")

if __name__ == "__main__":
    insert_order()
