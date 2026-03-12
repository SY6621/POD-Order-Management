"""
4PX API 测试 - 使用HTML工具生成的签名创建订单并获取PNG面单
"""
import requests
import base64

# 生产环境
BASE_URL = "https://open.4px.com/router/api/service"

# HTML工具生成的最新参数
TIMESTAMP = "1773065921097"
SIGN = "f74028fda55b63abc4c69adc9379a569"
BIZ_CONTENT = '{"ref_no":"ETSY202603092220","business_type":"BDS","duty_type":"U","cargo_type":"5","sales_platform":"etsy","logistics_service_info":{"logistics_product_code":"F3","customs_service":"N","signature_service":"N"},"sender":{"first_name":"ETSY","last_name":"Shop","company":"ETSY Store","phone":"8613800138000","email":"sender@example.com","post_code":"518000","country":"CN","state":"Guangdong","city":"Shenzhen","street":"Sender Street","house_number":"123"},"recipient_info":{"first_name":"John","last_name":"Smith","phone":"1234567890","email":"customer@example.com","post_code":"90001","country":"US","state":"CA","city":"Los Angeles","street":"Customer Street","house_number":"456"},"parcel_list":[{"weight":500,"length":15,"width":10,"height":8,"parcel_value":25,"currency":"USD","product_list":[{"sku_code":"SKU001","product_name":"Custom Product","product_description":"Personalized item","product_unit_price":25,"currency":"USD","qty":1}]}],"label_config_info":{"label_size":"label_100x100","response_label_format":"PNG","create_logistics_label":"Y"}}'

request_data = {
    "method": "ds.xms.order.create",
    "app_key": "6efa9a05-5e31-4d2a-9a9c-da7624627f26",
    "v": "1.1.0",
    "timestamp": TIMESTAMP,
    "format": "json",
    "sign": SIGN,
    "language": "cn",
    "biz_content": BIZ_CONTENT
}

print("=" * 60)
print("4PX API - 使用HTML工具签名创建订单")
print("=" * 60)
print(f"\n时间戳: {TIMESTAMP}")
print(f"签名: {SIGN}")
print(f"面单格式: PNG (10×10cm)")

response = requests.post(
    BASE_URL,
    data=request_data,
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    timeout=30
)

print(f"\n状态码: {response.status_code}")
print(f"响应: {response.text}")

result = response.json()

print("\n" + "=" * 60)
print("结果分析")
print("=" * 60)

if result.get("result") == "1":
    print("\n✅ 订单创建成功！")
    data = result.get('data', {})
    print(f"请求单号: {data.get('request_no')}")
    print(f"4PX单号: {data.get('fpx_order_no')}")
    print(f"跟踪号: {data.get('tracking_no')}")
    
    # 保存面单
    label_url = data.get('label_url')
    if label_url:
        print(f"\n📦 面单URL: {label_url}")
        try:
            print(f"📥 正在下载面单...")
            label_response = requests.get(label_url, timeout=30)
            if label_response.status_code == 200:
                filename = f"d:/ETSY_Order_Automation/backend/output/label_ETSY202603092220.png"
                with open(filename, 'wb') as f:
                    f.write(label_response.content)
                print(f"✅ 面单已保存: {filename}")
                print(f"   文件大小: {len(label_response.content)} bytes")
            else:
                print(f"❌ 下载失败: {label_response.status_code}")
        except Exception as e:
            print(f"❌ 下载异常: {e}")
    
    # 检查base64面单
    label_content = data.get('label_content')
    if label_content:
        try:
            print(f"\n📥 正在保存Base64面单...")
            image_data = base64.b64decode(label_content)
            filename = f"d:/ETSY_Order_Automation/backend/output/label_ETSY202603092220_base64.png"
            with open(filename, 'wb') as f:
                f.write(image_data)
            print(f"✅ 面单已保存: {filename}")
            print(f"   文件大小: {len(image_data)} bytes")
        except Exception as e:
            print(f"❌ 保存异常: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 物流面单生成完成！")
    print("=" * 60)
    print("\n请检查 output 目录下的面单文件")
    
else:
    print(f"\n❌ 失败: {result.get('msg')}")
    errors = result.get('errors', [])
    for err in errors:
        print(f"   错误码: {err.get('error_code')}")
        print(f"   错误信息: {err.get('error_msg')}")
        
    if errors:
        error_code = errors[0].get('error_code')
        if error_code == "000012":
            print("\n⚠️  签名验证错误 - 时间戳已过期，请重新生成")
        elif error_code == "DS000052":
            print("\n✅ 签名验证通过！这是业务参数错误")
