# -*- coding: utf-8 -*-
"""
生成测试生产文档PDF（使用占位面单）
"""
import sys
sys.path.insert(0, 'd:\\ETSY_Order_Automation\\backend')

from src.services.database_service import DatabaseService
from src.services.svg_pdf_service import svg_pdf_service
import os

def main():
    db = DatabaseService()
    
    # 查询有效果图的生产中订单
    orders = db.select('orders', {'status': 'producing'}, limit=5)
    print(f'生产中订单数量: {len(orders)}')
    
    target_order = None
    
    for o in orders:
        order_id = o.get('id')
        etsy_id = o.get('etsy_order_id')
        
        # 查生产文档
        docs = db.select('production_documents', {'order_id': order_id})
        if docs and docs[0].get('effect_svg_url'):
            doc = docs[0]
            print(f'\n找到有效果图的订单: {etsy_id} (ID: {order_id})')
            print(f'  - effect_svg_url: {doc.get("effect_svg_url", "无")[:60]}...')
            print(f'  - effect_jpg_url: {doc.get("effect_jpg_url", "无")[:60] if doc.get("effect_jpg_url") else "无"}')
            print(f'  - real_photo_urls: {doc.get("real_photo_urls", "无")[:60] if doc.get("real_photo_urls") else "无"}')
            
            # 查物流信息
            logistics = db.select('logistics', {'order_id': order_id})
            if logistics:
                log = logistics[0]
                print(f'  - tracking_number: {log.get("tracking_number", "无")}')
                print(f'  - label_url: {log.get("label_url", "无")[:60] if log.get("label_url") else "无"}')
            
            target_order = o
            target_order['production_doc'] = doc
            if logistics:
                target_order['logistics'] = logistics[0]
            break
    
    if not target_order:
        print('\n没有找到有效果图的订单，使用第一个生产中订单')
        if orders:
            target_order = orders[0]
            target_order['production_doc'] = {}
            target_order['logistics'] = {}
    
    if target_order:
        print(f'\n准备生成测试PDF，订单: {target_order.get("etsy_order_id")}')
        
        # 组装数据
        order_data = {
            'id': target_order.get('id'),
            'etsy_order_id': target_order.get('etsy_order_id', 'TEST-001'),
            'customer_name': target_order.get('customer_name', 'Test Customer'),
            'sku': target_order.get('sku', 'B-E01A'),
            'shape': target_order.get('product_shape', '骨头形'),
            'color': target_order.get('product_color', '金色'),
            'size': target_order.get('product_size', 'L'),
            'craft': '抛光',
            'front_text': target_order.get('front_text', 'MAX'),
            'back_text': target_order.get('back_text', '0412345678'),
            'quantity': target_order.get('quantity', 1),
            'created_at': str(target_order.get('created_at', '2024-01-01')),
            'effect_svg_url': target_order.get('production_doc', {}).get('effect_svg_url', ''),
            'effect_image_url': target_order.get('production_doc', {}).get('effect_jpg_url', ''),
            'real_photo_urls': target_order.get('production_doc', {}).get('real_photo_urls', ''),
            'tracking_number': target_order.get('logistics', {}).get('tracking_number', '500135030358'),
            'label_url': target_order.get('logistics', {}).get('label_url', ''),
            'recipient_name': target_order.get('shipping_name', 'John Doe'),
            'street_address': target_order.get('shipping_address_line1', '123 Test St'),
            'city': target_order.get('shipping_city', 'Sydney'),
            'state_code': target_order.get('shipping_state', 'NSW'),
            'postal_code': target_order.get('shipping_postal_code', '2000'),
            'country': target_order.get('shipping_country', 'Australia'),
        }
        
        print('\n订单数据:')
        for k, v in order_data.items():
            if v and k not in ['effect_svg_url', 'effect_image_url', 'real_photo_urls', 'label_url']:
                print(f'  {k}: {v}')
        
        # 生成PDF（使用占位面单）
        print('\n正在生成PDF...')
        try:
            pdf_path = svg_pdf_service.generate_from_raw_data(order_data)
            if pdf_path and os.path.exists(pdf_path):
                print(f'\n✅ PDF生成成功: {pdf_path}')
                print(f'文件大小: {os.path.getsize(pdf_path) / 1024:.1f} KB')
            else:
                print('\n❌ PDF生成失败')
        except Exception as e:
            print(f'\n❌ 生成PDF时出错: {e}')
            import traceback
            traceback.print_exc()
    else:
        print('没有可用的订单')

if __name__ == '__main__':
    main()
