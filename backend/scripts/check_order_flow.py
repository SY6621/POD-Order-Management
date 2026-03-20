# -*- coding: utf-8 -*-
"""
检查订单在各流转阶段的数据完整性
按照ETSY订单完整流转流程检查
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from services.database import db

# 测试订单ID
TEST_ORDER_ID = 103  # 根据截图中的订单 PO-202602-103

def check_order_flow():
    """检查订单在各阶段的数据完整性"""
    
    print("=" * 70)
    print("ETSY订单流转数据完整性检查")
    print("=" * 70)
    
    # 1. 查询订单基础数据 (orders表)
    print("\n【阶段1】订单基础数据 (orders表)")
    print("-" * 50)
    
    order = db.select_one("orders", {"id": TEST_ORDER_ID})
    if not order:
        # 尝试用 etsy_order_id 查询
        orders = db.select("orders", {}, limit=10)
        for o in orders:
            if 'PO-202602-103' in str(o.get('etsy_order_id', '')):
                order = o
                TEST_ORDER_ID = o['id']
                break
    
    if not order:
        print(f"❌ 未找到订单 ID={TEST_ORDER_ID}")
        # 列出所有订单
        print("\n系统中存在的订单:")
        all_orders = db.select("orders", {}, limit=5)
        for o in all_orders:
            print(f"  ID: {o.get('id')}, etsy_order_id: {o.get('etsy_order_id')}, status: {o.get('status')}")
        return
    
    print(f"✅ 找到订单")
    print(f"  数据库ID: {order.get('id')}")
    print(f"  Etsy订单号: {order.get('etsy_order_id')}")
    print(f"  状态: {order.get('status')}")
    print(f"  客户名: {order.get('customer_name')}")
    print(f"  正面文字: {order.get('front_text')}")
    print(f"  背面文字: {order.get('back_text')}")
    print(f"  sku_id: {order.get('sku_id')}")
    print(f"  effect_image_url: {order.get('effect_image_url')}")
    print(f"  production_pdf_url: {order.get('production_pdf_url')}")
    
    # 2. 检查SKU映射数据 (sku_mapping表)
    print("\n【阶段2】SKU映射数据 (sku_mapping表)")
    print("-" * 50)
    
    sku_id = order.get("sku_id")
    if sku_id:
        sku = db.select_one("sku_mapping", {"id": sku_id})
        if sku:
            print(f"✅ 找到SKU映射")
            print(f"  sku_code: {sku.get('sku_code')}")
            print(f"  shape: {sku.get('shape')}")
            print(f"  color: {sku.get('color')}")
            print(f"  size: {sku.get('size')}")
            print(f"  craft: {sku.get('craft')}")
        else:
            print(f"❌ 未找到SKU数据 (sku_id={sku_id})")
    else:
        print(f"❌ 订单没有关联sku_id")
        # 尝试通过其他方式查找SKU
        print("\n  尝试查找匹配的SKU...")
        all_skus = db.select("sku_mapping", {}, limit=3)
        print(f"  系统中存在 {len(all_skus)} 个SKU映射")
        for s in all_skus:
            print(f"    {s.get('sku_code')}: shape={s.get('shape')}, color={s.get('color')}, size={s.get('size')}")
    
    # 3. 检查物流数据 (logistics表)
    print("\n【阶段3】物流数据 (logistics表)")
    print("-" * 50)
    
    logistics_list = db.select("logistics", {"order_id": TEST_ORDER_ID})
    if logistics_list:
        logistics = logistics_list[0]
        print(f"✅ 找到物流数据")
        print(f"  id: {logistics.get('id')}")
        print(f"  tracking_number: {logistics.get('tracking_number')}")
        print(f"  recipient_name: {logistics.get('recipient_name')}")
        print(f"  country: {logistics.get('country')}")
        print(f"  city: {logistics.get('city')}")
        print(f"  state_code: {logistics.get('state_code')}")
        print(f"  postal_code: {logistics.get('postal_code')}")
        print(f"  street_address: {logistics.get('street_address')}")
    else:
        print(f"❌ 未找到物流数据")
    
    # 4. 检查生产文档数据 (production_documents表)
    print("\n【阶段4】生产文档数据 (production_documents表)")
    print("-" * 50)
    
    prod_docs = db.select("production_documents", {"order_id": TEST_ORDER_ID})
    if prod_docs:
        doc = prod_docs[0]
        print(f"✅ 找到生产文档数据")
        print(f"  id: {doc.get('id')}")
        print(f"  effect_svg_url: {doc.get('effect_svg_url', '')[:60]}...")
        print(f"  effect_jpg_url: {doc.get('effect_jpg_url', '')[:60]}...")
        print(f"  real_photo_urls: {doc.get('real_photo_urls', '')[:60]}...")
    else:
        print(f"❌ 未找到生产文档数据")
        print("  说明：效果图设计器生成的SVG未保存到数据库")
    
    # 5. 总结数据完整性
    print("\n" + "=" * 70)
    print("数据完整性总结")
    print("=" * 70)
    
    checks = [
        ("订单基础数据", order is not None),
        ("SKU映射数据", sku_id and db.select_one("sku_mapping", {"id": sku_id})),
        ("物流数据", len(logistics_list) > 0),
        ("生产文档数据", len(prod_docs) > 0),
    ]
    
    for name, status in checks:
        icon = "✅" if status else "❌"
        print(f"{icon} {name}")
    
    print("\n【问题分析】")
    missing = [name for name, status in checks if not status]
    if missing:
        print(f"缺失数据: {', '.join(missing)}")
        print("\n【解决方案】")
        if "SKU映射数据" in missing:
            print("1. 为订单设置正确的 sku_id")
        if "物流数据" in missing:
            print("2. 在【物流下单】页面为该订单创建物流运单")
        if "生产文档数据" in missing:
            print("3. 在【待确认订单】页面生成效果图并保存")
    else:
        print("✅ 所有数据完整，可以正常生成生产文档PDF")

if __name__ == "__main__":
    check_order_flow()
