# -*- coding: utf-8 -*-
"""4PX API 修复验证脚本 - 测试后端修复后的参数格式"""

import sys
sys.path.insert(0, '.')

from dotenv import load_dotenv
from pathlib import Path
import json
load_dotenv(Path('.env'))

from src.services.shipping_service import FourPXClient
from src.config.settings import settings

print('=== 4PX API 修复验证 ===')
print(f'APP_KEY: {settings.FOURPX_APP_KEY[:8]}...')
print(f'SANDBOX: {settings.FOURPX_SANDBOX}')

fourpx = FourPXClient(
    app_key=settings.FOURPX_APP_KEY,
    app_secret=settings.FOURPX_APP_SECRET,
    sandbox=settings.FOURPX_SANDBOX
)

# 测试1：模拟后端修复后的参数格式（加拿大订单）
print('\n--- 测试1：模拟修复后的后端参数格式（加拿大） ---')
try:
    # 这是修复后 main.py 构造的参数格式
    weight_kg = 0.027
    weight_g = int(weight_kg * 1000)  # 转换为克
    
    fixed_order = {
        "ref_no": "VERIFY-CA-FIX-001",
        "business_type": "BDS",
        "duty_type": "P",
        "logistics_service_info": {
            "logistics_product_code": "PX"
        },
        "parcel_list": [{
            "weight": weight_g,  # 克（整数）
            "parcel_value": 10,
            "currency": "USD",
            "include_battery": "N",
            "declare_product_info": [{
                "declare_product_name_cn": "不锈钢宠物牌",
                "declare_product_name_en": "Stainless Steel Pet Tag",
                "declare_product_code_qty": "1",
                "declare_unit_price_export": 10,
                "currency_export": "USD",
                "declare_unit_price_import": 10,
                "currency_import": "USD",
                "brand_export": "",
                "brand_import": ""
            }]
        }],
        "is_insure": "N",
        "sender": {
            "first_name": "EtsySeller",
            "company": "Etsy Shop",
            "phone": "13800138000",
            "post_code": "518000",
            "country": "CN",
            "state": "GuangDong",
            "city": "Shenzhen",
            "street": "Nanshan District Road 1"
        },
        "recipient_info": {
            "first_name": "MARINELLA NESSO",
            "phone": "4165559999",  # 隐私处理后的电话
            "email": "test@example.com",
            "country": "CA",
            "state": "ON",
            "city": "Toronto",
            "street": "1 Shaw St 501",
            "post_code": "M6K 0A1"
        },
        "deliver_type_info": {
            "deliver_type": "2"
        }
    }
    
    print("请求参数:")
    print(json.dumps(fixed_order, ensure_ascii=False, indent=2))
    
    result = fourpx.create_order(fixed_order)
    print(f'\n响应结果:')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if result.get('result') == '1':
        data = result.get('data', {})
        print(f'\n✅ 加拿大订单创建成功！')
        print(f'   4PX单号: {data.get("4px_tracking_no")}')
    else:
        error_msg = result.get('errors', [{}])[0].get('error_msg', '')
        print(f'\n❌ 失败: {error_msg}')
except Exception as e:
    print(f'异常: {e}')
    import traceback
    traceback.print_exc()

print('\n' + '='*50)
print('修复总结:')
print('1. logistics_service_info: 改为对象，包含 logistics_product_code')
print('2. sender: 字段名改为 first_name, phone, country 等')
print('3. recipient_info: 字段名改为 first_name, phone, post_code 等')
print('4. weight: 单位从千克改为克（整数）')
print('5. deliver_type_info: 对象包含 deliver_type')
print('6. is_insure: 设置为 "N"')
print('='*50)
