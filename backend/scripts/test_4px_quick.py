"""
4PX API 快速测试 - 使用HTML工具生成的最新签名
"""
import requests

# 生产环境
BASE_URL = "https://open.4px.com/router/api/service"

# HTML工具生成的最新参数
request_data = {
    "method": "ds.xms.order.create",
    "app_key": "6efa9a05-5e31-4d2a-9a9c-da7624627f26",
    "v": "1.1.0",
    "timestamp": "1773045728194",
    "format": "json",
    "sign": "8400e16709e0b836c89c3036eb4ec0d6",
    "language": "cn",
    "biz_content": '{"ref_no":"ETSYTEST001","business_type":"BDS","duty_type":"U","cargo_type":"5","sales_platform":"etsy","logistics_service_info":{"logistics_product_code":"F3","customs_service":"N","signature_service":"N"},"sender":{"first_name":"Test","last_name":"Sender","company":"ETSY Shop","phone":"8613800138000","email":"test@example.com","post_code":"518000","country":"CN","state":"Guangdong","city":"Shenzhen","street":"Test Street","house_number":"123"},"recipient_info":{"first_name":"John","last_name":"Smith","phone":"1234567890","email":"customer@example.com","post_code":"90001","country":"US","state":"CA","city":"Los Angeles","street":"Customer Street","house_number":"456"}}'
}

print("=" * 60)
print("4PX API 快速测试")
print("=" * 60)
print(f"时间戳: {request_data['timestamp']}")
print(f"签名: {request_data['sign']}")

response = requests.post(
    BASE_URL,
    data=request_data,
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    timeout=30
)

print(f"\n状态码: {response.status_code}")
print(f"响应: {response.text}")

result = response.json()

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
        
    if errors:
        error_code = errors[0].get('error_code')
        if error_code == "000012":
            print("\n⚠️  签名验证错误 - 时间戳可能已过期")
        elif error_code == "DS000052":
            print("\n✅ 签名验证通过！这是业务参数错误")
