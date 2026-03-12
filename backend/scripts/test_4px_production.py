"""
4PX API 生产环境测试 - 使用真实账号

步骤：
1. 创建直发委托单（下单）
2. 获取物流面单（标签）
3. 取消订单
"""
import hashlib
import json
import time
import requests

# 生产环境账号（来自 .env）
APP_KEY = "6efa9a05-5e31-4d2a-9a9c-da7624627f26"
APP_SECRET = "0b768497-0c7a-4247-a7c0-0ca20cb2ae16"
BASE_URL = "https://open.4px.com/router/api/service"

# 全局变量存储订单信息
order_info = {
    "request_no": None,
    "consignment_no": None,
    "tracking_no": None,
}


def generate_sign(method: str, v: str, timestamp: str, biz_content: str) -> str:
    """生成签名"""
    sign_str = "app_key" + APP_KEY + "formatjson" + "method" + method + "timestamp" + timestamp + "v" + v + biz_content + APP_SECRET
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().lower()


def make_request(method: str, v: str, biz_data: dict) -> dict:
    """发送API请求"""
    timestamp = str(int(time.time() * 1000))
    
    if not biz_data:
        biz_content = "{}"
    else:
        biz_content = json.dumps(biz_data, ensure_ascii=False, separators=(',', ':'))
    
    sign = generate_sign(method, v, timestamp, biz_content)
    
    request_data = {
        "app_key": APP_KEY,
        "method": method,
        "v": v,
        "timestamp": timestamp,
        "format": "json",
        "sign": sign,
        "language": "cn",
        "biz_content": biz_content
    }
    
    print(f"\n[请求] {method}")
    print(f"[时间戳] {timestamp}")
    print(f"[签名] {sign}")
    
    try:
        response = requests.post(
            BASE_URL,
            data=request_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30
        )
        
        result = response.json()
        
        if result.get("result") == "1":
            print(f"[响应] ✅ 成功")
            return result.get("data", {})
        else:
            print(f"[响应] ❌ 失败: {result.get('msg')}")
            if result.get('errors'):
                for err in result['errors']:
                    print(f"   错误: {err.get('error_code')} - {err.get('error_msg')}")
            return None
    except Exception as e:
        print(f"[异常] {e}")
        return None


def step1_create_order():
    """步骤1: 创建直发委托单"""
    print("\n" + "=" * 60)
    print("步骤 1/3: 创建直发委托单")
    print("=" * 60)
    
    consignment_no = f"ETSY{int(time.time())}"
    order_info["consignment_no"] = consignment_no
    
    order_data = {
        "consignment_no": consignment_no,
        "logistics_product_code": "PX",
        "destination_country": "US",
        "pieces": 1,
        "weight": 50,
        "receiver": {
            "first_name": "John",
            "last_name": "Smith",
            "country": "US",
            "state": "CA",
            "city": "Los Angeles",
            "post_code": "90001",
            "address": "123 Test St",
            "phone": "1234567890",
            "email": "test@example.com"
        },
        "sender": {
            "first_name": "Sender",
            "last_name": "Name",
            "country": "CN",
            "state": "Guangdong",
            "city": "Shenzhen",
            "post_code": "518000",
            "address": "Sender Address",
            "phone": "8613800138000"
        },
        "parcel_list": [
            {
                "sku": "PET001",
                "quantity": 1,
                "goods_title": "Pet ID Tag",
                "goods_category": "accessories",
                "goods_weight": 50,
                "goods_value": 5.99,
                "currency": "USD"
            }
        ]
    }
    
    result = make_request("ds.xms.order.create", "1.1.0", order_data)
    
    if result:
        order_info["request_no"] = result.get("request_no")
        order_info["tracking_no"] = result.get("tracking_no")
        
        print(f"\n✅ 订单创建成功!")
        print(f"   客户单号: {consignment_no}")
        print(f"   4PX单号: {result.get('fpx_order_no')}")
        print(f"   请求单号: {result.get('request_no')}")
        print(f"   跟踪号: {result.get('tracking_no')}")
        return True
    else:
        print(f"\n❌ 订单创建失败")
        return False


def step2_get_label():
    """步骤2: 获取物流面单"""
    print("\n" + "=" * 60)
    print("步骤 2/3: 获取物流面单")
    print("=" * 60)
    
    if not order_info["request_no"]:
        print("❌ 没有可用的请求单号，跳过此步骤")
        return False
    
    # 获取标签
    label_data = {
        "request_no": order_info["request_no"],
        "label_type": "1",
        "label_size": "10x10"
    }
    
    result = make_request("ds.xms.label.get", "1.1.0", label_data)
    
    if result:
        print(f"\n✅ 获取面单成功!")
        print(f"   标签URL: {result.get('label_url')}")
        print(f"   标签内容: {result.get('label_content', 'N/A')[:100]}...")
        return True
    else:
        print(f"\n❌ 获取面单失败")
        return False


def step3_cancel_order():
    """步骤3: 取消订单"""
    print("\n" + "=" * 60)
    print("步骤 3/3: 取消订单")
    print("=" * 60)
    
    if not order_info["request_no"]:
        print("❌ 没有可用的请求单号，跳过此步骤")
        return False
    
    cancel_data = {
        "request_no": order_info["request_no"],
        "cancel_reason": "测试取消"
    }
    
    result = make_request("ds.xms.order.cancel", "1.0.0", cancel_data)
    
    if result:
        print(f"\n✅ 订单取消成功!")
        print(f"   取消的单号: {order_info['request_no']}")
        return True
    else:
        print(f"\n❌ 订单取消失败")
        return False


def main():
    """主流程"""
    print("\n" + "=" * 60)
    print("4PX API 生产环境测试")
    print("=" * 60)
    print(f"AppKey: {APP_KEY}")
    print(f"环境: 生产环境")
    print(f"API地址: {BASE_URL}")
    
    # 步骤1: 创建订单
    if not step1_create_order():
        print("\n❌ 流程中止：创建订单失败")
        return
    
    # 等待订单处理
    print("\n[等待 3 秒让订单处理...]")
    time.sleep(3)
    
    # 步骤2: 获取面单
    step2_get_label()
    
    # 等待
    print("\n[等待 2 秒...]")
    time.sleep(2)
    
    # 步骤3: 取消订单
    step3_cancel_order()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    print(f"客户单号: {order_info['consignment_no']}")
    print(f"4PX单号: {order_info['request_no']}")
    print(f"跟踪号: {order_info['tracking_no']}")


if __name__ == "__main__":
    main()
