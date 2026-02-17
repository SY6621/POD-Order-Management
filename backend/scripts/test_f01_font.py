# -*- coding: utf-8 -*-
"""Test F-01 font effect image"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.effect_image_service import effect_image_service


def main():
    print("=" * 60)
    print("F-01 Font Effect Test")
    print("=" * 60)
    
    print("\nGenerating effect image...")
    print("  Shape: Bone")
    print("  Color: Gold")
    print("  Size: Large")
    print("  Front text: Alice")
    print("  Back text: 13923266621")
    print("  Font: F-01")
    
    result = effect_image_service.generate_effect_svg(
        shape="Bone",
        color="Gold",
        size="Large",
        text_front="Alice",
        text_back="13923266621",
        font_code="F-01",
        order_id="F01_TEST"
    )
    
    if result:
        front_path, back_path = result
        print(f"\n[OK] Effect images generated:")
        print(f"  Front: {front_path}")
        if back_path:
            print(f"  Back: {back_path}")
        print("\nPlease open the SVG files in browser to preview.")
    else:
        print("\n[ERROR] Failed to generate effect images")


if __name__ == "__main__":
    main()