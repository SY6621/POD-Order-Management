"""
处理真实订单物流下单流程
1. 取消测试订单
2. 从邮箱获取今天的真实订单
3. 创建物流面单
"""
import hashlib
import json
import time
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests
from typing import Dict, Any, Optional

# 加载环境变量
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# 生产环境配置
PROD_CONFIG = {
    "app_key": os.getenv("FOURPX_APP_KEY"),
    "app_secret": os.getenv("FOURPX_APP_SECRET"),
    "base_url": "https://open.4px.com/router/api/service"
}

print("=" * 70)
print("真实订单物流下单处理")
print("=" * 70)


def generate_sign(app_key: str, app_secret: str, method: str, v: str, 
                  body: Dict[Any, Any], timestamp: Optional[int] = None) -> tuple:
    """生成 4PX API 签名"""
    if timestamp is None:
        timestamp = int(time.time() * 1000)
    
    body_str = json.dumps(body, ensure_ascii=False, separators=(',', ':'))
    sign_string = f"app_key{app_key}formatjsonmethod{method}timestamp{timestamp}v{v}{body_str}{app_secret}"
    md5_sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest().lower()
    
    return sign_string, md5_sign, timestamp


def call_4px_api(method: str, v: str, body: Dict[Any, Any]) -> Dict[Any, Any]:
    """调用 4PX API"""
    app_key = PROD_CONFIG["app_key"]
    app_secret = PROD_CONFIG["app_secret"]
    base_url = PROD_CONFIG["base_url"]
    
    sign_string, sign, timestamp = generate_sign(app_key, app_secret, method, v, body)
    url = f"{base_url}?method={method}&app_key={app_key}&v={v}&timestamp={timestamp}&format=json&sign={sign}"
    body_str = json.dumps(body, ensure_ascii=False, separators=(',', ':'))
    
    try:
        response = requests.post(
            url,
            data=body_str,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        return response.json()
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return {"error": str(e)}


def cancel_order(request_no: str) -> bool:
    """取消 4PX 订单"""
    print(f"\n【取消测试订单】{request_no}")
    result = call_4px_api(
        "ds.xms.order.cancel",
        "1.0.0",
        {
            "request_no": request_no,
            "cancel_reason": "测试订单取消"
        }
    )
    
    if result.get("result") == "1":
        print(f"✅ 订单 {request_no} 已取消")
        return True
    else:
        print(f"⚠️ 取消订单失败: {result.get('errors', result.get('msg', 'Unknown'))}")
        return False


def get_logistics_products(country_code: str, postcode: str = "") -> list:
    """查询可用物流产品"""
    result = call_4px_api(
        "ds.xms.logistics_product.getlist",
        "1.0.0",
        {
            "country_code": country_code,
            "postcode": postcode,
            "transport_mode": "1"
        }
    )
    
    if result.get("result") == "1" and result.get("data"):
        return [p.get("logistics_product_code") for p in result["data"]]
    return []


def create_shipping_order(order_data: Dict) -> Dict:
    """创建物流订单"""
    print(f"\n【创建物流订单】{order_data.get('ref_no')}")
    
    # 查询可用物流产品
    country = order_data.get("recipient_country", "US")
    postcode = order_data.get("recipient_postcode", "")
    products = get_logistics_products(country, postcode)
    
    if not products:
        print(f"❌ 没有可用的物流产品到 {country}")
        return {"error": "No available logistics products"}
    
    selected_product = products[0]
    print(f"使用物流产品: {selected_product}")
    
    # 构建请求体
    body = {
        "ref_no": order_data["ref_no"],
        "business_type": "BDS",
        "duty_type": "P",
        "logistics_service_info": {
            "logistics_product_code": selected_product
        },
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
            "first_name": order_data.get("recipient_name", "Customer"),
            "phone": order_data.get("recipient_phone", "1234567890"),
            "post_code": order_data.get("recipient_postcode", "00000"),
            "country": country,
            "state": order_data.get("recipient_state", ""),
            "city": order_data.get("recipient_city", ""),
            "street": order_data.get("recipient_address", "")
        },
        "deliver_type_info": {
            "deliver_type": "2"
        },
        "parcel_list": [{
            "weight": order_data.get("weight", 10),
            "parcel_value": order_data.get("parcel_value", 5),
            "currency": "USD",
            "include_battery": "N",
            "declare_product_info": [{
                "declare_product_name_cn": order_data.get("product_name_cn", "宠物牌"),
                "declare_product_name_en": order_data.get("product_name_en", "Pet Tag"),
                "declare_product_code_qty": str(order_data.get("quantity", 1)),
                "declare_unit_price_export": order_data.get("unit_price", 5),
                "currency_export": "USD",
                "declare_unit_price_import": order_data.get("unit_price", 5),
                "currency_import": "USD",
                "brand_export": "无",
                "brand_import": "无"
            }]
        }]
    }
    
    result = call_4px_api("ds.xms.order.create", "1.1.0", body)
    return result


def get_label(request_no: str) -> Optional[str]:
    """获取面单URL"""
    print(f"\n【获取面单】{request_no}")
    
    # 等待面单生成
    time.sleep(5)
    
    result = call_4px_api(
        "ds.xms.label.get",
        "1.1.0",
        {
            "request_no": request_no,
            "label_type": "1",
            "label_size": "label_100x100"
        }
    )
    
    if result.get("result") == "1":
        label_data = result.get("data", {})
        label_url_info = label_data.get("label_url_info", {})
        label_url = label_url_info.get("logistics_label", "")
        if label_url:
            print(f"✅ 面单URL: {label_url}")
            return label_url
    
    print(f"❌ 获取面单失败: {result.get('errors', result.get('msg', 'Unknown'))}")
    return None


def fetch_today_orders_from_email() -> list:
    """从邮箱获取今天的订单"""
    import sys
    # 添加项目根目录到路径
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    from src.services.email_service import email_service
    from src.services.email_parser import EtsyEmailParser
    
    parser = EtsyEmailParser()
    orders = []
    
    try:
        with email_service:
            # 搜索今天的未读 Etsy 订单邮件
            msg_ids = email_service.search_all_unread_etsy_orders()
            
            if not msg_ids:
                print("⚠️ 今天没有新的 Etsy 订单邮件")
                return orders
            
            print(f"\n找到 {len(msg_ids)} 封 Etsy 订单邮件")
            
            for msg_id in msg_ids:
                try:
                    email_content = email_service.fetch_email_content(msg_id)
                    if not email_content:
                        continue
                    
                    # 解析订单数据
                    parsed_order = parser.parse(email_content["body"])
                    if parsed_order:
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
                            ],
                            "email_id": msg_id,
                            "email_subject": email_content.get("subject", "")
                        }
                        orders.append(order_data)
                        print(f"✅ 解析订单成功: {order_data.get('order_id', 'N/A')}")
                    else:
                        print(f"⚠️ 无法解析邮件 ID={msg_id}")
                        
                except Exception as e:
                    print(f"❌ 处理邮件 ID={msg_id} 失败: {e}")
    except Exception as e:
        print(f"❌ 邮箱连接失败: {e}")
    
    return orders


# ============ 主流程 ============

if __name__ == "__main__":
    # 步骤1: 取消之前的测试订单
    print("\n" + "=" * 70)
    print("步骤1: 取消测试订单")
    print("=" * 70)
    
    test_tracking_numbers = [
        "4PX3002571650803CN",  # 之前创建的测试订单
        "4PX3002571660819CN",  # 最新测试订单
    ]
    
    for tracking_no in test_tracking_numbers:
        cancel_order(tracking_no)
    
    # 步骤2: 从邮箱获取今天的真实订单
    print("\n" + "=" * 70)
    print("步骤2: 从邮箱获取今天的真实订单")
    print("=" * 70)
    
    today_orders = fetch_today_orders_from_email()
    
    if not today_orders:
        print("\n❌ 没有找到今天的订单")
        exit(1)
    
    print(f"\n找到 {len(today_orders)} 个今天的订单")
    
    # 步骤3: 为每个订单创建物流面单
    print("\n" + "=" * 70)
    print("步骤3: 创建物流面单")
    print("=" * 70)
    
    for order in today_orders:
        print(f"\n{'='*70}")
        print(f"处理订单: {order.get('order_id', 'N/A')}")
        print(f"客户: {order.get('customer_name', 'N/A')}")
        print(f"产品: {order.get('product_info', 'N/A')}")
        print(f"{'='*70}")
        
        # 准备物流订单数据
        shipping_data = {
            "ref_no": order.get("order_id", f"ETSY{int(time.time())}"),
            "recipient_name": order.get("shipping_name", ""),
            "recipient_phone": order.get("shipping_phone", "1234567890"),
            "recipient_address": order.get("shipping_address", ""),
            "recipient_city": order.get("shipping_city", ""),
            "recipient_state": order.get("shipping_state", ""),
            "recipient_postcode": order.get("shipping_postal_code", ""),
            "recipient_country": order.get("shipping_country", "US"),
            "weight": 10,  # 默认10克
            "parcel_value": 5,
            "unit_price": 5,
            "product_name_cn": "宠物牌",
            "product_name_en": "Pet Tag",
            "quantity": 1
        }
        
        # 创建物流订单
        result = create_shipping_order(shipping_data)
        
        if result.get("result") == "1":
            data = result.get("data", {})
            tracking_4px = data.get("4px_tracking_no", "")
            print(f"\n✅ 物流订单创建成功!")
            print(f"   4PX单号: {tracking_4px}")
            print(f"   DS委托单号: {data.get('ds_consignment_no', 'N/A')}")
            
            # 获取面单
            if tracking_4px:
                label_url = get_label(tracking_4px)
                if label_url:
                    print(f"\n{'='*70}")
                    print(f"📦 订单 {order.get('order_id')} 物流面单已生成")
                    print(f"🔗 面单URL: {label_url}")
                    print(f"{'='*70}")
        else:
            print(f"\n❌ 物流订单创建失败")
            errors = result.get('errors', [])
            for err in errors:
                print(f"   错误: {err.get('error_msg', 'Unknown')}")
    
    print("\n" + "=" * 70)
    print("处理完成")
    print("=" * 70)
