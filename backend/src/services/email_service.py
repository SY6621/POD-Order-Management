# -*- coding: utf-8 -*-
"""Email service module"""

import email
import smtplib
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from imapclient import IMAPClient
from pathlib import Path

from src.config.settings import settings


def clean_string(s: str) -> str:
    """Remove BOM and non-ASCII characters from string"""
    if not s:
        return ""
    # Remove BOM and strip whitespace
    s = s.replace('\ufeff', '').strip()
    # Ensure ASCII only
    return s.encode('ascii', 'ignore').decode('ascii')


class EmailService:
    """Email service class"""
    
    def __init__(self):
        # Clean all string values to remove hidden characters
        self.server: str = clean_string(settings.IMAP_SERVER)
        self.port: int = settings.IMAP_PORT
        self.email_address: str = clean_string(settings.EMAIL_ADDRESS)
        self.password: str = clean_string(settings.EMAIL_PASSWORD)
        self.client: Optional[IMAPClient] = None
        
        # Debug output
        print(f"[DEBUG] Server: {self.server}")
        print(f"[DEBUG] Email: {self.email_address}")
        print(f"[DEBUG] Password length: {len(self.password)}")
    
    def connect(self) -> bool:
        try:
            self.client = IMAPClient(self.server, port=self.port, ssl=True)
            self.client.login(self.email_address, self.password)
            print("[OK] Email connected: " + self.email_address)
            return True
        except Exception as e:
            print("[ERROR] Email connect failed: " + str(e))
            return False
    
    def disconnect(self):
        if self.client:
            try:
                self.client.logout()
                print("[OK] Email disconnected")
            except Exception:
                pass
            finally:
                self.client = None
    
    def search_today_unread_etsy_orders(self) -> List[int]:
        """搜索当天未读 Etsy 邮件（原始方法，保留兼容）"""
        if not self.client:
            print("[ERROR] Not connected")
            return []
        
        try:
            self.client.select_folder("INBOX")
            today = datetime.now().strftime("%d-%b-%Y")
            
            messages = self.client.search([
                "UNSEEN",
                "SINCE", today,
                "SUBJECT", "Etsy",
            ])
            
            print(f"[INFO] Found {len(messages)} unread Etsy emails today")
            return list(messages)
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            return []

    def search_all_unread_etsy_orders(self) -> List[int]:
        """
        搜索最近 7 天的 Etsy 订单邮件（不限是否已读）
        
        业务逻辑：
          - Etsy 订单邮件原始发件人是 transaction@etsy.com
          - 邮件主题包含 "Etsy Transactions"
          - 邮件正文包含 "transaction@etsy.com" 或 "Your order number is"
        
        优化：在 IMAP 服务器端直接过滤 FROM transaction@etsy.com，减少本地内容读取量
        使用方式：直接运行，会自动搜索最近 7 天的所有 Etsy 订单邮件
        """
        if not self.client:
            print("[ERROR] Not connected")
            return []
        
        try:
            self.client.select_folder("INBOX")
            
            # 第一步：搜索最近 7 天主题包含 "Etsy" 或 "转发" 的所有邮件
            since_date = datetime.now() - timedelta(days=7)
            
            # 优先搜索直接来自 transaction@etsy.com 的订单邮件（服务器端过滤，最准确高效）
            direct_etsy = self.client.search([
                "UNSEEN",
                "SINCE", since_date.strftime("%d-%b-%Y"),
                "FROM", "transaction@etsy.com"
            ])
            
            # 备用：搜索主题含 "Etsy" 的邮件（展容转发场景）
            all_etsy = self.client.search([
                "UNSEEN",
                "SINCE", since_date.strftime("%d-%b-%Y"),
                "SUBJECT", "Etsy"
            ])
            
            # 同时搜索主题含 "Fwd" 或 "Forward" 的邮件（手动转发的订单）
            forwarded_fwd = self.client.search([
                "UNSEEN",
                "SINCE", since_date.strftime("%d-%b-%Y"),
                "SUBJECT", "Fwd"
            ])
            forwarded_forward = self.client.search([
                "UNSEEN",
                "SINCE", since_date.strftime("%d-%b-%Y"),
                "SUBJECT", "Forward"
            ])
            
            # 合并去重（direct_etsy 结果优先，其它为备用兼容）
            all_msgs = list(set(direct_etsy + all_etsy + forwarded_fwd + forwarded_forward))
            print(f"[INFO] 最近 7 天主题含 'Etsy' 或 '转发' 的邮件: {len(all_msgs)} 封（其中直接来自 transaction@etsy.com: {len(direct_etsy)} 封），开始过滤订单邮件...")            
            
            etsy_msg_ids = []
            for msg_id in all_msgs:
                try:
                    # 获取邮件内容（同时获取 TEXT 和 HTML）
                    raw = self.client.fetch([msg_id], ["BODY[TEXT]", "BODY[HTML]"])
                    body_text = raw.get(msg_id, {}).get(b"BODY[TEXT]", b"").decode("utf-8", errors="ignore")[:3000]
                    body_html = raw.get(msg_id, {}).get(b"BODY[HTML]", b"").decode("utf-8", errors="ignore")[:3000]
                    
                    # 合并文本和HTML内容进行检查
                    full_content = body_text + body_html
                    
                    # 检查是否是 Etsy Transactions 订单邮件
                    # 规则（满足任一即可）：
                    # 1. 发件人是 yangqingssheng@gmail.com（转发邮件）
                    # 2. 内容包含 transaction@etsy.com
                    # 3. 内容包含 Your order number is
                    # 4. 内容包含 Congratulations on your Etsy order（直接订单邮件）
                    # 5. 内容包含 You made a sale on Etsy
                    # 6. 内容包含 Order# 或 Order #
                    is_from_forwarder = "yangqingssheng@gmail.com" in full_content
                    has_etsy_transaction = "transaction@etsy.com" in full_content
                    has_order_number = "Your order number is" in full_content
                    has_congratulations = "Congratulations on your Etsy order" in full_content
                    has_made_sale = "You made a sale on Etsy" in full_content
                    has_order_hash = "Order#" in full_content or "Order #" in full_content
                    
                    is_etsy_transaction = (is_from_forwarder or has_etsy_transaction or 
                                          has_order_number or has_congratulations or 
                                          has_made_sale or has_order_hash)
                    
                    # 调试输出
                    if not is_etsy_transaction:
                        print(f"    [DEBUG] 未匹配到关键词，内容预览: {full_content[:200]}")
                    
                    if is_etsy_transaction:
                        etsy_msg_ids.append(msg_id)
                        print(f"  [OK] ID={msg_id} 是 Etsy 订单邮件")
                    else:
                        print(f"  [SKIP] ID={msg_id} 不是 Etsy 订单邮件")
                except Exception as e:
                    print(f"  [WARN] ID={msg_id} 读取失败: {e}")
            
            print(f"[INFO] 共找到 {len(etsy_msg_ids)} 封 Etsy 订单邮件")
            return etsy_msg_ids
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            return []
    
    def search_etsy_orders(self, days: int = 7, unread_only: bool = False) -> List[int]:
        if not self.client:
            print("[ERROR] Not connected")
            return []
        
        try:
            self.client.select_folder("INBOX")
            since_date = datetime.now() - timedelta(days=days)
            
            criteria = ["SINCE", since_date.strftime("%d-%b-%Y"), "SUBJECT", "Etsy"]
            if unread_only:
                criteria.insert(0, "UNSEEN")
            
            messages = self.client.search(criteria)
            print(f"[INFO] Found {len(messages)} Etsy emails (last {days} days)")
            return list(messages)
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            return []
    
    def fetch_email_content(self, msg_id: int) -> Optional[Dict[str, Any]]:
        if not self.client:
            return None
        
        try:
            raw_messages = self.client.fetch([msg_id], ["RFC822"])
            if msg_id not in raw_messages:
                return None
            
            raw_email = raw_messages[msg_id][b"RFC822"]
            msg = email.message_from_bytes(raw_email)
            
            return {
                "id": msg_id,
                "subject": self._decode_header(msg["Subject"]),
                "from": self._decode_header(msg["From"]),
                "date": msg["Date"],
                "body": self._get_email_body(msg)
            }
        except Exception as e:
            print(f"[ERROR] Fetch failed: {e}")
            return None
    
    def _decode_header(self, header: str) -> str:
        if not header:
            return ""
        decoded_parts = decode_header(header)
        result = []
        for content, charset in decoded_parts:
            if isinstance(content, bytes):
                charset = charset or "utf-8"
                try:
                    result.append(content.decode(charset))
                except Exception:
                    result.append(content.decode("utf-8", errors="ignore"))
            else:
                result.append(content)
        return "".join(result)
    
    def _get_email_body(self, msg) -> str:
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == "text/plain":
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or "utf-8"
                    body = payload.decode(charset, errors="ignore")
                    break
                elif ctype == "text/html" and not body:
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or "utf-8"
                    body = payload.decode(charset, errors="ignore")
        else:
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset() or "utf-8"
            body = payload.decode(charset, errors="ignore")
        return body
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
    
    # ============ 发送邮件功能 ============
    
    def send_confirmation_email(
        self,
        to_email: str,
        customer_name: str,
        order_id: str,
        product_info: str,
        effect_image_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        发送订单确认邮件
        
        Args:
            to_email: 客户邮箱
            customer_name: 客户名称
            order_id: 订单ID
            product_info: 产品信息
            effect_image_path: 效果图文件路径(可选)
        
        Returns:
            {“success”: bool, “message”: str}
        """
        try:
            # 创建邮件
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_email
            msg['Subject'] = f'Order Confirmation - {order_id}'
            
            # 邮件正文
            body = f"""
Dear {customer_name},

Thank you for your order!

Order Details:
- Order ID: {order_id}
- Product: {product_info}

We have received your order and will start production soon.
Please review the attached effect image and let us know if you need any changes.

Best regards,
Your Store Team
"""
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 添加效果图附件
            if effect_image_path:
                image_path = Path(effect_image_path)
                if image_path.exists():
                    with open(image_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{image_path.name}"'
                    )
                    msg.attach(part)
            
            # 使用 SMTP 发送
            smtp_server = 'smtp.qq.com'
            smtp_port = 465
            
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(self.email_address, self.password)
                server.send_message(msg)
            
            print(f'[✅] Email sent to {to_email}')
            return {'success': True, 'message': f'邮件已发送至 {to_email}'}
            
        except Exception as e:
            print(f'[❌] Email send failed: {e}')
            return {'success': False, 'message': str(e)}


# 单例
email_service = EmailService()