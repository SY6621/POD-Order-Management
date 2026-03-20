# -*- coding: utf-8 -*-
"""
真实订单完整流程测试
从QQ邮箱抓取订单 → 解析 → 存入数据库 → 生成生产文档PDF
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.email_service import EmailService
from src.services.email_parser import email_parser
from src.services.order_service import order_service, lookup_sku
from src.services.svg_pdf_service import svg_pdf_service
from src.services.database_service import db

print("=" * 60)
print("ETSY 订单自动化 - 真实数据完整流程测试")
print("=" * 60)

# ========== 步骤1：连接邮箱 ==========
print("\n【步骤1】连接QQ邮箱...")
email_service = EmailService()
if not email_service.connect():
    print("❌ 邮箱连接失败，请检查 .env 配置")
    sys.exit(1)

# ========== 步骤2：搜索订单邮件 ==========
print("\n【步骤2】搜索最近7天的Etsy订单邮件...")
msg_ids = email_service.search_all_unread_etsy_orders()
print(f"找到 {len(msg_ids)} 封订单邮件")

if not msg_ids:
    print("⚠️ 没有找到订单邮件，尝试搜索已读邮件...")
    # 尝试搜索已读邮件
    email_service.client.select_folder("INBOX")
    from datetime import datetime, timedelta
    since_date = datetime.now() - timedelta(days=30)  # 扩大到30天
    all_msgs = email_service.client.search([
        "SINCE", since_date.strftime("%d-%b-%Y"),
        "FROM", "transaction@etsy.com"
    ])
    msg_ids = list(all_msgs)
    print(f"找到 {len(msg_ids)} 封已读订单邮件")

if not msg_ids:
    print("❌ 没有找到任何订单邮件")
    email_service.disconnect()
    sys.exit(1)

# ========== 步骤3：解析第一封订单邮件 ==========
print("\n【步骤3】解析订单邮件...")
msg_id = msg_ids[0]
print(f"处理邮件 ID: {msg_id}")

# 获取邮件内容
raw = email_service.client.fetch([msg_id], ["BODY[TEXT]", "BODY[HTML]"])
body_text = raw.get(msg_id, {}).get(b"BODY[TEXT]", b"").decode("utf-8", errors="ignore")
body_html = raw.get(msg_id, {}).get(b"BODY[HTML]", b"").decode("utf-8", errors="ignore")

# 解码 quoted-printable 编码
import quopri
try:
    body_text = quopri.decodestring(body_text.encode('utf-8')).decode('utf-8', errors='ignore')
except:
    pass
try:
    body_html = quopri.decodestring(body_html.encode('utf-8')).decode('utf-8', errors='ignore')
except:
    pass

# 清理邮件格式
import re
body_text = re.sub(r'=\r?\n', '', body_text)  # 移除软换行
body_html = re.sub(r'=\r?\n', '', body_html)

# 合并内容
full_content = body_text + body_html
print(f"邮件内容长度: {len(full_content)} 字符")
print(f"邮件内容预览: {full_content[:2000]}...")

# 解析订单
parsed = email_parser.parse(full_content)
if not parsed or not parsed.etsy_order_id:
    print("❌ 订单解析失败")
    print(f"邮件内容预览: {full_content[:500]}...")
    email_service.disconnect()
    sys.exit(1)

print(f"\n✅ 订单解析成功:")
print(f"  - Etsy订单号: {parsed.etsy_order_id}")
print(f"  - 客户名: {parsed.customer_name}")
print(f"  - 商品数量: {len(parsed.items)}")

for i, item in enumerate(parsed.items):
    print(f"  - 商品{i+1}: {item.product_name}")
    print(f"    外观: {item.shape}, 颜色: {item.color}, 尺寸: {item.size}")
    print(f"    正面文字: {item.customization_front}")
    print(f"    背面文字: {item.customization_back}")

# ========== 步骤4：SKU反推 ==========
print("\n【步骤4】SKU反推...")
if parsed.items:
    item = parsed.items[0]
    sku_info = lookup_sku(item.shape, item.color, item.size)
    if sku_info:
        print(f"✅ SKU匹配成功: {sku_info.get('sku_code')}")
        print(f"  - 外观: {sku_info.get('shape')}")
        print(f"  - 颜色: {sku_info.get('color')}")
        print(f"  - 尺寸: {sku_info.get('size')}")
    else:
        print("⚠️ SKU未匹配，使用默认值")
        sku_info = {"sku_code": "UNKNOWN", "shape": "心形", "color": "银色", "size": "L"}

# ========== 步骤5：存入数据库 ==========
print("\n【步骤5】存入数据库...")
order_data = order_service.process_parsed_order(parsed)
if order_data:
    print(f"✅ 订单已存入数据库")
    print(f"  - 数据库ID: {order_data.get('id')}")
    print(f"  - SKU: {order_data.get('sku')}")
else:
    # 订单可能已存在，尝试查询
    print("⚠️ 订单可能已存在，查询现有记录...")
    existing = db.get_order_by_etsy_id(parsed.etsy_order_id)
    if existing:
        order_data = existing
        print(f"✅ 找到现有订单: {order_data.get('id')}")
    else:
        print("❌ 订单存储失败")
        email_service.disconnect()
        sys.exit(1)

# ========== 步骤6：生成生产文档PDF ==========
print("\n【步骤6】生成生产文档PDF...")
try:
    # 准备订单数据
    pdf_data = {
        "etsy_order_id": parsed.etsy_order_id,
        "sku": sku_info.get("sku_code", "UNKNOWN") if sku_info else "UNKNOWN",
        "customer_name": parsed.customer_name or parsed.shipping_name,
        # 效果图参数
        "shape": sku_info.get("shape", "心形") if sku_info else "心形",
        "color": sku_info.get("color", "银色") if sku_info else "银色",
        "size": sku_info.get("size", "L") if sku_info else "L",
        "front_text": parsed.items[0].customization_front if parsed.items else "",
        "back_text": parsed.items[0].customization_back if parsed.items else "",
        # 收件人信息
        "recipient_name": parsed.shipping_name,
        "street_address": parsed.shipping_address_line1,
        "city": parsed.shipping_city,
        "state_code": parsed.shipping_state,
        "postal_code": parsed.shipping_zip,
        "country": parsed.shipping_country,
        "tracking_number": "",
    }
    
    # 尝试从数据库获取物流信息
    logistics_list = db.select("logistics", {"order_id": order_data.get("id")})
    if logistics_list:
        logistics = logistics_list[0]
        pdf_data.update({
            "recipient_name": logistics.get("recipient_name", ""),
            "street_address": logistics.get("street_address", ""),
            "city": logistics.get("city", ""),
            "state_code": logistics.get("state_code", ""),
            "postal_code": logistics.get("postal_code", ""),
            "country": logistics.get("country", ""),
            "tracking_number": logistics.get("tracking_number", ""),
        })
    
    pdf_path = svg_pdf_service.generate_from_raw_data(pdf_data)
    
    if pdf_path:
        print(f"✅ PDF生成成功!")
        print(f"  - 文件路径: {pdf_path}")
    else:
        print("❌ PDF生成失败")
        
except Exception as e:
    print(f"❌ PDF生成出错: {e}")
    import traceback
    traceback.print_exc()

# ========== 完成 ==========
email_service.disconnect()
print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
