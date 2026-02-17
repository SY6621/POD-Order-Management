"""
对比PDF输出 - 检查当前生成的PDF是否与预期格式一致
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.pdf_service import pdf_service
from src.services.shipping_service import shipping_service

# 模拟订单数据（与你提供的图片一致）
raw_data = {
    "order_id": "3891559803",
    "customer_name": "John Smith",
    "order_date": "2026-02-01",
    "ship_date": "2026-02-03",
    "sku": "B-E01B",
    "shape": "骨头形",
    "color": "金色",
    "size": "大",
    "craft": "激光",
    "front_text": "Alice",
    "front_font": "F-04",
    "back_text": "0412345678",
    "width_mm": "45.0",
    "height_mm": "26.0",
    "recipient_name": "Trish Weeden",
    "recipient_address": "36 Jubilee Rd",
    "recipient_city": "YOUNGTOWN",
    "recipient_state": "TAS",
    "recipient_postal_code": "7249",
    "recipient_country": "Australia",
    "recipient_country_code": "AU"
}

print("=" * 60)
print("PDF格式对比测试")
print("=" * 60)

# 创建订单数据
order_data = shipping_service.create_order_data(raw_data)
shipping_service.create_shipping_label(order_data)

# 生成PDF
pdf_path = pdf_service.generate_production_pdf(order_data)

if pdf_path:
    print(f"\n✅ PDF已生成: {pdf_path}")
    print("\n请检查以下关键元素：")
    print("  1. 标题：POD-订单生产文件（黑色，36pt）")
    print("  2. SKU：B-E01B（红色，24pt）")
    print("  3. 副标题：产品编号 (SKU)（黑色，10pt）")
    print("  4. 三列表格：订单信息 | 产品(SKU)规格 | 定制详情")
    print("  5. 预览区域：外观实拍图 + 效果图预览")
    print("  6. 物流信息：Postlink面单 + 收件人详情")
    print("\n如果以上元素都正确显示，说明PDF格式正常。")
else:
    print("\n❌ PDF生成失败")

print("=" * 60)
