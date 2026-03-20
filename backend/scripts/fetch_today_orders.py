"""
获取今天的 Etsy 订单邮件并解析
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import email
from email.header import decode_header
from datetime import datetime, timedelta
from imapclient import IMAPClient
from src.config.settings import settings
from src.services.email_parser import EtsyEmailParser


def decode_quoted_printable(content: bytes) -> str:
    """解码 quoted-printable 编码的内容"""
    try:
        # 尝试 UTF-8
        return content.decode('utf-8', errors='ignore')
    except:
        try:
            return content.decode('iso-8859-1', errors='ignore')
        except:
            return content.decode('ascii', errors='ignore')


def fetch_today_orders():
    """获取今天的 Etsy 订单"""
    print("=" * 70)
    print("获取今天的 Etsy 订单")
    print("=" * 70)
    
    # 连接邮箱
    server = settings.IMAP_SERVER
    email_addr = settings.EMAIL_ADDRESS
    password = settings.EMAIL_PASSWORD
    
    print(f"\n连接邮箱: {email_addr}")
    
    try:
        client = IMAPClient(server, port=993, ssl=True)
        client.login(email_addr, password)
        print("✅ 邮箱连接成功")
        
        client.select_folder("INBOX")
        
        # 搜索今天的未读邮件
        today = datetime.now().strftime("%d-%b-%Y")
        print(f"\n搜索今天的邮件 (日期: {today})")
        
        # 搜索未读邮件
        messages = client.search([
            "UNSEEN",
            "SINCE", today
        ])
        
        print(f"找到 {len(messages)} 封今天的未读邮件")
        
        parser = EtsyEmailParser()
        orders = []
        
        for msg_id in messages:
            try:
                # 获取邮件内容
                raw = client.fetch([msg_id], ["RFC822"])
                if msg_id not in raw:
                    continue
                
                raw_email = raw[msg_id][b"RFC822"]
                msg = email.message_from_bytes(raw_email)
                
                # 获取主题
                subject = ""
                if msg["Subject"]:
                    decoded_parts = decode_header(msg["Subject"])
                    for content, charset in decoded_parts:
                        if isinstance(content, bytes):
                            subject += content.decode(charset or 'utf-8', errors='ignore')
                        else:
                            subject += content
                
                # 获取发件人
                from_addr = msg.get("From", "")
                
                print(f"\n{'='*70}")
                print(f"邮件 ID: {msg_id}")
                print(f"主题: {subject}")
                print(f"发件人: {from_addr}")
                print(f"{'='*70}")
                
                # 获取邮件正文
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        if ctype == "text/plain":
                            payload = part.get_payload(decode=True)
                            charset = part.get_content_charset() or "utf-8"
                            body = decode_quoted_printable(payload)
                            break
                        elif ctype == "text/html" and not body:
                            payload = part.get_payload(decode=True)
                            charset = part.get_content_charset() or "utf-8"
                            body = decode_quoted_printable(payload)
                else:
                    payload = msg.get_payload(decode=True)
                    charset = msg.get_content_charset() or "utf-8"
                    body = decode_quoted_printable(payload)
                
                # 检查是否是 Etsy 订单邮件
                if "Etsy" in subject or "etsy" in from_addr.lower():
                    print("✅ 是 Etsy 邮件，开始解析...")
                    
                    # 调试：检查订单号匹配
                    import re
                    order_patterns = [
                        r"Your order number is:?\s*(\d+)",
                        r"Order\s*#(\d+)",
                        r"orders/(\d+)"
                    ]
                    for pattern in order_patterns:
                        m = re.search(pattern, body)
                        if m:
                            print(f"   找到订单号: {m.group(1)} (匹配模式: {pattern})")
                    
                    # 检查 Delivery address
                    if "Delivery address" in body:
                        print("   找到 Delivery address")
                    else:
                        print("   未找到 Delivery address")
                    
                    # 解析订单
                    parsed_order = parser.parse(body)
                    if parsed_order and parsed_order.etsy_order_id:
                        order_data = {
                            "order_id": parsed_order.etsy_order_id,
                            "customer_name": parsed_order.customer_name,
                            "customer_username": parsed_order.customer_username,
                            "shipping_name": parsed_order.shipping_name,
                            "shipping_address_line1": parsed_order.shipping_address_line1,
                            "shipping_address_line2": parsed_order.shipping_address_line2,
                            "shipping_city": parsed_order.shipping_city,
                            "shipping_state": parsed_order.shipping_state,
                            "shipping_zip": parsed_order.shipping_zip,
                            "shipping_country": parsed_order.shipping_country,
                            "order_total": parsed_order.order_total,
                            "currency": parsed_order.currency,
                            "items": [
                                {
                                    "product_name": item.product_name,
                                    "quantity": item.quantity,
                                    "personalization": item.personalization,
                                    "font_code": item.font_code,
                                    "front_text": item.front_text,
                                    "back_text": item.back_text,
                                    "shape": item.shape,
                                    "color": item.color,
                                    "size": item.size
                                }
                                for item in parsed_order.items
                            ]
                        }
                        orders.append(order_data)
                        print(f"✅ 解析订单成功!")
                        print(f"   订单号: {order_data['order_id']}")
                        print(f"   客户: {order_data['customer_name']}")
                        print(f"   地址: {order_data['shipping_address_line1']}, {order_data['shipping_city']}")
                        print(f"   国家: {order_data['shipping_country']}")
                        if order_data['items']:
                            print(f"   产品: {order_data['items'][0]['product_name']}")
                    else:
                        print("⚠️ 无法解析订单数据")
                        # 打印部分正文用于调试
                        print(f"\n正文预览 (前500字符):")
                        print(body[:500])
                else:
                    print("⏭️  不是 Etsy 邮件，跳过")
                    
            except Exception as e:
                print(f"❌ 处理邮件 ID={msg_id} 失败: {e}")
                import traceback
                traceback.print_exc()
        
        # 打印完整邮件内容用于调试
        if messages:
            print("\n" + "=" * 70)
            print("完整邮件内容 (用于调试):")
            print("=" * 70)
            msg_id = messages[0]
            raw = client.fetch([msg_id], ["RFC822"])
            raw_email = raw[msg_id][b"RFC822"]
            msg = email.message_from_bytes(raw_email)
            
            body_full = ""
            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    if ctype == "text/plain":
                        payload = part.get_payload(decode=True)
                        body_full = decode_quoted_printable(payload)
                        break
                    elif ctype == "text/html" and not body_full:
                        payload = part.get_payload(decode=True)
                        body_full = decode_quoted_printable(payload)
            else:
                payload = msg.get_payload(decode=True)
                body_full = decode_quoted_printable(payload)
            
            print(body_full[:2000])
        
        client.logout()
        print("\n" + "=" * 70)
        print(f"共找到 {len(orders)} 个订单")
        print("=" * 70)
        
        return orders
        
    except Exception as e:
        print(f"❌ 邮箱操作失败: {e}")
        import traceback
        traceback.print_exc()
        return []


if __name__ == "__main__":
    orders = fetch_today_orders()
    
    if orders:
        print("\n订单详情:")
        for i, order in enumerate(orders, 1):
            print(f"\n【订单 {i}】")
            print(f"  订单号: {order['order_id']}")
            print(f"  客户: {order['customer_name']}")
            print(f"  地址: {order['shipping_address_line1']}")
            print(f"  城市: {order['shipping_city']}, {order['shipping_state']}")
            print(f"  邮编: {order['shipping_zip']}")
            print(f"  国家: {order['shipping_country']}")
            if order['items']:
                item = order['items'][0]
                print(f"  产品: {item['product_name']}")
                print(f"  定制: {item['personalization'][:50]}..." if item['personalization'] else "  定制: 无")
