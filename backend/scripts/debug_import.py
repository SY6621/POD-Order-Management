# -*- coding: utf-8 -*-
"""Debug import issues"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("Step 1: Testing settings import...")
try:
    from src.config.settings import settings
    print(f"  [OK] settings loaded")
    print(f"  TEMPLATES_DIR: {settings.TEMPLATES_DIR}")
    print(f"  FONTS_DIR: {settings.FONTS_DIR}")
except Exception as e:
    print(f"  [ERROR] {e}")

print("\nStep 2: Testing template_service import...")
try:
    from src.services.template_service import TemplateService
    print(f"  [OK] TemplateService class imported")
    ts = TemplateService()
    print(f"  [OK] TemplateService instance created")
except Exception as e:
    print(f"  [ERROR] {e}")
    import traceback
    traceback.print_exc()

print("\nStep 3: Testing effect_image_service import...")
try:
    from src.services.effect_image_service import EffectImageService
    print(f"  [OK] EffectImageService class imported")
    eis = EffectImageService()
    print(f"  [OK] EffectImageService instance created")
except Exception as e:
    print(f"  [ERROR] {e}")
    import traceback
    traceback.print_exc()

print("\nStep 4: Testing template_service instance import...")
try:
    from src.services.template_service import template_service
    print(f"  [OK] template_service instance imported")
except Exception as e:
    print(f"  [ERROR] {e}")
    import traceback
    traceback.print_exc()

print("\nStep 5: Testing effect_image_service instance import...")
try:
    from src.services.effect_image_service import effect_image_service
    print(f"  [OK] effect_image_service instance imported")
except Exception as e:
    print(f"  [ERROR] {e}")
    import traceback
    traceback.print_exc()

print("\n[DONE] Debug completed")