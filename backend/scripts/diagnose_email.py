# -*- coding: utf-8 -*-
"""
邮件诊断脚本 - 第一步：摸清邮箱现状
功能：
  1. 连接QQ邮箱，列出最近30封主题含 "Etsy" 的邮件（无论已读未读）
  2. 显示每封邮件的主题、发件人、日期
  3. 打印第一封找到的 Etsy 邮件原始正文（前3000字符）
  4. 尝试用 email_parser 解析，显示解析结果
用途：让我们看清楚真实邮件是什么格式，再决定怎么改解析器
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import settings
from src.services.email_service import EmailService
from src.services.email_parser import email_parser


def diagnose():
    print("=" * 70)
    print("  邮件诊断工具 — 查看邮箱里的 Etsy 订单邮件")
    print("=" * 70)

    if not settings.validate():
        print("[ERROR] .env 配置不完整")
        return

    svc = EmailService()
    if not svc.connect():
        print("[ERROR] 邮箱连接失败，请检查 EMAIL_PASSWORD")
        return

    try:
        svc.client.select_folder("INBOX")

        # ─── 1. 搜索最近30天主题含 "Etsy" 的所有邮件（不管已读未读）───
        from datetime import datetime, timedelta
        since = (datetime.now() - timedelta(days=30)).strftime("%d-%b-%Y")

        print(f"\n[搜索] 最近30天 主题含 'Etsy' 的所有邮件 (since {since}) ...")
        etsy_ids = svc.client.search(["SINCE", since, "SUBJECT", "Etsy"])
        print(f"  → 找到 {len(etsy_ids)} 封\n")

        # ─── 2. 同时搜索主题含 "transaction" 的邮件 ───
        print("[搜索] 最近30天 主题含 'transaction' 的邮件 ...")
        trans_ids = svc.client.search(["SINCE", since, "SUBJECT", "transaction"])
        print(f"  → 找到 {len(trans_ids)} 封\n")

        # ─── 3. 搜索主题含 "order" 的邮件 ───
        print("[搜索] 最近30天 主题含 'order' 的邮件 ...")
        order_ids = svc.client.search(["SINCE", since, "SUBJECT", "order"])
        print(f"  → 找到 {len(order_ids)} 封\n")

        # 合并候选邮件
        all_ids = list(set(etsy_ids + trans_ids + order_ids))
        if not all_ids:
            print("⚠️  邮箱中没有找到任何相关邮件")
            print("   建议：登录 QQ 邮箱网页版，检查是否有 Etsy 订单邮件")
            return

        # ─── 4. 逐封列出主题和发件人 ───
        print("=" * 70)
        print(f"  找到 {len(all_ids)} 封候选邮件，列表如下：")
        print("=" * 70)

        import email as email_lib
        from email.header import decode_header

        def decode_h(h):
            if not h:
                return ""
            parts = decode_header(h)
            result = []
            for content, charset in parts:
                if isinstance(content, bytes):
                    result.append(content.decode(charset or "utf-8", errors="ignore"))
                else:
                    result.append(content)
            return "".join(result)

        first_etsy_id = None
        for i, mid in enumerate(sorted(all_ids, reverse=True)[:20], 1):
            raw = svc.client.fetch([mid], ["RFC822"])
            msg = email_lib.message_from_bytes(raw[mid][b"RFC822"])
            subj = decode_h(msg["Subject"])
            frm  = decode_h(msg["From"])
            date = msg["Date"] or ""
            print(f"  [{i:02d}] ID={mid}")
            print(f"        主题: {subj[:80]}")
            print(f"        发件: {frm[:60]}")
            print(f"        日期: {date[:40]}")
            print()
            if first_etsy_id is None:
                first_etsy_id = mid

        # ─── 5. 打印第一封邮件原始正文 ───
        if first_etsy_id:
            print("=" * 70)
            print(f"  第一封邮件（ID={first_etsy_id}）原始正文预览（前3000字符）：")
            print("=" * 70)
            email_data = svc.fetch_email_content(first_etsy_id)
            if email_data:
                body = email_data['body']
                print(body[:3000])
                print("\n" + "─" * 70)

                # ─── 6. 尝试解析 ───
                print("\n  解析结果：")
                parsed = email_parser.parse_forwarded_email(body)
                if parsed and parsed.etsy_order_id:
                    print(f"  ✅ 订单号: {parsed.etsy_order_id}")
                    print(f"  客户名: {parsed.customer_name}")
                    print(f"  收货城市: {parsed.shipping_city}, {parsed.shipping_country}")
                    print(f"  金额: {parsed.order_total} {parsed.currency}")
                    if parsed.items:
                        item = parsed.items[0]
                        print(f"  外观: {item.shape}")
                        print(f"  颜色: {item.color}")
                        print(f"  大小: {item.size}")
                        print(f"  工艺: —（暂无字段，默认抛光）")
                        print(f"  正面刻字: {item.customization_front}")
                        print(f"  字体: {item.font_code}")
                        print(f"  背面刻字: {item.customization_back}")
                else:
                    print("  ❌ 解析失败（未找到订单号）")
                    print("  → 需要看原始正文，找到订单号的格式，再修改解析器")

    finally:
        svc.disconnect()

    print("\n" + "=" * 70)
    print("  诊断完成！")
    print("  下一步：把上面的原始正文截图或复制给AI，修复解析器")
    print("=" * 70)


if __name__ == "__main__":
    diagnose()
