# -*- coding: utf-8 -*-
"""
检查订单 4002217518 的状态
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

def check_order():
    """检查订单状态"""
    
    print("=" * 70)
    print("检查订单 4002217518 状态")
    print("=" * 70)
    
    result = supabase.table('orders').select('*').eq('etsy_order_id', '4002217518').execute()
    if not result.data:
        print("❌ 未找到订单")
        return
    
    order = result.data[0]
    print(f"订单ID: {order['id']}")
    print(f"Etsy订单号: {order['etsy_order_id']}")
    print(f"客户: {order['customer_name']}")
    print(f"当前状态: {order['status']}")
    print(f"\n状态说明:")
    print(f"  - new: 新订单")
    print(f"  - pending: 待确认")
    print(f"  - effect_sent: 效果图已发")
    print(f"  - producing: 生产中")
    print(f"  - completed: 已完成")
    print(f"  - delivered: 已送达")
    
    # 检查物流
    logistics = supabase.table('logistics').select('*').eq('order_id', order['id']).execute()
    if logistics.data:
        print(f"\n物流信息:")
        print(f"  快递单号: {logistics.data[0].get('tracking_number', '无')}")
    
    # 检查生产文档
    prod_docs = supabase.table('production_documents').select('*').eq('order_id', order['id']).execute()
    if prod_docs.data:
        print(f"\n生产文档:")
        print(f"  效果图SVG: {prod_docs.data[0].get('effect_svg_url', '无')}")
    else:
        print(f"\n生产文档: 无")

if __name__ == "__main__":
    check_order()
