#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
4PX 物流 API 真实账号测试
使用你的 AppKey 和 AppSecret
"""
import sys
sys.path.insert(0, 'd:\\ETSY_Order_Automation\\backend')

from src.services.shipping_service import FourPXClient

# 你的 4PX 账号
APP_KEY = '6efa9a05-5e31-4d2a-9a9c-da7624627f26'
APP_SECRET = '0b768497-0c7a-4247-a7c0-0ca20cb2ae16'

def test_logistics_products():
    """测试：查询物流产品（不需要 customer_code）"""
    print("=" * 60)
    print("测试1：查询物流产品")
    print("=" * 60)
    
    client = FourPXClient(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        sandbox=True  # 测试环境
    )
    
    result = client.get_logistics_products('US', '10001')
    
    print(f"结果: {result}")
    
    if result.get('result') == '1':
        print("✅ 测试成功！")
    else:
        print(f"❌ 测试失败: {result.get('errors', '未知错误')}")
    
    return result


def test_query_order():
    """测试：查询订单（不需要 customer_code）"""
    print("\n" + "=" * 60)
    print("测试2：查询直发委托单")
    print("=" * 60)
    
    client = FourPXClient(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        sandbox=True
    )
    
    result = client.query_order('TEST123456')
    
    print(f"结果: {result}")
    
    # 这个接口可能会返回订单不存在，但只要不是签名错误就是成功
    errors = result.get('errors', [])
    if errors and any('签名' in str(e) for e in errors):
        print("❌ 签名验证失败")
    else:
        print("✅ API 调用成功（订单不存在是正常的）")
    
    return result


def test_create_order(customer_code: str = None):
    """测试：创建直发委托单（需要 customer_code）"""
    print("\n" + "=" * 60)
    print("测试3：创建直发委托单")
    print("=" * 60)
    
    if not customer_code:
        print("⚠️  需要提供 customer_code 才能测试创建订单")
        print("请在 4PX 后台找到你的客户编码")
        return None
    
    client = FourPXClient(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        sandbox=True
    )
    
    import time
    order_data = {
        "customer_code": customer_code,
        "order_no": f"TEST{int(time.time())}",
        "ref_no": f"REF{int(time.time())}",
        "transport_type": "A",
        "destination_country": "US",
        "destination_postcode": "10001",
        "pieces": 1,
        "weight": 0.5,
        "length": 10,
        "width": 10,
        "height": 5,
        "goods_type": "W",
        "start_consign_time": int(time.time()),
        "declare_goods": [
            {
                "name": "Pet ID Tag",
                "cn_name": "宠物身份牌",
                "quantity": 1,
                "unit_price": 10.0,
                "currency": "USD",
                "weight": 0.5
            }
        ],
        "consignee": {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
            "email": "john@example.com",
            "country": "US",
            "state": "NY",
            "city": "New York",
            "address1": "123 Test St",
            "postcode": "10001"
        }
    }
    
    result = client.create_order(order_data)
    
    print(f"结果: {result}")
    
    if result.get('result') == '1':
        print("✅ 订单创建成功！")
    else:
        print(f"❌ 订单创建失败: {result.get('errors', '未知错误')}")
    
    return result


def test_prod_create_order(customer_code: str):
    """生产环境：创建直发委托单"""
    print("\n" + "=" * 60)
    print("【生产环境】创建直发委托单")
    print("=" * 60)
    print("⚠️  警告：这会在生产环境创建真实订单！")
    print()
    
    client = FourPXClient(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        sandbox=False  # 生产环境
    )
    
    import time
    timestamp = int(time.time())
    order_data = {
        "customer_code": customer_code,
        "order_no": f"ETSY{timestamp}",
        "ref_no": f"REF{timestamp}",
        "business_type": "BDS",
        "duty_type": "DDP",  # 关税类型：DDP-寄件人付税
        "cargo_type": "5",  # 货物类型：5-其他
        "transport_type": "A",
        "destination_country": "US",
        "destination_postcode": "10001",
        "customer_weight": 0.1,
        "forecast_weight": 0.1,
        "pieces": 1,
        "length": 5,
        "width": 4,
        "height": 0.5,
        "goods_type": "W",
        "start_consign_time": timestamp,
        "logistics_service_info": {
            "logistics_product_code": "F3"  # 物流产品代码
        },
        "parcel_list": [
            {
                "customer_weight": 0.1,
                "weight": 0.1,
                "forecast_weight": 0.1,
                "length": 5,
                "width": 4,
                "height": 0.5,
                "parcel_value": 9.99,
                "currency": "USD",
                "product_list": [
                    {
                        "sku_code": "PET-TAG-001",
                        "product_name": "Pet ID Tag",
                        "product_name_cn": "宠物身份牌",
                        "qty": 1,
                        "product_unit_price": 9.99,
                        "currency": "USD"
                    }
                ],
                "declare_product_info": [
                    {
                        "declare_product_code": "PET001",
                        "declare_product_name_cn": "宠物身份牌",
                        "declare_product_name_en": "Pet ID Tag",
                        "declare_product_code_qty": 1,
                        "unit_declare_product": "个",
                        "origin_country": "CN",
                        "declare_unit_price_export": 9.99,
                        "currency_export": "USD",
                        "declare_unit_price_import": 9.99,
                        "currency_import": "USD"
                    }
                ]
            }
        ],
        "sender": {
            "first_name": "Sender",
            "last_name": "Name",
            "company": "ETSY Shop",
            "phone": "8613800138000",
            "email": "sender@example.com",
            "country": "CN",
            "state": "Guangdong",
            "city": "Shenzhen",
            "district": "Baoan",
            "street": "Test Street",
            "post_code": "518000"
        },
        "recipient_info": {
            "first_name": "Test",
            "last_name": "User",
            "company": "",
            "phone": "1234567890",
            "email": "test@example.com",
            "country": "US",
            "state": "CA",
            "city": "Los Angeles",
            "district": "",
            "street": "123 Test Street",
            "post_code": "90001"
        },
        "deliver_type_info": {
            "deliver_type": "1"  # 1-上门揽收, 2-快递到仓, 3-自送到仓
        }
    }
    
    print(f"订单号: {order_data['order_no']}")
    print(f"客户编码: {customer_code}")
    print()
    
    result = client.create_order(order_data)
    
    print(f"结果: {result}")
    
    if result.get('result') == '1':
        print("✅ 订单创建成功！")
        print(f"4PX 订单号: {result.get('data', {}).get('4px_order_no', 'N/A')}")
    else:
        print(f"❌ 订单创建失败: {result.get('errors', '未知错误')}")
    
    return result


if __name__ == "__main__":
    print("4PX 物流 API 生产环境测试")
    print(f"AppKey: {APP_KEY[:8]}...{APP_KEY[-8:]}")
    print()
    
    # 获取 customer_code
    import sys
    if len(sys.argv) > 1:
        customer_code = sys.argv[1]
        test_prod_create_order(customer_code)
    else:
        print("用法: python test_4px_real.py <customer_code>")
        print()
        print("请提供你的 4PX 客户编码（customer_code）")
        print("可以在 4PX 后台首页或账户信息页面找到")
        
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
