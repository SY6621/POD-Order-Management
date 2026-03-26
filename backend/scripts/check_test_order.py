import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.services.database_service import DatabaseService

def check():
    db = DatabaseService()
    # 查询订单 4002217518
    orders = db.select('orders', {'etsy_order_id': '4002217518'})
    for o in orders:
        print(f"ID: {o['id']}")
        print(f"Etsy: {o['etsy_order_id']}")
        print(f"Status: {o['status']}")
        print(f"Front: {o.get('front_text', '')}")
        print(f"Back: {o.get('back_text', '')}")
        print(f"Has Image: {o.get('effect_image_url') is not None}")
        print(f"Has SVG: {o.get('effect_svg_url') is not None}")
        print("---")
    return orders[0] if orders else None

if __name__ == "__main__":
    order = check()
    if order:
        print(f"\n找到订单: {order['id']}")
    else:
        print("\n未找到订单")
