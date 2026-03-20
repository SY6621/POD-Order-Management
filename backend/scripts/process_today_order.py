"""
处理今天的 Etsy 订单 - 获取邮件、创建物流面单
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import re
import json
import hashlib
import time
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests
from typing import Dict, Any, Optional
import email
from email.header import decode_header
from imapclient import IMAPClient
from src.config.settings import settings

# 加载环境变量
env_path = project_root / '.env'
load_dotenv(env_path)

# 4PX 生产环境配置
FOURPX_CONFIG = {
    "app_key": os.getenv("FOURPX_APP_KEY"),
    "app_secret": os.getenv("FOURPX_APP_SECRET"),
    "base_url": "https://open.4px.com/router/api/service"
}


def decode_quoted_printable(content: bytes) -> str:
    """解码 quoted-printable 编码的内容"""
    try:
        return content.decode('utf-8', errors='ignore')
    except:
        return content.decode('iso-8859-1', errors='ignore')


def parse_order_from_email(body: str) -> dict:
    """从邮件正文中解析订单数据"""
    order = {}
    
    # 1. 订单号
    m = re.search(r"orders/(\d+)", body)
    if m:
        order["order_id"] = m.group(1)
    else:
        return None
    
    # 2. 客户用户名
    m = re.search(r"Buyer:\s*(\S+)", body)
    order["customer_username"] = m.group(1) if m else ""
    
    # 3. 订单金额
    m = re.search(r"Order Total:\s*AU?\$?(\d+\.\d+)", body)
    order["order_total"] = float(m.group(1)) if m else 0.0
    order["currency"] = "AUD" if "AU" in body[:1000] else "USD"
    
    # 4. 地址 (HTML格式)
    m = re.search(r"<span class='name'>([^<]+)</span>", body)
    order["shipping_name"] = m.group(1).strip() if m else ""
    order["customer_name"] = order["shipping_name"]
    
    m = re.search(r"<span class='first-line'>([^<]+)</span>", body)
    order["shipping_address_line1"] = m.group(1).strip() if m else ""
    
    m = re.search(r"<span class='city'>([^<]+)</span>", body)
    order["shipping_city"] = m.group(1).strip() if m else ""
    
    m = re.search(r"<span class='state'>([^<]+)</span>", body)
    order["shipping_state"] = m.group(1).strip() if m else ""
    
    m = re.search(r"<span class='zip'>([^<]+)</span>", body)
    order["shipping_zip"] = m.group(1).strip() if m else ""
    
    m = re.search(r"<span class='country-name'>([^<]+)</span>", body)
    country_name = m.group(1).strip() if m else ""
    # 转换国家名称为两位代码
    country_map = {
        "Australia": "AU",
        "United States": "US",
        "USA": "US",
        "United Kingdom": "GB",
        "UK": "GB",
        "Canada": "CA",
        "Germany": "DE",
        "France": "FR"
    }
    order["shipping_country"] = country_map.get(country_name, country_name[:2].upper() if country_name else "US")
    
    # 5. 产品信息
    m = re.search(r"Item:\s*(.+?)(?:\n|Color)", body)
    product_name = m.group(1).strip() if m else "Pet ID Tag"
    
    m = re.search(r"Color \+ Size::?\s*(\S+)\s+(\S+)", body)
    color = m.group(1) if m else ""
    size = m.group(2) if m else ""
    
    # Personalization
    personalization = ""
    front_text = ""
    back_text = ""
    font_code = ""
    
    m = re.search(r"Personalization:\s*(.+?)(?:\n\n|Quantity:)", body, re.DOTALL)
    if m:
        personalization = m.group(1).strip()
        
        # front
        m2 = re.search(r"front\s*:?\s*(.+?)(?:\n|back|$)", personalization, re.IGNORECASE)
        if m2:
            front_text = m2.group(1).strip()
            m3 = re.search(r"\(F-(\d+)\)", front_text)
            if m3:
                font_code = f"F-{m3.group(1)}"
                front_text = re.sub(r"\s*\(F-\d+\)", "", front_text).strip()
        
        # back
        m2 = re.search(r"back\s*:?\s*(.+?)(?:\n|$)", personalization, re.IGNORECASE)
        if m2:
            back_text = m2.group(1).strip()
    
    m = re.search(r"Quantity:\s*(\d+)", body)
    quantity = int(m.group(1)) if m else 1
    
    order["items"] = [{
        "product_name": product_name,
        "quantity": quantity,
        "personalization": personalization,
        "font_code": font_code,
        "front_text": front_text,
        "back_text": back_text,
        "shape": "Heart" if "Heart" in product_name else "Bone" if "Bone" in product_name else "Circle" if "Circle" in product_name or "Round" in product_name else "",
        "color": color,
        "size": size
    }]
    
    return order


def fetch_today_order_from_email():
    """从邮箱获取今天的订单"""
    print("=" * 70)
    print("步骤1: 从邮箱获取今天的订单")
    print("=" * 70)
    
    try:
        client = IMAPClient(settings.IMAP_SERVER, port=993, ssl=True)
        client.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        print("✅ 邮箱连接成功")
        
        client.select_folder("INBOX")
        
        # 搜索今天的未读邮件
        today = datetime.now().strftime("%d-%b-%Y")
        messages = client.search(["UNSEEN", "SINCE", today])
        
        print(f"找到 {len(messages)} 封今天的未读邮件")
        
        for msg_id in messages:
            raw = client.fetch([msg_id], ["RFC822"])
            raw_email = raw[msg_id][b"RFC822"]
            msg = email.message_from_bytes(raw_email)
            
            subject = ""
            if msg["Subject"]:
                decoded = decode_header(msg["Subject"])
                for content, charset in decoded:
                    if isinstance(content, bytes):
                        subject += content.decode(charset or 'utf-8', errors='ignore')
                    else:
                        subject += content
            
            print(f"\n邮件主题: {subject}")
            
            if "Etsy" in subject:
                # 获取正文
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        if ctype == "text/plain":
                            body = decode_quoted_printable(part.get_payload(decode=True))
                            break
                        elif ctype == "text/html" and not body:
                            body = decode_quoted_printable(part.get_payload(decode=True))
                else:
                    body = decode_quoted_printable(msg.get_payload(decode=True))
                
                order = parse_order_from_email(body)
                if order:
                    print(f"✅ 解析订单成功: {order['order_id']}")
                    print(f"   客户: {order['customer_name']}")
                    print(f"   地址: {order['shipping_address_line1']}, {order['shipping_city']}")
                    print(f"   国家: {order['shipping_country']}")
                    if order['items']:
                        item = order['items'][0]
                        print(f"   产品: {item['product_name']}")
                        print(f"   定制: 正面={item['front_text']}, 背面={item['back_text']}, 字体={item['font_code']}")
                    client.logout()
                    return order
                else:
                    print("⚠️ 无法解析订单")
        
        client.logout()
        print("\n❌ 没有找到可解析的订单")
        return None
        
    except Exception as e:
        print(f"❌ 邮箱操作失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def generate_sign(app_key, app_secret, method, v, body, timestamp=None):
    """生成 4PX API 签名"""
    if timestamp is None:
        timestamp = int(time.time() * 1000)
    body_str = json.dumps(body, ensure_ascii=False, separators=(',', ':'))
    sign_string = f"app_key{app_key}formatjsonmethod{method}timestamp{timestamp}v{v}{body_str}{app_secret}"
    md5_sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest().lower()
    return sign_string, md5_sign, timestamp


def call_4px_api(method, v, body):
    """调用 4PX API"""
    app_key = FOURPX_CONFIG["app_key"]
    app_secret = FOURPX_CONFIG["app_secret"]
    base_url = FOURPX_CONFIG["base_url"]
    
    _, sign, timestamp = generate_sign(app_key, app_secret, method, v, body)
    url = f"{base_url}?method={method}&app_key={app_key}&v={v}&timestamp={timestamp}&format=json&sign={sign}"
    body_str = json.dumps(body, ensure_ascii=False, separators=(',', ':'))
    
    try:
        response = requests.post(url, data=body_str, headers={"Content-Type": "application/json"}, timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def create_shipping_order(order_data):
    """创建物流订单"""
    print("\n" + "=" * 70)
    print("步骤2: 创建物流订单")
    print("=" * 70)
    
    # 查询可用物流产品
    country = order_data.get("shipping_country", "US")
    postcode = order_data.get("shipping_zip", "")
    
    print(f"查询到 {country} (邮编: {postcode}) 的可用物流产品...")
    
    result = call_4px_api("ds.xms.logistics_product.getlist", "1.0.0", {
        "country_code": country,
        "postcode": postcode,
        "transport_mode": "1"
    })
    
    products = []
    if result.get("result") == "1" and result.get("data"):
        products = result["data"]
        print(f"找到 {len(products)} 个可用产品:")
        for p in products[:5]:
            print(f"   - {p.get('logistics_product_code')}: {p.get('logistics_product_name_cn')}")
    
    if not products:
        print(f"❌ 没有可用的物流产品到 {country}")
        return None
    
    # 选择第一个可用产品（跳过 A1，因为它在某些国家不可用）
    selected_product = None
    for p in products:
        code = p.get("logistics_product_code")
        if code != "A1":  # 跳过 A1
            selected_product = code
            break
    
    if not selected_product:
        selected_product = products[0].get("logistics_product_code")
    
    print(f"\n使用物流产品: {selected_product}")
    
    # 构建请求
    body = {
        "ref_no": order_data["order_id"],
        "business_type": "BDS",
        "duty_type": "P",
        "logistics_service_info": {"logistics_product_code": selected_product},
        "sender": {
            "first_name": "Sender",
            "phone": "13800138000",
            "post_code": "518000",
            "country": "CN",
            "state": "Guangdong",
            "city": "Shenzhen",
            "street": "Test Address 123"
        },
        "recipient_info": {
            "first_name": order_data.get("shipping_name", "Customer"),
            "phone": "1234567890",
            "post_code": order_data.get("shipping_zip", "00000"),
            "country": country,
            "state": order_data.get("shipping_state", ""),
            "city": order_data.get("shipping_city", ""),
            "street": order_data.get("shipping_address_line1", "")
        },
        "deliver_type_info": {"deliver_type": "2"},
        "parcel_list": [{
            "weight": 10,
            "parcel_value": 5,
            "currency": "USD",
            "include_battery": "N",
            "declare_product_info": [{
                "declare_product_name_cn": "宠物牌",
                "declare_product_name_en": "Pet Tag",
                "declare_product_code_qty": "1",
                "declare_unit_price_export": 5,
                "currency_export": "USD",
                "declare_unit_price_import": 5,
                "currency_import": "USD",
                "brand_export": "无",
                "brand_import": "无"
            }]
        }]
    }
    
    result = call_4px_api("ds.xms.order.create", "1.1.0", body)
    return result


def get_label(tracking_no):
    """获取面单"""
    print("\n" + "=" * 70)
    print("步骤3: 获取物流面单")
    print("=" * 70)
    
    time.sleep(5)  # 等待面单生成
    
    result = call_4px_api("ds.xms.label.get", "1.1.0", {
        "request_no": tracking_no,
        "label_type": "1",
        "label_size": "label_100x100"
    })
    
    if result.get("result") == "1":
        label_data = result.get("data", {})
        label_url_info = label_data.get("label_url_info", {})
        return label_url_info.get("logistics_label", "")
    
    return None


# ============ 主流程 ============
if __name__ == "__main__":
    print("=" * 70)
    print("处理今天的 Etsy 订单 - 物流下单")
    print("=" * 70)
    
    # 步骤1: 获取订单
    order = fetch_today_order_from_email()
    if not order:
        print("\n❌ 没有找到今天的订单")
        exit(1)
    
    # 步骤2: 创建物流订单
    result = create_shipping_order(order)
    if not result or result.get("result") != "1":
        print("\n❌ 物流订单创建失败")
        errors = result.get('errors', [])
        for err in errors:
            print(f"   错误: {err.get('error_msg', 'Unknown')}")
        exit(1)
    
    data = result.get("data", {})
    tracking_4px = data.get("4px_tracking_no", "")
    print(f"\n✅ 物流订单创建成功!")
    print(f"   4PX单号: {tracking_4px}")
    print(f"   DS委托单号: {data.get('ds_consignment_no', 'N/A')}")
    
    # 步骤3: 获取面单
    if tracking_4px:
        label_url = get_label(tracking_4px)
        if label_url:
            print(f"\n{'='*70}")
            print(f"✅ 物流面单生成成功!")
            print(f"{'='*70}")
            print(f"订单号: {order['order_id']}")
            print(f"客户: {order['customer_name']}")
            print(f"4PX单号: {tracking_4px}")
            print(f"面单URL: {label_url}")
            print(f"{'='*70}")
        else:
            print("\n⚠️ 面单获取失败，请稍后手动查询")
    
    print("\n处理完成!")
