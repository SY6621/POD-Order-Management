"""
4PX 物流 API 测试脚本

测试账号：18820295523 / fpx@123456
物流渠道：美国联邮通优先挂号-普货 (PX)

功能：
1. 测试 API 签名和连接
2. 创建测试订单
3. 查询订单状态
"""
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')

from src.services.logistics_service import logistics_service


def test_api_connection():
    """测试 API 连接（通过查询一个不存在的订单来验证签名）"""
    print("=" * 60)
    print("4PX 物流 API 连接测试")
    print("=" * 60)
    
    # 尝试查询一个测试订单（会返回失败，但能验证签名机制）
    result = logistics_service.get_order(consignment_no="TEST_001")
    
    if result is None:
        print("\n⚠️ 查询返回空，可能是：")
        print("  1. 签名验证失败")
        print("  2. 订单不存在（这是正常的）")
        print("  3. 网络连接问题")
    else:
        print(f"\n✅ API 连接成功！")
        print(f"响应数据: {result}")
    
    return result


def create_test_order():
    """创建测试订单"""
    print("\n" + "=" * 60)
    print("创建测试订单")
    print("=" * 60)
    
    # 测试订单数据（参考 4PX 在线调试页面的 JAVA 示例）
    order_data = {
        "ref_no": "TEST_20240304_001",  # 客户参考号（唯一）
        "business_type": "BDS",  # 业务类型
        "duty_type": "U",  # 税费承担方式：DDU由收件人支付
        "cargo_type": "5",  # 货物类型：其它
        
        # 物流服务信息
        "logistics_service_info": {
            "logistics_product_code": "PX",  # 美国联邮通优先挂号-普货
            "customs_service": "N",
            "signature_service": "N"
        },
        
        # 随货资料类型（必填）
        "attachment_type": "I",  # I=发票，根据业务需要选择
        
        # 包裹列表
        "parcel_list": [
            {
                "weight": 50,  # 重量(g)
                "length": 5.0,
                "width": 3.0,
                "height": 0.5,
                "parcel_value": 10.0,
                "currency": "USD",
                "product_list": [
                    {
                        "sku_code": "PET_TAG_001",
                        "product_name": "Pet ID Tag",
                        "product_description": "Stainless steel pet ID tag",
                        "product_unit_price": 10.0,
                        "currency": "USD",
                        "qty": 1
                    }
                ]
            }
        ],
        
        # 发件人信息
        "sender": {
            "first_name": "Test",
            "last_name": "Sender",
            "phone": "18820295523",
            "email": "sender@example.com",
            "country": "CN",
            "state": "Guangdong",
            "city": "Shenzhen",
            "post_code": "518000",
            "street": "Test Street 123"
        },
        
        # 收件人信息
        "recipient_info": {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
            "email": "john.doe@example.com",
            "country": "US",
            "state": "CA",
            "city": "Los Angeles",
            "post_code": "90001",
            "street": "123 Test Street"
        }
    }
    
    print(f"订单号: {order_data['ref_no']}")
    print(f"物流渠道: PX (美国联邮通优先挂号-普货)")
    print(f"业务类型: {order_data['business_type']}")
    
    result = logistics_service.create_order(order_data)
    
    if result:
        print(f"\n✅ 订单创建成功！")
        print(f"4PX 请求单号: {result.get('request_no')}")
        print(f"完整响应: {result}")
    else:
        print(f"\n❌ 订单创建失败")
    
    return result


def main():
    print("4PX 递四方物流 API 测试")
    print("测试账号: 18820295523 / fpx@123456")
    print()
    
    # 先测试 API 连接
    # test_api_connection()
    
    # 创建测试订单
    create_test_order()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
