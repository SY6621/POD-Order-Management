"""
4PX 物流 API 测试 - 使用固定签名

测试账号：18820295523 / fpx@123456
物流渠道：美国联邮通优先挂号-普货 (PX)
"""
import sys
import io
import json
import time
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')

from src.config.settings import settings

# API 配置
BASE_URL = "https://open.4px.com/router/api/service"
APP_KEY = settings.FPX_APP_KEY
APP_SECRET = settings.FPX_APP_SECRET

# 在线调试页面生成的签名（针对特定参数）
FIXED_SIGN = "c7a869771903112ce8e57176288699f5"


def create_order_with_fixed_sign():
    """使用固定签名创建订单"""
    print("=" * 60)
    print("4PX 物流 API 测试 - 使用固定签名")
    print("=" * 60)
    
    # 业务参数（必须与生成签名的参数完全一致）
    biz_data = {
        "ref_no": "TEST_SIGN_001",
        "business_type": "BDS",
        "duty_type": "U",
        "cargo_type": "5",
        "attachment_type": "I",  # 随货资料类型：发票
        "logistics_service_info": {
            "logistics_product_code": "PX",
            "customs_service": "N",
            "signature_service": "N"
        },
        "parcel_list": [
            {
                "weight": 50,
                "length": 5.0,
                "width": 3.0,
                "height": 0.5,
                "parcel_value": 10.0,
                "currency": "USD",
                "product_list": [
                    {
                        "sku_code": "PET_TAG_001",
                        "product_name": "Pet ID Tag",
                        "product_description": "Stainless steel pet ID tag",
                        "product_unit_price": 10.0,
                        "currency": "USD",
                        "qty": 1
                    }
                ]
            }
        ],
        "sender": {
            "first_name": "Test",
            "last_name": "Sender",
            "phone": "18820295523",
            "email": "sender@example.com",
            "country": "CN",
            "state": "Guangdong",
            "city": "Shenzhen",
            "post_code": "518000",
            "street": "Test Street 123"
        },
        "recipient_info": {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
            "email": "john.doe@example.com",
            "country": "US",
            "state": "CA",
            "city": "Los Angeles",
            "post_code": "90001",
            "street": "123 Test Street"
        }
    }
    
    # 序列化业务参数
    biz_content = json.dumps(biz_data, ensure_ascii=False, separators=(',', ':'))
    
    # 构建请求数据
    timestamp = str(int(time.time() * 1000))
    
    request_data = {
        "app_key": APP_KEY,
        "method": "ds.xms.order.create",
        "v": "1.1.0",
        "timestamp": timestamp,
        "format": "json",
        "sign": FIXED_SIGN,  # 使用固定签名
        "language": "cn",
        "biz_content": biz_content
    }
    
    print(f"\n[请求参数]")
    print(f"  URL: {BASE_URL}")
    print(f"  Method: ds.xms.order.create")
    print(f"  使用签名: {FIXED_SIGN[:20]}...")
    print(f"  订单号: {biz_data['ref_no']}")
    
    try:
        response = requests.post(
            BASE_URL,
            data=request_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
        
        print(f"\n[响应结果]")
        print(f"  状态码: {response.status_code}")
        
        result = response.json()
        print(f"  结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get("result") == "1":
            print(f"\n✅ 订单创建成功！")
            return result.get("data")
        else:
            print(f"\n❌ 订单创建失败")
            print(f"   错误: {result.get('msg')}")
            if result.get('errors'):
                for err in result['errors']:
                    print(f"   - {err.get('error_msg')} ({err.get('error_code')})")
            return None
            
    except Exception as e:
        print(f"\n❌ 请求异常: {e}")
        return None


if __name__ == "__main__":
    print("4PX 递四方物流 API 测试")
    print("测试账号: 18820295523 / fpx@123456")
    print("固定签名测试\n")
    
    create_order_with_fixed_sign()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
