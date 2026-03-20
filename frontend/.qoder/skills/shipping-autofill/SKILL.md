---
name: shipping-autofill
description: 物流下单页面自动填充数据规范，批量下单场景必须全自动填充
---

# 物流下单 - 自动填充数据规范

批量下单场景下，选择订单后所有字段必须自动填充，操作员无需手动输入。
适用于：物流下单页面开发、4PX API集成、订单数据处理。

---

## 核心原则

> ⚠️ **最基本要求**：订单多时无法一个个手动填写，选择订单后所有表单字段必须自动填充完成。

- 操作员只需：选择订单 → 确认提交
- 禁止：要求操作员手动输入任何可从数据库获取的字段

---

## 自动填充字段映射表

### 订单基础信息

| 表单字段 | 数据来源 | 必填 | 说明 |
|---------|---------|------|------|
| 订单号 | orders.etsy_order_id | ✅ | ETSY平台订单ID |
| 客户名 | orders.customer_name | ✅ | 买家姓名 |
| SKU | sku_mapping.sku_code | ✅ | 通过 orders.sku_id 关联 |
| 产品名(中) | 固定值："不锈钢宠物牌" | ✅ | 海关申报用 |
| 产品名(英) | 固定值："Stainless Steel Pet ID Tag" | ✅ | 海关申报用 |

### 收件人信息

| 表单字段 | 数据来源 | 必填 | fallback |
|---------|---------|------|---------|
| 姓名 | orders.shipping_name | ✅ | → orders.customer_name |
| 电话 | 系统自动生成 | ✅ | +1 + 美国区号 + 7位随机数 |
| 街道地址 | orders.shipping_address_line1 | ✅ | 无fallback，必须有值 |
| 城市 | orders.shipping_city | ✅ | 无 |
| 州/省 | orders.shipping_state | ❌ | 可空 |
| 邮编 | orders.shipping_zip | ✅ | 无 |
| 国家 | orders.shipping_country | ✅ | → orders.country |

### 产品信息

| 表单字段 | 数据来源 | 必填 | 说明 |
|---------|---------|------|------|
| 重量(g) | sku_mapping.weight_g | ✅ | 三级获取逻辑 |
| 申报价值 | orders.total_amount | ✅ | 单位：USD |

### 物流渠道

| 表单字段 | 数据来源 | 必填 | 说明 |
|---------|---------|------|------|
| 渠道代码 | 固定 'PX' | ✅ | 联邮通优先挂号-普货，通用渠道 |

---

## 重量三级获取逻辑

```
优先级（从高到低）：
1. 前端表单输入值（操作员手动修改）
2. sku_mapping.weight_g（数据库配置）
3. 30g（兜底默认值）
```

### 实际SKU重量参考

| SKU形状 | 大号(L) | 小号(S) |
|--------|--------|--------|
| 骨头形 Bone | 33g | 20g |
| 心形 Heart | 27g | 20g |
| 圆形 Round | 30g | 20g |

---

## 电话隐私号码生成规则

4PX接口要求收件人电话必填，但为保护客户隐私，系统自动生成虚拟号码。

### 格式规则

```
+1 + 3位美国区号 + 7位随机数
```

### 区号池

```javascript
const areaCodes = ['202', '213', '312', '415', '510', '617', '718', '786', '917', '323']
```

### 代码示例

```javascript
function generateFakePhone() {
  const areaCodes = ['202', '213', '312', '415', '510', '617', '718', '786', '917', '323']
  const areaCode = areaCodes[Math.floor(Math.random() * areaCodes.length)]
  const randomDigits = Math.floor(Math.random() * 9000000 + 1000000)
  return `+1${areaCode}${randomDigits}`
}
```

> ⚠️ 注意：这是通用格式（非仅美国订单），因4PX接口强制要求电话字段

---

## Supabase 查询要点

### 外键关联查询

```javascript
// ✅ 正确写法：显式指定外键名称
const { data } = await supabase
  .from('orders')
  .select('*, sku_mapping!orders_sku_id_fkey(*)')
  .eq('status', 'confirmed')
```

> ⚠️ orders表有两个FK指向sku_mapping：`sku_id` 和 `matched_sku_id`，必须显式指定

### 筛选条件

| 条件 | 说明 |
|------|------|
| `status = 'confirmed'` | 仅已确认订单可下单 |
| 无logistics记录 | 排除已下单订单 |

---

## 渠道说明

### 当前默认渠道

| 代码 | 名称 | 适用范围 | 时效 |
|------|------|---------|------|
| PX | 联邮通优先挂号-普货 | 所有国家 | 7-15天 |

### 后续规划

```
国家选择 → 展开可用渠道列表 → 选择最优渠道
```

---

## 关键代码位置

### 前端

| 功能 | 文件路径 | 函数/变量 |
|------|---------|----------|
| 自动填充逻辑 | `D:\ETSY_Order_Automation\frontend\src\views\Admin\OrdersShipping.vue` | `selectOrder()` |
| 电话生成 | 同上 | `generateFakePhone()` |
| 渠道定义 | 同上 | `channels` ref |

### 后端

| 功能 | 文件路径 | 端点/函数 |
|------|---------|----------|
| 4PX下单API | `D:\ETSY_Order_Automation\backend\src\api\main.py` | `/api/shipping/create-order` |
| 重量fallback | 同上 | `weight_kg` 三级处理 |
| 收件人fallback | 同上 | `recipient_*` 字段 |

---

## 常见踩坑与解决方案

### 1. 忘记填充某些字段

**问题**：新增字段时忘记在 selectOrder() 中添加填充逻辑  
**解决**：每次新增表单字段，必须同步更新 selectOrder() 的映射

### 2. 外键查询报错

**问题**：`Could not find a relationship between 'orders' and 'sku_mapping'`  
**解决**：使用显式外键语法 `sku_mapping!orders_sku_id_fkey(*)`

### 3. 重量为空导致API报错

**问题**：sku_mapping.weight_g 为 null 时提交失败  
**解决**：前端和后端都要实现三级fallback，最终兜底30g

### 4. 电话格式不符合4PX要求

**问题**：电话格式不规范导致API拒绝  
**解决**：统一使用 `+1` + 区号 + 7位数字格式

### 5. 已下单订单重复显示

**问题**：已创建物流单的订单还在列表中  
**解决**：查询时排除有logistics记录的订单

---

## 开发检查清单

新增或修改物流下单功能时，逐项确认：

- [ ] 所有表单字段都有自动填充来源
- [ ] fallback逻辑完整（姓名、国家、重量）
- [ ] 电话号码自动生成
- [ ] Supabase查询使用显式外键
- [ ] 仅显示 status=confirmed 的订单
- [ ] 排除已有logistics记录的订单
- [ ] 重量三级获取逻辑正确
- [ ] 渠道代码正确（当前固定PX）

---

## 版本记录

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-03 | 初始版本，基于4PX物流下单实战提炼 |
