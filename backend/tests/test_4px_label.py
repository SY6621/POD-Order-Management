#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
4PX 物流 API 测试 - 获取标签
"""
import sys
sys.path.insert(0, 'd:\\ETSY_Order_Automation\\backend')

from src.services.shipping_service import FourPXClient
import json

# 你的 4PX 账号
APP_KEY = '6efa9a05-5e31-4d2a-9a9c-da7624627f26'
APP_SECRET = '0b768497-0c7a-4247-a7c0-0ca20cb2ae16'
ORDER_NO = '4PX3002555902331CN'


def test_get_label():
    """测试获取标签"""
    print("=" * 60)
    print("【生产环境】获取物流标签")
    print("=" * 60)
    print(f"订单号: {ORDER_NO}")
    print()
    
    client = FourPXClient(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        sandbox=False  # 生产环境
    )
    
    # 调用获取标签接口
    # 根据文档，可能需要用 request_no 或 4px_tracking_no
    result = client.get_label(
        order_no=ORDER_NO,
        label_type="1",  # 1-地址标签
        label_size="10x10"  # 标签尺寸
    )
    
    # 如果失败，尝试直接用 call_api 自定义参数
    if result.get('result') != '1':
        print("尝试使用 request_no 参数...")
        result2 = client.call_api(
            method="ds.xms.label.get",
            v="1.1.0",
            body={
                "request_no": ORDER_NO,
                "label_type": "1",
                "label_size": "10x10"
            }
        )
        print(f"使用 request_no 结果: {json.dumps(result2, ensure_ascii=False, indent=2)}")
        if result2.get('result') == '1':
            result = result2
    
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print()
    
    if result.get('result') == '1':
        print("✅ 获取标签成功！")
        data = result.get('data', {})
        if 'label_url' in data:
            print(f"标签URL: {data['label_url']}")
        if 'label_content' in data:
            print(f"标签内容: {data['label_content'][:100]}...")
    else:
        print(f"❌ 获取标签失败: {result.get('errors', '未知错误')}")
    
    return result


if __name__ == "__main__":
    test_get_label()
