"""
测试 orders 表结构和数据
验证前后端字段对齐
"""
import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from supabase import create_client, Client

# 加载 .env 文件
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

def test_orders_table():
    """测试 orders 表"""
    print("=" * 60)
    print("Orders 表结构和数据测试")
    print("=" * 60)
    
    # 读取配置
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    try:
        # 创建客户端
        supabase: Client = create_client(url, key)
        print("✅ Supabase 客户端创建成功\n")
        
        # 1. 查询 orders 表所有数据
        print("【1】查询 orders 表所有订单...")
        response = supabase.table("orders").select("*").execute()
        
        orders = response.data
        print(f"✅ 查询成功！共有 {len(orders)} 条订单记录\n")
        
        if len(orders) > 0:
            # 2. 显示第一条订单的所有字段
            print("【2】第一条订单的完整字段：")
            first_order = orders[0]
            for key, value in first_order.items():
                print(f"   {key:25s} = {value}")
            
            # 3. 检查关键字段是否存在
            print("\n【3】关键字段检查：")
            required_fields = [
                'id', 'etsy_order_id', 'customer_name', 'customer_email',
                'quantity', 'total_amount', 'status', 'progress',
                'created_at', 'updated_at'
            ]
            
            for field in required_fields:
                exists = field in first_order
                symbol = "✅" if exists else "❌"
                print(f"   {symbol} {field}")
            
            # 4. 统计各状态的订单数量
            print("\n【4】订单状态统计：")
            status_counts = {}
            for order in orders:
                status = order.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            for status, count in status_counts.items():
                print(f"   {status:15s}: {count} 条")
            
            # 5. 测试关联查询
            print("\n【5】测试关联查询（orders + sku_mapping）...")
            response = supabase.table("orders").select("*, sku_mapping(*)").limit(1).execute()
            if response.data and len(response.data) > 0:
                print("   ✅ 关联查询成功！")
                order_with_sku = response.data[0]
                if 'sku_mapping' in order_with_sku and order_with_sku['sku_mapping']:
                    print(f"   SKU信息: {order_with_sku['sku_mapping']}")
                else:
                    print("   ⚠️ 该订单暂无SKU关联")
            
        else:
            print("⚠️ orders 表为空，没有订单数据")
            print("\n提示：可以通过以下方式添加测试数据：")
            print("1. 运行邮件解析脚本自动导入")
            print("2. 在 Supabase 控制台手动添加")
        
        print("\n" + "=" * 60)
        print("🎉 测试完成！")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_orders_table()
