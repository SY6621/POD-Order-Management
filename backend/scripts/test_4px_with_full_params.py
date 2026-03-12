"""
4PX API 测试 - 使用完整参数（参考在线调试页面的JSON）
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
    """生成签名 - HTML工具算法"""
    sign_str = "app_key" + APP_KEY + "formatjson" + "method" + method + "timestamp" + timestamp + "v" + v + biz_content + APP_SECRET
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()


def create_order():
    """创建订单 - 使用简化但完整的参数"""
    timestamp = str(int(time.time() * 1000))
    
    # 简化但完整的订单参数（参考在线调试页面的JSON结构）
    order_data = {
        "ref_no": f"ETSY{int(time.time())}",
        "business_type": "BDS",
        "duty_type": "U",
        "cargo_type": "5",
        "sales_platform": "etsy",
        "logistics_service_info": {
            "logistics_product_code": "F3",
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
            "street": "Sender Street",
            "house_number": "123"
        },
        "recipient_info": {
            "first_name": "John",
            "last_name": "Smith",
            "company": "",
            "phone": "1234567890",
            "email": "customer@example.com",
            "post_code": "90001",
            "country": "US",
            "state": "CA",
            "city": "Los Angeles",
            "street": "123 Customer St",
            "house_number": "456"
        },
        "parcel_list": [
            {
                "weight": 100,
                "length": 10,
                "width": 10,
                "height": 5,
                "parcel_value": 25.00,
                "currency": "USD",
                "product_list": [
                    {
                        "sku_code": "SKU001",
                        "product_name": "Custom Product",
                        "product_description": "Personalized item",
                        "product_unit_price": 25.00,
                        "currency": "USD",
                        "qty": 1
                    }
                ]
            }
        ]
    }
    
    # 压缩JSON
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
    print("4PX API 测试 - 生产环境（完整参数）")
    print("=" * 60)
    print(f"\n时间戳: {timestamp}")
    print(f"签名: {sign}")
    print(f"\n请求参数预览（前200字符）:")
    print(biz_content[:200] + "...")
    
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
            
        # 分析错误
        if errors:
            error_code = errors[0].get('error_code')
            if error_code == "000012":
                print("\n⚠️  签名验证错误 - 需要检查签名算法")
            elif error_code == "DS000052":
                print("\n⚠️  业务参数错误 - 签名已通过，需要补充参数")
