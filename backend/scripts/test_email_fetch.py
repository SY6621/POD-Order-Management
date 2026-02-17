# -*- coding: utf-8 -*-
"""Email fetch test script"""

import sys
import io

# Fix Windows PowerShell encoding issue
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings
from src.services.email_service import EmailService
from src.services.email_parser import email_parser


def test_email_fetch():
    print("=" * 60)
    print("Etsy Email Fetch Test")
    print("=" * 60)
    
    if not settings.validate():
        return
    
    settings.ensure_output_dir()
    print(f"[OK] Output dir: {settings.OUTPUT_DIR}")
    
    email_svc = EmailService()
    if not email_svc.connect():
        return
    
    try:
        print("\n[INFO] Searching Etsy emails...")
        msg_ids = email_svc.search_today_unread_etsy_orders()
        
        if not msg_ids:
            print("[WARN] No unread emails today, searching last 7 days...")
            msg_ids = email_svc.search_etsy_orders(days=7, unread_only=False)
        
        if not msg_ids:
            print("[ERROR] No Etsy emails found")
            return
        
        print(f"\n[INFO] Processing {min(len(msg_ids), 3)} of {len(msg_ids)} emails...\n")
        
        for i, msg_id in enumerate(msg_ids[:3], 1):
            print("=" * 50)
            print(f"Email {i} (ID: {msg_id})")
            print("=" * 50)
            
            email_data = email_svc.fetch_email_content(msg_id)
            if not email_data:
                print("[ERROR] Failed to fetch")
                continue
            
            subj = email_data['subject'][:50] if email_data['subject'] else "No subject"
            print(f"Subject: {subj}...")
            print(f"From: {email_data['from']}")
            
            parsed = email_parser.parse_forwarded_email(email_data['body'])
            if not parsed:
                print("[ERROR] Parse failed")
                continue
            
            print(f"\n[OK] Parsed:")
            print(f"  Order ID: {parsed.etsy_order_id}")
            print(f"  Customer: {parsed.customer_name}")
            print(f"  Address: {parsed.shipping_city}, {parsed.shipping_country}")
            print(f"  Total: {parsed.currency} {parsed.order_total}")
            
            if parsed.items:
                item = parsed.items[0]
                print(f"  Product: {item.shape} {item.color} {item.size}")
                print(f"  Front: {item.customization_front} (Font: {item.font_code})")
                if item.customization_back:
                    print(f"  Back: {item.customization_back}")
            print()
    finally:
        email_svc.disconnect()
    
    print("=" * 60)
    print("[OK] Test completed")
    print("=" * 60)


if __name__ == "__main__":
    test_email_fetch()