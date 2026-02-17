# -*- coding: utf-8 -*-
"""Test production PDF generation with shipping label"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.shipping_service import shipping_service
from src.services.pdf_service import pdf_service


def test_full_production_pdf():
    print("=" * 60)
    print("Production PDF Generation Test")
    print("=" * 60)
    
    # Test order data (simulating parsed email)
    raw_order = {
        "order_id": "3891559803",
        "customer_name": "John Smith",
        "order_date": "2026-02-01",
        "shape": "Bone",
        "color": "Gold",
        "size": "Large",
        "front_text": "ALice",
        "font": "F-04",
        "back_text": "0412345678",
        "shipping_name": "Trish Weeden",
        "shipping_address": "36 Jubilee Rd",
        "shipping_city": "YOUNGTOWN",
        "shipping_state": "TAS",
        "shipping_postal_code": "7249",
        "shipping_country": "Australia",
    }
    
    print("\n[Step 1] Creating OrderData from raw data...")
    order_data = shipping_service.create_order_data(raw_order)
    print(f"  SKU: {order_data.sku}")
    print(f"  Shape: {order_data.shape} ({order_data.shape_en})")
    print(f"  Color: {order_data.color} ({order_data.color_en})")
    print(f"  Size: {order_data.size} ({order_data.size_en})")
    
    print("\n[Step 2] Creating shipping label...")
    shipping_service.create_shipping_label(order_data)
    print(f"  Tracking: {order_data.shipping.tracking_number}")
    print(f"  Country Code: {order_data.shipping.recipient_country_code}")
    
    print("\n[Step 3] Generating production PDF...")
    result = pdf_service.generate_production_pdf(order_data)
    
    if result:
        print(f"\n[OK] PDF generated: {result}")
        print("\nPlease open the PDF to verify it matches the template:")
        print("  - POD-订单生产文件 title")
        print("  - SKU code (B-E01B)")
        print("  - Three column info section")
        print("  - Product photo + Effect image preview")
        print("  - Shipping label (Postlink format)")
        print("  - Shipping info with red tracking number")
    else:
        print("\n[ERROR] PDF generation failed")


def main():
    test_full_production_pdf()
    print("\n" + "=" * 60)
    print("[DONE] Test completed")
    print("=" * 60)


if __name__ == "__main__":
    main()