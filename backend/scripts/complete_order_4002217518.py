# -*- coding: utf-8 -*-
"""
将订单 4002217518 改为 completed 状态
并创建 production_documents 记录
"""

from supabase import create_client
import os
from datetime import datetime

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

def complete_order():
    """完成订单并创建生产文档记录"""
    
    print("=" * 70)
    print("将订单 4002217518 标记为已完成")
    print("=" * 70)
    
    # 1. 查找订单
    result = supabase.table('orders').select('*').eq('etsy_order_id', '4002217518').execute()
    if not result.data:
        print("❌ 未找到订单")
        return
    
    order = result.data[0]
    order_id = order['id']
    print(f"✅ 找到订单: {order_id}")
    print(f"   客户: {order['customer_name']}")
    print(f"   当前状态: {order['status']}")
    
    # 2. 更新订单状态为 delivered（数据库允许的值为: confirmed, delivered, effect_sent, producing）
    update_result = supabase.table('orders').update({
        'status': 'delivered',
        'updated_at': datetime.now().isoformat()
    }).eq('id', order_id).execute()
    
    if update_result.data:
        print(f"✅ 订单状态已更新为: delivered")
    else:
        print(f"❌ 订单状态更新失败")
        return
    
    # 3. 检查是否已有 production_documents 记录
    prod_check = supabase.table('production_documents').select('*').eq('order_id', order_id).execute()
    
    if prod_check.data:
        print(f"✅ 生产文档记录已存在")
        doc = prod_check.data[0]
        print(f"   效果图SVG: {doc.get('effect_svg_url', '无')}")
    else:
        # 创建空的 production_documents 记录
        # 注意：实际使用时需要填入真实的效果图SVG URL
        insert_result = supabase.table('production_documents').insert({
            'order_id': order_id,
            'effect_svg_url': '',  # 暂时为空，需要设计器生成后填入
            'effect_jpg_url': '',
            'real_photo_urls': '',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }).execute()
        
        if insert_result.data:
            print(f"✅ 生产文档记录已创建（效果图URL为空，需设计器生成）")
        else:
            print(f"⚠️ 生产文档记录创建失败")
    
    print("\n" + "=" * 70)
    print("订单现在可以在【已完成订单】页面查看（delivered状态）")
    print("请刷新前端页面测试生产文档PDF生成功能")
    print("=" * 70)

if __name__ == "__main__":
    complete_order()
