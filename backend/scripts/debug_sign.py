"""
调试签名生成过程
"""
import hashlib
import json

# 测试环境账号
APP_KEY = "5dca6db7-6a21-4d31-a5f8-33a24a4f5b9d"
APP_SECRET = "b8bd24a5-35b0-4e8a-bbc0-c7458e21c7ad"

# 来自HTML工具的参考数据
HTML_TIMESTAMP = "1773040531984"
HTML_SIGN = "f043aaba91258ba794ef9af3a73df47c"

# 业务参数
order_data = {
    "consignment_no": "TEST1773040496",
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

# 序列化
biz_content = json.dumps(order_data, ensure_ascii=False, separators=(',', ':'))

print("=" * 60)
print("签名调试")
print("=" * 60)
print(f"\n[业务参数JSON]")
print(biz_content)

# 生成签名串
method = "ds.xms.order.create"
v = "1.1.0"

sign_str = "app_key" + APP_KEY + "formatjson" + "method" + method + "timestamp" + HTML_TIMESTAMP + "v" + v + biz_content + APP_SECRET

print(f"\n[签名拼接字符串]")
print(sign_str)

# 计算签名
sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()

print(f"\n[签名结果]")
print(f"Python计算: {sign}")
print(f"HTML工具:  {HTML_SIGN}")
print(f"是否一致:  {'✅' if sign == HTML_SIGN else '❌'}")

# 如果不同，找出差异
if sign != HTML_SIGN:
    print("\n[差异分析]")
    print(f"长度: Python={len(sign_str)}, 需要对比")
    
    # 检查JSON是否一致
    html_biz_content = '{"consignment_no":"TEST1773040496","logistics_product_code":"PX","destination_country":"US","pieces":1,"weight":50,"receiver":{"first_name":"John","last_name":"Smith","country":"US","state":"CA","city":"Los Angeles","post_code":"90001","address":"123 Test St","phone":"1234567890","email":"test@example.com"},"sender":{"first_name":"Sender","last_name":"Name","country":"CN","state":"Guangdong","city":"Shenzhen","post_code":"518000","address":"Sender Address","phone":"8613800138000"},"parcel_list":[{"sku":"TEST001","quantity":1,"goods_title":"Pet ID Tag","goods_category":"accessories","goods_weight":50,"goods_value":5.99,"currency":"USD"}]}'
    
    print(f"\nJSON对比:")
    print(f"Python: {biz_content}")
    print(f"HTML:   {html_biz_content}")
    print(f"JSON一致: {'✅' if biz_content == html_biz_content else '❌'}")
