import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.services.database_service import DatabaseService
from src.services.svg_pdf_service import SVGPDFService
from datetime import datetime

def gen_pdf():
    db = DatabaseService()
    # 查询订单
    orders = db.select('orders', {'etsy_order_id': '4002217518'})
    if not orders:
        print("❌ 未找到订单")
        return
    order = orders[0]
    print(f"✅ 订单: {order['etsy_order_id']}, 状态: {order['status']}")
    
    # 查询 production_documents
    docs = db.select('production_documents', {'order_id': order['id']})
    if docs:
        doc = docs[0]
        print(f"📄 生产文档ID: {doc['id']}")
        print(f"🖼️  效果图SVG URL: {doc.get('effect_svg_url', '无')}")
        print(f"🖼️  效果图JPG URL: {doc.get('effect_jpg_url', '无')}")
    else:
        print("⚠️ 无生产文档记录，直接用订单数据生成")
        doc = {}
    
    # 查询 sku_mapping（确定正确的形状/颜色/尺寸）
    sku_row = db.select_one('sku_mapping', {'id': order.get('sku_id')}) or {}
    sku_code = sku_row.get('sku_code', '')
    sku_shape = sku_row.get('shape', '心形')
    sku_color = sku_row.get('color', '金色')
    sku_size_raw = sku_row.get('size', 'L')
    # 统一为英文 Large/Small 供 create_order_data 处理
    size_en = 'Large' if str(sku_size_raw).upper() in ['L', '大', 'LARGE'] else 'Small'
    print(f"📦 SKU: {sku_code}, 形状: {sku_shape}, 颜色: {sku_color}, 尺寸: {sku_size_raw} → {size_en}")
    
    # 查询 logistics
    logistics_list = db.select('logistics', {'order_id': order['id']})
    logistics = logistics_list[0] if logistics_list else {}
    
    # 构建 PDF 数据
    effect_svg_url = doc.get('effect_svg_url') or order.get('effect_image_url')
    print(f"\n📎 使用效果图URL: {effect_svg_url}")
    
    pdf_data = {
        'etsy_order_id': order['etsy_order_id'],
        'customer_name': order.get('customer_name', ''),
        'front_text': order.get('front_text', ''),
        'back_text': order.get('back_text', ''),
        # 关键：传英文形状/颜色/尺寸，确保 generate_sku 能正确识别
        'shape': sku_shape,          # 中文："心形"，svg_pdf_service 有中文映射
        'color': sku_color,          # 中文："金色"
        'size': size_en,             # 英文："Large"，确保 SIZE_MAP 能匹配
        # 直接传正确 SKU，防止 generate_sku 重算出错
        'sku_code': sku_code,        # B-G01B
        'craft': '抛光',
        'quantity': order.get('quantity', 1),
        'effect_svg_url': effect_svg_url,
        'tracking_number': logistics.get('tracking_number', ''),
        'country': order.get('shipping_country', ''),
        'shipping_name': logistics.get('recipient_name') or order.get('customer_name', ''),
        # 地址字段使用 create_order_data 能识别的字段名
        'shipping_address': logistics.get('address') or order.get('shipping_address_line1', ''),
        'city': logistics.get('city') or order.get('shipping_city', ''),
        'state': logistics.get('state') or order.get('shipping_state', ''),
        # 邮编：同时传多个字段名确保被读取到
        'postal_code': logistics.get('postal_code') or order.get('shipping_zip', ''),
        'shipping_zip': logistics.get('postal_code') or order.get('shipping_zip', ''),
        'address': logistics.get('address') or order.get('shipping_address_line1', ''),
    }
    
    # 生成PDF
    svc = SVGPDFService()
    
    print(f"\n⏳ 正在生成PDF...")
    pdf_path = svc.generate_from_raw_data(pdf_data)
    if pdf_path:
        print(f"✅ PDF已生成: {pdf_path}")
    else:
        print("❌ PDF生成失败")

if __name__ == "__main__":
    gen_pdf()
