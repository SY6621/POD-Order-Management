#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
4PX API 测试脚本
使用测试环境进行假数据下单测试
"""
import sys
sys.path.insert(0, 'd:\\ETSY_Order_Automation\\backend')

from src.services.shipping_service import FourPXClient
from src.config.settings import settings
import json

def test_4px_create_order():
    """测试4PX创建订单API"""
    print("=" * 60)
    print("4PX API 测试 - 创建订单")
    print("=" * 60)
    
    # 使用测试环境
    client = FourPXClient(
        app_key="5dca6db7-6a21-4d31-a5f8-33a24a4f5b9d",  # 测试环境AppKey
        app_secret="b8bd24a5-35b0-4e8a-bbc0-c7458e21c7ad",  # 测试环境AppSecret
        sandbox=True  # 测试环境
    )
    
    # 构造测试订单数据
    test_order_data = {
        "ref_no": "TEST-ORDER-001",  # 客户参考号（唯一）
        "business_type": "BDS",  # 直发业务类型
        "duty_type": "P",  # 税费承担方式
        "logistics_service_info": {
            "logistics_product_code": "A1"  # 物流产品代码（A1是4PX标准产品）
        },
        "parcel_list": [{
            "weight": 30,  # 重量（克）
            "parcel_value": 9.99,  # 申报价值
            "currency": "USD",  # 币种
            "include_battery": "N",  # 是否带电
            "declare_product_info": [{
                "declare_product_name_cn": "不锈钢宠物牌",
                "declare_product_name_en": "Stainless Steel Pet Tag",
                "declare_product_code_qty": "1",
                "declare_unit_price_export": 9.99,
                "currency_export": "USD",
                "declare_unit_price_import": 9.99,
                "currency_import": "USD",
                "brand_export": "",
                "brand_import": ""
            }]
        }],
        "is_insure": "N",
        "sender": {
            "first_name": "Etsy Seller",
            "company": "Etsy Shop",
            "phone": "13800138000",
            "post_code": "518000",
            "country": "CN",
            "state": "GuangDong",
            "city": "Shenzhen",
            "street": "Nanshan District Road 1"
        },
        "recipient_info": {
            "first_name": "Test Customer",
            "phone": "1234567890",
            "post_code": "2000",
            "country": "AU",  # 澳大利亚
            "state": "NSW",
            "city": "Sydney",
            "street": "123 Test Street"
        },
        "deliver_type_info": {
            "deliver_type": "2"  # 快递到仓
        }
    }
    
    print("\n请求数据:")
    print(json.dumps(test_order_data, ensure_ascii=False, indent=2))
    
    # 调用创建订单API
    print("\n调用 4PX API 创建订单...")
    result = client.create_order(test_order_data)
    
    print("\n响应结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 检查结果
    if result.get("result") == "1":
        print("\n✅ 测试成功！订单创建成功")
        data = result.get("data", {})
        print(f"   4PX单号: {data.get('4px_tracking_no')}")
        print(f"   订单号: {data.get('order_no')}")
        
        # 测试获取面单
        tracking_no = data.get('4px_tracking_no')
        if tracking_no:
            print(f"\n测试获取面单...")
            label_result = client.get_label(tracking_no)
            if label_result.get("result") == "1":
                label_data = label_result.get("data", {})
                label_url_info = label_data.get("label_url_info", {})
                label_url = label_url_info.get("logistics_label")
                print(f"✅ 面单URL: {label_url}")
            else:
                print(f"⚠️ 获取面单失败: {label_result.get('msg')}")
        
        return True
    else:
        print(f"\n❌ 测试失败: {result.get('msg') or result.get('error')}")
        return False

def test_4px_query_order():
    """测试4PX查询订单API"""
    print("\n" + "=" * 60)
    print("4PX API 测试 - 查询订单")
    print("=" * 60)
    
    client = FourPXClient(
        app_key="5dca6db7-6a21-4d31-a5f8-33a24a4f5b9d",
        app_secret="b8bd24a5-35b0-4e8a-bbc0-c7458e21c7ad",
        sandbox=True
    )
    
    # 查询刚才创建的订单
    result = client.query_order("TEST-ORDER-001")
    print("\n查询结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    # 运行测试
    success = test_4px_create_order()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ 测试失败")
        print("=" * 60)
