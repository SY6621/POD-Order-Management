#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
4PX 物流 API 测试 - 取消订单
"""
import sys
sys.path.insert(0, 'd:\\ETSY_Order_Automation\\backend')

from src.services.shipping_service import FourPXClient
import json

# 你的 4PX 账号
APP_KEY = '6efa9a05-5e31-4d2a-9a9c-da7624627f26'
APP_SECRET = '0b768497-0c7a-4247-a7c0-0ca20cb2ae16'
ORDER_NO = '4PX3002555902331CN'


def test_cancel_order():
    """测试取消订单"""
    print("=" * 60)
    print("【生产环境】取消直发委托单")
    print("=" * 60)
    print(f"订单号: {ORDER_NO}")
    print()
    
    client = FourPXClient(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        sandbox=False  # 生产环境
    )
    
    # 调用取消订单接口
    result = client.call_api(
        method="ds.xms.order.cancel",
        v="1.0.0",
        body={
            "request_no": ORDER_NO,
            "cancel_reason": "测试订单取消"
        }
    )
    
    print(f"API 结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print()
    
    if result.get('result') == '1':
        print("✅ 订单取消成功！")
        return True
    else:
        print(f"❌ 订单取消失败")
        errors = result.get('errors', [])
        for error in errors:
            print(f"   错误码: {error.get('error_code')}")
            print(f"   错误信息: {error.get('error_msg')}")
        
        # 检查是否是已经取消或无法取消的状态
        for error in errors:
            if '已取消' in str(error.get('error_msg', '')):
                print("\n⚠️  订单可能已经被取消或已完成")
        return False


if __name__ == "__main__":
    test_cancel_order()
