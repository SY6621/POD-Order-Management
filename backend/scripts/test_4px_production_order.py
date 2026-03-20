"""
4PX 物流 API 生产环境下单测试
使用真实账号测试创建直发委托单
"""
import hashlib
import json
import time
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# 生产环境配置
PROD_CONFIG = {
    "app_key": os.getenv("FOURPX_APP_KEY"),
    "app_secret": os.getenv("FOURPX_APP_SECRET"),
    "base_url": "https://open.4px.com/router/api/service"
}

print("=" * 60)
print("4PX 物流 API 生产环境测试")
print("=" * 60)
print(f"App Key: {PROD_CONFIG['app_key'][:8]}...")
print(f"环境: {'测试环境' if os.getenv('FOURPX_SANDBOX') == 'true' else '生产环境'}")
print("=" * 60)

# 检查配置是否完整
if not PROD_CONFIG["app_key"] or not PROD_CONFIG["app_secret"]:
    print("❌ 错误: 4PX API 密钥未配置")
    print("请检查 .env 文件中的 FOURPX_APP_KEY 和 FOURPX_APP_SECRET")
    exit(1)

print("✅ API 密钥已配置")
print("\n" + "=" * 60)

import requests
from typing import Dict, Any, Optional

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
    
    print(f"\n【API 调用】{method}")
    print(f"请求 URL: {url[:120]}...")
    print(f"请求 Body: {body_str[:200]}...")
    
    try:
        response = requests.post(
            url,
            data=body_str,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"响应状态: {response.status_code}")
        return response.json()
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return {"error": str(e)}

# 测试1：查询物流产品（最简单接口）
print("\n【测试1】查询物流产品列表")
result1 = call_4px_api(
    "ds.xms.logistics_product.getlist",
    "1.0.0",
    {
        "country_code": "US",
        "postcode": "10001",
        "transport_mode": "1"  # 1-空运, 2-海运, 3-陆运
    }
)
print(f"响应: {json.dumps(result1, ensure_ascii=False, indent=2)}")

# 提取可用的物流产品代码
available_products = []
if result1.get("result") == "success" and result1.get("data"):
    available_products = [p.get("logistics_product_code") for p in result1["data"]]
    print(f"\n可用的物流产品代码: {available_products}")

# 选择第一个可用的产品
selected_product = available_products[0] if available_products else "PY"

# 测试2：创建直发委托单
print("\n【测试2】创建直发委托单（测试订单）")
order_no = f"TEST{int(time.time())}"
result2 = call_4px_api(
    "ds.xms.order.create",
    "1.1.0",
    {
        "ref_no": order_no,  # 客户参考号，保持唯一
        "business_type": "BDS",  # 直发业务类型
        "duty_type": "P",  # 税费承担方式
        "logistics_service_info": {
            "logistics_product_code": selected_product  # 使用查询到的可用产品
        },
        "sender": {  # 注意：文档用 sender，不是 sender_info
            "first_name": "Sender",
            "phone": "13800138000",
            "post_code": "518000",
            "country": "CN",
            "state": "Guangdong",
            "city": "Shenzhen",
            "street": "Test Address 123"  # 注意：文档用 street，不是 address1
        },
        "recipient_info": {
            "first_name": "Test",
            "phone": "1234567890",
            "post_code": "10001",
            "country": "US",
            "state": "NY",
            "city": "New York",
            "street": "123 Test Street"
        },
        "deliver_type_info": {
            "deliver_type": "2"  # 2:快递到仓
        },
        "parcel_list": [{
            "weight": 10,  # 单位：克
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
)
print(f"响应: {json.dumps(result2, ensure_ascii=False, indent=2)}")

print("\n" + "=" * 60)
if result2.get("result") == "1":  # 4PX API 返回 "1" 表示成功
    print(f"✅ 测试订单创建成功！")
    print(f"客户参考号: {order_no}")
    data = result2.get('data', {})
    tracking_4px = data.get('4px_tracking_no', 'N/A')
    print(f"4PX单号: {tracking_4px}")
    print(f"DS委托单号: {data.get('ds_consignment_no', 'N/A')}")
    
    # 测试3：获取面单（需要等待服务商单号生成）
    print("\n" + "=" * 60)
    print("【测试3】查询订单状态并获取面单")
    
    # 先查询订单，确认服务商单号
    import time as time_module
    print("等待服务商单号生成...")
    time_module.sleep(5)  # 等待5秒
    
    # 查询订单需要时间范围
    from datetime import datetime, timedelta
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    result_query = call_4px_api(
        "ds.xms.order.get",
        "1.1.0",
        {
            "ref_no": order_no,  # 使用客户参考号查询
            "start_time": yesterday,  # 开始时间
            "end_time": today  # 结束时间
        }
    )
    print(f"查询响应: {json.dumps(result_query, ensure_ascii=False, indent=2)[:800]}...")
    
    # 获取面单
    print("\n获取面单...")
    result3 = call_4px_api(
        "ds.xms.label.get",
        "1.1.0",
        {
            "request_no": tracking_4px,  # 使用4PX单号
            "label_type": "1",  # 1-地址标签
            "label_size": "label_100x100"  # 10x10cm
        }
    )
    print(f"响应: {json.dumps(result3, ensure_ascii=False, indent=2)}")
    
    if result3.get("result") == "1":
        label_data = result3.get('data', {})
        # 面单URL在 label_url_info.logistics_label 中
        label_url_info = label_data.get('label_url_info', {})
        label_url = label_url_info.get('logistics_label', '')
        print(f"\n✅ 面单获取成功！")
        print(f"面单URL: {label_url}")
        print(f"面单条码: {label_data.get('label_barcode', 'N/A')}")
    else:
        print(f"\n❌ 面单获取失败")
        print(f"错误: {result3.get('errors', result3.get('msg', 'Unknown'))}")
else:
    print(f"❌ 测试订单创建失败")
    errors = result2.get('errors', [])
    if errors:
        for err in errors:
            print(f"错误码: {err.get('error_code')}")
            print(f"错误信息: {err.get('error_msg')}")
    else:
        print(f"错误信息: {result2.get('msg', 'Unknown')}")
print("\n" + "=" * 60)
