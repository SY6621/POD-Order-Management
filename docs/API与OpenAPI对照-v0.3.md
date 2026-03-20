# API（OpenAPI）与业务 / 前端文档对照 v0.3

> **规范文件**：`docs/openapi.yaml`  
> **状态定稿**：`docs/开发文档-页面状态按钮-v1.0.md`（`orders.status` 全量、`confirmed`=待下物流）  
> **v0.3 变更**：根据现网 `orders` 表与前端查询逻辑，**已定稿** §3；关闭 v0.2「待确认」项。

---

## 1. 已覆盖的能力（与模块对应）

（同 v0.2，略 —— 见 `openapi.yaml` 路径清单。）

---

## 2. 与《开发文档》双快照规则的对照

（同 v0.2 §2；**客户确认**在数据层对应过渡到 `orders.status = 'confirmed'`，见 v1.0 页面文档 §2–3。）

---

## 3. 订单状态：`orders.status`（已定稿）与 OpenAPI 的差异

### 3.1 数据库 / 后端全量（主流程）

| `orders.status` | 含义 |
|-----------------|------|
| `new` | 新订单 |
| `pending` | 待确认 |
| `effect_sent` | 效果图已发送 |
| `confirmed` | 已确认 = **待下物流** |
| `producing` | 生产中（已下物流后，结合 `logistics.tracking_number` 判断） |
| `shipped` | 已发货 |
| `delivered` | 已送达 |
| `cancelled` | 已取消 |
| `completed` | 已完成 |

### 3.2 OpenAPI `OrderStatusRequest.status` 当前枚举

`pending` | `effect_sent` | `producing` | `delivered`

### 3.3 差异与建议

| 差距 | 说明 |
|------|------|
| **缺少** `new`、`confirmed`、`shipped`、`cancelled`、`completed` | 更新 OpenAPI 枚举与现网一致，或文档中注明「仅部分状态可通过该接口切换」 |
| **`confirmed` 为核心** | 物流页列表使用 `confirmed`；**必须在 API 文档中显式列出**，避免对接歧义 |
| **`delivered` 与 DB 一致** | ✓ |
| **`pending` 语义** | DB 为「待确认」；与 OpenAPI 描述一致时需区分勿与 `new` 混淆 |

**建议**：下一轮 `openapi.yaml` 升级将 `OrderStatusRequest.status` **扩展为与 §3.1 一致**，或拆分为「允许迁移的状态子集」并在文档中列状态机图。

---

## 4. 物流下单页 UI 与 `ShippingCreateOrderRequest` 字段对照

（同 v0.2 §4 —— 长宽高、中英品名、带电等仍以接口补全为准。）

---

## 5. OpenAPI 中未出现、但管理端通常需要的接口（缺口）

（同 v0.2 §5 —— 列表/详情仍以 Supabase 直连或自建 API 为准。）

---

## 6. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v0.2 | 2025-03-20 | OpenAPI 初稿对照 |
| v0.3 | 2025-03-20 | **已定稿** `orders.status` 与「待下物流」=`confirmed`；OpenAPI 枚举差异说明 |

---

**v0.2 已废止**：请以 **v0.3** 为准；旧文件可删除或保留归档。
