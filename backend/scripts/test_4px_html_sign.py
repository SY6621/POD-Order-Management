"""
4PX API 测试 - 使用 HTML 工具的签名算法

签名规则（来自 sign.js 第111行）：
app_key + AppKey + formatjson + method + method + timestamp + timestamp + v + v + body + AppSecret

实际为：app_key{app_key}formatjsonmethod{method}timestamp{timestamp}v{v}{biz_content}{app_secret}
"""
import hashlib
import json
import time
import requests

# 测试环境账号（来自 api_data.js）
APP_KEY = "5dca6db7-6a21-4d31-a5f8-33a24a4f5b9d"
APP_SECRET = "b8bd24a5-35b0-4e8a-bbc0-c7458e21c7ad"
BASE_URL = "https://open-test.4px.com/router/api/service"


def generate_sign_html(app_key, app_secret, method, v, timestamp, biz_content):
    """
    按照 HTML 工具的算法生成签名
    
    sign.js 第111行：
    var sign = "app_key"+AppKey+"formatjson"+"method"+method+"timestamp"+timestamp+"v"+v+body+AppSecret;
    
    格式：app_key{app_key}formatjsonmethod{method}timestamp{timestamp}v{v}{biz_content}{app_secret}
    """
    # 严格按照 sign.js 第111行的格式拼接
    sign_str = "app_key" + app_key + "formatjson" + "method" + method + "timestamp" + timestamp + "v" + v + biz_content + app_secret
    
    print(f"[Sign String] {sign_str[:150]}...{sign_str[-30:]}")
    
    # MD5 加密，转小写（HTML工具使用 $.md5，通常是小写）
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()
    print(f"[Sign MD5] {sign}")
    
    return sign


def create_order_test():
    """测试创建直发委托单"""
    
    # 构建业务参数
    timestamp = str(int(time.time() * 1000))
    
    order_data = {
        "consignment_no": f"TEST{int(time.time())}",
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
                "sku": "TEST001",
                "quantity": 1,
                "goods_title": "Pet ID Tag",
                "goods_category": "accessories",
                "goods_weight": 50,
                "goods_value": 5.99,
                "currency": "USD"
            }
        ]
    }
    
    # 序列化业务参数
    biz_content = json.dumps(order_data, ensure_ascii=False, separators=(',', ':'))
    print(f"[Biz Content] {biz_content[:200]}...")
    
    # 生成签名
    method = "ds.xms.order.create"
    v = "1.1.0"
    sign = generate_sign_html(APP_KEY, APP_SECRET, method, v, timestamp, biz_content)
    
    # 构建请求参数
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
    
    print(f"\n[Request Data]")
    for k, v in request_data.items():
        if k == "biz_content":
            print(f"  {k}: {v[:100]}...")
        else:
            print(f"  {k}: {v}")
    
    # 发送请求
    print(f"\n[Sending Request to] {BASE_URL}")
    response = requests.post(
        BASE_URL,
        data=request_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30
    )
    
    print(f"[Status Code] {response.status_code}")
    print(f"[Response] {response.text}")
    
    return response.json()


if __name__ == "__main__":
    print("=" * 60)
    print("4PX API 测试 - HTML工具签名算法")
    print("=" * 60)
    print(f"AppKey: {APP_KEY}")
    print(f"AppSecret: {APP_SECRET[:10]}...")
    print()
    
    result = create_order_test()
    
    print("\n" + "=" * 60)
    print("测试结果分析")
    print("=" * 60)
    
    if result.get("result") == "1":
        print("✅ 成功！签名算法正确")
        print(f"请求单号: {result.get('data', {}).get('request_no')}")
        print(f"跟踪号: {result.get('data', {}).get('tracking_no')}")
    else:
        print(f"❌ 失败: {result.get('msg')}")
        print(f"错误码: {result.get('errors')}")
