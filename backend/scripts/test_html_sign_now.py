"""
使用HTML工具生成的最新签名测试API
"""
import requests

# 生产环境
APP_KEY = "6efa9a05-5e31-4d2a-9a9c-da7624627f26"
BASE_URL = "https://open.4px.com/router/api/service"

# 来自HTML工具的最新数据
HTML_TIMESTAMP = "1773043935389"
HTML_SIGN = "622a4241dd8b61420f3582068ebfc4f9"

# 业务参数（与HTML工具完全一致）
BIZ_CONTENT = '{"ref_no":"YIN201803280000002","business_type":"BDS","duty_type":"U","cargo_type":"5","sales_platform":"ebay","logistics_service_info":{"logistics_product_code":"F3","customs_service":"N","signature_service":"N"},"sender":{"first_name":"ZHANG_sender","last_name":"YU_sender","company":"fpx_sender","phone":"8956232659","phone2":"18562356856","email":"ZHANGYZ_sender@4PX.COM","post_code":"518000","country":"CN","state":"state_sender","city":"city_sender","street":"street_sender","house_number":"18"},"recipient_info":{"first_name":"ZHANG_recipient","last_name":"YU_recipient","company":"fpx_recipient","phone":"8956232659","phone2":"18562356856","email":"ZHANGYZ_recipient@4PX.COM","post_code":"518000","country":"SG","state":"state_recipient","city":"city_recipient","street":"street_recipient","house_number":"19"}}'

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
print("使用HTML工具最新签名测试API")
print("=" * 60)
print(f"\n时间戳: {HTML_TIMESTAMP}")
print(f"签名: {HTML_SIGN}")
print(f"\n请求URL: {BASE_URL}")

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
