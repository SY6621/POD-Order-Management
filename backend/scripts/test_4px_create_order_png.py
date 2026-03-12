"""
4PX API 测试 - 创建订单并获取PNG格式物流面单（10×10cm）
"""
import hashlib
import json
import time
import requests
import base64
from datetime import datetime

# 生产环境账号
APP_KEY = "6efa9a05-5e31-4d2a-9a9c-da7624627f26"
APP_SECRET = "0b768497-0c7a-4247-a7c0-0ca20cb2ae16"
BASE_URL = "https://open.4px.com/router/api/service"


def generate_sign(method, v, timestamp, biz_content):
    """生成签名"""
    sign_str = "app_key" + APP_KEY + "formatjson" + "method" + method + "timestamp" + timestamp + "v" + v + biz_content + APP_SECRET
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()


def create_order():
    """创建直发委托单"""
    timestamp = str(int(time.time() * 1000))
    ref_no = f"ETSY{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # 订单数据（包含PNG面单配置）
    order_data = {
        "ref_no": ref_no,
        "business_type": "BDS",
        "duty_type": "U",
        "cargo_type": "5",
        "sales_platform": "etsy",
        "logistics_service_info": {
            "logistics_product_code": "F3",
            "customs_service": "N",
            "signature_service": "N"
        },
        "sender": {
            "first_name": "ETSY",
            "last_name": "Shop",
            "company": "ETSY Store",
            "phone": "8613800138000",
            "email": "sender@example.com",
            "post_code": "518000",
            "country": "CN",
            "state": "Guangdong",
            "city": "Shenzhen",
            "street": "Sender Street",
            "house_number": "123"
        },
        "recipient_info": {
            "first_name": "John",
            "last_name": "Smith",
            "phone": "1234567890",
            "email": "customer@example.com",
            "post_code": "90001",
            "country": "US",
            "state": "CA",
            "city": "Los Angeles",
            "street": "Customer Street",
            "house_number": "456"
        },
        "parcel_list": [
            {
                "weight": 500,
                "length": 15,
                "width": 10,
                "height": 8,
                "parcel_value": 25.00,
                "currency": "USD",
                "product_list": [
                    {
                        "sku_code": "SKU001",
                        "product_name": "Custom Product",
                        "product_description": "Personalized item",
                        "product_unit_price": 25.00,
                        "currency": "USD",
                        "qty": 1
                    }
                ]
            }
        ],
        # 关键配置：PNG格式面单，10×10cm
        "label_config_info": {
            "label_size": "label_100x100",  # 10×10cm
            "response_label_format": "PNG",  # PNG格式
            "create_logistics_label": "Y"
        }
    }
    
    biz_content = json.dumps(order_data, ensure_ascii=False, separators=(',', ':'))
    method = "ds.xms.order.create"
    v = "1.1.0"
    
    sign = generate_sign(method, v, timestamp, biz_content)
    
    request_data = {
        "app_key": APP_KEY,
        "method": method,
        "v": v,
        "timestamp": timestamp,
        "format": "json",
        "sign": sign,
        "language": "cn",
        "biz_content": biz_content
    }
    
    print("=" * 60)
    print("4PX API - 创建订单（PNG面单 10×10cm）")
    print("=" * 60)
    print(f"\n客户单号: {ref_no}")
    print(f"时间戳: {timestamp}")
    print(f"签名: {sign}")
    
    response = requests.post(
        BASE_URL,
        data=request_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30
    )
    
    print(f"\n状态码: {response.status_code}")
    
    result = response.json()
    
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
            download_label(label_url, ref_no)
        
        # 检查是否有base64编码的面单
        label_content = data.get('label_content')
        if label_content:
            save_base64_label(label_content, ref_no)
        
        return data
    else:
        print(f"\n❌ 失败: {result.get('msg')}")
        errors = result.get('errors', [])
        for err in errors:
            print(f"   错误码: {err.get('error_code')}")
            print(f"   错误信息: {err.get('error_msg')}")
        return None


def download_label(url: str, ref_no: str):
    """下载面单图片"""
    try:
        print(f"\n📥 正在下载面单...")
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            filename = f"d:/ETSY_Order_Automation/backend/output/label_{ref_no}.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ 面单已保存: {filename}")
            print(f"   文件大小: {len(response.content)} bytes")
        else:
            print(f"❌ 下载失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 下载异常: {e}")


def save_base64_label(base64_content: str, ref_no: str):
    """保存base64编码的面单"""
    try:
        print(f"\n📥 正在保存Base64面单...")
        # 解码base64
        image_data = base64.b64decode(base64_content)
        filename = f"d:/ETSY_Order_Automation/backend/output/label_{ref_no}_base64.png"
        with open(filename, 'wb') as f:
            f.write(image_data)
        print(f"✅ 面单已保存: {filename}")
        print(f"   文件大小: {len(image_data)} bytes")
    except Exception as e:
        print(f"❌ 保存异常: {e}")


if __name__ == "__main__":
    result = create_order()
    
    if result:
        print("\n" + "=" * 60)
        print("订单创建完成！")
        print("=" * 60)
        print(f"\n请检查 output 目录下的面单文件")
    else:
        print("\n" + "=" * 60)
        print("订单创建失败")
        print("=" * 60)
