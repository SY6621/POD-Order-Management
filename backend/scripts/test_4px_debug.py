"""
4PX API 调试测试

测试不同的参数组合，找出签名验证失败的原因
"""
import json
import subprocess
import os

app_key = '6efa9a05-5e31-4d2a-9a9c-da7624627f26'
app_secret = '0b768497-0c7a-4247-a7c0-0ca20cb2ae16'

# Java 路径
java_exe = r"C:\Program Files\Microsoft\jdk-17.0.18.8-hotspot\bin\java.exe"
sdk_jar = r"C:\Users\Administrator\Downloads\Edge浏览器下载\fpx-api-sdk-1.0.0-SNAPSHOT.jar"
java_dir = r"d:\ETSY_Order_Automation\backend\scripts"

def generate_sign(timestamp, biz_content):
    """使用 Java SDK 生成签名"""
    cmd = [
        java_exe,
        "-cp",
        f"{java_dir};{sdk_jar}",
        "SignGenerator",
        timestamp,
        biz_content,
        app_key,
        app_secret
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    if result.returncode != 0:
        print(f"Java 错误: {result.stderr}")
        return None
    return result.stdout.strip()

print("=" * 60)
print("4PX API 调试测试")
print("=" * 60)

# 测试1：最简单的参数
print("\n测试1：最简单参数")
timestamp = "1772943207885"
biz_content = json.dumps({"ref_no": "TEST001"}, ensure_ascii=False, separators=(',', ':'))
sign = generate_sign(timestamp, biz_content)
print(f"biz_content: {biz_content}")
print(f"签名: {sign}")

# 测试2：空参数
print("\n测试2：空参数")
biz_content2 = "{}"
sign2 = generate_sign(timestamp, biz_content2)
print(f"biz_content: {biz_content2}")
print(f"签名: {sign2}")

# 测试3：检查 AppKey 和 AppSecret
print("\n测试3：检查密钥")
print(f"AppKey: {app_key}")
print(f"AppSecret: {app_secret}")
print(f"AppKey 长度: {len(app_key)}")
print(f"AppSecret 长度: {len(app_secret)}")

# 测试4：不同的时间戳
print("\n测试4：不同时间戳")
import time
current_ts = str(int(time.time() * 1000))
print(f"当前时间戳: {current_ts}")
sign4 = generate_sign(current_ts, biz_content)
print(f"签名: {sign4}")

print("\n" + "=" * 60)
print("可能的问题：")
print("1. AppKey/AppSecret 不正确或已被重置")
print("2. 账号未开通 API 权限")
print("3. 需要使用沙箱环境的密钥")
print("4. 请求参数格式不正确")
print("=" * 60)
