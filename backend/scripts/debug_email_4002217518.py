# -*- coding: utf-8 -*-
"""调试邮件 4002217518 的完整内容"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.email_service import email_service
from src.services.email_parser import email_parser

print("=" * 70)
print("调试邮件 4002217518 内容")
print("=" * 70)

if not email_service.connect():
    print("❌ 邮箱连接失败")
    sys.exit(1)

try:
    # 搜索邮件
    email_service.client.select_folder("INBOX")
    messages = email_service.client.search([
        "SUBJECT", "4002217518"
    ])
    
    if not messages:
        print("❌ 未找到邮件")
    else:
        for msg_id in messages:
            print(f"\n邮件 ID: {msg_id}")
            print("-" * 70)
            
            # 获取完整内容
            email_data = email_service.fetch_email_content(msg_id)
            if email_data:
                print(f"主题: {email_data['subject']}")
                print(f"发件人: {email_data['from']}")
                print("\n【正文内容】")
                print(email_data['body'])
                print("\n" + "=" * 70)
                
                # 尝试解析
                order = email_parser.parse_forwarded_email(email_data['body'])
                if order:
                    print(f"\n【解析结果】")
                    print(f"  订单号: {order.etsy_order_id}")
                    print(f"  客户名: {order.customer_name}")
                    print(f"  收货人: {order.shipping_name}")
                    print(f"  地址1: {order.shipping_address_line1}")
                    print(f"  地址2: {order.shipping_address_line2}")
                    print(f"  城市: {order.shipping_city}")
                    print(f"  州/省: {order.shipping_state}")
                    print(f"  邮编: {order.shipping_zip}")
                    print(f"  国家: {order.shipping_country}")
                else:
                    print("\n❌ 解析失败")
            
finally:
    email_service.disconnect()
