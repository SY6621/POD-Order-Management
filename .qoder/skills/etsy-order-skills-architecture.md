# ETSY POD 订单管理系统 - Skills 架构文档

## 文档说明

本文档定义了 ETSY 订单管理系统的 Skills 体系架构，基于项目当前进度和业务需求，将系统功能拆分为 11 个可独立验证的 Skills。

---

## Skills 层级结构

### Layer 1: 数据获取层（已实现 ✅）

#### Skill 1.1: IngestEtsyOrderEmail
**目的**：从 IMAP 读取 Etsy 订单邮件并产生邮件事件

**触发条件**：
- 定时轮询（每 30 分钟）
- 手动触发（前端按钮）

**输入**：
```json
{
  "imap_config_ref": "env.EMAIL_ADDRESS",
  "filter": {
    "sender": "transaction@etsy.com",
    "subject_contains": "Etsy order",
    "time_window": "24h"
  }
}
```

**输出**：
```json
{
  "email_events": [{
    "message_id": "string",
    "received_at": "ISO8601",
    "raw_content_ref": "storage_path",
    "thread_key": "order_id"
  }]
}
```

**副作用/权限**：
- IMAP 只读
- 写入日志
- 写入 DB（message_id 去重）

**实现位置**：
- `backend/src/services/email_service.py`
- 方法：`search_etsy_orders()`, `fetch_email_content()`

**状态**：✅ 已实现

**测试要求**：
- 正例：符合规则的邮件应产出 1 个事件
- 反例：重复运行不应产出重复事件
- 边界：无新邮件时应返回空列表

---

#### Skill 1.2: ParseOrderFromEmail
**目的**：解析邮件文本为标准订单模型

**触发条件**：
- 收到 `email_event`

**输入**：
```json
{
  "email_event": {
    "message_id": "string",
    "raw_content": "string"
  },
  "parse_strategy": "etsy_transaction_email_v1"
}
```

**输出**：
```json
{
  "order_draft": {
    "etsy_order_id": "string",
    "customer_name": "string",
    "customer_username": "string",
    "shipping_address": "object",
    "items": [{
      "product_name": "string",
      "customization_front": "string",
      "customization_back": "string",
      "font_code": "string",
      "quantity": "number",
      "price": "number"
    }],
    "total": "number",
    "currency": "string",
    "completeness_score": 0.95,
    "missing_fields": [],
    "confidence": 0.98
  }
}
```

**实现位置**：
- `backend/src/services/email_parser.py`
- 类：`EtsyEmailParser`

**状态**：✅ 已实现

**测试要求**：
- 正例：标准邮件应完整解析所有字段
- 反例：格式错误邮件应输出缺失字段清单
- 边界：部分缺失字段时应给出 completeness_score

---

### Layer 2: 数据持久化层（已实现 ✅）

#### Skill 2.1: UpsertOrderToSupabase
**目的**：将订单写入 Supabase，保证幂等性

**触发条件**：
- 收到 `order_draft`

**输入**：
```json
{
  "order_draft": "object",
  "idempotency_key": "etsy_order_id",
  "initial_status": "pending"
}
```

**输出**：
```json
{
  "order_record": {
    "id": "number",
    "etsy_order_id": "string",
    "status": "pending",
    "created_at": "ISO8601",
    "correlation_id": "uuid"
  }
}
```

**副作用/权限**：
- Supabase 读写
- 写入审计日志
- 初始化状态机

**状态机起始状态**：
```
pending → (awaiting_mockup)
```

**实现位置**：
- `backend/src/services/order_service.py`
- `backend/src/services/database_service.py`

**状态**：✅ 已实现

**测试要求**：
- 正例：同一 etsy_order_id 重复 upsert 不应产生重复记录
- 反例：非法状态迁移应失败
- 边界：并发写入应保证幂等性

---

### Layer 3: 工件生成层（已实现 ✅）

#### Skill 3.1: GenerateEffectImage
**目的**：根据订单信息生成效果图（支持版本管理）

**触发条件**：
- 订单状态 = `pending`
- 手动触发

**输入**：
```json
{
  "order_record": {
    "id": "number",
    "customization_front": "string",
    "customization_back": "string",
    "font_code": "string",
    "shape": "string",
    "color": "string",
    "size": "string"
  },
  "output_spec": {
    "formats": ["svg", "jpg"],
    "svg_size": "800x600",
    "jpg_quality": 85
  },
  "revision": 1
}
```

**输出**：
```json
{
  "artifacts": [{
    "artifact_id": "uuid",
    "type": "effect_image",
    "format": "svg",
    "revision": 1,
    "file_path": "string",
    "checksum": "sha256",
    "created_at": "ISO8601"
  }]
}
```

**副作用/权限**：
- 文件系统写入
- DB 写入（artifact 索引）
- 日志记录

**实现位置**：
- `backend/src/services/effect_image_service.py`
- 方法：`generate_effect_svg()`

**状态**：✅ 已实现

**测试要求**：
- 正例：给定固定输入能生成工件
- 反例：缺素材/字体失败能产出可定位错误
- 边界：特殊字符应正确转义

---

#### Skill 3.2: GenerateProductionPDF
**目的**：生成生产文档 PDF

**触发条件**：
- 订单状态 = `approved`

**输入**：
```json
{
  "order_record": "object",
  "template": "production_doc_template_v1"
}
```

**输出**：
```json
{
  "artifact": {
    "artifact_id": "uuid",
    "type": "production_pdf",
    "file_path": "string",
    "checksum": "sha256"
  }
}
```

**实现位置**：
- `backend/src/services/svg_pdf_service.py`

**状态**：✅ 已实现

---

### Layer 4: 客户交互层（待开发 ⏳）

#### Skill 4.1: SendEffectImageToCustomer
**目的**：发送效果图确认邮件给客户

**触发条件**：
- 效果图生成完成
- 订单状态 = `pending` → `awaiting_approval`

**输入**：
```json
{
  "order_id": "number",
  "customer_email": "string",
  "effect_image_urls": ["url"],
  "email_template_id": "effect_confirmation_v1",
  "language": "en"
}
```

**输出**：
```json
{
  "email_log": {
    "id": "number",
    "order_id": "number",
    "sent_at": "ISO8601",
    "status": "sent",
    "thread_id": "string"
  }
}
```

**副作用/权限**：
- SMTP 发送邮件
- 写入 email_logs 表
- 更新订单状态

**状态机迁移**：
```
pending → awaiting_approval
```

**实现位置**：
- ⏳ 待开发：`backend/src/services/email_template_service.py`

**测试要求**：
- 正例：邮件发送成功应记录到 email_logs
- 反例：SMTP 失败应重试并记录错误
- 边界：重复发送应基于 thread_id 去重

---

#### Skill 4.2: MonitorCustomerApproval
**目的**：监控客户回复并更新订单状态

**触发条件**：
- 定时轮询（每 2 小时）
- 订单状态 = `awaiting_approval`

**输入**：
```json
{
  "order_id": "number",
  "thread_id": "string",
  "timeout": "48h"
}
```

**处理逻辑**：
1. 检查邮箱是否有回复（基于 thread_id）
2. 解析回复类型：
   - 同意关键词：`approve`, `ok`, `looks good`
   - 修改关键词：`change`, `modify`, `different`
   - 疑问关键词：`question`, `how`, `when`
3. 更新订单状态

**输出**：
```json
{
  "approval_state": "approved | needs_revision | awaiting_response",
  "customer_reply": {
    "received_at": "ISO8601",
    "content": "string",
    "classification": "approval | revision | question"
  }
}
```

**状态机迁移**：
```
awaiting_approval → approved (客户同意)
awaiting_approval → needs_revision (客户要求修改)
awaiting_approval → awaiting_response (超时无回复，需人工介入)
```

**实现位置**：
- ⏳ 待开发：`backend/src/services/approval_service.py`

**测试要求**：
- 正例：同意回复应推进到 approved
- 正例：修改请求应进入 needs_revision
- 反例：重复回复不应导致状态混乱
- 边界：48h 超时应触发人工任务

---

#### Skill 4.3: HandleRevisionRequest
**目的**：处理客户修改请求，生成新版本效果图

**触发条件**：
- 订单状态 = `needs_revision`

**输入**：
```json
{
  "order_id": "number",
  "revision_request": {
    "customer_reply": "string",
    "requested_changes": "string",
    "current_revision": 1
  }
}
```

**处理逻辑**：
1. 创建人工任务记录（需人工确认修改内容）
2. 人工完成后标记任务为 `resolved`
3. 调用 Skill 3.1 生成新版本效果图（revision + 1）
4. 调用 Skill 4.1 重新发送邮件
5. 更新订单状态回到 `awaiting_approval`

**输出**：
```json
{
  "manual_task": {
    "id": "number",
    "type": "revision_request",
    "assigned_to": "operator",
    "status": "pending | resolved",
    "created_at": "ISO8601"
  },
  "new_revision": 2
}
```

**状态机迁移**：
```
needs_revision → awaiting_manual_review
awaiting_manual_review → pending (人工确认后重新生成)
pending → awaiting_approval (新效果图发送)
```

**实现位置**：
- ⏳ 待开发：`backend/src/services/revision_service.py`

**测试要求**：
- 正例：修改请求应创建人工任务
- 正例：人工任务 resolved 后应触发新效果图生成
- 反例：未 resolved 的任务不应自动推进
- 边界：版本号应正确递增

---

### Layer 5: 物流履约层（待开发 ⏳）

#### Skill 5.1: GenerateShippingLabel
**目的**：生成物流标签并获取物流单号

**触发条件**：
- 订单状态 = `approved` → `production_ready`

**输入**：
```json
{
  "order_id": "number",
  "shipping_address": {
    "recipient_name": "string",
    "address_line1": "string",
    "city": "string",
    "state": "string",
    "postal_code": "string",
    "country": "string"
  },
  "shipping_params": {
    "carrier": "USPS | UPS | DHL",
    "service_level": "standard | express"
  }
}
```

**输出**：
```json
{
  "logistics_record": {
    "id": "number",
    "order_id": "number",
    "tracking_number": "string",
    "carrier": "string",
    "label_pdf_path": "string",
    "created_at": "ISO8601"
  }
}
```

**副作用/权限**：
- 调用物流 API
- 文件系统写入（PDF）
- 写入 logistics 表
- 更新订单状态

**状态机迁移**：
```
approved → production_ready
production_ready → shipped (物流标签生成完成)
```

**实现位置**：
- ⏳ 待开发：`backend/src/services/shipping_service.py`

**测试要求**：
- 正例：完整地址应成功生成标签
- 反例：缺地址字段应失败并返回缺失清单
- 边界：API 超时应重试并记录

---

#### Skill 5.2: TrackShippingStatus
**目的**：查询物流状态（发货后 8 天自动触发）

**触发条件**：
- 订单状态 = `shipped`
- 发货日期 + 8 天

**输入**：
```json
{
  "order_id": "number",
  "tracking_number": "string",
  "carrier": "string"
}
```

**输出**：
```json
{
  "shipping_status": {
    "status": "in_transit | delivered | delayed | lost",
    "last_update": "ISO8601",
    "location": "string",
    "estimated_delivery": "ISO8601"
  }
}
```

**异常处理**：
- 若状态为 `delayed` 或 `lost`：创建人工任务，通知客户

**实现位置**：
- ⏳ 待开发：`backend/src/services/tracking_service.py`

---

## Skills 依赖关系图

```
Layer 1 (数据获取)
    ↓
Layer 2 (持久化)
    ↓
Layer 3 (工件生成)
    ↓
Layer 4 (客户交互) ← 关键依赖：邮件模板、状态机
    ↓
Layer 5 (物流履约) ← 关键依赖：物流 API
```

---

## 开发优先级

### 阶段 14（当前）：订单管理页面
- 不需要新增 Skills
- 使用现有 Layer 1-3 的 Skills

### 阶段 15-17：核心功能
- **优先级 1**：Skill 4.1 (发送效果图)
- **优先级 2**：Skill 4.2 (监控审批)
- **优先级 3**：Skill 4.3 (处理修改)

### 阶段 18-19：状态流转与物流
- **优先级 4**：Skill 5.1 (物流标签)
- **优先级 5**：Skill 5.2 (物流追踪)

---

## 状态机完整定义

```
pending 
  → awaiting_mockup (效果图生成中)
  → awaiting_approval (已发送效果图，等待客户确认)
  → [分支1] approved (客户同意) → production_ready
  → [分支2] needs_revision (客户要求修改) → awaiting_manual_review
  → [分支3] awaiting_response (超时无回复) → manual_task_created

awaiting_manual_review 
  → pending (人工确认后重新生成)

production_ready 
  → shipped (物流标签生成完成)

shipped 
  → delivered (物流完成)
  → [异常] delayed / lost → manual_task_created
```

---

## 测试策略

### 单元测试
每个 Skill 必须至少包含：
- 1 个正例
- 1 个反例
- 1 个边界用例

### 集成测试
测试完整流程：
- 邮件 → 解析 → 入库 → 生成效果图 → 发送 → 审批 → 生产

### 回归测试
建立 test fixtures：
- 标准邮件样本
- 修改请求样本
- 异常邮件样本

---

## 附录：数据库表映射

| Skill | 数据库表 |
|-------|----------|
| 1.1, 1.2 | email_logs |
| 2.1 | orders, order_items |
| 3.1, 3.2 | （文件系统） |
| 4.1 | email_logs, email_templates |
| 4.2, 4.3 | order_status_logs |
| 5.1, 5.2 | logistics |
