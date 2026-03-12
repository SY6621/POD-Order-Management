"""
验证签名算法 - 对比HTML工具和Python实现
"""
import hashlib
import json

# 测试环境账号
APP_KEY = "5dca6db7-6a21-4d31-a5f8-33a24a4f5b9d"
APP_SECRET = "b8bd24a5-35b0-4e8a-bbc0-c7458e21c7ad"

# 使用HTML工具生成的数据
def generate_sign(method, v, timestamp, body):
    """按照HTML工具的算法生成签名"""
    sign_str = "app_key" + APP_KEY + "formatjson" + "method" + method + "timestamp" + timestamp + "v" + v + body + APP_SECRET
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower(), sign_str

# HTML工具的数据（从截图中获取）
HTML_TIMESTAMP = "1773043935389"
HTML_SIGN = "622a4241dd8b61420f3582068ebfc4f9"

# 业务参数
body_dict = {
    "ref_no": "YIN201803280000002",
    "business_type": "BDS",
    "duty_type": "U",
    "cargo_type": "5",
    "sales_platform": "ebay",
    "logistics_service_info": {
        "logistics_product_code": "F3",
        "customs_service": "N",
        "signature_service": "N"
    },
    "sender": {
        "first_name": "ZHANG_sender",
        "last_name": "YU_sender",
        "company": "fpx_sender",
        "phone": "8956232659",
        "phone2": "18562356856",
        "email": "ZHANGYZ_sender@4PX.COM",
        "post_code": "518000",
        "country": "CN",
        "state": "state_sender",
        "city": "city_sender",
        "street": "street_sender",
        "house_number": "18"
    },
    "recipient_info": {
        "first_name": "ZHANG_recipient",
        "last_name": "YU_recipient",
        "company": "fpx_recipient",
        "phone": "8956232659",
        "phone2": "18562356856",
        "email": "ZHANGYZ_recipient@4PX.COM",
        "post_code": "518000",
        "country": "SG",
        "state": "state_recipient",
        "city": "city_recipient",
        "street": "street_recipient",
        "house_number": "19"
    }
}

# 方法1: 使用 json.dumps 压缩
body1 = json.dumps(body_dict, ensure_ascii=False, separators=(',', ':'))
sign1, sign_str1 = generate_sign("ds.xms.order.create", "1.1.0", HTML_TIMESTAMP, body1)

# 方法2: 使用 eval 模拟HTML工具的JSON处理（HTML工具使用eval）
# HTML工具的 format1 函数会对JSON进行特殊处理
body2 = json.dumps(body_dict, ensure_ascii=False, separators=(',', ':'))
# 注意：HTML工具使用 eval 解析JSON，可能会有细微差别

print("=" * 70)
print("签名算法验证")
print("=" * 70)
print(f"\nHTML工具生成的签名: {HTML_SIGN}")
print(f"Python生成的签名:   {sign1}")
print(f"\n签名是否匹配: {'✅ 匹配' if sign1 == HTML_SIGN else '❌ 不匹配'}")

print(f"\n签名字符串（前100字符）:")
print(sign_str1[:100] + "...")

print(f"\n业务参数JSON:")
print(body1[:150] + "...")

# 检查可能的差异
if sign1 != HTML_SIGN:
    print("\n" + "=" * 70)
    print("签名不匹配的可能原因:")
    print("=" * 70)
    print("1. JSON键值对的顺序不同")
    print("2. 数字类型的处理方式不同（字符串 vs 数字）")
    print("3. 特殊字符的转义方式不同")
    
    # 尝试不同的body格式
    print("\n尝试不同的JSON格式...")
    
    # 方法3: 按照特定键顺序排序
    def sort_dict(d):
        if isinstance(d, dict):
            return {k: sort_dict(v) for k, v in sorted(d.items())}
        elif isinstance(d, list):
            return [sort_dict(item) for item in d]
        return d
    
    body3 = json.dumps(sort_dict(body_dict), ensure_ascii=False, separators=(',', ':'))
    sign3, _ = generate_sign("ds.xms.order.create", "1.1.0", HTML_TIMESTAMP, body3)
    print(f"排序后JSON签名: {sign3} {'✅' if sign3 == HTML_SIGN else '❌'}")
