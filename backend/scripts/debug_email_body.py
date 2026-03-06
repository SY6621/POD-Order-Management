# -*- coding: utf-8 -*-
"""临时调试脚本：读取指定邮件ID的完整正文"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from src.services.email_service import email_service

email_service.connect()
# search_all_unread 会自动 select_folder(INBOX)
msg_ids = email_service.search_all_unread_etsy_orders()
print(f"\n找到 Etsy 邮件: {msg_ids}")

# 强制读取 ID=4120
for mid in [4120]:
    data = email_service.fetch_email_content(mid)
    if data:
        print(f"\n=== 邮件主题 ===")
        print(data.get('subject', ''))
        print(f"\n=== 邮件正文（前5000字符）===")
        print(data['body'][:5000])
    else:
        print(f"ID={mid} 获取失败")
email_service.disconnect()
