# -*- coding: utf-8 -*-
"""测试效果图生成 + 上传到 Supabase Storage"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.database_service import db
from src.services.effect_image_service import effect_image_service

# 订单 3891559803 的真实数据（含背面电话）
order = {
    "id": "a3dc7443-94c5-43a7-bc53-254923228c09",
    "etsy_order_id": "3891559803",
    "product_shape": "Heart",
    "product_color": "Gold",
    "product_size": "Large",
    "front_text": "Spirit 0402 830 481",
    "back_text": "0402 830 481",  # 背面显示电话
    "font_code": "F-01",
}

print("=" * 50)
print("测试：效果图生成 + 上传 Supabase Storage")
print("=" * 50)

result = effect_image_service.generate_and_upload(order)

if result.get("effect_image_url"):
    print(f"\n✅ 全流程成功！")
    print(f"   效果图 URL: {result['effect_image_url']}")
    print(f"\n现在可以在浏览器打开上面的 URL 查看效果图")
else:
    print("\n❌ 流程失败，请查看上方错误信息")
