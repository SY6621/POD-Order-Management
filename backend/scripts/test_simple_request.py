"""
测试最简单的 4PX API 请求

使用最小化的参数，排除参数格式问题
"""
import requests
import json
import subprocess
import time

app_key = '6efa9a05-5e31-4d2a-9a9c-da7624627f26'
app_secret = '0b768497-0c7a-4247-a7c0-0ca20cb2ae16'

java_exe = r"C:\Program Files\Microsoft\jdk-17.0.18.8-hotspot\bin\java.exe"
sdk_jar = r"C:\Users\Administrator\Downloads\Edge浏览器下载\fpx-api-sdk-1.0.0-SNAPSHOT.jar"
java_dir = r"d:\ETSY_Order_Automation\backend\scripts"

def generate_sign(timestamp, biz_content):
    cmd = [
        java_exe, "-cp", f"{java_dir};{sdk_jar}",
        "SignGenerator", timestamp, biz_content, app_key, app_secret
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return result.stdout.strip()

print("=" * 60)
print("4PX API 最小化测试")
print("=" * 60)

# 使用最简单、最短的参数
timestamp = str(int(time.time() * 1000))
biz_data = {"ref_no": "T1"}  # 最简单的参数
biz_content = json.dumps(biz_data, ensure_ascii=False, separators=(',', ':'))

sign = generate_sign(timestamp, biz_content)

print(f"\n请求参数:")
print(f"  timestamp: {timestamp}")
print(f"  biz_content: {biz_content}")
print(f"  sign: {sign}")

# 构建请求
url = "https://open.4px.com/router/api/service"
data = {
    "app_key": app_key,
    "method": "ds.xms.order.create",
    "v": "1.1.0",
    "timestamp": timestamp,
    "format": "json",
    "sign": sign,
    "language": "cn",
    "biz_content": biz_content
}

print(f"\n发送请求到: {url}")
print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

try:
    response = requests.post(url, data=data, timeout=30)
    print(f"\n状态码: {response.status_code}")
    print(f"响应: {response.text}")
    
    result = response.json()
    if result.get("result") == "1":
        print("\n✅ 请求成功！")
    else:
        print(f"\n❌ 请求失败: {result.get('msg')}")
        if "errors" in result:
            for error in result["errors"]:
                print(f"   错误码: {error.get('error_code')}, 错误信息: {error.get('error_msg')}")
except Exception as e:
    print(f"\n❌ 异常: {e}")

print("\n" + "=" * 60)
