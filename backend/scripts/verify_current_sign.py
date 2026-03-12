"""
验证当前签名算法
"""
import hashlib

# 账号信息
APP_KEY = "6efa9a05-5e31-4d2a-9a9c-da7624627f26"
APP_SECRET = "0b768497-0c7a-4247-a7c0-0ca20cb2ae16"

# HTML工具生成的数据
TIMESTAMP = "1773045728194"
HTML_SIGN = "8400e16709e0b836c89c3036eb4ec0d6"

# JSON字符串（从HTML工具复制）
JSON_STR = '{"ref_no":"ETSYTEST001","business_type":"BDS","duty_type":"U","cargo_type":"5","sales_platform":"etsy","logistics_service_info":{"logistics_product_code":"F3","customs_service":"N","signature_service":"N"},"sender":{"first_name":"Test","last_name":"Sender","company":"ETSY Shop","phone":"8613800138000","email":"test@example.com","post_code":"518000","country":"CN","state":"Guangdong","city":"Shenzhen","street":"Test Street","house_number":"123"},"recipient_info":{"first_name":"John","last_name":"Smith","phone":"1234567890","email":"customer@example.com","post_code":"90001","country":"US","state":"CA","city":"Los Angeles","street":"Customer Street","house_number":"456"}}'

# 构建签名字符串（按照HTML工具的格式）
sign_str = "app_key" + APP_KEY + "formatjson" + "method" + "ds.xms.order.create" + "timestamp" + TIMESTAMP + "v" + "1.1.0" + JSON_STR + APP_SECRET

# 计算MD5签名
python_sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()

print("=" * 60)
print("签名验证")
print("=" * 60)
print(f"\nHTML工具签名: {HTML_SIGN}")
print(f"Python签名:   {python_sign}")
print(f"\n签名是否匹配: {'✅ 匹配!' if python_sign == HTML_SIGN else '❌ 不匹配'}")

if python_sign != HTML_SIGN:
    print("\n签名字符串:")
    print(sign_str)
    print(f"\n签名字符串长度: {len(sign_str)}")
    print(f"MD5输入（前200字符）: {sign_str[:200]}...")
