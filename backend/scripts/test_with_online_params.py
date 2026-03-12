"""
使用在线调试页面的实际参数测试

思路：如果我能知道在线调试页面使用的完整参数（包括时间戳），
就可以反推出正确的签名算法
"""
import hashlib
import json
import time

app_key = '6efa9a05-5e31-4d2a-9a9c-da7624627f26'
app_secret = '0b768497-0c7a-4247-a7c0-0ca20cb2ae16'

# 在线调试页面可能使用的参数
# 让我们尝试暴力破解时间戳（假设签名是在最近生成的）

biz_data = {"ref_no": "TEST001"}
biz_content = json.dumps(biz_data, ensure_ascii=False, separators=(',', ':'))

print("=" * 60)
print("暴力破解时间戳")
print("=" * 60)

# 当前时间戳
current_ts = int(time.time() * 1000)
print(f"当前时间戳: {current_ts}")

# 尝试最近10分钟的时间戳
found = False
for offset in range(-600000, 600000, 1000):  # 前后10分钟，每秒一个
    ts = str(current_ts + offset)
    
    # SDK 格式
    sign_str = f"+app_key{app_key}formatjsonmethodds.xms.order.createtimestamp{ts}v1.1.0{biz_content}{app_secret}"
    sign = hashlib.md5(sign_str.encode()).hexdigest().lower()
    
    if sign == 'c7a869771903112ce8e57176288699f5':
        print(f"\n✅ 找到匹配！")
        print(f"时间戳: {ts}")
        print(f"签名串: {sign_str}")
        found = True
        break

if not found:
    print("\n❌ 未找到匹配的时间戳")
    print("\n可能原因：")
    print("1. 固定签名是针对不同的参数生成的")
    print("2. 签名算法还有其他未知的部分")
    print("3. 可能需要不同的 biz_content")

print("\n" + "=" * 60)
