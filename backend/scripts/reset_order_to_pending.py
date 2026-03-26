import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.services.database_service import DatabaseService

def reset():
    db = DatabaseService()
    order_id = 'fd8455c4-1a2d-4b37-a8bf-e385cad993fd'
    
    # 重置订单状态为 pending，清空效果图（effect_svg_url 在 production_documents 表）
    result = db.update('orders', 
        {'id': order_id},
        {
            'status': 'pending',
            'effect_image_url': None
        }
    )
    
    if result:
        print(f"✅ 订单重置成功: {order_id}")
        print(f"   状态: pending")
        print(f"   效果图: 已清空")
    else:
        print(f"❌ 重置失败")

if __name__ == "__main__":
    reset()
