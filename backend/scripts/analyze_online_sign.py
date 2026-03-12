"""
分析在线调试页面的签名算法

在线调试显示：
- sign: fe0450f6304bdaf3c0640a8fc984f50a
- timestamp: 1773043181502
- appKey: 6efa9a05-5e31-4d2a-9a9c-da7624627f26
- appSecret: 0b768497-0c7a-4247-a7c0-0ca20cb2ae16
"""
import hashlib
import json

APP_KEY = "6efa9a05-5e31-4d2a-9a9c-da7624627f26"
APP_SECRET = "0b768497-0c7a-4247-a7c0-0ca20cb2ae16"
ONLINE_TIMESTAMP = "1773043181502"
ONLINE_SIGN = "fe0450f6304bdaf3c0640a8fc984f50a"

# 尝试不同的签名算法

print("=" * 60)
print("分析在线调试页面的签名算法")
print("=" * 60)
print(f"\n在线调试签名: {ONLINE_SIGN}")
print(f"时间戳: {ONLINE_TIMESTAMP}")

# 尝试1: HTML工具的算法
method = "ds.xms.order.create"
v = "1.1.0"

# 注意：在线调试使用的是 appKey（驼峰），不是 app_key
# 而且可能使用不同的参数名

# 尝试不同的签名格式
formats_to_try = [
    # 格式1: HTML工具格式（使用app_key）
    f"app_key{APP_KEY}formatjsonmethod{method}timestamp{ONLINE_TIMESTAMP}v{v}",
    # 格式2: 使用appKey（驼峰）
    f"appKey{APP_KEY}formatjsonmethod{method}timestamp{ONLINE_TIMESTAMP}v{v}",
    # 格式3: 只有公共参数（没有biz_content）
    f"app_key{APP_KEY}formatjsonmethod{method}timestamp{ONLINE_TIMESTAMP}v{v}{APP_SECRET}",
    # 格式4: 使用appKey（驼峰）+ appSecret
    f"appKey{APP_KEY}formatjsonmethod{method}timestamp{ONLINE_TIMESTAMP}v{v}{APP_SECRET}",
]

print("\n尝试不同的签名格式（不含biz_content）:")
for i, sign_str in enumerate(formats_to_try, 1):
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()
    match = "✅ 匹配!" if sign == ONLINE_SIGN else "❌ 不匹配"
    print(f"\n格式{i}: {sign_str[:80]}...")
    print(f"  结果: {sign}")
    print(f"  {match}")

# 尝试包含biz_content
# 在线调试使用的是 ref_no 参数结构
biz_content = '{"ref_no":"YIN201803280000002","business_type":"BDS","duty_type":"U","cargo_type":"5","sales_platform":"ebay","logistics_service_info":{"logistics_product_code":"F3","customs_service":"N","signature_service":"N"},"sender":{"first_name":"ZHANG_sender","last_name":"YU_sender","company":"fpx_sender","phone":"8956232659","phone2":"18562356856","email":"ZHANGYZ_sender@4PX.COM","post_code":"518000","country":"CN","state":"state_sender","city":"city_sender","street":"street_sender","house_number":"18"},"recipient_info":{"first_name":"ZHANG_recipient","last_name":"YU_recipient","company":"fpx_recipient","phone":"8956232659","phone2":"18562356856","email":"ZHANGYZ_recipient@4PX.COM","post_code":"518000","country":"SG","state":"state_recipient","city":"city_recipient","street":"street_recipient","house_number":"19"}}'

formats_with_biz = [
    # 格式5: HTML工具格式 + biz_content
    f"app_key{APP_KEY}formatjsonmethod{method}timestamp{ONLINE_TIMESTAMP}v{v}{biz_content}{APP_SECRET}",
    # 格式6: 使用appKey + biz_content
    f"appKey{APP_KEY}formatjsonmethod{method}timestamp{ONLINE_TIMESTAMP}v{v}{biz_content}{APP_SECRET}",
    # 格式7: 只有biz_content + appSecret
    f"{biz_content}{APP_SECRET}",
    # 格式8: appSecret + biz_content + appSecret
    f"{APP_SECRET}{biz_content}{APP_SECRET}",
]

print("\n" + "=" * 60)
print("尝试包含biz_content的签名格式:")
print("=" * 60)

for i, sign_str in enumerate(formats_with_biz, 5):
    sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()
    match = "✅ 匹配!" if sign == ONLINE_SIGN else "❌ 不匹配"
    print(f"\n格式{i}: {sign_str[:100]}...")
    print(f"  结果: {sign}")
    print(f"  {match}")

print("\n" + "=" * 60)
print("结论")
print("=" * 60)
print("如果都不匹配，说明在线调试使用了不同的签名算法")
print("可能需要查看页面源码或联系4PX技术支持")
