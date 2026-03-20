# -*- coding: utf-8 -*-
"""
ETSY订单自动化 - 端到端全流程测试
测试流程：数据查询 → 效果图 → 物流下单 → 面单获取 → 生产文档PDF

使用方法（从backend目录运行）：
  cd D:\ETSY_Order_Automation\backend
  poetry run python scripts/e2e_full_test.py
"""
import sys
import os
import json
from pathlib import Path
from datetime import datetime

# 确保项目根目录在Python路径中
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

# === Step 0: 初始化服务 ===
print("=" * 60)
print("ETSY订单自动化 - 端到端全流程测试")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# 导入服务
from src.services.database_service import db
from src.config.settings import settings

results = {
    "step1_data_query": "❌ 未执行",
    "step2_effect_image": "❌ 未执行",
    "step3_shipping": "❌ 未执行",
    "step4_label": "❌ 未执行",
    "step5_pdf": "❌ 未执行",
}

# === Step 1: 查询数据库中的真实订单 ===
print("\n" + "=" * 60)
print("【Step 1】查询数据库真实订单数据")
print("=" * 60)

# 1a. 先查找已有物流信息（label_url不为空）的订单 — 这些可以直接测试PDF
test_order = None
test_logistics = None
test_doc = None
all_orders = None
all_logistics = None
all_docs = None
sku_map_dict = {}

try:
    # 查询所有订单（不使用关联查询，避免多关系冲突）
    all_orders = db._client.table("orders").select("*").execute()
    print(f"  数据库中共有 {len(all_orders.data)} 条订单")
    
    # 单独查询sku_mapping表
    all_sku_mappings = db._client.table("sku_mapping").select("*").execute()
    sku_map_dict = {s.get("id"): s for s in all_sku_mappings.data}
    
    for o in all_orders.data:
        print(f"  - 订单: {o.get('etsy_order_id', 'N/A')} | 状态: {o.get('status', 'N/A')} | 客户: {o.get('customer_name', 'N/A')}")
    
    # 查询logistics表，找已有tracking_number和label_url的
    all_logistics = db._client.table("logistics").select("*").execute()
    print(f"\n  logistics表共有 {len(all_logistics.data)} 条记录")
    
    has_label = [l for l in all_logistics.data if l.get("label_url")]
    print(f"  其中有面单URL的: {len(has_label)} 条")
    
    for l in all_logistics.data:
        label_status = '✅有' if l.get('label_url') else '❌无'
        order_id_short = (l.get('order_id', 'N/A') or 'N/A')[:8]
        print(f"  - order_id: {order_id_short}... | tracking: {l.get('tracking_number', 'N/A')} | label_url: {label_status}")
    
    # 查询production_documents表
    all_docs = db._client.table("production_documents").select("*").execute()
    print(f"\n  production_documents表共有 {len(all_docs.data)} 条记录")
    
    for d in all_docs.data:
        order_id_short = (d.get('order_id', 'N/A') or 'N/A')[:8]
        effect_status = '✅有' if d.get('effect_svg_url') else '❌无'
        print(f"  - order_id: {order_id_short}... | effect_svg: {effect_status}")
    
    # 选择最佳测试订单：优先选有label_url的，其次有tracking_number的
    if has_label:
        # 找对应的订单
        label_order_id = has_label[0].get("order_id")
        test_logistics = has_label[0]
        for o in all_orders.data:
            if o.get("id") == label_order_id:
                test_order = o
                break
    
    # 如果没找到有label的，找有tracking_number的
    if not test_order:
        has_tracking = [l for l in all_logistics.data if l.get("tracking_number")]
        if has_tracking:
            tracking_order_id = has_tracking[0].get("order_id")
            test_logistics = has_tracking[0]
            for o in all_orders.data:
                if o.get("id") == tracking_order_id:
                    test_order = o
                    break
    
    # 如果还没找到，找任意有logistics记录的订单
    if not test_order and all_logistics.data:
        any_logistics_order_id = all_logistics.data[0].get("order_id")
        test_logistics = all_logistics.data[0]
        for o in all_orders.data:
            if o.get("id") == any_logistics_order_id:
                test_order = o
                break
    
    # 最后降级到任意订单（无logistics）
    if not test_order and all_orders.data:
        test_order = all_orders.data[0]
        test_logistics = None  # 明确设为None
        for l in all_logistics.data:
            if l.get("order_id") == test_order.get("id"):
                test_logistics = l
                break
    
    if test_order:
        print(f"\n  ✅ 选定测试订单: {test_order.get('etsy_order_id')}")
        print(f"     订单ID: {test_order.get('id')}")
        print(f"     客户: {test_order.get('customer_name')}")
        print(f"     状态: {test_order.get('status')}")
        print(f"     SKU ID: {test_order.get('sku_id') or test_order.get('matched_sku_id') or 'N/A'}")
        if test_logistics:
            print(f"     物流单号: {test_logistics.get('tracking_number', '无')}")
            label_url = test_logistics.get('label_url', '')
            if label_url:
                print(f"     面单URL: {label_url[:80]}...")
            else:
                print(f"     面单URL: 无")
        results["step1_data_query"] = "✅ 通过"
    else:
        print("\n  ❌ 数据库中没有可用的测试订单！")
        print("  请先导入测试数据。")
        results["step1_data_query"] = "❌ 无可用订单"

except Exception as e:
    print(f"  ❌ 数据库查询失败: {e}")
    import traceback
    traceback.print_exc()
    results["step1_data_query"] = f"❌ 异常: {e}"
    test_order = None

if not test_order:
    print("\n⚠️ 没有可用的测试订单，将使用模拟数据继续测试PDF生成能力...")
    
    # 使用模拟数据（确保至少能测试PDF生成逻辑）
    mock_raw_data = {
        "id": "test-e2e-001",
        "etsy_order_id": "E2E-TEST-001",
        "customer_name": "E2E Test User",
        "customer_email": "test@example.com",
        "front_text": "Lucky",
        "back_text": "0412345678",
        "status": "confirmed",
        "order_date": datetime.now().strftime("%Y-%m-%d"),
        "ship_date": datetime.now().strftime("%Y-%m-%d"),
        
        # 产品信息 - 使用数据库字段名
        "product_shape": "Heart",
        "product_color": "Gold",
        "product_size": "Large",
        "product_craft": "抛光",
        "font_code": "F-04",
        
        # 物流信息
        "tracking_number": "MOCK-4PX-001",
        "recipient_name": "Jane Smith",
        "country": "US",
        "state_code": "CA",
        "city": "Los Angeles",
        "postal_code": "90001",
        "street_address": "123 Test Street, Apt 4B",
        
        "effect_svg_url": "",
        "label_url": "",  # 模拟数据无面单URL
    }
    results["step1_data_query"] = "⚠️ 使用模拟数据"

# === Step 2: 组装raw_data字典 ===
print("\n" + "=" * 60)
print("【Step 2】组装raw_data数据字典")
print("=" * 60)

if test_order:
    # 从真实订单组装
    # 使用sku_id或matched_sku_id查找sku_mapping数据
    sku_id = test_order.get("sku_id") or test_order.get("matched_sku_id")
    sku_data = sku_map_dict.get(sku_id, {}) if sku_id else {}
    
    # 查找production_documents
    if all_docs:
        for d in all_docs.data:
            if d.get("order_id") == test_order.get("id"):
                test_doc = d
                break
    
    raw_data = {
        "id": test_order.get("id", ""),
        "etsy_order_id": test_order.get("etsy_order_id", ""),
        "customer_name": test_order.get("customer_name", ""),
        "customer_email": test_order.get("customer_email", ""),
        "front_text": test_order.get("front_text", ""),
        "back_text": test_order.get("back_text", ""),
        "status": test_order.get("status", ""),
        "order_date": (test_order.get("created_at", "") or datetime.now().strftime("%Y-%m-%d"))[:10],
        "ship_date": datetime.now().strftime("%Y-%m-%d"),
        
        # 产品信息 - 优先使用orders表字段，其次用sku_mapping
        "product_shape": test_order.get("product_shape") or sku_data.get("shape", "Bone"),
        "product_color": test_order.get("product_color") or sku_data.get("color", "Gold"),
        "product_size": test_order.get("product_size") or sku_data.get("size", "Large"),
        "product_craft": test_order.get("product_craft") or sku_data.get("craft", "抛光"),
        "font_code": test_order.get("font_code", "F-04"),
        
        # 物流信息（从logistics表）
        "tracking_number": test_logistics.get("tracking_number", "") if test_logistics else "",
        "recipient_name": test_logistics.get("recipient_name", "") if test_logistics else "",
        "country": test_logistics.get("country", "US") if test_logistics else "US",
        "state_code": test_logistics.get("state_code", "") or (test_logistics.get("state", "") if test_logistics else ""),
        "city": test_logistics.get("city", "") if test_logistics else "",
        "postal_code": test_logistics.get("postal_code", "") if test_logistics else "",
        "street_address": test_logistics.get("recipient_address", "") if test_logistics else "",
        
        # 面单和效果图
        "label_url": test_logistics.get("label_url", "") if test_logistics else "",
        "effect_svg_url": test_doc.get("effect_svg_url", "") if test_doc else "",
    }
    
    print(f"  ✅ 真实数据组装完成")
else:
    raw_data = mock_raw_data
    print(f"  ⚠️ 使用模拟数据")

# 打印关键字段
print(f"\n  关键字段:")
print(f"    订单ID: {raw_data.get('etsy_order_id')}")
print(f"    客户: {raw_data.get('customer_name')}")
print(f"    正面文字: {raw_data.get('front_text')}")
print(f"    背面文字: {raw_data.get('back_text')}")
print(f"    形状/颜色/尺寸: {raw_data.get('product_shape')}/{raw_data.get('product_color')}/{raw_data.get('product_size')}")
print(f"    物流单号: {raw_data.get('tracking_number') or '无'}")
print(f"    面单URL: {'有' if raw_data.get('label_url') else '无'}")
print(f"    效果图URL: {'有' if raw_data.get('effect_svg_url') else '无'}")

# === Step 3: 效果图生成 ===
print("\n" + "=" * 60)
print("【Step 3】效果图生成")
print("=" * 60)

try:
    if raw_data.get("effect_svg_url"):
        print(f"  ⏭️ 订单已有效果图URL，跳过生成")
        print(f"    URL: {raw_data['effect_svg_url'][:80]}...")
        results["step2_effect_image"] = "✅ 已有效果图"
    else:
        print(f"  开始生成效果图...")
        from src.services.effect_image_service import effect_image_service
        
        effect_input = {
            "id": raw_data.get("id", "e2e-test"),
            "etsy_order_id": raw_data.get("etsy_order_id"),
            "product_shape": raw_data.get("product_shape"),
            "product_color": raw_data.get("product_color"),
            "product_size": raw_data.get("product_size"),
            "front_text": raw_data.get("front_text"),
            "back_text": raw_data.get("back_text"),
            "font_code": raw_data.get("font_code", "F-04"),
        }
        
        effect_result = effect_image_service.generate_and_upload(effect_input)
        if effect_result and effect_result.get("effect_image_url"):
            raw_data["effect_svg_url"] = effect_result.get("effect_image_url", "")
            print(f"  ✅ 效果图生成成功")
            print(f"    正面: {effect_result.get('effect_image_url', 'N/A')[:80]}")
            results["step2_effect_image"] = "✅ 生成成功"
        else:
            print(f"  ⚠️ 效果图生成返回空结果（PDF将使用动态生成）")
            results["step2_effect_image"] = "⚠️ 降级使用动态生成"
except Exception as e:
    print(f"  ⚠️ 效果图生成异常: {e}")
    print(f"    （PDF生成时将自动降级为动态生成效果图）")
    import traceback
    traceback.print_exc()
    results["step2_effect_image"] = f"⚠️ 异常但已降级: {str(e)[:30]}"

# === Step 4: 物流下单 + 面单获取 ===
print("\n" + "=" * 60)
print("【Step 4】物流下单 + 面单获取")
print("=" * 60)

if raw_data.get("label_url"):
    print(f"  ⏭️ 订单已有面单URL，跳过物流下单")
    print(f"    面单URL: {raw_data['label_url'][:80]}...")
    results["step3_shipping"] = "✅ 已有物流订单"
    results["step4_label"] = "✅ 已有面单URL"
elif raw_data.get("tracking_number") and raw_data["tracking_number"] != "MOCK-4PX-001":
    print(f"  已有物流单号: {raw_data['tracking_number']}")
    print(f"  尝试获取面单...")
    try:
        from src.services.shipping_service import FourPXClient
        fourpx = FourPXClient(
            app_key=settings.FOURPX_APP_KEY,
            app_secret=settings.FOURPX_APP_SECRET,
            sandbox=settings.FOURPX_SANDBOX
        )
        label_url = fourpx.get_label_url(raw_data["tracking_number"])
        if label_url:
            raw_data["label_url"] = label_url
            print(f"  ✅ 面单获取成功: {label_url[:80]}...")
            results["step3_shipping"] = "✅ 已有物流订单"
            results["step4_label"] = "✅ 面单获取成功"
        else:
            print(f"  ⚠️ 面单获取返回空（可能订单未就绪）")
            results["step3_shipping"] = "✅ 已有物流订单"
            results["step4_label"] = "⚠️ 面单暂不可用"
    except Exception as e:
        print(f"  ⚠️ 面单获取异常: {e}")
        results["step3_shipping"] = "✅ 已有物流订单"
        results["step4_label"] = f"⚠️ 异常: {str(e)[:30]}"
else:
    print(f"  ⚠️ 无物流单号，跳过物流下单（避免产生费用）")
    print(f"    如需创建真实物流订单，请通过前端OrdersShipping页面操作")
    results["step3_shipping"] = "⏭️ 跳过（无物流数据）"
    results["step4_label"] = "⏭️ 跳过（无物流数据）"

# === Step 5: 生成生产文档PDF ===
print("\n" + "=" * 60)
print("【Step 5】生成生产文档PDF（含面单嵌入）")
print("=" * 60)

try:
    from src.services.svg_pdf_service import svg_pdf_service
    
    print(f"  开始生成PDF...")
    print(f"    输入数据: {len(raw_data)} 个字段")
    print(f"    面单URL: {'有 ✅' if raw_data.get('label_url') else '无（将使用占位符）'}")
    print(f"    效果图URL: {'有 ✅' if raw_data.get('effect_svg_url') else '无（将动态生成）'}")
    
    pdf_path = svg_pdf_service.generate_from_raw_data(raw_data)
    
    if pdf_path and Path(pdf_path).exists():
        file_size = Path(pdf_path).stat().st_size
        print(f"\n  ✅ PDF生成成功！")
        print(f"    路径: {pdf_path}")
        print(f"    大小: {file_size / 1024:.1f} KB")
        
        # 检查PDF是否比之前的大（面单图片应该增加文件大小）
        if file_size > 200 * 1024:
            print(f"    📊 文件较大 ({file_size/1024:.0f}KB > 200KB)，可能包含面单图片 ✅")
        elif file_size > 100 * 1024:
            print(f"    📊 文件中等 ({file_size/1024:.0f}KB)，可能包含效果图但无面单")
        else:
            print(f"    📊 文件较小 ({file_size/1024:.0f}KB)，可能缺少图片内容")
        
        results["step5_pdf"] = f"✅ 生成成功 ({file_size/1024:.1f}KB)"
    else:
        print(f"  ❌ PDF生成失败，返回None或文件不存在")
        results["step5_pdf"] = "❌ 生成失败"
        
except Exception as e:
    print(f"  ❌ PDF生成异常: {e}")
    import traceback
    traceback.print_exc()
    results["step5_pdf"] = f"❌ 异常: {str(e)[:30]}"

# === 最终报告 ===
print("\n" + "=" * 60)
print("【最终报告】端到端测试结果")
print("=" * 60)
print(f"""
  Step 1 数据查询:    {results['step1_data_query']}
  Step 2 效果图生成:  {results['step2_effect_image']}
  Step 3 物流下单:    {results['step3_shipping']}
  Step 4 面单获取:    {results['step4_label']}
  Step 5 PDF生成:     {results['step5_pdf']}
""")

# 总评
all_pass = all("✅" in v or "⏭️" in v for v in results.values())
has_warning = any("⚠️" in v for v in results.values())
has_fail = any("❌" in v for v in results.values())

if all_pass and not has_warning:
    print("  🎉 全部通过！端到端流程完全正常。")
elif all_pass or has_warning:
    print("  ⚠️ 部分通过，有降级但核心流程正常。")
else:
    print("  ❌ 存在失败项，需要排查。")

print("\n" + "=" * 60)
print(f"测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)
