"""
4PX API 生产环境实时测试 - 使用当前时间戳
"""
import hashlib
import json
import time
import requests

# 生产环境账号
APP_KEY = "6efa9a05-5e31-4d2a-9a9c-da7624627f26"
APP_SECRET = "0b768497-0c7a-4247-a7c0-0ca20cb2ae16"
BASE_URL = "https://open.4px.com/router/api/service"


def generate_sign(method, v, timestamp, biz_content):
    """生成签名"""
    sign_str = "app_key" + APP_KEY + "formatjson" + "method" + method + "timestamp" + timestamp + "v" + v + biz_content + APP_SECRET
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()


def create_order():
    """创建订单"""
    timestamp = str(int(time.time() * 1000))
    
    order_data = {
        "consignment_no": f"ETSY{int(time.time())}",
        "logistics_product_code": "PX",
        "destination_country": "US",
        "pieces": 1,
        "weight": 50,
        "receiver": {
            "first_name": "John",
            "last_name": "Smith",
            "country": "US",
            "state": "CA",
            "city": "Los Angeles",
            "post_code": "90001",
            "address": "123 Test St",
            "phone": "1234567890",
            "email": "test@example.com"
        },
        "sender": {
            "first_name": "Sender",
            "last_name": "Name",
            "country": "CN",
            "state": "Guangdong",
            "city": "Shenzhen",
            "post_code": "518000",
            "address": "Sender Address",
            "phone": "8613800138000"
        },
        "parcel_list": [
            {
                "sku": "PET001",
                "quantity": 1,
                "goods_title": "Pet ID Tag",
                "goods_category": "accessories",
                "goods_weight": 50,
                "goods_value": 5.99,
                "currency": "USD"
            }
        ]
    }
    
    biz_content = json.dumps(order_data, ensure_ascii=False, separators=(',', ':'))
    method = "ds.xms.order.create"
    v = "1.1.0"
    
    sign = generate_sign(method, v, timestamp, biz_content)
    
    request_data = {
        "app_key": APP_KEY,
        "method": method,
        "v": v,
        "timestamp": timestamp,
        "format": "json",
        "sign": sign,
        "language": "cn",
        "biz_content": biz_content
    }
    
    print("=" * 60)
    print("4PX API 生产环境实时测试")
    print("=" * 60)
    print(f"\n时间戳: {timestamp}")
    print(f"签名: {sign}")
    print(f"\n请求URL: {BASE_URL}")
    
    response = requests.post(
        BASE_URL,
        data=request_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30
    )
    
    print(f"\n状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
    return response.json()


if __name__ == "__main__":
    result = create_order()
    
    print("\n" + "=" * 60)
    print("结果分析")
    print("=" * 60)
    
    if result.get("result") == "1":
        print("✅ 成功！")
        data = result.get('data', {})
        print(f"请求单号: {data.get('request_no')}")
        print(f"跟踪号: {data.get('tracking_no')}")
        print(f"4PX单号: {data.get('fpx_order_no')}")
    else:
        print(f"❌ 失败: {result.get('msg')}")
        errors = result.get('errors', [])
        for err in errors:
            print(f"   错误码: {err.get('error_code')}")
            print(f"   错误信息: {err.get('error_msg')}")
