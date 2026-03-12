# -*- coding: utf-8 -*-
"""
测试新的效果图模板 - 生成包含效果图的完整PDF
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.svg_pdf_service import svg_pdf_service
from src.services.shipping_service import OrderData, ShippingLabel


def create_test_order() -> OrderData:
    """创建测试订单数据"""
    
    # 创建物流标签
    shipping = ShippingLabel()
    shipping.tracking_number = "4PX123456789"
    shipping.recipient_name = "Alice Johnson"
    shipping.recipient_country = "United States"
    shipping.recipient_country_code = "US"
    shipping.recipient_state = "California"
    shipping.recipient_city = "Los Angeles"
    shipping.recipient_postal_code = "90001"
    shipping.recipient_address = "123 Test Street"
    
    # 创建订单数据
    order = OrderData()
    order.order_id = "TEST_BONE_001"
    order.customer_name = "Alice Johnson"
    order.order_date = datetime.now().strftime("%Y-%m-%d")
    order.ship_date = datetime.now().strftime("%Y-%m-%d")
    
    order.shape = "骨头形"
    order.color = "玫瑰金"
    order.size = "L"
    order.craft = "抛光"
    
    order.front_text = "Alice"
    order.front_font = "F-04"
    order.back_text = "13999926688"
    
    order.sku = "B-E01C"
    order.shipping = shipping
    
    order.width_mm = 45
    order.height_mm = 26
    
    return order


def main():
    print("=" * 60)
    print("测试新的效果图模板")
    print("=" * 60)
    
    # 创建订单
    order = create_test_order()
    
    print(f"\n订单信息:")
    print(f"  订单ID: {order.order_id}")
    print(f"  客户: {order.customer_name}")
    print(f"  形状: {order.shape}")
    print(f"  颜色: {order.color}")
    print(f"  尺寸: {order.size} ({order.width_mm}mm × {order.height_mm}mm)")
    print(f"  正面: {order.front_text}")
    print(f"  背面: {order.back_text}")
    
    # 生成 PDF
    print(f"\n正在生成PDF...")
    pdf_path = svg_pdf_service.generate_pdf(order)
    
    if pdf_path and pdf_path.exists():
        size_kb = pdf_path.stat().st_size / 1024
        print(f"\n✅ PDF 生成成功!")
        print(f"   文件: {pdf_path.name}")
        print(f"   大小: {size_kb:.1f} KB")
        print(f"   路径: {pdf_path}")
    else:
        print(f"\n❌ PDF 生成失败")
        return False
    
    print("\n" + "=" * 60)
    print("请打开PDF文件查看效果图效果")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
