---
name: orders-pending
description: 待确认订单模块开发与测试规范。包含新订单 Tab（设计器 + 效果图）、邮件撰写 Tab（中英文对照）、待创建 Tab（预览 + 复制）三个子页面的功能规范、状态流转逻辑和测试检查清单。当开发或调试待确认订单功能时使用。
---

# 待确认订单模块开发与测试规范（OrdersPending.vue）

## 模块概述

待确认订单模块是订单工作流的核心入口，处理从新订单到物流下单的完整流程。

**文件路径**：`D:\ETSY_Order_Automation\frontend\src\views\Admin\OrdersPending.vue`

**路由地址**：`/admin/orders/pending`

## 订单状态流转

```
pending（新订单）
    ↓ 生成效果图（edGetSVGData）
    ↓ 上传到Supabase Storage
pending + effect_image_url（邮件撰写）
    ↓ 生成邮件（generateEmail）
    ↓ 点击「邮件确认」按钮
pending + email_sent=true（待创建）
    ↓ 点击「物流下单」按钮
    ↓ 跳转 /admin/orders/shipping
confirmed（物流下单页面处理）
```

## 三个Tab页规范

### Tab 1：新订单

**筛选条件**：`status === 'pending' && !effect_image_url`

**左侧区域**：
- 订单列表（点击选中）
**右侧区域**：
- 订单详情（实拍图、SKU信息、正背面文字）

**核心功能**：
1. 选中订单后，设计器自动加载订单数据（postMessage通信）
2. 点击设计器内「发送效果图」按钮
3. 调用 `window.edGetSVGData()` 获取矢量SVG（opentype.js文字转路径）
4. 上传到Supabase Storage，更新订单 `effect_image_url`
5. 自动流转到「邮件撰写」Tab

**注意事项**：
- 后端服务必须运行（`localhost:8000`），否则字体加载失败
- SVG使用opentype.js将文字转为贝塞尔路径，无字体依赖
- iframe通信使用 `postMessage`，需确保字段名一致（`svgData`）

---

### Tab 2：邮件撰写

**筛选条件**：`status === 'pending' && effect_image_url && !email_sent`

**左侧区域**：
- 订单列表
- 邮件撰写表单（中英文对照）
  - 类型选择：首封确认 / 修改确认 / 追评邮件
  - 模板选择：标准确认 / 加急确认 / 定制需求确认
  - 风格设置：语气 / 长度 / 称呼 / 落款
- 操作按钮：生成邮件 / 复制 / 邮件确认

**右侧区域**：
- 订单详情
- 效果图预览（4:3宽高比）

**核心功能**：
1. 点击「生成邮件」：根据模板和风格生成中英文邮件
2. 邮件内容包含效果图URL链接
3. 点击「邮件确认」：
   - 保存邮件到 `email_logs` 表
   - 更新订单 `email_sent = true`
   - 自动流转到「待创建」Tab

**注意事项**：
- 邮件内容格式：`=== 中文版本 Chinese Version ===\n...\n=== English Version ===\n...`
- `getEnglishEmailContent()` 函数提取英文部分用于预览
- 邮件设置可保存到 localStorage

---

### Tab 3：待创建

**筛选条件**：`status === 'pending' && effect_image_url && email_sent`

**左侧区域**：
- 订单列表
- 效果图+邮件预览（左右并排，4:3宽高比）
  - 左侧：效果图（SVG）
  - 右侧：英文邮件预览

**右侧区域**：
- 订单详情
- 效果图预览
- 发送给客户面板
  - 复制链接 / 复制邮件
  - 物流下单按钮

**核心功能**：
1. 显示已确认的效果图和邮件内容
2. 点击「复制链接」：复制效果图分享URL
3. 点击「复制邮件」：复制英文邮件内容到剪贴板
4. 点击「物流下单」：跳转到 `/admin/orders/shipping?orderId=xxx`

**注意事项**：
- 邮件内容从 `email_logs` 表加载（selectOrder时触发）
- 流转后 `pendingEmailContent` 应有值（submitEmail函数设置）

---

## 关键函数说明

| 函数名 | 作用 | 所在Tab |
|--------|------|---------|
| `selectOrder(order)` | 选中订单，加载详情和邮件内容 | 所有 |
| `onDesignerLoad()` | 设计器加载完成回调 | 新订单 |
| `generateEmail()` | 生成中英文邮件内容 | 邮件撰写 |
| `submitEmail()` | 保存邮件并流转到待创建 | 邮件撰写 |
| `copyShareLink()` | 复制效果图分享链接 | 待创建 |
| `copyEmailContent()` | 复制邮件内容 | 待创建 |
| `goToShipping()` | 跳转到物流下单页面 | 待创建 |
| `getEnglishEmailContent(content)` | 提取邮件英文部分 | 待创建 |

---

## 测试检查清单

### 流程测试

```
测试进度：
- [ ] 1. 新订单Tab显示正确（无效果图的pending订单）
- [ ] 2. 选中订单后设计器加载数据
- [ ] 3. 点击「发送效果图」生成SVG并上传
- [ ] 4. 自动流转到邮件撰写Tab
- [ ] 5. 邮件撰写Tab显示效果图
- [ ] 6. 点击「生成邮件」生成中英文内容
- [ ] 7. 点击「邮件确认」保存并流转
- [ ] 8. 待创建Tab显示效果图+邮件预览
- [ ] 9. 复制链接/复制邮件功能正常
- [ ] 10. 点击「物流下单」跳转正确
```

### UI检查

```
UI检查项：
- [ ] 订单列表选中高亮
- [ ] Tab计数器数字正确
- [ ] 效果图宽高比4:3
- [ ] 右侧订单详情完整显示
- [ ] 按钮禁用状态正确
- [ ] 加载状态显示
```

### 数据检查

```
数据库检查：
- [ ] effect_image_url 正确写入
- [ ] email_sent 状态正确
- [ ] email_logs 表有记录
- [ ] Supabase Storage 文件存在
```

---

## 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 效果图字体错误 | 后端服务未运行 | 启动 `poetry run uvicorn` |
| SVG上传失败 | Supabase URL配置错误 | 检查 `.env` 中 `VITE_SUPABASE_URL` |
| 邮件预览空白 | `pendingEmailContent` 未赋值 | 检查 `submitEmail` 函数 |
| Tab计数不对 | 筛选条件错误 | 检查 `filteredOrders` computed |
| 设计器不加载数据 | postMessage字段名不匹配 | 确保使用 `svgData` 字段 |

---

## 相关文件

| 文件 | 说明 |
|------|------|
| `D:\ETSY_Order_Automation\frontend\src\views\Admin\OrdersPending.vue` | 主组件 |
| `D:\ETSY_Order_Automation\frontend\public\designer-standalone.html` | 设计器 |
| `D:\ETSY_Order_Automation\frontend\src\stores\orderStore.js` | 数据存储 |
| `D:\ETSY_Order_Automation\backend\src\services\effect_image_service.py` | 效果图服务 |
