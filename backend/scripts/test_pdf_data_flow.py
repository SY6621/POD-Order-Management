# -*- coding: utf-8 -*-
"""
测试生产文档PDF生成的数据流
验证前后端字段是否正确对齐
"""

import requests
import json

API_BASE_URL = "http://localhost:8000"

# 测试订单ID（请替换为实际的已完成订单ID）
# 从已完成订单页面获取一个实际订单ID
TEST_ORDER_ID = 1  # 请修改为实际的订单ID

def test_pdf_generation():
    """测试PDF生成API"""
    print("=" * 60)
    print("测试生产文档PDF生成数据流")
    print("=" * 60)
    
    url = f"{API_BASE_URL}/api/pdf/generate-and-upload"
    payload = {"order_id": TEST_ORDER_ID}
    
    print(f"\n请求URL: {url}")
    print(f"请求参数: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"\n响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ PDF生成成功!")
            print(f"PDF URL: {result.get('production_pdf_url')}")
        else:
            print(f"\n❌ PDF生成失败!")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"\n❌ 连接错误: 后端服务未启动或无法访问")
        print(f"错误详情: {e}")
    except Exception as e:
        print(f"\n❌ 请求出错: {e}")

def test_order_data():
    """测试订单数据查询"""
    print("\n" + "=" * 60)
    print("测试订单数据查询")
    print("=" * 60)
    
    # 这里需要直接查询数据库来验证数据结构
    from services.database import db
    
    # 查询订单
    order = db.select_one("orders", {"id": TEST_ORDER_ID})
    if not order:
        print(f"❌ 未找到订单 ID={TEST_ORDER_ID}")
        return
    
    print(f"\n订单基础数据:")
    print(f"  etsy_order_id: {order.get('etsy_order_id')}")
    print(f"  customer_name: {order.get('customer_name')}")
    print(f"  front_text: {order.get('front_text')}")
    print(f"  back_text: {order.get('back_text')}")
    print(f"  sku_id: {order.get('sku_id')}")
    
    # 查询SKU映射
    sku_id = order.get("sku_id")
    if sku_id:
        sku = db.select_one("sku_mapping", {"id": sku_id})
        if sku:
            print(f"\nSKU映射数据:")
            print(f"  sku_code: {sku.get('sku_code')}")
            print(f"  shape: {sku.get('shape')}")
            print(f"  color: {sku.get('color')}")
            print(f"  size: {sku.get('size')}")
            print(f"  craft: {sku.get('craft')}")
        else:
            print(f"\n⚠️ 未找到SKU数据 (sku_id={sku_id})")
    else:
        print(f"\n⚠️ 订单没有关联SKU")
    
    # 查询物流信息
    logistics_list = db.select("logistics", {"order_id": TEST_ORDER_ID})
    if logistics_list:
        logistics = logistics_list[0]
        print(f"\n物流数据:")
        print(f"  recipient_name: {logistics.get('recipient_name')}")
        print(f"  country: {logistics.get('country')}")
        print(f"  tracking_number: {logistics.get('tracking_number')}")
    else:
        print(f"\n⚠️ 未找到物流数据")
    
    # 查询生产文档
    prod_docs = db.select("production_documents", {"order_id": TEST_ORDER_ID})
    if prod_docs:
        doc = prod_docs[0]
        print(f"\n生产文档数据:")
        print(f"  effect_jpg_url: {doc.get('effect_jpg_url', '')[:50]}...")
        print(f"  effect_svg_url: {doc.get('effect_svg_url', '')[:50]}...")
    else:
        print(f"\n⚠️ 未找到生产文档数据")

if __name__ == "__main__":
    # 先测试数据查询
    test_order_data()
    
    # 再测试PDF生成
    print("\n" + "=" * 60)
    print("准备测试PDF生成...")
    print("=" * 60)
    
    # 询问用户是否继续
    user_input = input("\n是否继续测试PDF生成? (y/n): ")
    if user_input.lower() == 'y':
        test_pdf_generation()
    else:
        print("已跳过PDF生成测试")
