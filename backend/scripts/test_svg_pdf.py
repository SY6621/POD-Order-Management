# -*- coding: utf-8 -*-
"""
Test SVG template to PDF generation
Pixel-perfect PDF based on SVG template
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.svg_pdf_service import svg_pdf_service
from src.services.shipping_service import shipping_service

def test_svg_pdf():
    """Test SVG-based PDF generation"""
    
    print("=" * 60)
    print("SVG Template PDF Test")
    print("=" * 60)
    
    # Test data matching template
    raw_data = {
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
    
    # Create order data
    print("\n[Step 1] Creating order data...")
    order_data = shipping_service.create_order_data(raw_data)
    print(f"  Order ID: {order_data.order_id}")
    print(f"  SKU: {order_data.sku}")
    print(f"  Shape: {order_data.shape}")
    print(f"  Color: {order_data.color}")
    
    # Create shipping label
    print("\n[Step 2] Creating shipping label...")
    shipping_service.create_shipping_label(order_data)
    print(f"  Tracking: {order_data.shipping.tracking_number}")
    
    # Generate PDF
    print("\n[Step 3] Generating PDF from SVG template...")
    pdf_path = svg_pdf_service.generate_pdf(order_data)
    
    if pdf_path and pdf_path.exists():
        print(f"\n[SUCCESS] PDF created: {pdf_path}")
        print(f"  File size: {pdf_path.stat().st_size} bytes")
        print("\nPlease open the PDF to verify pixel-perfect layout!")
    else:
        print("\n[FAILED] PDF generation failed")
        return False
    
    print("\n" + "=" * 60)
    print("[DONE] Test completed")
    print("=" * 60)
    return True


if __name__ == "__main__":
    test_svg_pdf()
