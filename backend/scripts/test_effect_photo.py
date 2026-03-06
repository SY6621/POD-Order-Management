# -*- coding: utf-8 -*-
"""
测试效果图形状和实拍图动态加载
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.svg_pdf_service import svg_pdf_service
from src.services.shipping_service import OrderData, ShippingLabel


def test_heart_gold():
    """测试心形金色订单"""
    print("=" * 60)
    print("测试：心形金色大号订单")
    print("=" * 60)
    
    # 创建物流信息
    shipping = ShippingLabel(
        tracking_number="PL20260305TEST01",
        recipient_name="MARINELLA NESSO",
        recipient_address="123 Main Street",
        recipient_country="Canada",
        recipient_country_code="CA",
        recipient_state="ON",
        recipient_city="TORONTO",
        recipient_postal_code="M5V 1A1",
    )
    
    # 创建订单数据
    order = OrderData(
        order_id="TEST_HEART_GOLD",
        customer_name="MARINELLA NESSO",
        order_date=datetime.now().strftime("%Y-%m-%d"),
        ship_date=datetime.now().strftime("%Y-%m-%d"),
        shape="心形",  # Heart
        color="金色",  # Gold
        size="大",
        craft="抛光",
        front_text="Luna",
        front_font="F-04",
        back_text="1234567890",
        sku="B-G01B",  # Heart Gold Large
        width_mm=45,
        height_mm=26,
        shipping=shipping,
    )
    
    # 生成 PDF
    pdf_path = svg_pdf_service.generate_pdf(order)
    
    if pdf_path and pdf_path.exists():
        print(f"\n✅ 测试成功!")
        print(f"   PDF: {pdf_path}")
        print(f"   大小: {pdf_path.stat().st_size / 1024:.1f} KB")
        return True
    else:
        print("\n❌ 测试失败!")
        return False


def test_circle_silver():
    """测试圆形银色订单"""
    print("\n" + "=" * 60)
    print("测试：圆形银色大号订单")
    print("=" * 60)
    
    shipping = ShippingLabel(
        tracking_number="PL20260305TEST02",
        recipient_name="John Smith",
        recipient_address="456 Oak Avenue",
        recipient_country="USA",
        recipient_country_code="US",
        recipient_state="CA",
        recipient_city="Los Angeles",
        recipient_postal_code="90001",
    )
    
    order = OrderData(
        order_id="TEST_CIRCLE_SILVER",
        customer_name="John Smith",
        order_date=datetime.now().strftime("%Y-%m-%d"),
        ship_date=datetime.now().strftime("%Y-%m-%d"),
        shape="圆形",  # Circle
        color="银色",  # Silver
        size="大",
        craft="抛光",
        front_text="Max",
        front_font="F-04",
        back_text="9876543210",
        sku="B-C01A",  # Circle Silver Large
        width_mm=32,
        height_mm=32,
        shipping=shipping,
    )
    
    pdf_path = svg_pdf_service.generate_pdf(order)
    
    if pdf_path and pdf_path.exists():
        print(f"\n✅ 测试成功!")
        print(f"   PDF: {pdf_path}")
        print(f"   大小: {pdf_path.stat().st_size / 1024:.1f} KB")
        return True
    else:
        print("\n❌ 测试失败!")
        return False


def test_bone_rosegold():
    """测试骨头形玫瑰金订单"""
    print("\n" + "=" * 60)
    print("测试：骨头形玫瑰金大号订单")
    print("=" * 60)
    
    shipping = ShippingLabel(
        tracking_number="PL20260305TEST03",
        recipient_name="Emma Wilson",
        recipient_address="789 Pine Street",
        recipient_country="UK",
        recipient_country_code="GB",
        recipient_state="London",
        recipient_city="London",
        recipient_postal_code="SW1A 1AA",
    )
    
    order = OrderData(
        order_id="TEST_BONE_ROSEGOLD",
        customer_name="Emma Wilson",
        order_date=datetime.now().strftime("%Y-%m-%d"),
        ship_date=datetime.now().strftime("%Y-%m-%d"),
        shape="骨头形",  # Bone
        color="玫瑰金",  # RoseGold
        size="大",
        craft="抛光",
        front_text="Buddy",
        front_font="F-04",
        back_text="5551234567",
        sku="B-E01C",  # Bone RoseGold Large
        width_mm=45,
        height_mm=26,
        shipping=shipping,
    )
    
    pdf_path = svg_pdf_service.generate_pdf(order)
    
    if pdf_path and pdf_path.exists():
        print(f"\n✅ 测试成功!")
        print(f"   PDF: {pdf_path}")
        print(f"   大小: {pdf_path.stat().st_size / 1024:.1f} KB")
        return True
    else:
        print("\n❌ 测试失败!")
        return False


if __name__ == "__main__":
    results = []
    
    results.append(("心形金色", test_heart_gold()))
    results.append(("圆形银色", test_circle_silver()))
    results.append(("骨头形玫瑰金", test_bone_rosegold()))
    
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {name}: {status}")
    
    passed = sum(1 for _, s in results if s)
    print(f"\n总计: {passed}/{len(results)} 通过")
