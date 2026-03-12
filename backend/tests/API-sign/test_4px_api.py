"""
4PX 物流 API 签名测试
基于物流公司提供的 JS 签名工具实现
"""
import hashlib
import json
import time
import requests
from typing import Dict, Any, Optional

# 测试环境配置
TEST_CONFIG = {
    "app_key": "5dca6db7-6a21-4d31-a5f8-33a24a4f5b9d",
    "app_secret": "b8bd24a5-35b0-4e8a-bbc0-c7458e21c7ad",
    "base_url": "https://open-test.4px.com/router/api/service"
}

# 生产环境配置（正式环境需填写自己的 AppKey）
PROD_CONFIG = {
    "app_key": "",
    "app_secret": "",
    "base_url": "https://open.4px.com/router/api/service"
}


def generate_sign(app_key: str, app_secret: str, method: str, v: str, 
                  body: Dict[Any, Any], timestamp: Optional[int] = None) -> tuple:
    """
    生成 4PX API 签名
    
    签名规则：
    sign = app_key + {AppKey} + formatjson + method + {method} + timestamp + {timestamp} + v + {v} + {body} + {AppSecret}
    然后对 sign 字符串进行 MD5 加密（32位小写）
    
    Returns:
        (sign_string, md5_sign, timestamp)
    """
    if timestamp is None:
        timestamp = int(time.time() * 1000)  # 毫秒时间戳
    
    # 压缩 JSON body（无空格、无换行）
    body_str = json.dumps(body, ensure_ascii=False, separators=(',', ':'))
    
    # 拼接签名字符串
    sign_string = f"app_key{app_key}formatjsonmethod{method}timestamp{timestamp}v{v}{body_str}{app_secret}"
    
    # MD5 加密（32位小写）
    md5_sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest().lower()
    
    return sign_string, md5_sign, timestamp


def call_4px_api(method: str, v: str, body: Dict[Any, Any], 
                 config: Dict[str, str] = TEST_CONFIG) -> Dict[Any, Any]:
    """
    调用 4PX API
    """
    app_key = config["app_key"]
    app_secret = config["app_secret"]
    base_url = config["base_url"]
    
    # 生成签名
    sign_string, sign, timestamp = generate_sign(app_key, app_secret, method, v, body)
    
    # 构建请求 URL
    url = f"{base_url}?method={method}&app_key={app_key}&v={v}&timestamp={timestamp}&format=json&sign={sign}"
    
    # 压缩 body
    body_str = json.dumps(body, ensure_ascii=False, separators=(',', ':'))
    
    print(f"\n{'='*60}")
    print(f"API 方法: {method}")
    print(f"请求 URL: {url}")
    print(f"签名原文: {sign_string}")
    print(f"签名结果: {sign}")
    print(f"请求 Body: {body_str}")
    print(f"{'='*60}\n")
    
    try:
        response = requests.post(
            url,
            data=body_str,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"响应状态: {response.status_code}")
        print(f"响应内容: {response.text}\n")
        
        return response.json()
    except Exception as e:
        print(f"请求失败: {e}")
        return {"error": str(e)}


# ==================== 测试用例 ====================

def test_create_order():
    """
    测试：创建直发委托单
    API: ds.xms.order.create v1.1.0
    """
    method = "ds.xms.order.create"
    v = "1.1.0"
    
    # 示例请求体（需要根据实际业务填写）
    body = {
        "customer_code": "TEST001",  # 客户编码，需向4PX申请
        "order_no": f"TEST{int(time.time())}",  # 订单号
        "reference_no": f"REF{int(time.time())}",  # 参考号（必填）
        "transport_type": "A",  # 运输方式：A-空运
        "destination_country": "US",  # 目的国家
        "destination_postcode": "10001",  # 目的邮编
        "pieces": 1,  # 件数
        "weight": 0.5,  # 重量(kg)
        "length": 10,  # 长(cm)
        "width": 10,  # 宽(cm)
        "height": 5,  # 高(cm)
        "goods_type": "W",  # 货物类型：W-普货
        "start_consign_time": int(time.time()),  # 创建时间戳
        "declare_goods": [
            {
                "name": "Test Product",
                "cn_name": "测试产品",
                "quantity": 1,
                "unit_price": 10.0,
                "currency": "USD",
                "weight": 0.5
            }
        ],
        "consignee": {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
            "email": "john@example.com",
            "country": "US",
            "state": "NY",
            "city": "New York",
            "address1": "123 Test St",
            "postcode": "10001"
        }
    }
    
    return call_4px_api(method, v, body)


def test_get_label():
    """
    测试：获取标签
    API: ds.xms.label.get v1.1.0
    """
    method = "ds.xms.label.get"
    v = "1.1.0"
    
    body = {
        "order_no": "TEST123456",  # 需要替换为实际订单号
        "label_type": "1",  # 标签类型：1-地址标签
        "label_size": "10x10"  # 标签尺寸
    }
    
    return call_4px_api(method, v, body)


def test_get_logistics_products():
    """
    测试：查询物流产品
    API: ds.xms.logistics_product.getlist v1.0.0
    """
    method = "ds.xms.logistics_product.getlist"
    v = "1.0.0"
    
    body = {
        "country_code": "US",  # 目的国家
        "postcode": "10001",  # 目的邮编
        "transport_mode": "A"  # 运输方式：A-空运
    }
    
    return call_4px_api(method, v, body)


def test_query_order():
    """
    测试：查询直发委托单
    API: ds.xms.order.get v1.1.0
    """
    method = "ds.xms.order.get"
    v = "1.1.0"
    
    body = {
        "order_no": "TEST123456"  # 需要替换为实际订单号
    }
    
    return call_4px_api(method, v, body)


if __name__ == "__main__":
    print("4PX 物流 API 签名测试")
    print("=" * 60)
    
    # 先测试最简单的接口：查询物流产品
    print("\n【测试1】查询物流产品")
    result1 = test_get_logistics_products()
    
    # 测试查询订单
    print("\n【测试2】查询直发委托单")
    result2 = test_query_order()
    
    # 测试创建订单（需要有效的 customer_code）
    print("\n【测试3】创建直发委托单")
    result3 = test_create_order()
    
    print("\n" + "=" * 60)
    print("测试完成")
