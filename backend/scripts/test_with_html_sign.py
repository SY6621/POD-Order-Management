"""
使用HTML工具生成的签名，通过POST方式调用API
"""
import requests

# 生产环境
APP_KEY = "6efa9a05-5e31-4d2a-9a9c-da7624627f26"
BASE_URL = "https://open.4px.com/router/api/service"

# 来自HTML工具的数据（请更新为最新的）
HTML_TIMESTAMP = "1773042285775"  # 请替换为HTML工具生成的最新时间戳
HTML_SIGN = "6b39dd7bca8e75a2690417f4c74fd223"  # 请替换为HTML工具生成的最新签名
BIZ_CONTENT = '{"consignment_no":"ETSY1773041336","logistics_product_code":"PX","destination_country":"US","pieces":1,"weight":50,"receiver":{"first_name":"John","last_name":"Smith","country":"US","state":"CA","city":"Los Angeles","post_code":"90001","address":"123 Test St","phone":"1234567890","email":"test@example.com"},"sender":{"first_name":"Sender","last_name":"Name","country":"CN","state":"Guangdong","city":"Shenzhen","post_code":"518000","address":"Sender Address","phone":"8613800138000"},"parcel_list":[{"sku":"PET001","quantity":1,"goods_title":"Pet ID Tag","goods_category":"accessories","goods_weight":50,"goods_value":5.99,"currency":"USD"}]}'

request_data = {
    "app_key": APP_KEY,
    "method": "ds.xms.order.create",
    "v": "1.1.0",
    "timestamp": HTML_TIMESTAMP,
    "format": "json",
    "sign": HTML_SIGN,
    "language": "cn",
    "biz_content": BIZ_CONTENT
}

print("=" * 60)
print("使用HTML工具签名通过POST调用")
print("=" * 60)
print(f"\n时间戳: {HTML_TIMESTAMP}")
print(f"签名: {HTML_SIGN}")

response = requests.post(
    BASE_URL,
    data=request_data,
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    timeout=30
)

print(f"\n状态码: {response.status_code}")
print(f"响应: {response.text}")

result = response.json()
if result.get("result") == "1":
    print("\n✅ 成功！")
    data = result.get('data', {})
    print(f"请求单号: {data.get('request_no')}")
    print(f"跟踪号: {data.get('tracking_no')}")
else:
    print(f"\n❌ 失败: {result.get('msg')}")
    if result.get('errors'):
        for err in result['errors']:
            print(f"   错误: {err.get('error_code')} - {err.get('error_msg')}")
