"""
验证签名算法 - 使用HTML工具提供的参数
"""
import hashlib
import json

# 来自HTML工具的参数
APP_KEY = "5dca6db7-6a21-4d31-a5f8-33a24a4f5b9d"
APP_SECRET = "b8bd24a5-35b0-4e8a-bbc0-c7458e21c7ad"
TIMESTAMP = "1773040531984"  # HTML工具使用的时间戳
METHOD = "ds.xms.order.create"
V = "1.1.0"

# 业务参数JSON（必须和HTML工具完全一致）
BIZ_CONTENT = '{"consignment_no":"TEST1773040496","logistics_product_code":"PX","destination_country":"US","pieces":1,"weight":50,"receiver":{"first_name":"John","last_name":"Smith","country":"US","state":"CA","city":"Los Angeles","post_code":"90001","address":"123 Test St","phone":"1234567890","email":"test@example.com"},"sender":{"first_name":"Sender","last_name":"Name","country":"CN","state":"Guangdong","city":"Shenzhen","post_code":"518000","address":"Sender Address","phone":"8613800138000"},"parcel_list":[{"sku":"TEST001","quantity":1,"goods_title":"Pet ID Tag","goods_category":"accessories","goods_weight":50,"goods_value":5.99,"currency":"USD"}]}'

# 按照 sign.js 第111行生成签名
sign_str = "app_key" + APP_KEY + "formatjson" + "method" + METHOD + "timestamp" + TIMESTAMP + "v" + V + BIZ_CONTENT + APP_SECRET

print("=" * 60)
print("签名验证测试")
print("=" * 60)
print(f"\n签名拼接字符串:\n{sign_str}\n")

# MD5加密
sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()

print(f"Python生成的签名: {sign}")
print(f"HTML工具生成的签名: f043aaba91258ba794ef9af3a73df47c")
print(f"\n签名是否一致: {'✅ 一致' if sign == 'f043aaba91258ba794ef9af3a73df47c' else '❌ 不一致'}")

# 现在用这个签名调用API
import requests
import time

print("\n" + "=" * 60)
print("使用HTML工具签名调用API")
print("=" * 60)

request_data = {
    "app_key": APP_KEY,
    "method": METHOD,
    "v": V,
    "timestamp": TIMESTAMP,
    "format": "json",
    "sign": "f043aaba91258ba794ef9af3a73df47c",  # 使用HTML工具的签名
    "language": "cn",
    "biz_content": BIZ_CONTENT
}

BASE_URL = "https://open-test.4px.com/router/api/service"

response = requests.post(
    BASE_URL,
    data=request_data,
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    timeout=30
)

print(f"状态码: {response.status_code}")
print(f"响应: {response.text}")

result = response.json()
if result.get("result") == "1":
    print("\n✅ API调用成功！")
    print(f"请求单号: {result.get('data', {}).get('request_no')}")
    print(f"跟踪号: {result.get('data', {}).get('tracking_no')}")
else:
    print(f"\n❌ API调用失败: {result.get('msg')}")
    print(f"错误码: {result.get('errors')}")
