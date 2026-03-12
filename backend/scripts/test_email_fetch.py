# -*- coding: utf-8 -*-
"""
Etsy 订单邮件抓取并导入 Supabase

使用方式：
  1. 在 QQ 邮箱中，把要导入的 Etsy 订单邮件标注为「未读」
  2. 运行此脚本：poetry run python scripts/test_email_fetch.py
  3. 脚本会自动搜索所有未读 Etsy 邮件（不限日期）并导入数据库
"""

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
from src.services.order_service import order_service
from src.services.database_service import db
from src.services.effect_template_service import generate_effect_image_for_order


def test_email_fetch():
    print("=" * 60)
    print("Etsy 订单邮件抓取工具")
    print("=" * 60)
    print("提示：请在 QQ 邮箱中将要导入的订单邮件标注为「未读」")
    print("=" * 60)
    
    if not settings.validate():
        return
    
    settings.ensure_output_dir()
    
    email_svc = EmailService()
    if not email_svc.connect():
        return
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    try:
        # 使用新方法：搜索所有未读 Etsy 订单邮件（不限日期）
        print("\n[INFO] 搜索所有未读 Etsy 订单邮件（不限日期）...")
        msg_ids = email_svc.search_all_unread_etsy_orders()
        
        if not msg_ids:
            print("[WARN] 未找到未读的 Etsy 订单邮件")
            print("[HINT] 请在 QQ 邮箱中把订单邮件标注为未读，再重新运行")
            return
        
        print(f"[INFO] 共找到 {len(msg_ids)} 封未读 Etsy 邮件，开始处理...\n")
        
        for i, msg_id in enumerate(msg_ids, 1):
            print(f"--- 第 {i}/{len(msg_ids)} 封 (ID: {msg_id}) ---")
            
            email_data = email_svc.fetch_email_content(msg_id)
            if not email_data:
                print("  [ERROR] 获取邮件内容失败")
                fail_count += 1
                continue
            
            subj = email_data['subject'][:60] if email_data['subject'] else "(无主题)"
            print(f"  主题: {subj}")
            print(f"  发件人: {email_data['from']}")
            
            # 解析邮件
            parsed = email_parser.parse_forwarded_email(email_data['body'])
            if not parsed or not parsed.etsy_order_id:
                print("  [SKIP] 解析失败，可能不是订单通知邮件")
                fail_count += 1
                continue
            
            # 显示解析结果
            print(f"  订单号: {parsed.etsy_order_id}")
            print(f"  客户: {parsed.customer_name}")
            print(f"  收货地: {parsed.shipping_city}, {parsed.shipping_country}")
            print(f"  金额: AUD {parsed.order_total}")
            if parsed.items:
                item = parsed.items[0]
                print(f"  商品: {item.shape} | {item.color} | {item.size}")
                print(f"  正面刻字: {item.customization_front} (字体: {item.font_code})")
                if item.customization_back:
                    print(f"  背面刻字: {item.customization_back}")
            
            # 写入 Supabase 数据库
            result = order_service.process_parsed_order(parsed)
            if result:
                success_count += 1
                # 新订单自动生成效果图
                print(f"  [效果图] 开始生成...")
                url = generate_effect_image_for_order(result, upload=True)
                if url:
                    # 回写 effect_image_url 到数据库
                    db.update('orders', {'id': result['id']}, {'effect_image_url': url})
                    print(f"  [效果图] 已保存并回写 URL")
                else:
                    print(f"  [效果图] 生成失败，可手动重试")
            else:
                # process_parsed_order 返回 None 表示订单已存在被跳过
                skip_count += 1
            print()
    
    finally:
        email_svc.disconnect()
    
    print("=" * 60)
    print(f"导入结果汇总：")
    print(f"  新建订单: {success_count} 条")
    print(f"  重复跳过: {skip_count} 条")
    print(f"  解析失败: {fail_count} 条")
    print("=" * 60)


if __name__ == "__main__":
    test_email_fetch()