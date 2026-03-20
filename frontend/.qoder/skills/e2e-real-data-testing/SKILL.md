---
name: e2e-real-data-testing
description: ETSY订单自动化端到端真实数据测试流程，强制要求AI按链路检查数据完整性，禁止省略上游数据准备步骤
---

# ETSY订单自动化 - 端到端真实数据测试流程

## 核心原则

> ⚠️ **禁止省略任何上游数据准备步骤。每个阶段测试前，必须先验证该阶段的所有前置数据已就绪。**

- **测试阶段N之前**，必须先验证阶段1~N-1的数据全部存在且有效
- **禁止用假数据替代真实数据**：如果真实数据不存在，必须先通过正确的上游流程创建
- **演示模式是BUG信号**：如果页面显示"演示模式"或默认假数据，说明数据链路断裂，必须排查修复

---

## 完整订单生命周期流程图

```
📧 邮件接收 (IMAP监控 transaction@etsy.com)
    │
    ▼
🔍 自动解析邮件 (提取：客户名/产品SKU/刻字内容/收件地址)
    │
    ▼
📋 【新订单】status = 'new'
    │  ├─ 点击订单行 → 进入详情页
    │  ├─ 设计器自动加载订单数据（shape/color/font/text）
    │  └─ 生成SVG效果图 → 保存到Supabase Storage
    │
    ▼
📤 【效果图已发送】status = 'effect_sent'
    │  ├─ 效果图通过邮件/链接发送给客服
    │  └─ 客户确认或修改（修改时停留此状态）
    │
    ▼
✅ 【待创建】status = 'pending' 或 'confirmed'
    │  ├─ 出现"创建订单"按钮
    │  └─ 点击"创建订单" → 跳转到【物流下单】页面
    │
    ▼
🚚 【物流下单】
    │  ├─ 自动填充收件人信息（shipping_*字段）
    │  ├─ 自动填充产品重量（sku_mapping.weight_g）
    │  ├─ 选择物流渠道（当前固定PX）
    │  ├─ 创建4PX物流订单 → 获取tracking_number + label_url
    │  └─ 物流面单集成到【生产文档】
    │
    ▼
🏭 【生产中】status = 'producing'
    │  ├─ 生产文档PDF 5大模块完整
    │  │    ├─ 模块1：订单信息（客户/SKU/刻字内容）
    │  │    ├─ 模块2：产品实拍图
    │  │    ├─ 模块3：设计器SVG效果图
    │  │    ├─ 模块4：物流面单
    │  │    └─ 模块5：物流信息
    │  └─ 按生产文档生产
    │
    ▼
📦 【已完成】status = 'delivered'
```

---

## 阶段1：邮件接收与解析

### 功能说明

IMAP监控QQ邮箱，自动抓取来自 `transaction@etsy.com` 的订单通知邮件，解析HTML内容提取订单数据。

### 前置条件

| 条件 | 检查方式 | 说明 |
|------|---------|------|
| QQ邮箱IMAP已启用 | 登录QQ邮箱设置 | 需开启IMAP/SMTP服务 |
| .env配置正确 | 检查 `D:\ETSY_Order_Automation\backend\.env` | EMAIL_HOST/EMAIL_USER/EMAIL_PASSWORD |
| 有未读Etsy订单邮件 | 邮箱收件箱 | 来自 transaction@etsy.com |

### 数据产出（写入orders表）

| 字段 | 来源 | 必须有值 | 说明 |
|------|------|---------|------|
| etsy_order_id | 邮件解析 | ✅ | ETSY平台订单ID |
| customer_name | 邮件解析 | ✅ | 买家姓名 |
| front_text | 邮件解析（刻字内容） | ✅ | 正面刻字 |
| back_text | 邮件解析（背面刻字） | ❌ | 可空 |
| shipping_name | 邮件解析（收件人） | ✅ | 收件人姓名 |
| shipping_address_line1 | 邮件解析 | ✅ | 收件地址 |
| shipping_city | 邮件解析 | ✅ | 城市 |
| shipping_state | 邮件解析 | ❌ | 州/省，可空 |
| shipping_zip | 邮件解析 | ✅ | 邮编 |
| shipping_country | 邮件解析 | ✅ | 国家 |
| country | 邮件解析 | ✅ | 国家代码 |
| sku_id | SKU反推匹配 | ✅ | 关联sku_mapping表 |
| matched_sku_id | SKU反推匹配 | ✅ | 备用SKU关联 |
| status | 初始值 'new' | ✅ | 订单状态 |
| total_amount | 邮件解析 | ✅ | 订单金额 |

### 数据库检查SQL

```sql
-- 检查指定订单的邮件解析数据完整性
SELECT 
    etsy_order_id,
    customer_name,
    front_text,
    shipping_name,
    shipping_address_line1,
    shipping_city,
    shipping_zip,
    shipping_country,
    country,
    sku_id,
    status,
    total_amount,
    CASE 
        WHEN shipping_address_line1 IS NULL OR shipping_address_line1 = '' THEN '❌ 地址缺失'
        WHEN sku_id IS NULL THEN '❌ SKU未关联'
        WHEN country IS NULL OR country = '' THEN '❌ 国家缺失'
        ELSE '✅ 数据完整'
    END AS 检查结果
FROM orders
WHERE etsy_order_id = '你的订单号';
```

### 常见遗漏（AI容易犯的错误）

| 错误行为 | 后果 | 正确做法 |
|---------|------|---------|
| ❌ 跳过邮件解析，直接手动INSERT | shipping_*地址字段为空 | 必须通过邮件解析服务导入 |
| ❌ 未运行SKU反推 | sku_id为空，无法获取shape/color | 确保SKU匹配逻辑执行 |
| ❌ country字段为空 | 后续物流无法选择渠道 | 检查邮件解析逻辑 |
| ❌ 直接复制旧订单数据 | shipping_*字段不匹配新订单 | 每个订单必须独立解析 |

### 验证脚本

```python
# 使用方式：cd D:\ETSY_Order_Automation\backend && poetry run python -c "以下代码"
import os; os.chdir(r'D:\ETSY_Order_Automation\backend')
from src.services.database_service import db

order_id = '你的订单号'  # 替换为实际订单号
order = db.select_one('orders', {'etsy_order_id': order_id})

if not order:
    print(f'❌ 订单 {order_id} 不存在')
else:
    required = ['etsy_order_id', 'customer_name', 'front_text', 'shipping_name', 
                'shipping_address_line1', 'shipping_city', 'shipping_zip', 'shipping_country', 'sku_id']
    missing = [f for f in required if not order.get(f)]
    if missing:
        print(f'❌ 阶段1-邮件解析: 失败（缺失字段: {missing}）')
    else:
        print(f'✅ 阶段1-邮件解析: 通过（{len(required)}字段完整）')
```

---

## 阶段2：效果图生成

### 功能说明

在"待确认订单"页面，选择订单后设计器自动加载：
- 从 `sku_mapping` 获取 shape/color/size
- 从 `orders` 获取 front_text/back_text/font_code
- 设计器渲染效果图SVG
- 上传到 Supabase Storage

### 前置条件（必须全部满足）

| 条件 | 检查方式 | 说明 |
|------|---------|------|
| orders表有status='new'的订单 | SQL查询 | 邮件解析产出 |
| sku_mapping关联正确 | orders.sku_id不为空 | SKU反推结果 |
| 设计器HTML可加载 | 文件存在 | `D:\ETSY_Order_Automation\frontend\public\designer-offline-vector.html` |
| 字体文件已上传 | fonts表有数据 | 9条字体记录 |
| front_text有值 | SQL查询 | 刻字内容不能为空 |

### 数据产出

| 数据 | 存储位置 | 必须有值 | 说明 |
|------|---------|---------|------|
| effect_image_url | orders.effect_image_url | ✅ | 效果图预览URL |
| effect_svg_url | production_documents.effect_svg_url | ✅ | 设计器SVG URL |
| 订单状态更新 | orders.status → 'effect_sent' | ✅ | 状态流转 |

### 常见遗漏（AI容易犯的错误）

| 错误行为 | 后果 | 正确做法 |
|---------|------|---------|
| ❌ saveEffectImage()只弹窗提示 | 未实际保存到数据库 | 检查保存逻辑是否调用后端API |
| ❌ sku_mapping查询失败 | 设计器无法获取shape/color | 使用显式外键 `sku_mapping!orders_sku_id_fkey(*)` |
| ❌ production_documents表未创建记录 | effect_svg_url不存在 | 确保保存时创建关联记录 |
| ❌ 效果图SVG未上传到Storage | URL为空或无效 | 检查Supabase Storage配置 |
| ❌ 直接修改status跳过此阶段 | 后续PDF无设计图 | 必须完成效果图生成 |

### 验证脚本

```python
# 使用方式：cd D:\ETSY_Order_Automation\backend && poetry run python -c "以下代码"
import os; os.chdir(r'D:\ETSY_Order_Automation\backend')
from src.services.database_service import db

order_id = '你的订单号'  # 替换为实际订单号
order = db.select_one('orders', {'etsy_order_id': order_id})

if not order:
    print(f'❌ 订单不存在')
else:
    # 检查效果图
    effect_url = order.get('effect_image_url')
    status = order.get('status')
    
    # 检查production_documents
    prod_doc = db.select_one('production_documents', {'order_id': order.get('id')})
    svg_url = prod_doc.get('effect_svg_url') if prod_doc else None
    
    if effect_url and svg_url:
        print(f'✅ 阶段2-效果图生成: 通过')
        print(f'   effect_image_url: {effect_url[:50]}...')
        print(f'   effect_svg_url: {svg_url[:50]}...')
    else:
        missing = []
        if not effect_url: missing.append('effect_image_url')
        if not svg_url: missing.append('effect_svg_url')
        print(f'❌ 阶段2-效果图生成: 失败（缺失: {missing}）')
```

---

## 阶段3：订单确认 → 创建订单

### 功能说明

效果图发送给客服后，客户确认无误，订单状态流转为'confirmed'/'pending'，出现"创建订单"按钮。

### 前置条件

| 条件 | 检查方式 | 说明 |
|------|---------|------|
| effect_image_url有值 | SQL | 效果图已生成 |
| 状态为effect_sent | SQL | 效果图已发送 |
| 客户已确认 | 业务流程 | 无修改需求 |

### 数据产出

| 操作 | 结果 | 说明 |
|------|------|------|
| 点击"创建订单" | status → 'confirmed' | 状态流转 |
| 页面跳转 | 进入物流下单页面 | 前端路由 |

### 常见遗漏

| 错误行为 | 后果 | 正确做法 |
|---------|------|---------|
| ❌ 直接手动修改status为confirmed | 跳过效果图生成 | 必须先完成阶段2 |
| ❌ "创建订单"按钮未绑定状态变更 | status不变 | 检查按钮onClick逻辑 |

### 验证脚本

```python
# 使用方式：cd D:\ETSY_Order_Automation\backend && poetry run python -c "以下代码"
import os; os.chdir(r'D:\ETSY_Order_Automation\backend')
from src.services.database_service import db

order_id = '你的订单号'
order = db.select_one('orders', {'etsy_order_id': order_id})

if not order:
    print(f'❌ 订单不存在')
else:
    status = order.get('status')
    effect_url = order.get('effect_image_url')
    
    if status in ['confirmed', 'pending'] and effect_url:
        print(f'✅ 阶段3-订单确认: 通过（status={status}）')
    elif status in ['confirmed', 'pending'] and not effect_url:
        print(f'⚠️ 阶段3-订单确认: 异常（status={status} 但 effect_image_url为空）')
    else:
        print(f'❌ 阶段3-订单确认: 未完成（当前status={status}）')
```

---

## 阶段4：物流下单

### 功能说明

在物流下单页面，选择confirmed订单，自动填充所有字段，调用4PX API创建物流订单。

### 前置条件（⚠️ 关键！大量测试失败出在这里）

| 条件 | 检查方式 | 为什么重要 | 错误表现 |
|------|---------|-----------|---------|
| orders.status = 'confirmed' | SQL | 页面只显示confirmed订单 | 订单列表为空 |
| shipping_address_line1有值 | SQL | 4PX必填：收件地址 | "地址不能为空" |
| shipping_city有值 | SQL | 4PX必填：城市 | API报错 |
| shipping_zip有值 | SQL | 4PX必填：邮编 | API报错 |
| shipping_country有值 | SQL | 4PX必填：国家 | 无法选渠道 |
| sku_mapping.weight_g有值 | SQL | 产品重量计算 | 默认30g不准确 |
| 4PX API凭证有效 | .env检查 | FOURPX_APP_KEY/SECRET | 401认证失败 |
| 后端API运行中 | http://localhost:8000 | 后端服务 | 网络错误 |
| 前端dev运行中 | http://localhost:5173 | 前端服务 | 页面无法访问 |

### 自动填充字段映射

详见 `D:\ETSY_Order_Automation\frontend\.qoder\skills\shipping-autofill\SKILL.md`

| 表单字段 | 数据来源 | 必填 | fallback |
|---------|---------|------|---------|
| 收件人姓名 | orders.shipping_name | ✅ | → orders.customer_name |
| 收件人电话 | 系统自动生成 | ✅ | +1 + 区号 + 7位随机数 |
| 街道地址 | orders.shipping_address_line1 | ✅ | 无fallback，必须有值 |
| 城市 | orders.shipping_city | ✅ | 无 |
| 州/省 | orders.shipping_state | ❌ | 可空 |
| 邮编 | orders.shipping_zip | ✅ | 无 |
| 国家 | orders.shipping_country | ✅ | → orders.country |
| 重量(g) | sku_mapping.weight_g | ✅ | → 30g默认 |
| 申报价值 | orders.total_amount | ✅ | 无 |

### 数据产出

| 数据 | 存储位置 | 必须有值 | 说明 |
|------|---------|---------|------|
| tracking_number | logistics.tracking_number | ✅ | 4PX运单号 |
| label_url | logistics.label_url | ✅ | 面单PNG URL |
| channel_code | logistics.channel_code | ✅ | 物流渠道代码 |
| 订单状态更新 | orders.status → 'producing' | ✅ | 状态流转 |

### 常见遗漏（AI容易犯的错误）

| 错误行为 | 后果 | 正确做法 |
|---------|------|---------|
| ❌ 数据库无confirmed订单 | 页面显示演示模式 | 确保阶段1-3完成 |
| ❌ shipping_*字段为空 | 地址自动填充为空，4PX报错 | 检查邮件解析是否提取地址 |
| ❌ sku_mapping.weight_g为0 | 重量默认30g不准确 | 更新sku_mapping表 |
| ❌ Supabase查询双外键歧义 | 页面回退演示模式 | 使用显式外键语法 |
| ❌ 4PX API参数格式错误 | "System processing failed" | 参考经验：weight用克，严格按API格式 |
| ❌ 直接手动插入logistics记录 | 缺少tracking_number | 必须调用4PX API |

### 验证脚本

```python
# 使用方式：cd D:\ETSY_Order_Automation\backend && poetry run python -c "以下代码"
import os; os.chdir(r'D:\ETSY_Order_Automation\backend')
from src.services.database_service import db

order_id = '你的订单号'
order = db.select_one('orders', {'etsy_order_id': order_id})

if not order:
    print(f'❌ 订单不存在')
else:
    # 检查前置条件
    shipping_fields = ['shipping_address_line1', 'shipping_city', 'shipping_zip', 'shipping_country']
    missing_shipping = [f for f in shipping_fields if not order.get(f)]
    
    if missing_shipping:
        print(f'❌ 阶段4-物流下单: 前置条件不满足')
        print(f'   缺失shipping字段: {missing_shipping}')
    else:
        # 检查logistics记录
        logistics = db.select_one('logistics', {'order_id': order.get('id')})
        if logistics and logistics.get('tracking_number') and logistics.get('label_url'):
            print(f'✅ 阶段4-物流下单: 通过')
            print(f'   tracking_number: {logistics.get("tracking_number")}')
            print(f'   label_url: {logistics.get("label_url")[:50]}...')
        else:
            print(f'❌ 阶段4-物流下单: 未完成（logistics记录不完整）')
```

---

## 阶段5：生产文档PDF集成

### 功能说明

整合5大模块生成A4生产文档PDF。

### 前置条件

| 模块 | 数据来源 | 必须存在 | 降级方案 |
|------|---------|---------|---------|
| 模块1：订单信息 | orders表 | ✅ | 无 |
| 模块2：产品实拍图 | product_photos表 + Supabase Storage | ✅ | 占位符 |
| 模块3：设计器SVG | production_documents.effect_svg_url | ✅ | 动态生成（精度降低） |
| 模块4：物流面单 | logistics.label_url → 4PX API下载PNG | ✅ | 占位符 |
| 模块5：物流信息 | logistics表 | ✅ | 显示"待下单" |

### SVG模板占位符

| 占位符 | 数据来源 | 说明 |
|--------|---------|------|
| EFFECT_FRONT_SHAPE | 设计器SVG或动态生成 | 正面效果图 |
| EFFECT_BACK_SHAPE | 设计器SVG或动态生成 | 背面效果图 |
| PRODUCT_PHOTO_BASE64 | 产品实拍图base64 | 产品照片 |
| SHIPPING_LABEL_DATA | 面单PNG base64 | 物流面单 |

### 数据产出

| 数据 | 存储位置 | 说明 |
|------|---------|------|
| PDF文件 | `D:\ETSY_Order_Automation\backend\output\POD_xxx.pdf` | 本地文件 |
| PDF URL | orders.production_pdf_url | Supabase Storage URL |

### 常见遗漏

| 错误行为 | 后果 | 正确做法 |
|---------|------|---------|
| ❌ effect_svg_url为空 | 降级到动态生成（可能不够精确） | 确保阶段2完成 |
| ❌ label_url为空或无效 | 面单区域为占位符 | 确保阶段4完成 |
| ❌ product_photos表无对应SKU照片 | 产品图为占位符 | 上传产品照片 |
| ❌ 直接跳过PDF生成 | 无生产文档 | 必须调用PDF生成API |

### 验证脚本

```python
# 使用方式：cd D:\ETSY_Order_Automation\backend && poetry run python -c "以下代码"
import os; os.chdir(r'D:\ETSY_Order_Automation\backend')
from src.services.database_service import db
from pathlib import Path

order_id = '你的订单号'
order = db.select_one('orders', {'etsy_order_id': order_id})

if not order:
    print(f'❌ 订单不存在')
else:
    pdf_url = order.get('production_pdf_url')
    
    # 检查本地PDF文件
    output_dir = Path(r'D:\ETSY_Order_Automation\backend\output')
    pdf_files = list(output_dir.glob(f'POD_{order_id}*.pdf'))
    
    if pdf_url:
        print(f'✅ 阶段5-生产文档PDF: 通过')
        print(f'   production_pdf_url: {pdf_url[:50]}...')
    elif pdf_files:
        print(f'⚠️ 阶段5-生产文档PDF: 本地文件存在但未上传')
        print(f'   本地文件: {pdf_files[0]}')
    else:
        print(f'❌ 阶段5-生产文档PDF: 未生成')
```

---

## 阶段6：生产中 → 已完成

### 功能说明

按生产文档PDF打印并生产，完成后更新状态。

### 前置条件

| 条件 | 检查方式 | 说明 |
|------|---------|------|
| production_pdf_url有值 | orders表 | 生产文档已生成 |
| PDF文件可下载 | 直接访问URL | 文件有效 |
| 5大模块完整 | 打开PDF目视检查 | 无占位符 |

### 状态流转

```
producing → delivered（生产完成并发货）
```

---

## 全链路数据完整性检查脚本

**一次性检查指定订单的全链路数据完整性：**

```python
# 使用方式：
# cd D:\ETSY_Order_Automation\backend
# poetry run python -c "
import os
os.chdir(r'D:\ETSY_Order_Automation\backend')
from src.services.database_service import db

def check_order_integrity(order_id):
    '''检查订单全链路数据完整性'''
    print(f'\n========== 订单 {order_id} 全链路检查 ==========\n')
    
    # 1. 查询订单
    order = db.select_one('orders', {'etsy_order_id': order_id})
    if not order:
        print(f'❌ 订单不存在: {order_id}')
        return
    
    db_id = order.get('id')
    results = []
    
    # 阶段1: 邮件解析
    stage1_fields = ['etsy_order_id', 'customer_name', 'front_text', 'shipping_name', 
                     'shipping_address_line1', 'shipping_city', 'shipping_zip', 
                     'shipping_country', 'sku_id', 'total_amount']
    stage1_missing = [f for f in stage1_fields if not order.get(f)]
    if stage1_missing:
        results.append(f'❌ 阶段1-邮件解析: 失败（缺失: {stage1_missing}）')
    else:
        results.append(f'✅ 阶段1-邮件解析: 通过（{len(stage1_fields)}字段完整）')
    
    # 阶段2: 效果图生成
    prod_doc = db.select_one('production_documents', {'order_id': db_id})
    effect_url = order.get('effect_image_url')
    svg_url = prod_doc.get('effect_svg_url') if prod_doc else None
    if effect_url and svg_url:
        results.append(f'✅ 阶段2-效果图生成: 通过')
    else:
        missing = []
        if not effect_url: missing.append('effect_image_url')
        if not svg_url: missing.append('effect_svg_url')
        results.append(f'❌ 阶段2-效果图生成: 失败（缺失: {missing}）')
    
    # 阶段3: 订单确认
    status = order.get('status')
    if status in ['confirmed', 'pending', 'producing', 'delivered']:
        results.append(f'✅ 阶段3-订单确认: 通过（status={status}）')
    else:
        results.append(f'❌ 阶段3-订单确认: 未完成（status={status}）')
    
    # 阶段4: 物流下单
    logistics = db.select_one('logistics', {'order_id': db_id})
    if logistics and logistics.get('tracking_number') and logistics.get('label_url'):
        results.append(f'✅ 阶段4-物流下单: 通过（tracking: {logistics.get(\"tracking_number\")}）')
    else:
        results.append(f'❌ 阶段4-物流下单: 未完成')
    
    # 阶段5: 生产文档PDF
    pdf_url = order.get('production_pdf_url')
    if pdf_url:
        results.append(f'✅ 阶段5-生产文档PDF: 通过')
    else:
        results.append(f'❌ 阶段5-生产文档PDF: 未生成')
    
    # 输出结果
    for r in results:
        print(r)
    
    # 统计
    passed = sum(1 for r in results if r.startswith('✅'))
    print(f'\n========== 检查完成: {passed}/5 阶段通过 ==========')

# 执行检查
check_order_integrity('你的订单号')
# "
```

---

## AI开发规则（强制执行）

### 禁止行为

| 禁止行为 | 原因 | 替代方案 |
|---------|------|---------|
| ❌ 跳过上游数据准备 | 下游测试必定失败 | 先验证阶段1~N-1数据 |
| ❌ 用假数据替代真实数据 | 无法验证真实流程 | 通过正确上游流程创建数据 |
| ❌ 手动INSERT替代邮件解析 | shipping_*字段缺失 | 通过邮件解析服务导入 |
| ❌ 直接修改status跳过阶段 | 关联数据不存在 | 按顺序完成每个阶段 |
| ❌ 忽略"演示模式"提示 | 说明数据链路断裂 | 排查修复数据问题 |

### 必须执行

| 必须行为 | 时机 | 方式 |
|---------|------|------|
| ✅ 运行全链路检查脚本 | 每次测试前 | 执行上方Python脚本 |
| ✅ 验证前置数据完整 | 测试任何阶段前 | 检查该阶段的所有前置条件 |
| ✅ 检查服务运行状态 | 测试API前 | 确认后端8000/前端5173端口 |
| ✅ 查看实际页面显示 | 测试功能后 | 确认无"演示模式"提示 |

---

## 关键文件清单

### 前端

| 文件 | 功能 |
|------|------|
| `D:\ETSY_Order_Automation\frontend\src\views\Admin\OrdersPending.vue` | 待确认订单+设计器 |
| `D:\ETSY_Order_Automation\frontend\src\views\Admin\OrdersShipping.vue` | 物流下单 |
| `D:\ETSY_Order_Automation\frontend\src\stores\orderStore.js` | 订单数据管理 |
| `D:\ETSY_Order_Automation\frontend\public\designer-offline-vector.html` | 离线设计器 |

### 后端

| 文件 | 功能 |
|------|------|
| `D:\ETSY_Order_Automation\backend\src\api\main.py` | API路由 |
| `D:\ETSY_Order_Automation\backend\src\services\svg_pdf_service.py` | PDF生成 |
| `D:\ETSY_Order_Automation\backend\src\services\shipping_service.py` | 4PX物流 |
| `D:\ETSY_Order_Automation\backend\src\services\effect_image_service.py` | 效果图生成 |
| `D:\ETSY_Order_Automation\backend\src\services\email_service.py` | 邮件解析 |
| `D:\ETSY_Order_Automation\backend\src\services\database_service.py` | 数据库操作 |
| `D:\ETSY_Order_Automation\backend\src\models\order.py` | 数据模型 |

### 数据库表

| 表 | 核心字段 | 说明 |
|------|---------|------|
| orders | etsy_order_id, status, shipping_*, sku_id, effect_image_url, production_pdf_url | 订单主表 |
| sku_mapping | shape, color, size, weight_g, sku_code | SKU对照表 |
| logistics | tracking_number, label_url, channel_code, order_id | 物流信息表 |
| production_documents | effect_svg_url, effect_jpg_url, order_id | 生产文档表 |
| product_photos | photo_url, shape, size | 产品实拍图 |
| fonts | font_code, font_file_url | 字体表 |

### API端点

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/effect-image/generate-and-upload` | POST | 生成并上传效果图 |
| `/api/pdf/generate-and-upload` | POST | 生成并上传PDF |
| `/api/shipping/create-order` | POST | 创建4PX物流订单 |
| `/api/order/update-status` | POST | 更新订单状态 |

---

## 版本记录

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-03 | 初始版本，基于端到端真实数据测试实战提炼 |
