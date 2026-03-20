# -*- coding: utf-8 -*-
"""
从QQ邮箱抓取新订单邮件
订单号: 4002217518
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

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
os.environ['SUPABASE_URL'] = env_vars.get('SUPABASE_URL', '')
os.environ['SUPABASE_KEY'] = env_vars.get('SUPABASE_KEY', '')
os.environ['IMAP_SERVER'] = env_vars.get('IMAP_SERVER', 'imap.qq.com')
os.environ['IMAP_PORT'] = env_vars.get('IMAP_PORT', '993')
os.environ['EMAIL_ADDRESS'] = env_vars.get('EMAIL_ADDRESS', '')
os.environ['EMAIL_PASSWORD'] = env_vars.get('EMAIL_PASSWORD', '')

from services.email_service import EmailService
from services.email_parser import parse_etsy_email
from services.order_service import order_service

def fetch_and_process_order(target_order_id="4002217518"):
    """抓取并处理指定订单"""
    
    print("=" * 70)
    print(f"抓取订单邮件: {target_order_id}")
    print("=" * 70)
    
    # 连接邮箱
    email_service = EmailService()
    if not email_service.connect():
        print("❌ 邮箱连接失败")
        return
    
    try:
        # 搜索最近7天的Etsy邮件
        print("\n搜索最近7天的Etsy订单邮件...")
        message_ids = email_service.search_all_unread_etsy_orders()
        
        if not message_ids:
            print("❌ 未找到任何Etsy订单邮件")
            return
        
        print(f"找到 {len(message_ids)} 封Etsy邮件")
        
        # 遍历邮件查找目标订单
        found_order = None
        for msg_id in message_ids:
            print(f"\n检查邮件 ID: {msg_id}")
            
            # 获取邮件内容
            email_data = email_service.fetch_email_content(msg_id)
            if not email_data:
                continue
            
            # 检查邮件主题或内容是否包含目标订单号
            subject = email_data.get('subject', '')
            body = email_data.get('body', '')
            
            if target_order_id in subject or target_order_id in body:
                print(f"✅ 找到目标订单邮件!")
                print(f"  主题: {subject}")
                
                # 解析邮件
                parsed_order = parse_etsy_email(body)
                if parsed_order:
                    print(f"\n解析结果:")
                    print(f"  Etsy订单号: {parsed_order.etsy_order_id}")
                    print(f"  客户: {parsed_order.customer_name}")
                    print(f"  收件人: {parsed_order.shipping_name}")
                    print(f"  地址: {parsed_order.shipping_address_line1}, {parsed_order.shipping_city} {parsed_order.shipping_state} {parsed_order.shipping_zip}, {parsed_order.shipping_country}")
                    
                    if parsed_order.items:
                        item = parsed_order.items[0]
                        print(f"\n  产品信息:")
                        print(f"    名称: {item.product_name}")
                        print(f"    形状: {item.shape}")
                        print(f"    颜色: {item.color}")
                        print(f"    尺寸: {item.size}")
                        print(f"    正面: {item.customization_front}")
                        print(f"    背面: {item.customization_back}")
                        print(f"    字体: {item.font_code}")
                    
                    found_order = parsed_order
                    
                    # 保存到数据库
                    print(f"\n保存到数据库...")
                    result = order_service.process_parsed_order(parsed_order)
                    if result:
                        print(f"✅ 订单已保存到数据库")
                        print(f"  数据库ID: {result.get('id')}")
                    else:
                        print(f"❌ 保存失败")
                    
                    break
        
        if not found_order:
            print(f"\n❌ 未找到订单 {target_order_id} 的邮件")
            print("请确认:")
            print("1. 邮件是否已到达QQ邮箱")
            print("2. 邮件是否标记为未读")
            print("3. 订单号是否正确")
            
    finally:
        email_service.disconnect()

if __name__ == "__main__":
    fetch_and_process_order("4002217518")
