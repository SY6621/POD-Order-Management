#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订单状态回退脚本
功能：将订单状态重置为 new（新订单）或 pending（待创建），并清空效果图数据
用法：python reset_order_status.py <order_id> [--status new|pending]
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv(project_root / ".env")

from supabase import create_client


def reset_order_status(order_id: str, target_status: str = "pending"):
    """
    重置订单状态（清空效果图，将订单重置为待设计状态）
    :param order_id: Etsy 订单ID（如 4002217518）或数据库订单ID
    :param target_status: 目标状态，只能是 'pending'
    """
    
    # 初始化 Supabase
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ 错误：请检查 .env 文件中的 SUPABASE_URL 和 SUPABASE_KEY")
        return False
    
    supabase = create_client(supabase_url, supabase_key)
    
    # 查找订单
    try:
        # 先尝试按 etsy_order_id 查找
        result = supabase.table("orders").select("*").eq("etsy_order_id", order_id).execute()
        
        if not result.data:
            # 再尝试按 id 查找
            result = supabase.table("orders").select("*").eq("id", order_id).execute()
        
        if not result.data:
            print(f"❌ 错误：未找到订单 {order_id}")
            return False
        
        order = result.data[0]
        order_db_id = order["id"]
        etsy_id = order.get("etsy_order_id", "N/A")
        current_status = order.get("status", "unknown")
        
        print(f"\n📋 订单信息:")
        print(f"   数据库ID: {order_db_id}")
        print(f"   Etsy订单ID: {etsy_id}")
        print(f"   客户: {order.get('customer_name', 'N/A')}")
        print(f"   当前状态: {current_status}")
        
        has_effect = order.get('effect_image_url') is not None
        print(f"   效果图: {'✅ 有' if has_effect else '❌ 无'}")
        
        # 确认操作
        confirm = input(f"\n⚠️  确认清空效果图数据？订单将回到待设计状态。[y/N]: ")
        if confirm.lower() != 'y':
            print("❌ 操作已取消")
            return False
        
        # 更新订单状态
        update_data = {
            "effect_image_url": None,  # 清空效果图URL
            "updated_at": "now()"
        }
        
        result = supabase.table("orders").update(update_data).eq("id", order_db_id).execute()
        
        if result.data:
            print(f"\n✅ 成功！效果图已清空，订单回到待设计状态")
            return True
        else:
            print(f"\n❌ 错误：更新失败")
            return False
            
    except Exception as e:
        print(f"\n❌ 错误：{str(e)}")
        return False


def batch_reset(order_ids: list, target_status: str = "pending"):
    """批量重置多个订单（清空效果图）"""
    print(f"\n🔄 批量清空 {len(order_ids)} 个订单的效果图\n")
    
    success_count = 0
    for order_id in order_ids:
        print(f"\n{'='*50}")
        if reset_order_status(order_id, target_status):
            success_count += 1
    
    print(f"\n{'='*50}")
    print(f"\n📊 批量重置完成：成功 {success_count}/{len(order_ids)}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="订单状态回退工具 - 清空效果图，将订单重置为待设计状态",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python reset_order_status.py 4002217518
  python reset_order_status.py 4002217518 --status pending
  python reset_order_status.py --batch 4002217518,3891559803,3986891868
        """)
    
    parser.add_argument("order_id", nargs="?", help="订单ID（Etsy订单ID或数据库ID）")
    parser.add_argument("--status", choices=["pending"], default="pending",
                       help="目标状态：pending（待确认），默认 pending")
    parser.add_argument("--batch", help="批量重置，逗号分隔订单ID列表")
    
    args = parser.parse_args()
    
    # 批量模式
    if args.batch:
        order_ids = [id.strip() for id in args.batch.split(",")]
        batch_reset(order_ids, args.status)
        return
    
    # 单订单模式
    if not args.order_id:
        parser.print_help()
        print("\n❌ 错误：请提供订单ID或使用 --batch 参数")
        sys.exit(1)
    
    # 执行重置
    success = reset_order_status(args.order_id, args.status)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
