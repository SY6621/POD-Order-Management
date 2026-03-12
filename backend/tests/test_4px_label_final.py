#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
4PX 物流 API 测试 - 获取面单（标签）
使用正确的参数名 request_no
"""
import sys
sys.path.insert(0, 'd:\\ETSY_Order_Automation\\backend')

from src.services.shipping_service import FourPXClient
import json
import base64

# 你的 4PX 账号
APP_KEY = '6efa9a05-5e31-4d2a-9a9c-da7624627f26'
APP_SECRET = '0b768497-0c7a-4247-a7c0-0ca20cb2ae16'
ORDER_NO = '4PX3002555902331CN'


def test_get_label():
    """测试获取标签 - 使用 request_no 参数"""
    print("=" * 60)
    print("【生产环境】获取物流面单")
    print("=" * 60)
    print(f"订单号: {ORDER_NO}")
    print()
    
    client = FourPXClient(
        app_key=APP_KEY,
        app_secret=APP_SECRET,
        sandbox=False  # 生产环境
    )
    
    # 使用正确的参数名 request_no
    result = client.call_api(
        method="ds.xms.label.get",
        v="1.1.0",
        body={
            "request_no": ORDER_NO,
            "label_type": "1",  # 1-地址标签
            "label_size": "10x10"  # 标签尺寸 10x10cm
        }
    )
    
    print(f"API 结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print()
    
    if result.get('result') == '1':
        print("✅ 获取面单成功！")
        data = result.get('data', {})
        
        # 检查返回的标签数据
        if 'label_url' in data:
            print(f"\n📄 面单URL: {data['label_url']}")
        
        if 'label_content' in data:
            label_content = data['label_content']
            print(f"\n📄 面单内容长度: {len(label_content)} 字符")
            
            # 尝试保存为 PDF 文件
            try:
                # 检查是否是 base64 编码
                if label_content.startswith('data:application/pdf;base64,'):
                    # 提取 base64 数据
                    base64_data = label_content.split(',')[1]
                    pdf_data = base64.b64decode(base64_data)
                    
                    output_path = f'd:/ETSY_Order_Automation/backend/output/label_{ORDER_NO}.pdf'
                    with open(output_path, 'wb') as f:
                        f.write(pdf_data)
                    print(f"✅ 面单已保存: {output_path}")
                    
                elif label_content.startswith('JVBERi0'):  # PDF 文件头
                    pdf_data = base64.b64decode(label_content)
                    output_path = f'd:/ETSY_Order_Automation/backend/output/label_{ORDER_NO}.pdf'
                    with open(output_path, 'wb') as f:
                        f.write(pdf_data)
                    print(f"✅ 面单已保存: {output_path}")
                    
                else:
                    # 可能是图片或其他格式
                    output_path = f'd:/ETSY_Order_Automation/backend/output/label_{ORDER_NO}.txt'
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(label_content)
                    print(f"✅ 面单内容已保存: {output_path}")
                    
            except Exception as e:
                print(f"⚠️ 保存面单时出错: {e}")
                # 保存原始内容
                output_path = f'd:/ETSY_Order_Automation/backend/output/label_{ORDER_NO}.json'
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"✅ 原始数据已保存: {output_path}")
        
        return True
    else:
        print(f"❌ 获取面单失败")
        errors = result.get('errors', [])
        for error in errors:
            print(f"   错误码: {error.get('error_code')}")
            print(f"   错误信息: {error.get('error_msg')}")
        return False


if __name__ == "__main__":
    test_get_label()
