# -*- coding: utf-8 -*-
"""PDF generation test script"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.pdf_service import pdf_service


def test_pdf_generation():
    print("=" * 60)
    print("PDF Generation Test")
    print("=" * 60)
    
    # Test data (simulating a parsed order)
    test_order = {
        "order_id": "3891559803",
        "customer_name": "John Smith",
        "order_date": "2026-02-01",
        "shape": "Bone",
        "color": "Gold",
        "size": "Large",
        "front_text": "Max",
        "back_text": "0412345678",
        "font": "F-04",
        "shipping_name": "John Smith",
        "shipping_address": "123 Main Street",
        "shipping_city": "Sydney",
        "shipping_state": "NSW",
        "shipping_postal_code": "2000",
        "shipping_country": "Australia",
        "total_price": "AUD 34.46",
    }
    
    print("\nTest Order Data:")
    print(f"  Order ID: {test_order['order_id']}")
    print(f"  Customer: {test_order['customer_name']}")
    print(f"  Product: {test_order['shape']} {test_order['color']} {test_order['size']}")
    print(f"  Front: {test_order['front_text']}")
    print(f"  Back: {test_order['back_text']}")
    print(f"  Font: {test_order['font']}")
    print(f"  Ship to: {test_order['shipping_city']}, {test_order['shipping_country']}")
    
    print("\nGenerating PDF...")
    result = pdf_service.generate_from_order_data(test_order)
    
    if result:
        print(f"\n[OK] PDF generated successfully!")
        print(f"  Path: {result}")
        print(f"\nPlease open the PDF file to verify the content.")
    else:
        print("\n[ERROR] PDF generation failed")


def test_pdf_with_manual_params():
    print("\n" + "=" * 60)
    print("PDF Generation with Manual Parameters")
    print("=" * 60)
    
    result = pdf_service.generate_production_pdf(
        order_id="TEST002",
        customer_name="Alice Wong",
        order_date="2026-02-02",
        product_info={
            "shape": "Heart",
            "color": "Rose Gold",
            "size": "Small",
        },
        customization={
            "front_text": "Bella",
            "back_text": "I Love You",
            "font": "F-01",
        },
        shipping_address={
            "name": "Alice Wong",
            "address": "456 Queen Street",
            "city": "Melbourne",
            "state": "VIC",
            "postal_code": "3000",
            "country": "Australia",
        },
        total_price="AUD 28.99"
    )
    
    if result:
        print(f"\n[OK] Second PDF generated: {result.name}")
    else:
        print("\n[ERROR] Second PDF generation failed")


def main():
    test_pdf_generation()
    test_pdf_with_manual_params()
    
    print("\n" + "=" * 60)
    print("[OK] All PDF tests completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
