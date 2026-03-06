# -*- coding: utf-8 -*-
"""
端到端测试：PDF 生成
验证占位符替换是否正确
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.svg_pdf_service import svg_pdf_service
from src.services.shipping_service import shipping_service


def test_pdf_generation():
    """测试 PDF 生成"""
    print("=" * 60)
    print("端到端测试：PDF 生成")
    print("=" * 60)
    
    # 模拟订单数据（使用心形/金色/大号）
    test_order = {
        "etsy_order_id": "3986891868",
        "customer_name": "MARINELLA NESSO",
        "created_at": "2026-03-01T10:00:00",
        
        # 产品信息
        "product_shape": "Heart",
        "product_color": "Gold", 
        "product_size": "Large",
        "product_craft": "抛光",
        
        # 定制内容
        "front_text": "Luna",
        "back_text": "1234567890",
        "font_code": "F-04",
        
        # 物流信息（从 logistics 表合并）
        "recipient_name": "MARINELLA NESSO",
        "street_address": "123 Main Street",
        "city": "TORONTO",
        "state_code": "ON",
        "postal_code": "M5V 1A1",
        "country": "Canada",
        "tracking_number": "PL20260301123456",
    }
    
    print("\n[1] 测试数据:")
    print(f"    订单号: {test_order['etsy_order_id']}")
    print(f"    形状: {test_order['product_shape']}")
    print(f"    颜色: {test_order['product_color']}")
    print(f"    尺寸: {test_order['product_size']}")
    print(f"    正面: {test_order['front_text']}")
    print(f"    背面: {test_order['back_text']}")
    print(f"    收件人: {test_order['recipient_name']}")
    print(f"    国家: {test_order['country']}")
    
    # 转换为 OrderData
    print("\n[2] 转换订单数据...")
    order_data = shipping_service.create_order_data(test_order)
    print(f"    生成的 SKU: {order_data.sku}")
    print(f"    形状（中文）: {order_data.shape}")
    print(f"    颜色（中文）: {order_data.color}")
    print(f"    尺寸（中文）: {order_data.size}")
    
    # 生成 PDF
    print("\n[3] 生成 PDF...")
    pdf_path = svg_pdf_service.generate_pdf(order_data)
    
    if pdf_path and pdf_path.exists():
        print(f"\n[SUCCESS] PDF 生成成功!")
        print(f"    文件路径: {pdf_path}")
        print(f"    文件大小: {pdf_path.stat().st_size / 1024:.1f} KB")
        return True
    else:
        print("\n[FAILED] PDF 生成失败!")
        return False


if __name__ == "__main__":
    success = test_pdf_generation()
    sys.exit(0 if success else 1)
