"""
使用从HTML工具复制的完整URL测试

请在HTML工具中：
1. 选择「生产环境」
2. 填入生产环境的AppKey和AppSecret
3. 填入业务参数
4. 点击「立即生成」
5. 复制「请求URL」
6. 将URL粘贴到下面的 COPIED_URL 变量中
"""
import requests
from urllib.parse import urlparse, parse_qs

# 请将从HTML工具复制的完整URL粘贴到这里
# 格式示例：https://open.4px.com/router/api/service?method=ds.xms.order.create&app_key=...&v=1.1.0&timestamp=...&format=json&sign=...
COPIED_URL = ""  # <-- 请在这里粘贴URL

if not COPIED_URL:
    print("⚠️  请先在代码中粘贴从HTML工具复制的URL")
    print("\n操作步骤：")
    print("1. 在浏览器中打开 HTML工具 (sign.html)")
    print("2. 选择「生产环境」")
    print("3. 填入生产环境的AppKey和AppSecret")
    print("4. 填入业务参数")
    print("5. 点击「立即生成」")
    print("6. 复制「请求URL」")
    print("7. 将URL粘贴到本文件的 COPIED_URL 变量中")
    exit(1)

# 解析URL
parsed = urlparse(COPIED_URL)
base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
params = parse_qs(parsed.query)

# 将参数转换为单值字典（parse_qs返回列表）
request_data = {k: v[0] if len(v) == 1 else v for k, v in params.items()}

print("=" * 60)
print("使用HTML工具生成的URL测试API")
print("=" * 60)
print(f"\nAPI地址: {base_url}")
print(f"\n参数:")
for key, value in request_data.items():
    if key == 'sign':
        print(f"  {key}: {value}")
    elif key == 'biz_content':
        print(f"  {key}: {value[:100]}...")
    else:
        print(f"  {key}: {value}")

# 发送POST请求
response = requests.post(
    base_url,
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
    print(f"4PX单号: {data.get('fpx_order_no')}")
else:
    print(f"\n❌ 失败: {result.get('msg')}")
    errors = result.get('errors', [])
    for err in errors:
        print(f"   错误码: {err.get('error_code')}")
        print(f"   错误信息: {err.get('error_msg')}")
