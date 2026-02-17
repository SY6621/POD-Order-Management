# -*- coding: utf-8 -*-
"""Effect image generation test script"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Direct imports to avoid circular dependency
from src.services.template_service import template_service
from src.services.effect_image_service import effect_image_service


def test_template_service():
    print("=" * 60)
    print("Template Service Test")
    print("=" * 60)
    
    test_cases = [
        ("Bone", "Silver", "Large"),
        ("Heart", "Gold", "Small"),
        ("Circle", "Rose Gold", "Large"),
        ("Bone", "Black", "Small"),
    ]
    
    for shape, color, size in test_cases:
        print(f"\nLooking for: {shape} {color} {size}")
        path = template_service.get_template_path(shape, color, size, "F")
        if path:
            print(f"  Front: {path.name}")
        path = template_service.get_template_path(shape, color, size, "B")
        if path:
            print(f"  Back: {path.name}")


def test_effect_image_generation():
    print("\n" + "=" * 60)
    print("Effect Image Generation Test")
    print("=" * 60)
    
    print("\nGenerating effect image...")
    print("  Shape: Bone")
    print("  Color: Silver")
    print("  Size: Large")
    print("  Front text: Max")
    print("  Back text: 0412345678")
    print("  Font: F-04")
    
    result = effect_image_service.generate_effect_svg(
        shape="Bone",
        color="Silver",
        size="Large",
        text_front="Max",
        text_back="0412345678",
        font_code="F-04",
        order_id="TEST001"
    )
    
    if result:
        front_path, back_path = result
        print(f"\n[OK] Effect images generated:")
        print(f"  Front: {front_path}")
        if back_path:
            print(f"  Back: {back_path}")
    else:
        print("\n[ERROR] Failed to generate effect images")


def main():
    test_template_service()
    test_effect_image_generation()
    print("\n" + "=" * 60)
    print("[OK] All tests completed")
    print("=" * 60)


if __name__ == "__main__":
    main()