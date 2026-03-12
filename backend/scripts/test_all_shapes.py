# -*- coding: utf-8 -*-
"""
测试效果图形状链接、实拍图动态加载和尺寸标注
验证圆形、心形、骨头形的完整生成流程
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.svg_pdf_service import svg_pdf_service
from src.services.shipping_service import OrderData, ShippingLabel


def create_test_order(
    order_id: str,
    customer_name: str,
    shape: str,
    color: str,
    size: str,
    sku: str,
    front_text: str,
    back_text: str,
) -> OrderData:
    """创建测试订单数据（包含完整信息）"""
    
    # 创建物流标签
    shipping = ShippingLabel()
    shipping.tracking_number = "4PX123456789"
    shipping.recipient_name = customer_name
    shipping.recipient_country = "United States"
    shipping.recipient_country_code = "US"
    shipping.recipient_state = "California"
    shipping.recipient_city = "Los Angeles"
    shipping.recipient_postal_code = "90001"
    shipping.recipient_address = "123 Test Street"
    
    # 创建订单数据
    order = OrderData()
    order.order_id = order_id
    order.customer_name = customer_name
    order.order_date = datetime.now().strftime("%Y-%m-%d")
    order.ship_date = datetime.now().strftime("%Y-%m-%d")
    
    order.shape = shape
    order.color = color
    order.size = size
    order.craft = "抛光"
    
    order.front_text = front_text
    order.front_font = "F-04"
    order.back_text = back_text
    
    order.sku = sku
    order.shipping = shipping
    
    # 根据形状设置尺寸（从 sku_mapping 数据）
    size_data = {
        ("圆形", "L"): (32, 32),
        ("圆形", "S"): (23, 23),
        ("心形", "L"): (32, 30),
        ("心形", "S"): (23, 21),
        ("骨头形", "L"): (45, 26),
        ("骨头形", "S"): (28, 16),
    }
    order.width_mm, order.height_mm = size_data.get((shape, size), (45, 26))
    
    return order


def run_tests():
    """运行所有形状的测试"""
    
    print("=" * 60)
    print("效果图形状链接 + 实拍图动态加载 + 尺寸标注 测试")
    print("=" * 60)
    
    test_cases = [
        # 测试 1: 圆形大号银色（B-C01A）
        {
            "name": "圆形大号银色",
            "order_id": "TEST_CIRCLE_001",
            "customer_name": "John Smith",
            "shape": "圆形",
            "color": "银色",
            "size": "L",
            "sku": "B-C01A",
            "front_text": "Max",
            "back_text": "9876543210",
        },
        # 测试 2: 心形大号金色（B-G01B）
        {
            "name": "心形大号金色",
            "order_id": "TEST_HEART_001",
            "customer_name": "MARINELLA NESSO",
            "shape": "心形",
            "color": "金色",
            "size": "L",
            "sku": "B-G01B",
            "front_text": "Luna",
            "back_text": "1234567890",
        },
        # 测试 3: 骨头形大号玫瑰金（B-E01C）- 测试完整订单信息
        {
            "name": "骨头形大号玫瑰金",
            "order_id": "ORD_3891559803",
            "customer_name": "Alice Johnson",
            "shape": "骨头形",
            "color": "玫瑰金",
            "size": "L",
            "sku": "B-E01C",
            "front_text": "Alice",
            "back_text": "13999926688",
        },
    ]
    
    results = []
    
    for i, tc in enumerate(test_cases, 1):
        print(f"\n{'─' * 40}")
        print(f"测试 {i}: {tc['name']}")
        print(f"{'─' * 40}")
        
        # 创建订单
        order = create_test_order(
            order_id=tc["order_id"],
            customer_name=tc["customer_name"],
            shape=tc["shape"],
            color=tc["color"],
            size=tc["size"],
            sku=tc["sku"],
            front_text=tc["front_text"],
            back_text=tc["back_text"],
        )
        
        # 打印订单信息
        print(f"  订单ID: {order.order_id}")
        print(f"  客户: {order.customer_name}")
        print(f"  形状: {order.shape}")
        print(f"  颜色: {order.color}")
        print(f"  尺寸: {order.size} ({order.width_mm}mm × {order.height_mm}mm)")
        print(f"  SKU: {order.sku}")
        print(f"  正面: {order.front_text}")
        print(f"  背面: {order.back_text}")
        
        # 生成 PDF
        pdf_path = svg_pdf_service.generate_pdf(order)
        
        if pdf_path and pdf_path.exists():
            size_kb = pdf_path.stat().st_size / 1024
            print(f"\n  ✅ PDF 生成成功: {pdf_path.name} ({size_kb:.1f} KB)")
            results.append((tc["name"], True, pdf_path, size_kb))
        else:
            print(f"\n  ❌ PDF 生成失败")
            results.append((tc["name"], False, None, 0))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = 0
    for name, success, path, size in results:
        status = "✅ 通过" if success else "❌ 失败"
        if success:
            passed += 1
            print(f"  {name}: {status} - {path.name} ({size:.1f} KB)")
        else:
            print(f"  {name}: {status}")
    
    print(f"\n总计: {passed}/{len(results)} 测试通过")
    print("=" * 60)
    
    # 打印验证要点
    print("\n验证要点：")
    print("  1. 实拍图：检查左侧区域是否显示对应形状的产品实拍图")
    print("  2. 效果图位置：形状应在黑色框内居中偏上")
    print("  3. 尺寸标注：检查红色标注是否显示正确的尺寸")
    print("  4. 订单信息：检查订单ID和客户名称是否正确显示")
    
    return passed == len(results)


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
