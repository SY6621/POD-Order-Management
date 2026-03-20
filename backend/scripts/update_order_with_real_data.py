# -*- coding: utf-8 -*-
"""
将测试订单 PO-202602-103 更新为真实订单数据
真实订单号: 3891559803
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))

from services.database import db

def update_order_with_real_data():
    """更新订单为真实数据"""
    
    # 查找订单 PO-202602-103
    order = db.select_one("orders", {"etsy_order_id": "PO-202602-103"})
    if not order:
        print("❌ 未找到订单 PO-202602-103")
        return
    
    order_id = order['id']
    print(f"✅ 找到订单 ID: {order_id}")
    
    # 1. 更新订单基础数据
    print("\n【步骤1】更新订单基础数据...")
    order_update = {
        "etsy_order_id": "3891559803",  # 真实订单号
        "customer_name": "Demi Brooker",
        "front_text": "Spirit",
        "back_text": "0402 830 481",
        "font_code": "F-04",
        "quantity": 1,
        "total_amount": 34.46,
    }
    
    result = db.update("orders", {"id": order_id}, order_update)
    print(f"  订单更新: {'✅ 成功' if result else '❌ 失败'}")
    
    # 2. 查找或创建SKU映射
    print("\n【步骤2】查找SKU映射...")
    # 根据 shape=Heart, color=Gold, size=Large 查找SKU
    sku = db.select_one("sku_mapping", {
        "shape": "Heart",
        "color": "Gold", 
        "size": "Large"
    })
    
    if sku:
        print(f"  ✅ 找到SKU: {sku['sku_code']} (ID: {sku['id']})")
        # 更新订单的sku_id
        db.update("orders", {"id": order_id}, {"sku_id": sku['id']})
        print(f"  ✅ 已关联SKU到订单")
    else:
        print(f"  ⚠️ 未找到匹配的SKU (Heart/Gold/Large)")
        # 显示可用的SKU
        all_skus = db.select("sku_mapping", {}, limit=5)
        print(f"  可用SKU示例:")
        for s in all_skus:
            print(f"    - {s['sku_code']}: {s['shape']}/{s['color']}/{s['size']}")
    
    # 3. 创建物流记录
    print("\n【步骤3】创建物流记录...")
    logistics_data = {
        "order_id": order_id,
        "recipient_name": "Demi Brooker",
        "street_address": "3/1A Salisbury Rd",
        "city": "ROSE BAY",
        "state_code": "NSW",
        "postal_code": "2029",
        "country": "Australia",
        "tracking_number": "TEST123456",  # 测试单号
    }
    
    # 检查是否已有物流记录
    existing_logistics = db.select("logistics", {"order_id": order_id})
    if existing_logistics:
        db.update("logistics", {"order_id": order_id}, logistics_data)
        print(f"  ✅ 已更新物流记录")
    else:
        db.insert("logistics", logistics_data)
        print(f"  ✅ 已创建物流记录")
    
    # 4. 创建生产文档记录（模拟效果图已生成）
    print("\n【步骤4】创建生产文档记录...")
    prod_doc_data = {
        "order_id": order_id,
        "effect_svg_url": "https://example.com/effect_3891559803.svg",  # 占位符
        "effect_jpg_url": "https://example.com/effect_3891559803.jpg",  # 占位符
        "real_photo_urls": "https://example.com/photo1.jpg,https://example.com/photo2.jpg",
        "created_at": "2026-03-18T10:00:00",
    }
    
    existing_docs = db.select("production_documents", {"order_id": order_id})
    if existing_docs:
        db.update("production_documents", {"order_id": order_id}, prod_doc_data)
        print(f"  ✅ 已更新生产文档记录")
    else:
        db.insert("production_documents", prod_doc_data)
        print(f"  ✅ 已创建生产文档记录")
    
    print("\n" + "=" * 60)
    print("订单数据更新完成!")
    print("=" * 60)
    print(f"订单ID: {order_id}")
    print(f"Etsy订单号: 3891559803")
    print(f"客户: Demi Brooker")
    print(f"正面文字: Spirit (F-04)")
    print(f"背面文字: 0402 830 481")
    print(f"物流: 3/1A Salisbury Rd, ROSE BAY NSW 2029, Australia")
    print("\n请刷新页面并重新生成PDF测试!")

if __name__ == "__main__":
    update_order_with_real_data()
