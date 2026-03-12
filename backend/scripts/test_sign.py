"""测试 4PX 签名算法"""
import hashlib
import json

# 配置
app_key = '6efa9a05-5e31-4d2a-9a9c-da7624627f26'
app_secret = '0b768497-0c7a-4247-a7c0-0ca20cb2ae16'
app_secret_no_dash = '0b7684970c7a4247a7c00ca20cb2ae16'  # 去掉连字符

# 业务数据
biz_data = {'consignment_no': 'TEST_001'}

print("=" * 60)
print("4PX 签名算法测试")
print("=" * 60)

# 方式1：无空格 JSON
biz_json1 = json.dumps(biz_data, ensure_ascii=False, separators=(',', ':'))
sign1 = hashlib.md5(f'{app_secret}{biz_json1}{app_secret}'.encode()).hexdigest().upper()
print(f"\n方式1 (无空格 JSON):")
print(f"  JSON: {biz_json1}")
print(f"  签名串: {app_secret}{biz_json1}{app_secret}")
print(f"  签名: {sign1}")

# 方式2：有空格 JSON
biz_json2 = json.dumps(biz_data, ensure_ascii=False)
sign2 = hashlib.md5(f'{app_secret}{biz_json2}{app_secret}'.encode()).hexdigest().upper()
print(f"\n方式2 (有空格 JSON):")
print(f"  JSON: {biz_json2}")
print(f"  签名: {sign2}")

# 方式3：AppSecret 去掉连字符
sign3 = hashlib.md5(f'{app_secret_no_dash}{biz_json1}{app_secret_no_dash}'.encode()).hexdigest().upper()
print(f"\n方式3 (AppSecret 去连字符):")
print(f"  Secret: {app_secret_no_dash}")
print(f"  签名: {sign3}")

# 方式4：仅 MD5(biz_content)
sign4 = hashlib.md5(biz_json1.encode()).hexdigest().upper()
print(f"\n方式4 (仅 MD5 JSON):")
print(f"  签名: {sign4}")

# 方式5：MD5(app_key + app_secret + biz_content)
sign5 = hashlib.md5(f'{app_key}{app_secret}{biz_json1}'.encode()).hexdigest().upper()
print(f"\n方式5 (含 app_key):")
print(f"  签名: {sign5}")

print("\n" + "=" * 60)
