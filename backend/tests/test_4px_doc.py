#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
4PX 物流 API 测试 - 使用文档中的完整示例
"""
import sys
sys.path.insert(0, 'd:\\ETSY_Order_Automation\\backend')

from src.services.shipping_service import FourPXClient
import json

# 你的 4PX 账号
APP_KEY = '6efa9a05-5e31-4d2a-9a9c-da7624627f26'
APP_SECRET = '0b768497-0c7a-4247-a7c0-0ca20cb2ae16'
CUSTOMER_CODE = '764DW99'

# 使用文档中的示例数据（稍作修改）
order_data = {
    "4px_tracking_no": "",
    "ref_no": "YIN201803280000002",
    "business_type": "BDS",
    "duty_type": "U",
    "cargo_type": "5",
    "vat_no": "8956232323",
    "eori_no": "8956232323",
    "buyer_id": "aliwangwang",
    "sales_platform": "ebay",
    "seller_id": "cainiao",
    "logistics_service_info": {
        "logistics_product_code": "PX",
        "customs_service": "N",
        "signature_service": "N",
        "value_added_services": ""
    },
    "label_barcode": "",
    "return_info": {
        "is_return_on_domestic": "Y",
        "domestic_return_addr": {
            "first_name": "ZHANG_return",
            "last_name": "YU_return",
            "company": "fpx_return",
            "phone": "8956232659",
            "phone2": "18562356856",
            "email": "return_ZHANGYZ@4PX.COM",
            "post_code": "518000",
            "country": "CN",
            "state": "广东省__return",
            "city": "深圳市_return",
            "district": "宝安区_return",
            "street": "财富港大厦D座25楼__return",
            "house_number": "16"
        },
        "is_return_on_oversea": "Y",
        "oversea_return_addr": {
            "first_name": "ZHANG_return_oversea",
            "last_name": "YU_return_oversea",
            "company": "fpx_return_oversea",
            "phone": "8956232659",
            "phone2": "18562356856",
            "email": "ZHANGYZ@4PX_return_oversea.COM",
            "post_code": "518000",
            "country": "CN",
            "state": "state_return_oversea",
            "city": "city_return_oversea",
            "district": "district__return_oversea",
            "street": "street_return_oversea",
            "house_number": "17"
        }
    },
    "parcel_list": [
        {
            "weight": 22,
            "length": 123,
            "width": 789,
            "height": 456,
            "parcel_value": 666.66,
            "currency": "USD",
            "include_battery": "N",
            "battery_type": "",
            "product_list": [
                {
                    "sku_code": "iPhone6  plus_sku_code",
                    "standard_product_barcode": "56323598",
                    "product_name": "iPhone6  plus_product_name",
                    "product_description": "iPhone6  plusiPhone6  plus_product_description",
                    "product_unit_price": 3,
                    "currency": "USD",
                    "qty": 3
                }
            ],
            "declare_product_info": [
                {
                    "declare_product_code": "62323_declare_product_code",
                    "declare_product_name_cn": "手机贴膜_declare_name_cn",
                    "declare_product_name_en": "phone_declare_product_name_en",
                    "uses": "装饰_uses",
                    "specification": "dgd23_specification",
                    "component": "塑料_component",
                    "unit_net_weight": 20,
                    "unit_gross_weight": 45,
                    "material": "565323",
                    "declare_product_code_qty": 2,
                    "unit_declare_product": "个",
                    "origin_country": "中国",
                    "country_export": "越南",
                    "country_import": "新加坡",
                    "hscode_export": "45673576397",
                    "hscode_import": "12332213134",
                    "declare_unit_price_export": 23,
                    "currency_export": "USD",
                    "declare_unit_price_import": 1.25,
                    "currency_import": "USD",
                    "brand_export": "象印",
                    "brand_import": "虎牌",
                    "sales_url": "http://172.16.30.134:8038/loggerMessage/",
                    "package_remarks": "skutest"
                }
            ]
        }
    ],
    "is_insure": "N",
    "insurance_info": {
        "insure_type": "",
        "insure_value": 0,
        "currency": "",
        "insure_person": "",
        "certificate_type": "",
        "certificate_no": "",
        "category_code": "",
        "insure_product_name": "",
        "package_qty": ""
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
        "district": "district_sender",
        "street": "street_sender",
        "house_number": "18",
        "certificate_info": {
            "certificate_type": "PP",
            "certificate_no": "965232323232656532",
            "id_front_url": "https://ju.taobao.com/jusp/other/mingpin/tp.htmbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            "id_back_url": "https://ju.taobao.com/jusp/other/mingpin/tp.htmcccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
        }
    },
    "recipient_info": {
        "first_name": "John",
        "last_name": "Doe",
        "company": "",
        "phone": "1234567890",
        "phone2": "",
        "email": "john.doe@example.com",
        "post_code": "10001",
        "country": "US",
        "state": "NY",
        "city": "New York",
        "district": "Manhattan",
        "street": "123 Main Street",
        "house_number": "Apt 4B",
        "certificate_info": {
            "certificate_type": "",
            "certificate_no": "",
            "id_front_url": "",
            "id_back_url": ""
        }
    },
    "deliver_type_info": {
        "deliver_type": "2",
        "warehouse_code": "",
        "pick_up_info": {
            "expect_pick_up_earliest_time": "1432710115000",
            "expect_pick_up_latest_time": "1432710115000",
            "pick_up_address_info": {
                "first_name": "ZHANG_pick_up",
                "last_name": "YU_pick_up",
                "company": "fpx_pick_up",
                "phone": "8956232659",
                "phone2": "18562356856",
                "email": "ZHANGYZ_pick_up@4PX.COM",
                "post_code": "518000",
                "country": "CN",
                "state": "state_pick_up",
                "city": "city_pick_up",
                "district": "district_pick_up",
                "street": "street_pick_up",
                "house_number": "20"
            }
        },
        "express_to_4px_info": {
            "express_company": "4PXexpress_company",
            "tracking_no": "8956232323"
        },
        "self_send_to_4px_info": {
            "booking_earliest_time": "1432710115000",
            "booking_latest_time": "1432710115000"
        }
    },
    "label_config_info": {
        "label_size": "label_80x90",
        "response_label_format": "PDF",
        "create_logistics_label": "Y",
        "logistics_label_config": {
            "is_print_time": "N",
            "is_print_buyer_id": "N",
            "is_print_pick_info": "N"
        },
        "create_package_label": "Y"
    },
    "order_attachment_info": [
        {
            "attachment_type": "1",
            "attachment_url": ""
        }
    ]
}


def test_with_doc_format():
    """使用文档格式测试"""
    print("=" * 60)
    print("【生产环境】使用文档格式创建订单")
    print("=" * 60)
    print("⚠️  警告：这会在生产环境创建真实订单！")
    print()
    
    client = FourPXClient(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        sandbox=False  # 生产环境
    )
    
    result = client.create_order(order_data)
    
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    if result.get('result') == '1':
        print("✅ 订单创建成功！")
        print(f"4PX 订单号: {result.get('data', {}).get('4px_order_no', 'N/A')}")
    else:
        print(f"❌ 订单创建失败")
    
    return result


if __name__ == "__main__":
    test_with_doc_format()
