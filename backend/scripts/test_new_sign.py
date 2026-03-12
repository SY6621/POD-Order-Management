"""测试新的签名算法"""
import hashlib
import json

app_key = '6efa9a05-5e31-4d2a-9a9c-da7624627f26'
app_secret = '0b768497-0c7a-4247-a7c0-0ca20cb2ae16'

# 测试参数
method = 'ds.xms.order.create'
format_type = 'json'
version = '1.1.0'
timestamp = '1772943207885'  # 固定时间戳测试

biz_data = {
    "ref_no": "TEST_20240304_001",
    "business_type": "BDS"
}
biz_content = json.dumps(biz_data, ensure_ascii=False, separators=(',', ':'))

print("=" * 60)
print("4PX 签名算法测试")
print("=" * 60)

# 方式1：根据提取的格式字符串
# +app_key%sformat%smethod%stimestamp%sv%s%s%s
sign_str1 = f"+app_key{app_key}format{format_type}method{method}timestamp{timestamp}v{version}{biz_content}{app_secret}"
sign1 = hashlib.md5(sign_str1.encode()).hexdigest().upper()
print(f"\n方式1:")
print(f"  签名串: {sign_str1}")
print(f"  签名: {sign1}")

# 方式2：没有 + 前缀
sign_str2 = f"app_key{app_key}format{format_type}method{method}timestamp{timestamp}v{version}{biz_content}{app_secret}"
sign2 = hashlib.md5(sign_str2.encode()).hexdigest().upper()
print(f"\n方式2 (无+前缀):")
print(f"  签名: {sign2}")

# 方式3：尝试不同的顺序
sign_str3 = f"app_key={app_key}&format={format_type}&method={method}&timestamp={timestamp}&v={version}&biz_content={biz_content}&app_secret={app_secret}"
sign3 = hashlib.md5(sign_str3.encode()).hexdigest().upper()
print(f"\n方式3 (key=value&):")
print(f"  签名: {sign3}")

# 方式4：只有 value 没有 key
sign_str4 = f"{app_key}{format_type}{method}{timestamp}{version}{biz_content}{app_secret}"
sign4 = hashlib.md5(sign_str4.encode()).hexdigest().upper()
print(f"\n方式4 (只有value):")
print(f"  签名: {sign4}")

# 方式5：尝试 _ 连接
sign_str5 = f"app_key_{app_key}_format_{format_type}_method_{method}_timestamp_{timestamp}_v_{version}_{biz_content}_{app_secret}"
sign5 = hashlib.md5(sign_str5.encode()).hexdigest().upper()
print(f"\n方式5 (_连接):")
print(f"  签名: {sign5}")

print("\n" + "=" * 60)
