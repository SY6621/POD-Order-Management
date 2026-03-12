"""
对比在线调试页面生成的签名

用户在在线调试页面使用的参数：
- app_key: 6efa9a05-5e31-4d2a-9a9c-da7624627f26
- 固定签名: c7a869771903112ce8e57176288699f5

让我们反推签名算法
"""
import hashlib
import json

app_key = '6efa9a05-5e31-4d2a-9a9c-da7624627f26'
app_secret = '0b768497-0c7a-4247-a7c0-0ca20cb2ae16'
fixed_sign = 'c7a869771903112ce8e57176288699f5'

# 尝试找出在线调试页面使用的 timestamp
# 固定签名对应的可能是某个特定时间戳

# 尝试不同的签名组合
print("=" * 60)
print("尝试反推签名算法")
print("=" * 60)
print(f"固定签名: {fixed_sign}")
print(f"长度: {len(fixed_sign)} (应该是32位MD5)")

# 测试数据（简化版）
biz_data = {"ref_no": "TEST001"}
biz_content = json.dumps(biz_data, ensure_ascii=False, separators=(',', ':'))

# 尝试各种组合
combinations = [
    # 原始格式
    f"{app_secret}{biz_content}{app_secret}",
    # SDK格式
    f"+app_key{app_key}formatjsonmethodds.xms.order.createtimestamp1234567890123v1.1.0{biz_content}{app_secret}",
    # 没有+
    f"app_key{app_key}formatjsonmethodds.xms.order.createtimestamp1234567890123v1.1.0{biz_content}{app_secret}",
    # 不同的顺序
    f"app_key={app_key}&format=json&method=ds.xms.order.create&timestamp=1234567890123&v=1.1.0&biz_content={biz_content}&app_secret={app_secret}",
    # 只有 value
    f"{app_key}jsonds.xms.order.create12345678901231.1.0{biz_content}{app_secret}",
    # 尝试 biz_content 为空
    f"+app_key{app_key}formatjsonmethodds.xms.order.createtimestamp1234567890123v1.1.0{app_secret}",
    # 尝试 URL 编码的 biz_content
    f"+app_key{app_key}formatjsonmethodds.xms.order.createtimestamp1234567890123v1.1.0%7B%7D{app_secret}",
]

print("\n测试不同的签名组合:")
for i, sign_str in enumerate(combinations):
    sign_upper = hashlib.md5(sign_str.encode()).hexdigest().upper()
    sign_lower = hashlib.md5(sign_str.encode()).hexdigest().lower()
    match_upper = "✓" if sign_upper == fixed_sign.upper() else ""
    match_lower = "✓" if sign_lower == fixed_sign else ""
    print(f"\n方式 {i+1}:")
    print(f"  签名串前50字符: {sign_str[:50]}...")
    print(f"  Upper: {sign_upper} {match_upper}")
    print(f"  Lower: {sign_lower} {match_lower}")

print("\n" + "=" * 60)
