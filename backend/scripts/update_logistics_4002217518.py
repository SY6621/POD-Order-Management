# -*- coding: utf-8 -*-
"""
更新订单 4002217518 的物流信息
"""

from supabase import create_client
import os

def load_env_from_file():
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

env_vars = load_env_from_file()
url = env_vars.get('SUPABASE_URL')
key = env_vars.get('SUPABASE_KEY')
supabase = create_client(url, key)

def update_logistics():
    """更新物流信息"""
    
    print("=" * 70)
    print("更新订单 4002217518 物流信息")
    print("=" * 70)
    
    # 查找订单
    order_result = supabase.table('orders').select('*').eq('etsy_order_id', '4002217518').execute()
    if not order_result.data:
        print("❌ 未找到订单 4002217518")
        return
    
    order_id = order_result.data[0]['id']
    print(f"✅ 找到订单 ID: {order_id}")
    
    # 更新物流记录
    logistics_data = {
        "tracking_number": "7559932026031800004261",
    }
    
    result = supabase.table('logistics').update(logistics_data).eq('order_id', order_id).execute()
    if result.data:
        print("✅ 物流信息更新成功")
        print(f"  快递单号: 7559932026031800004261")
        print(f"  渠道: 美国联邮通优先挂号-普货(PX)")
        print(f"  重量: 0.03kg")
    else:
        print("❌ 物流信息更新失败")

if __name__ == "__main__":
    update_logistics()
