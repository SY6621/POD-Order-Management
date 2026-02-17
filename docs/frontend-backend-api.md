# 前后端对接文档

> 项目: ETSY 订单自动化管理系统  
> 日期: 2026-02-04  
> 版本: v1.0

---

## 一、数据库表结构概览

| 序号 | 表名 | 中文名称 | 前端关联 |
|------|------|---------|---------|
| 1 | fonts | 字体表 | 后端渲染 |
| 2 | templates | 模板表 | 后端渲染 |
| 3 | sku_mapping | SKU对照表 | 产品信息 |
| 4 | orders | 订单主表 | 核心数据 |
| 5 | logistics | 物流信息表 | 物流状态 |
| 6 | email_templates | 邮件模板表 | 邮件管理 |
| 7 | production_documents | 生产文档表 | 设计稿件 |
| 8 | product_photos | 产品实拍图库 | 产品展示 |
| 9 | email_logs | 邮件发送记录 | 邮件状态 |
| 10 | order_status_logs | 订单状态变更记录 | 处理详情 |
| 11 | carrier_settings | 物流公司配置 | 后端配置 |

---

## 二、核心表字段定义

### 2.1 orders（订单主表）

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| id | Integer | 是 | 自增 | 主键 |
| etsy_order_id | String(50) | 是 | - | Etsy订单号（唯一） |
| sku_id | Integer | 否 | NULL | 关联 sku_mapping.id |
| customer_name | String(100) | 否 | NULL | 客户名称 |
| customer_email | String(100) | 否 | NULL | 客户邮箱 |
| front_text | Text | 否 | NULL | 正面刻字 |
| back_text | Text | 否 | NULL | 背面刻字 |
| quantity | Integer | 否 | 1 | 数量 |
| total_amount | Decimal(10,2) | 否 | 0 | 订单金额 |
| status | String(20) | 否 | 'new' | 订单状态 |
| progress | Integer | 否 | 0 | 进度 (0-100) |
| priority | String(10) | 否 | 'normal' | 优先级 |
| estimated_delivery | DateTime | 否 | NULL | 预计交付日期 |
| production_started_at | DateTime | 否 | NULL | 生产开始时间 |
| completed_at | DateTime | 否 | NULL | 完成时间 |
| created_at | DateTime | 否 | NOW() | 创建时间 |
| updated_at | DateTime | 否 | NOW() | 更新时间（自动） |

**status 状态值：**
| 值 | 中文 | UI 对应 |
|----|------|---------|
| new | 新订单 | 待确认订单 |
| pending | 待确认 | 待确认订单 |
| confirmed | 已确认 | 生产中订单 |
| producing | 生产中 | 生产中订单 |
| completed | 已完成 | 已完成订单 |
| shipped | 已发货 | 已完成订单 |
| delivered | 已送达 | 已完成订单 |
| cancelled | 已取消 | - |

**priority 优先级值：**
| 值 | 中文 |
|----|------|
| normal | 普通 |
| high | 高优先级 |
| urgent | 紧急 |

---

### 2.2 logistics（物流信息表）

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| id | Integer | 是 | 自增 | 主键 |
| order_id | Integer | 是 | - | 关联 orders.id |
| recipient_name | String(100) | 否 | NULL | 收件人姓名 |
| country | String(50) | 否 | NULL | 国家 |
| city | String(50) | 否 | NULL | 城市 |
| street_address | Text | 否 | NULL | 街道地址 |
| postal_code | String(20) | 否 | NULL | 邮编 |
| tracking_number | String(100) | 否 | NULL | 物流单号 |
| label_url | String(500) | 否 | NULL | 面单链接 |
| delivery_status | String(20) | 否 | 'pending' | 物流状态 |
| shipped_at | DateTime | 否 | NULL | 发货日期 |
| delivered_at | DateTime | 否 | NULL | 收货日期 |
| pickup_date | DateTime | 否 | NULL | 取货日期 |

**delivery_status 状态值：**
| 值 | 中文 | UI 对应 |
|----|------|---------|
| pending | 待发货 | - |
| shipped | 已发货 | 物流送达 |
| in_transit | 运输中 | 物流送达 |
| delivered | 已送达 | 物流送达 |
| failed | 配送失败 | - |

---

### 2.3 production_documents（生产文档表）

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| id | Integer | 是 | 自增 | 主键 |
| order_id | Integer | 是 | - | 关联 orders.id |
| effect_jpg_url | String(500) | 否 | NULL | 效果图 JPG 链接 |
| effect_svg_url | String(500) | 否 | NULL | 效果图 SVG 链接 |
| production_pdf_url | String(500) | 否 | NULL | 生产 PDF 链接 |
| real_photo_urls | Text | 否 | NULL | 实拍图（JSON数组） |
| created_at | DateTime | 否 | NOW() | 创建时间 |

---

### 2.4 email_logs（邮件发送记录）

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| id | Integer | 是 | 自增 | 主键 |
| order_id | Integer | 是 | - | 关联 orders.id |
| email_type | String(30) | 否 | NULL | 邮件类型 |
| recipient_email | String(100) | 否 | NULL | 收件人邮箱 |
| subject | String(200) | 否 | NULL | 邮件主题 |
| status | String(20) | 否 | 'pending' | 发送状态 |
| sent_at | DateTime | 否 | NULL | 发送时间 |

**email_type 邮件类型：**
| 值 | 中文 | UI 对应 |
|----|------|---------|
| confirmation | 确认邮件 | 确认邮件按钮 |
| shipping | 发货通知 | - |
| logistics_delay | 物流延迟 | 物流耽误模板 |
| review_request | 追评请求 | 追评邮件按钮 |

---

### 2.5 sku_mapping（SKU对照表）

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| id | Integer | 是 | 自增 | 主键 |
| sku_code | String(50) | 是 | - | SKU编码（唯一） |
| material | String(50) | 否 | NULL | 材质 |
| shape | String(50) | 否 | NULL | 形状 |
| color | String(50) | 否 | NULL | 颜色 |
| size | String(50) | 否 | NULL | 尺寸 |
| craft | String(50) | 否 | NULL | 工艺 |

---

## 三、UI 与数据库字段映射

### 3.1 待确认订单表格

| UI 列名 | 数据来源 | 字段路径 |
|--------|---------|---------|
| 订单ID | orders | etsy_order_id |
| 客户名称 | orders | customer_name |
| 产品 | sku_mapping | sku_code |
| 设计稿件 | production_documents | effect_jpg_url |
| 确认邮件 | email_logs | email_type='confirmation' |
| 数量 | orders | quantity |
| 状态 | orders | status |
| 创建日期 | orders | created_at |

### 3.2 生产中订单表格

| UI 列名 | 数据来源 | 字段路径 |
|--------|---------|---------|
| 客户名称 | orders | customer_name |
| 产品 | sku_mapping | sku_code |
| 生产表单 | production_documents | production_pdf_url |
| 进度 | orders | progress |
| 数量 | orders | quantity |
| 状态 | orders | status |
| 物流面单 | logistics | label_url |
| 下单取货 | logistics | pickup_date |
| 创建日期 | orders | created_at |

### 3.3 已完成订单表格

| UI 列名 | 数据来源 | 字段路径 |
|--------|---------|---------|
| 订单ID | orders | etsy_order_id |
| 客户名称 | orders | customer_name |
| 产品 | sku_mapping | sku_code |
| 国家地址 | logistics | country + city |
| 发货日期 | logistics | shipped_at |
| 收货日期 | logistics | delivered_at |
| 物流送达 | logistics | delivery_status |
| 追评邮件 | email_logs | email_type='review_request' |

---

## 四、前端 API 调用示例

### 4.1 获取待确认订单

```javascript
const { data } = await supabase
  .from('orders')
  .select(`
    *,
    sku_mapping (*),
    production_documents (*),
    email_logs (*)
  `)
  .in('status', ['new', 'pending'])
  .order('created_at', { ascending: false })
```

### 4.2 获取生产中订单

```javascript
const { data } = await supabase
  .from('orders')
  .select(`
    *,
    sku_mapping (*),
    logistics (*),
    production_documents (*)
  `)
  .in('status', ['confirmed', 'producing'])
  .order('priority', { ascending: false })
```

### 4.3 获取已完成订单（30天内）

```javascript
const thirtyDaysAgo = new Date()
thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)

const { data } = await supabase
  .from('orders')
  .select(`
    *,
    sku_mapping (*),
    logistics (*),
    email_logs (*)
  `)
  .in('status', ['completed', 'shipped', 'delivered'])
  .gte('completed_at', thirtyDaysAgo.toISOString())
```

### 4.4 更新订单状态

```javascript
await supabase
  .from('orders')
  .update({ 
    status: 'producing',
    production_started_at: new Date().toISOString()
  })
  .eq('id', orderId)
```

### 4.5 更新订单进度

```javascript
await supabase
  .from('orders')
  .update({ progress: 60 })
  .eq('id', orderId)
```

---

## 五、文件清单

| 文件路径 | 说明 |
|---------|------|
| backend/scripts/supabase_schema_update.sql | 数据库表结构更新 SQL |
| backend/src/models/order.py | 后端数据模型 |
| frontend/src/stores/orderStore.js | 前端状态管理 |
| frontend/src/utils/supabase.js | Supabase 客户端 |
| frontend/src/pages/production-dashboard-final.html | UI 设计稿 |

---

## 六、执行步骤

1. **在 Supabase 控制台执行 SQL 脚本**
   ```
   backend/scripts/supabase_schema_update.sql
   ```

2. **验证表结构更新**
   - 检查 orders 表新增 10 个字段
   - 检查 logistics 表字段重命名和新增
   - 检查 production_documents 表新增外键
   - 检查 email_logs 表新增字段

3. **启动前端开发服务器**
   ```bash
   cd frontend
   npm run dev
   ```

4. **测试数据加载**
   - 打开浏览器控制台
   - 检查 Supabase 查询是否成功

---

## 七、注意事项

1. **字段命名统一使用 snake_case**
2. **时间字段统一使用 TIMESTAMP WITH TIME ZONE**
3. **外键关联必须指向有效的主键**
4. **状态值必须在约束范围内**
5. **进度值范围 0-100**
