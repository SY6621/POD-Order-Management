"""对比 Python 和 Java SDK 生成的签名"""
import hashlib
import json

app_key = '6efa9a05-5e31-4d2a-9a9c-da7624627f26'
app_secret = '0b768497-0c7a-4247-a7c0-0ca20cb2ae16'
timestamp = '1772943207885'
biz_content = '{"ref_no":"TEST001"}'

# Java SDK 生成的签名
java_sign = '0f7172382be266ff76e546a9ed730b1b'

print("=" * 60)
print("签名对比")
print("=" * 60)
print(f"Java SDK 签名: {java_sign}")

# 尝试不同的 Python 签名算法

# 方式1：SDK 格式（小写）
sign_str1 = f"+app_key{app_key}formatjsonmethodds.xms.order.createtimestamp{timestamp}v1.1.0{biz_content}{app_secret}"
sign1 = hashlib.md5(sign_str1.encode()).hexdigest().lower()
print(f"Python SDK格式: {sign1}")
print(f"  签名串: {sign_str1}")

# 方式2：没有 + 前缀
sign_str2 = f"app_key{app_key}formatjsonmethodds.xms.order.createtimestamp{timestamp}v1.1.0{biz_content}{app_secret}"
sign2 = hashlib.md5(sign_str2.encode()).hexdigest().lower()
print(f"Python 无+前缀: {sign2}")

# 方式3：尝试不同的参数顺序
sign_str3 = f"app_key={app_key}&format=json&method=ds.xms.order.create&timestamp={timestamp}&v=1.1.0&biz_content={biz_content}&app_secret={app_secret}"
sign3 = hashlib.md5(sign_str3.encode()).hexdigest().lower()
print(f"Python key=value: {sign3}")

print("\n" + "=" * 60)
print("结论")
print("=" * 60)
if sign1 == java_sign:
    print("✅ Python SDK 格式与 Java SDK 一致！")
else:
    print("❌ Python SDK 格式与 Java SDK 不一致")
    print("\n必须使用 Java SDK 生成签名")
