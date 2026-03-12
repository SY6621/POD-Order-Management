"""
4PX API 测试 - 使用测试环境账号（与HTML工具一致）
"""
import hashlib
import json
import time
import requests

# 测试环境账号（与HTML工具一致）
APP_KEY = "5dca6db7-6a21-4d31-a5f8-33a24a4f5b9d"
APP_SECRET = "b8bd24a5-35b0-4e8a-bbc0-c7458e21c7ad"
BASE_URL = "https://open-test.4px.com/router/api/service"


def generate_sign(method, v, timestamp, biz_content):
    """生成签名"""
    sign_str = "app_key" + APP_KEY + "formatjson" + "method" + method + "timestamp" + timestamp + "v" + v + biz_content + APP_SECRET
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()


def create_order():
    """创建订单"""
    timestamp = str(int(time.time() * 1000))
    
    # 使用与HTML工具相同的参数
    order_data = {
        "ref_no": f"TEST{int(time.time())}",
        "business_type": "BDS",
        "duty_type": "U",
        "cargo_type": "5",
        "sales_platform": "etsy",
        "logistics_service_info": {
            "logistics_product_code": "PX",
            "customs_service": "N",
            "signature_service": "N"
        },
        "sender": {
            "first_name": "Sender",
            "last_name": "Name",
            "company": "ETSY Shop",
            "phone": "8613800138000",
            "email": "sender@example.com",
            "post_code": "518000",
            "country": "CN",
            "state": "Guangdong",
            "city": "Shenzhen",
            "street": "Sender Address"
        },
        "recipient_info": {
            "first_name": "John",
            "last_name": "Smith",
            "company": "",
            "phone": "1234567890",
            "email": "test@example.com",
            "post_code": "90001",
            "country": "US",
            "state": "CA",
            "city": "Los Angeles",
            "street": "123 Test St"
        }
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
    print("4PX API 测试 - 测试环境")
    print("=" * 60)
    print(f"\nAppKey: {APP_KEY}")
    print(f"环境: 测试环境")
    print(f"API地址: {BASE_URL}")
    print(f"\n时间戳: {timestamp}")
    print(f"签名: {sign}")
    
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
