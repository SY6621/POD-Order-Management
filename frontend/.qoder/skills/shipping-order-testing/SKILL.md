---
name: shipping-order-e2e-testing
description: 物流下单模块端到端测试规范。测试4PX物流API对接、面单获取、数据库状态流转。适用于物流下单功能测试、物流API对接调试、订单状态流转验证。
---

# 物流下单模块端到端测试规范

## 概述

本文档定义ETSY订单自动化系统"物流下单"模块的完整测试流程，覆盖前端交互、后端API、4PX物流对接、数据库状态流转的端到端验证。

## 测试环境要求

### 前置条件检查清单

```
测试环境检查清单：
- [ ] Vue 开发服务器运行中 (http://localhost:5173)
- [ ] FastAPI 后端服务运行中 (http://localhost:8000)
- [ ] Supabase 数据库连接正常
- [ ] 4PX API 凭证配置正确 (backend/.env)
- [ ] 至少1个测试订单处于"待下单"状态
```

### 必需配置文件

**后端环境变量** (`backend/.env`)：
```ini
# 4PX递四方物流API配置
FOURPX_APP_KEY=your_app_key
FOURPX_APP_SECRET=your_app_secret
FOURPX_SANDBOX=false  # true=测试环境, false=正式环境
```

**API端点**：
- 正式环境：`https://open.4px.com/router/api/service`
- 测试环境：`https://open-test.4px.com/router/api/service`

---

## 测试流程

### 阶段一：测试数据准备

#### 1.1 检查订单状态

执行脚本检查当前订单：

```bash
cd D:\ETSY_Order_Automation\backend
poetry run python scripts/check_order_status.py
```

预期输出：
```
订单总数: X 条
- pending: X 条
- confirmed: X 条 (待下单)
- producing: X 条
```

#### 1.2 准备测试订单

**方式A：使用现有订单**
- 需要订单状态为 `confirmed`
- 订单需包含完整收件人信息

**方式B：创建测试订单**

使用脚本创建测试订单：
```bash
poetry run python scripts/create_test_order.py
```

或手动插入测试数据：
```sql
INSERT INTO orders (
    etsy_order_id, 
    customer_name, 
    country, 
    status,
    front_text,
    quantity
) VALUES (
    'TEST-SHIPPING-001',
    'Test Customer',
    'United States',
    'confirmed',
    'Bella',
    1
);
```

#### 1.3 验证订单完整性

检查订单必须包含：
- ✅ `etsy_order_id`: Etsy订单号
- ✅ `customer_name`: 客户姓名
- ✅ `country`: 目的国家
- ✅ 收件人地址信息（`shipping_*` 字段或 logistics 表关联）
- ✅ SKU信息（包含重量 `weight_g`）

---

### 阶段二：前端界面测试

#### 2.1 访问物流下单页面

**测试步骤**：
1. 打开浏览器访问：`http://localhost:5173/admin/orders/shipping`
2. 检查页面是否正常加载

**验证点**：
- [ ] 页面标题显示"物流下单"
- [ ] 顶部显示统计数据：待下单数、今日已下数
- [ ] 物流公司Tab显示：4PX全球直发、燕文物流、云途物流
- [ ] 左侧订单列表加载完成
- [ ] 右侧显示"请从左侧选择一个订单"提示

#### 2.2 订单列表展示测试

**测试步骤**：
1. 查看左侧订单列表
2. 检查订单信息显示

**验证点**：
- [ ] 订单号显示正确（`etsy_order_id`）
- [ ] 客户姓名显示正确
- [ ] SKU代码显示正确（从 `sku_mapping` 表关联）
- [ ] 国家显示正确
- [ ] 每行有"选择"按钮
- [ ] 支持搜索功能（输入订单号/客户名）

#### 2.3 选择订单测试

**测试步骤**：
1. 点击某个订单的"选择"按钮
2. 观察右侧表单

**验证点**：
- [ ] 选中行背景变为蓝色
- [ ] "选择"按钮变为"当前"
- [ ] 右侧表单区域显示
- [ ] Section A（订单信息）自动填充
- [ ] Section B（收件人信息）自动填充
- [ ] Section C（物流渠道）显示默认选项

---

### 阶段三：表单填写测试

#### 3.1 订单信息展示（只读）

**验证点**：
- [ ] 订单号正确
- [ ] 客户姓名正确
- [ ] SKU代码正确
- [ ] 产品描述合理

#### 3.2 收件人信息填写

**必填字段**（标记红色星号 *）：
- [ ] 姓名：自动填充，可修改
- [ ] 详细地址：自动填充，可修改
- [ ] 城市：自动填充，可修改
- [ ] 邮编：自动填充，可修改
- [ ] 国家：下拉选择，默认值合理

**可选字段**：
- [ ] 电话：可选填写
- [ ] 邮箱：可选填写
- [ ] 州/省：可选填写

#### 3.3 物流渠道选择

**验证点**：
- [ ] 下拉框显示可用渠道列表
- [ ] 默认选择 "PX" 或其他预设渠道
- [ ] 渠道代码格式正确（如 `PX`, `U0107600`）

#### 3.4 高级选项（可选）

**展开测试**：
1. 点击"展开高级选项"
2. 检查显示内容

**验证点**：
- [ ] 包裹信息：重量、长宽高
- [ ] 申报信息：中英文品名、申报价值
- [ ] 是否带电选项
- [ ] 发件人信息（只读）

---

### 阶段四：创建物流订单测试

#### 4.1 单订单下单测试

**测试步骤**：
1. 选择一个订单
2. 填写/确认表单信息
3. 点击"创建物流订单"按钮

**预期行为**：
- 按钮显示 loading 状态
- 控制台显示请求日志
- 等待响应（通常 3-10 秒）

#### 4.2 成功响应验证

**验证点**：
- [ ] 显示绿色成功提示框
- [ ] 显示物流单号（tracking_number）
- [ ] 显示"下载面单PDF"和"打印面单"按钮
- [ ] 显示"继续下单"按钮
- [ ] 订单从左侧列表移除
- [ ] 今日已下数量 +1

**数据库验证**：
```bash
# 检查 logistics 表更新
cd D:\ETSY_Order_Automation\backend
poetry run python -c "
from supabase import create_client
import os
env = {}
with open('.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            env[k] = v.strip('\"').strip(\"'\")
sb = create_client(env['SUPABASE_URL'], env['SUPABASE_KEY'])
logs = sb.table('logistics').select('*').eq('order_id', 'YOUR_ORDER_ID').execute()
print(logs.data)
"
```

**检查项**：
- [ ] `tracking_number` 已填充
- [ ] `label_url` 已填充（PDF URL）
- [ ] `shipping_status` = 'shipped'
- [ ] `shipped_at` 有值

**订单状态验证**：
```sql
SELECT id, etsy_order_id, status FROM orders WHERE id = YOUR_ORDER_ID;
```
- [ ] `status` 已更新为 `producing`

#### 4.3 面单下载测试

**测试步骤**：
1. 点击"下载面单PDF"按钮
2. 检查新标签页打开

**验证点**：
- [ ] 新标签页打开 4PX 面单 PDF
- [ ] PDF 显示正确信息：
  - 收件人姓名、地址
  - 运单号（条形码）
  - 物流渠道信息
  - 目的国家代码

#### 4.4 面单打印测试

**测试步骤**：
1. 点击"打印面单"按钮
2. 检查打印预览

**验证点**：
- [ ] 打印预览窗口打开
- [ ] 面单格式正确（通常 10x10cm 或 10x15cm）
- [ ] 条形码清晰可读

---

### 阶段五：错误处理测试

#### 5.1 必填字段验证

**测试步骤**：
1. 清空某个必填字段
2. 点击"创建物流订单"

**预期结果**：
- [ ] 显示提示："请填写必填项：姓名、地址、城市、邮编、国家"
- [ ] 不发送请求

#### 5.2 4PX API 错误测试

**常见错误场景**：

| 错误代码 | 原因 | 验证点 |
|---------|------|--------|
| 签名错误 | app_key/app_secret 不正确 | 显示"签名验证失败" |
| 地址无效 | 地址格式不正确 | 显示具体错误信息 |
| 渠道不可用 | 该国家不支持该渠道 | 显示"渠道不可用" |
| 网络超时 | 4PX服务不可达 | 显示"网络错误" |

**模拟测试方法**：
1. 在 `.env` 中设置错误的 `FOURPX_APP_KEY`
2. 尝试下单
3. 验证错误提示是否友好

#### 5.3 数据库更新失败测试

**测试步骤**：
1. 暂时断开 Supabase 连接
2. 尝试下单
3. 观察错误处理

**验证点**：
- [ ] 捕获异常
- [ ] 显示友好错误提示
- [ ] 不影响其他订单

---

### 阶段六：批量下单测试

#### 6.1 多选订单

**测试步骤**：
1. 在左侧列表勾选 2-3 个订单
2. 观察顶部"已选 X 单"提示

**验证点**：
- [ ] 复选框工作正常
- [ ] "全选"功能正常
- [ ] 显示批量下单按钮

#### 6.2 批量下单执行

**测试步骤**：
1. 点击"批量下单 (X单)"按钮
2. 观察进度显示

**验证点**：
- [ ] 显示批量进度："正在批量下单 (1/X)"
- [ ] 每个订单独立处理
- [ ] 部分成功时显示成功/失败统计

#### 6.3 批量结果展示

**验证点**：
- [ ] 显示批量下单结果列表
- [ ] 每条记录显示：订单号、状态、运单号
- [ ] 失败记录显示错误原因
- [ ] 提供批量下载面单功能（如有）

---

### 阶段七：数据流完整性验证

#### 7.1 前端 → 后端

**验证点**：
- [ ] 请求参数完整
- [ ] 数据类型正确
- [ ] 字段命名一致

**示例请求体**：
```json
{
  "order_id": "uuid-string",
  "logistics_product_code": "PX",
  "recipient_name": "John Doe",
  "recipient_phone": "+1234567890",
  "recipient_email": "john@example.com",
  "recipient_street": "123 Main St",
  "recipient_city": "New York",
  "recipient_state": "NY",
  "recipient_postcode": "10001",
  "recipient_country": "US",
  "weight_kg": 0.03,
  "declare_value": 10.0,
  "declare_currency": "USD"
}
```

#### 7.2 后端 → 4PX API

**验证点**：
- [ ] 签名生成正确
- [ ] 请求格式符合 4PX 规范
- [ ] 必填字段完整
- [ ] 重量单位正确（克，整数）

**4PX 请求结构**：
```json
{
  "ref_no": "ETSY-ORDER-ID",
  "business_type": "BDS",
  "logistics_service_info": {
    "logistics_product_code": "PX"
  },
  "parcel_list": [{
    "weight": 30,
    "parcel_value": 10.0,
    "currency": "USD",
    "declare_product_info": [...]
  }],
  "sender": {...},
  "recipient_info": {...}
}
```

#### 7.3 4PX → 数据库

**验证点**：
- [ ] 解析返回数据正确
- [ ] 提取 `4px_tracking_no`
- [ ] 获取 `label_url`
- [ ] 更新 logistics 表
- [ ] 更新 orders 表状态

---

## 测试命令速查表

### 后端服务操作

```powershell
# 启动后端服务
cd D:\ETSY_Order_Automation\backend
poetry run uvicorn src.api.main:app --reload --port 8000

# 检查服务状态
curl http://localhost:8000/health

# 查看 4PX API 日志（调试用）
# 在 main.py 中添加 print() 输出
```

### 数据库操作

```powershell
# 查询订单状态
poetry run python scripts/check_order_status.py

# 重置订单状态为待下单
poetry run python scripts/reset_orders_for_test.py

# 查看物流记录
poetry run python -c "
from supabase import create_client
import os
env = {}
with open('.env') as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            env[k] = v.strip('\"').strip(\"'\")
sb = create_client(env['SUPABASE_URL'], env['SUPABASE_KEY'])
logs = sb.table('logistics').select('*').execute()
for log in logs.data:
    print(f'{log[\"id\"]}: {log[\"tracking_number\"]} - {log[\"shipping_status\"]}')
"
```

### 前端服务操作

```powershell
# 启动前端服务
cd D:\ETSY_Order_Automation\frontend
npm run dev

# 构建生产版本
npm run build
```

---

## 常见问题排查

### Q1: 订单列表为空

**原因**：
- 订单状态不是 `confirmed`
- Supabase 连接失败

**排查**：
```powershell
# 检查订单状态
poetry run python scripts/check_order_status.py

# 检查 Supabase 连接
curl https://rtuzqnoztrdvhfnndqjv.supabase.co/rest/v1/orders \
  -H "apikey: YOUR_KEY"
```

### Q2: 下单返回"签名验证失败"

**原因**：
- `FOURPX_APP_KEY` 或 `FOURPX_APP_SECRET` 错误
- 签名算法实现不正确

**排查**：
```powershell
# 检查配置
cd D:\ETSY_Order_Automation\backend
type .env | findstr "FOURPX"

# 测试签名生成
poetry run python -c "
from src.services.shipping_service import FourPXClient
client = FourPXClient()
sign_str, sign, ts = client.generate_sign('test.method', '1.0', {})
print(f'Sign: {sign}')
"
```

### Q3: 面单 URL 为空

**原因**：
- 4PX 订单创建成功但面单未生成
- `get_label` API 调用失败

**排查**：
```powershell
# 手动获取面单
poetry run python -c "
from src.services.shipping_service import FourPXClient
client = FourPXClient()
result = client.get_label('YOUR_TRACKING_NUMBER')
print(result)
"
```

### Q4: 订单状态未更新

**原因**：
- 数据库更新失败
- `logistics` 表记录不存在

**排查**：
```sql
-- 检查 logistics 表是否有对应订单的记录
SELECT * FROM logistics WHERE order_id = 'YOUR_ORDER_ID';

-- 如果没有，手动插入
INSERT INTO logistics (order_id, recipient_name, country, city, street_address, postal_code)
SELECT id, customer_name, country, shipping_city, shipping_address_line1, shipping_zip
FROM orders WHERE id = 'YOUR_ORDER_ID';
```

---

## 测试报告模板

### 测试执行记录

```
物流下单模块测试报告
====================

测试日期：YYYY-MM-DD
测试人员：
测试环境：[开发/测试/生产]

一、环境检查
- [ ] Vue 服务运行
- [ ] FastAPI 服务运行
- [ ] Supabase 连接
- [ ] 4PX API 配置

二、功能测试结果
| 测试项 | 结果 | 备注 |
|--------|------|------|
| 订单列表展示 | PASS/FAIL | |
| 订单选择 | PASS/FAIL | |
| 表单自动填充 | PASS/FAIL | |
| 创建物流订单 | PASS/FAIL | |
| 面单下载 | PASS/FAIL | |
| 面单打印 | PASS/FAIL | |
| 批量下单 | PASS/FAIL | |

三、异常场景测试
| 场景 | 预期 | 实际 | 结果 |
|------|------|------|------|
| 必填字段为空 | 提示错误 | | |
| API签名错误 | 友好提示 | | |
| 网络超时 | 友好提示 | | |

四、数据流验证
- [ ] 前端→后端数据正确
- [ ] 后端→4PX数据正确
- [ ] 4PX→数据库更新正确

五、问题记录
1. [问题描述]
   - 重现步骤：
   - 预期结果：
   - 实际结果：
   - 截图：

六、结论
[ ] 测试通过
[ ] 需修复后重测
[ ] 严重问题，阻塞发布

七、建议
[改进建议]
```

---

## 自动化测试建议

### 单元测试示例

```python
# tests/test_shipping_service.py
def test_fourpx_sign_generation():
    """测试4PX签名生成"""
    client = FourPXClient(
        app_key="test_key",
        app_secret="test_secret"
    )
    sign_str, sign, ts = client.generate_sign("test.method", "1.0", {})
    assert len(sign) == 32  # MD5 32位
    assert sign.islower()   # 小写

def test_create_shipping_order(client):
    """测试创建物流订单API"""
    response = client.post("/api/shipping/create-order", json={
        "order_id": "test-uuid",
        "logistics_product_code": "PX",
        "recipient_name": "Test User",
        "recipient_street": "123 Test St",
        "recipient_city": "Test City",
        "recipient_postcode": "12345",
        "recipient_country": "US"
    })
    assert response.status_code == 200
```

### E2E 测试示例

```javascript
// tests/e2e/shipping.spec.js
describe('物流下单模块', () => {
  it('应该显示待下单订单列表', () => {
    cy.visit('/admin/orders/shipping')
    cy.get('[data-cy=order-list]').should('be.visible')
    cy.get('[data-cy=order-item]').should('have.length.gt', 0)
  })

  it('应该成功创建物流订单', () => {
    cy.visit('/admin/orders/shipping')
    cy.get('[data-cy=order-item]').first().click()
    cy.get('[data-cy=create-order-btn]').click()
    cy.get('[data-cy=success-message]').should('be.visible')
    cy.get('[data-cy=tracking-number]').should('be.visible')
  })
})
```

---

## 附录

### A. 4PX API 错误码对照表

| 错误码 | 含义 | 处理建议 |
|--------|------|----------|
| 1001 | 签名错误 | 检查 app_key 和 app_secret |
| 1002 | 参数错误 | 检查必填字段 |
| 1003 | 订单已存在 | 使用不同订单号 |
| 1004 | 渠道不可用 | 更换物流渠道 |
| 1005 | 地址格式错误 | 检查地址字段格式 |

### B. 国家代码对照表

| 国家 | 代码 | 国家 | 代码 |
|------|------|------|------|
| 美国 | US | 加拿大 | CA |
| 英国 | GB | 澳大利亚 | AU |
| 德国 | DE | 法国 | FR |
| 日本 | JP | 韩国 | KR |
| 新加坡 | SG | 新西兰 | NZ |

### C. 物流产品代码

| 代码 | 名称 | 时效 | 备注 |
|------|------|------|------|
| PX | 4PX全球直发 | 7-15天 | 默认渠道 |
| U0107600 | 4PX联邮通 | 10-20天 | 经济型 |

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0 | 2026-03-25 | 初始版本，覆盖完整测试流程 |
