# -*- coding: utf-8 -*-
"""
从 QQ 邮箱提取 Etsy 订单邮件并导入数据库
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.services.email_service import email_service
from src.services.email_parser import email_parser
from src.services.database_service import db


def fetch_and_import_orders():
    """从 QQ 邮箱获取未读 Etsy 订单并导入数据库"""
    
    print("=" * 60)
    print("从 QQ 邮箱提取 Etsy 订单")
    print("=" * 60)
    
    # 连接邮箱
    if not email_service.connect():
        print("❌ 邮箱连接失败")
        return
    
    try:
        # 搜索所有未读 Etsy 订单邮件
        print("\n[1] 搜索未读 Etsy 订单邮件...")
        msg_ids = email_service.search_all_unread_etsy_orders()
        
        if not msg_ids:
            print("⚠️ 没有找到未读的 Etsy 订单邮件")
            print("提示：请先在 QQ 邮箱中将订单邮件标记为「未读」")
            return
        
        print(f"\n[2] 找到 {len(msg_ids)} 封订单邮件，开始处理...")
        
        imported_count = 0
        for msg_id in msg_ids:
            print(f"\n{'─' * 50}")
            print(f"处理邮件 ID: {msg_id}")
            
            # 获取邮件内容
            email_data = email_service.fetch_email_content(msg_id)
            if not email_data:
                print("❌ 获取邮件内容失败")
                continue
            
            print(f"主题: {email_data['subject']}")
            print(f"发件人: {email_data['from']}")
            
            # 调试：打印正文前 500 字符
            print(f"正文预览: {email_data['body'][:500]}")
            
            # 解析订单
            order = email_parser.parse_forwarded_email(email_data['body'])
            if not order or not order.etsy_order_id:
                print("❌ 无法解析订单信息")
                continue
            
            print(f"\n✅ 解析成功:")
            print(f"  订单号: {order.etsy_order_id}")
            print(f"  客户: {order.customer_name}")
            print(f"  产品: {order.items[0].product_name if order.items else 'N/A'}")
            print(f"  形状: {order.items[0].shape if order.items else 'N/A'}")
            print(f"  颜色: {order.items[0].color if order.items else 'N/A'}")
            print(f"  尺寸: {order.items[0].size if order.items else 'N/A'}")
            print(f"  正面: {order.items[0].customization_front if order.items else 'N/A'}")
            print(f"  背面: {order.items[0].customization_back if order.items else 'N/A'}")
            print(f"  字体: {order.items[0].font_code if order.items else 'N/A'}")
            print(f"  地址: {order.shipping_name}, {order.shipping_address_line1}")
            print(f"         {order.shipping_city} {order.shipping_state} {order.shipping_zip}")
            print(f"         {order.shipping_country}")
            
            # 检查订单是否已存在
            existing = db.get_order_by_etsy_id(order.etsy_order_id)
            if existing:
                print(f"⚠️ 订单 {order.etsy_order_id} 已存在，跳过")
                continue
            
            # SKU 反推：根据形状/颜色/尺寸查找SKU
            from src.services.order_service import lookup_sku
            sku_info = lookup_sku(
                order.items[0].shape if order.items else "",
                order.items[0].color if order.items else "",
                order.items[0].size if order.items else ""
            )
            sku_id = sku_info.get("id") if sku_info else None
            weight_g = sku_info.get("weight_g") if sku_info else 30  # 默认30g
            
            # 导入数据库
            print(f"\n[3] 导入数据库...")
            
            # 准备订单数据（status 使用 pending，符合数据库约束）
            order_data = {
                "etsy_order_id": order.etsy_order_id,
                "customer_name": order.customer_name,
                "customer_email": "",  # 从邮件中无法直接获取
                "front_text": order.items[0].customization_front if order.items else "",
                "back_text": order.items[0].customization_back if order.items else "",
                "font_code": order.items[0].font_code if order.items else "",
                "product_shape": order.items[0].shape if order.items else "",
                "product_color": order.items[0].color if order.items else "",
                "product_size": order.items[0].size if order.items else "",
                "product_craft": "抛光",  # 默认值
                "quantity": order.items[0].quantity if order.items else 1,
                "total_amount": order.order_total,
                "status": "pending",  # 使用 pending（符合 orders_status_check 约束）
                "sku_id": sku_id,  # 关联 SKU
                "created_at": order.order_date or datetime.now().isoformat(),
                # 地址信息（用于物流下单页自动填充）
                "shipping_name": order.shipping_name,
                "shipping_address_line1": order.shipping_address_line1,
                "shipping_address_line2": order.shipping_address_line2,
                "shipping_city": order.shipping_city,
                "shipping_state": order.shipping_state,
                "shipping_zip": order.shipping_zip,
                "shipping_country": order.shipping_country,
                "weight_g": weight_g,  # 从SKU获取重量
            }
            
            # 插入订单
            result = db.insert("orders", order_data)
            if result:
                print(f"✅ 订单导入成功: {order.etsy_order_id}")
                
                # 插入 logistics 信息
                if result.get("id"):
                    logistics_data = {
                        "order_id": result["id"],
                        "recipient_name": order.shipping_name,
                        "street_address": order.shipping_address_line1,
                        "city": order.shipping_city,
                        "state_code": order.shipping_state,
                        "postal_code": order.shipping_zip,
                        "country": order.shipping_country,
                        "tracking_number": "",  # 初始为空，发货后填写
                    }
                    db.insert("logistics", logistics_data)
                    print(f"✅ 物流信息导入成功")
                
                imported_count += 1
            else:
                print(f"❌ 订单导入失败")
        
        print(f"\n{'=' * 60}")
        print(f"处理完成: 共导入 {imported_count} 个新订单")
        print(f"{'=' * 60}")
        
    finally:
        email_service.disconnect()


if __name__ == "__main__":
    from datetime import datetime
    fetch_and_import_orders()
