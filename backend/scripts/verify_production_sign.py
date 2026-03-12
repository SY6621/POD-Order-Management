"""
验证生产环境签名算法
"""
import hashlib
import json
import requests

# 生产环境账号
APP_KEY = "6efa9a05-5e31-4d2a-9a9c-da7624627f26"
APP_SECRET = "0b768497-0c7a-4247-a7c0-0ca20cb2ae16"
BASE_URL = "https://open.4px.com/router/api/service"

# 来自HTML工具的参考数据
HTML_TIMESTAMP = "1773041451799"
HTML_SIGN = "a61cad07bbdbc89fc54291afd49d6113"

# 业务参数JSON（必须完全一致）
BIZ_CONTENT = '{"consignment_no":"ETSY1773041336","logistics_product_code":"PX","destination_country":"US","pieces":1,"weight":50,"receiver":{"first_name":"John","last_name":"Smith","country":"US","state":"CA","city":"Los Angeles","post_code":"90001","address":"123 Test St","phone":"1234567890","email":"test@example.com"},"sender":{"first_name":"Sender","last_name":"Name","country":"CN","state":"Guangdong","city":"Shenzhen","post_code":"518000","address":"Sender Address","phone":"8613800138000"},"parcel_list":[{"sku":"PET001","quantity":1,"goods_title":"Pet ID Tag","goods_category":"accessories","goods_weight":50,"goods_value":5.99,"currency":"USD"}]}'

print("=" * 60)
print("生产环境签名验证")
print("=" * 60)

# 生成签名串
method = "ds.xms.order.create"
v = "1.1.0"

sign_str = "app_key" + APP_KEY + "formatjson" + "method" + method + "timestamp" + HTML_TIMESTAMP + "v" + v + BIZ_CONTENT + APP_SECRET

print(f"\n[签名拼接字符串]")
print(sign_str)

# 计算签名
sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()

print(f"\n[签名结果对比]")
print(f"Python计算: {sign}")
print(f"HTML工具:  {HTML_SIGN}")
print(f"是否一致:  {'✅ 一致' if sign == HTML_SIGN else '❌ 不一致'}")

# 如果一致，用此签名调用API
if sign == HTML_SIGN:
    print("\n" + "=" * 60)
    print("使用HTML工具签名调用API")
    print("=" * 60)
    
    request_data = {
        "app_key": APP_KEY,
        "method": method,
        "v": v,
        "timestamp": HTML_TIMESTAMP,
        "format": "json",
        "sign": HTML_SIGN,
        "language": "cn",
        "biz_content": BIZ_CONTENT
    }
    
    print(f"\n[请求数据]")
    for k, v in request_data.items():
        if k == "biz_content":
            print(f"  {k}: {v[:80]}...")
        else:
            print(f"  {k}: {v}")
    
    response = requests.post(
        BASE_URL,
        data=request_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30
    )
    
    print(f"\n[API响应]")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    result = response.json()
    if result.get("result") == "1":
        print("\n✅ API调用成功！")
        data = result.get("data", {})
        print(f"   请求单号: {data.get('request_no')}")
        print(f"   跟踪号: {data.get('tracking_no')}")
        print(f"   4PX单号: {data.get('fpx_order_no')}")
    else:
        print(f"\n❌ API调用失败: {result.get('msg')}")
        if result.get('errors'):
            for err in result['errors']:
                print(f"   错误: {err.get('error_code')} - {err.get('error_msg')}")
