# -*- coding: utf-8 -*-
"""
检查订单在各流转阶段的数据完整性 - 使用Supabase直接查询
"""

from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# 初始化Supabase客户端
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_SERVICE_KEY')
supabase = create_client(url, key)

def check_order_flow():
    """检查订单在各阶段的数据完整性"""
    
    print("=" * 70)
    print("ETSY订单流转数据完整性检查")
    print("=" * 70)
    
    # 查找订单 PO-202602-103
    print("\n【阶段1】查找订单 (orders表)")
    print("-" * 50)
    
    result = supabase.table('orders').select('*').ilike('etsy_order_id', '%PO-202602-103%').execute()
    
    if not result.data:
        print("❌ 未找到订单 PO-202602-103")
        # 列出所有订单
        all_orders = supabase.table('orders').select('id, etsy_order_id, status, customer_name').limit(5).execute()
        print("\n系统中存在的订单:")
        for o in all_orders.data:
            print(f"  ID: {o.get('id')}, 订单号: {o.get('etsy_order_id')}, 状态: {o.get('status')}, 客户: {o.get('customer_name')}")
        return
    
    order = result.data[0]
    order_id = order['id']
    
    print(f"✅ 找到订单")
    print(f"  数据库ID: {order_id}")
    print(f"  Etsy订单号: {order.get('etsy_order_id')}")
    print(f"  状态: {order.get('status')}")
    print(f"  客户名: {order.get('customer_name')}")
    print(f"  正面文字: {order.get('front_text')}")
    print(f"  背面文字: {order.get('back_text')}")
    print(f"  sku_id: {order.get('sku_id')}")
    print(f"  effect_image_url: {order.get('effect_image_url')}")
    
    # 2. 检查SKU映射数据
    print("\n【阶段2】SKU映射数据 (sku_mapping表)")
    print("-" * 50)
    
    sku_id = order.get("sku_id")
    if sku_id:
        sku_result = supabase.table('sku_mapping').select('*').eq('id', sku_id).execute()
        if sku_result.data:
            sku = sku_result.data[0]
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
        # 显示可用的SKU
        skus_result = supabase.table('sku_mapping').select('sku_code, shape, color, size').limit(3).execute()
        print(f"\n  系统中可用的SKU映射:")
        for s in skus_result.data:
            print(f"    {s.get('sku_code')}: shape={s.get('shape')}, color={s.get('color')}, size={s.get('size')}")
    
    # 3. 检查物流数据
    print("\n【阶段3】物流数据 (logistics表)")
    print("-" * 50)
    
    logistics_result = supabase.table('logistics').select('*').eq('order_id', order_id).execute()
    if logistics_result.data:
        logistics = logistics_result.data[0]
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
    
    # 4. 检查生产文档数据
    print("\n【阶段4】生产文档数据 (production_documents表)")
    print("-" * 50)
    
    prod_result = supabase.table('production_documents').select('*').eq('order_id', order_id).execute()
    if prod_result.data:
        doc = prod_result.data[0]
        print(f"✅ 找到生产文档数据")
        print(f"  id: {doc.get('id')}")
        print(f"  effect_svg_url: {doc.get('effect_svg_url', '无')[:60]}...")
        print(f"  effect_jpg_url: {doc.get('effect_jpg_url', '无')[:60]}...")
        print(f"  real_photo_urls: {doc.get('real_photo_urls', '无')[:60] if doc.get('real_photo_urls') else '无'}")
    else:
        print(f"❌ 未找到生产文档数据")
        print("  说明：效果图设计器生成的SVG未保存到数据库")
    
    # 5. 总结
    print("\n" + "=" * 70)
    print("数据完整性总结")
    print("=" * 70)
    
    has_sku = sku_id and supabase.table('sku_mapping').select('id').eq('id', sku_id).execute().data
    has_logistics = len(logistics_result.data) > 0
    has_prod_doc = len(prod_result.data) > 0
    
    checks = [
        ("订单基础数据", True),
        ("SKU映射数据", has_sku),
        ("物流数据", has_logistics),
        ("生产文档数据 (效果图SVG)", has_prod_doc),
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
            print("1. 为订单设置正确的 sku_id 或完善订单数据")
        if "物流数据" in missing:
            print("2. 在【物流下单】页面为该订单创建物流运单")
        if "生产文档数据 (效果图SVG)" in missing:
            print("3. 在【待确认订单】页面使用设计器生成效果图并保存")
            print("   注意：设计器生成的SVG需要保存到 production_documents 表")
    else:
        print("✅ 所有数据完整，可以正常生成生产文档PDF")

if __name__ == "__main__":
    check_order_flow()
