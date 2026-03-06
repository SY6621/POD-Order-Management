---
name: etsy-html-prototype
description: ETSY订单管理系统前端静态HTML原型开发规范与迭代流程
---

# etsy-html-prototype

基于 ETSY 订单自动化系统实战提炼的前端静态 HTML 原型开发规范。
适用于：创建新页面原型、迭代修改现有页面、将静态 HTML 迁移为 Vue 组件前的视觉确认阶段。

---

## 项目 UI 原型规范

### 标准容器尺寸

```html
<!-- body 背景 -->
<body class="bg-slate-200 min-h-screen flex items-center justify-center p-8">

<!-- 主容器（固定不变） -->
<div class="flex h-[900px] w-[1480px] bg-white shadow-2xl rounded-2xl overflow-hidden shrink-0">
```

> ⚠️ 宽度固定 1480px、高度固定 900px，禁止使用 max-width 或响应式布局。

### 字体引入

```html
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    body { font-family: 'Inter', sans-serif; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>
```

### 左侧导航栏（固定 6 项，顺序不变）

```html
<!-- 导航容器 -->
<div class="w-64 bg-white border-r border-slate-200 flex flex-col h-full overflow-y-auto shrink-0">

<!-- 标题 -->
<div class="p-6">
    <h1 class="text-xl font-bold text-slate-800 flex items-center gap-2">
        <span class="w-2 h-6 bg-blue-600 rounded-full"></span>
        仪表盘总览
    </h1>
</div>
```

6 个导航项顺序固定：
1. 仪表盘总览
2. 待确认订单（badge: 数量）
3. 生产中订单（badge: 数量）
4. 已完成订单（badge: 数量）
5. 物流追踪（badge: 数量）
6. 邮件模板

### 导航项激活样式规则

| 页面 | 激活背景 | 激活文字 | 图标颜色 | badge 颜色 |
|------|---------|---------|---------|-----------|
| 仪表盘/待确认/生产中/物流/邮件 | `bg-blue-50` | `text-blue-600` | `#2563eb` | `bg-blue-200 text-blue-700` |
| 已完成订单 | `bg-green-50` | `text-green-700` | `#15803d` | `bg-green-200 text-green-700` |

非激活项：`text-slate-600 hover:bg-slate-50`，图标颜色 `#64748b`

### 统计卡片（左侧 2×2 圆形仪表）

```html
<div class="relative w-20 h-20 flex items-center justify-center mb-1">
    <svg width="80" height="80" viewBox="0 0 80 80" class="absolute transform -rotate-90">
        <circle cx="40" cy="40" r="28" stroke="#e2e8f0" stroke-width="5" fill="transparent" />
        <circle cx="40" cy="40" r="28" stroke="#3b82f6" stroke-width="5" fill="transparent"
            stroke-dasharray="175.93" stroke-dashoffset="43.98" stroke-linecap="round" />
    </svg>
    <span class="text-lg font-bold z-10 text-blue-600">128</span>
</div>
```

> `stroke-dashoffset` 计算：圆周 = 2π×28 ≈ 175.93，offset = 175.93 × (1 - 填充百分比)

---

## 文字大小规范（已提炼）

| 层级 | 用途 | 推荐 class |
|------|------|-----------|
| 页面主标题 | 右侧内容区大标题 | `text-2xl font-bold text-slate-800` |
| 卡片标题 | 订单号、详情标题 | `text-base font-bold` |
| 表格内容 | 订单列表 | `text-xs` |
| 辅助文字/时间 | 时间、描述 | `text-[11px] text-slate-400` |
| 超小标注 | badge 内文字、标签 | `text-[10px]` |
| 状态 badge | 订单状态标签 | `px-1.5 py-0.5 rounded text-[10px] font-bold` |

---

## 颜色语义规则

| 含义 | 背景 | 文字 |
|------|------|------|
| 正常/蓝色系 | `bg-blue-100` | `text-blue-600` |
| 成功/完成 | `bg-green-100` | `text-green-700` |
| 警告/逾期/须跟进 | `bg-orange-100` | `text-orange-600` |
| 异常/红色强调 | 保留原色 | `text-orange-600`（非纯红） |
| 中性信息 | `bg-slate-100` | `text-slate-600` |
| 生产中 | `bg-blue-100` | `text-blue-600` |
| 追评/次要紫色 | `bg-indigo-100` | `text-indigo-700` |

> ⚠️ 规范：日期数字等数据文字统一用灰色（`text-slate-500`），异常仅在"已逾期"等关键词上保留橙色。

---

## 页面开发 SOP（标准操作流程）

### Step 1：明确页面信息架构

在动手前先确认：
- 这个页面的**主要职责**是什么？
- 需要展示哪些**核心数据/操作**？
- 是否有三列布局（列表 + 详情 + 操作）？

### Step 2：read_file 参考现有页面

**必须先读取** 1～2 个现有页面，提取导航、卡片、按钮等可复用片段：

```
推荐参考页面优先级：
1. 02_待确认订单.html（视觉基准页）
2. 03_生产中订单.html（表格 + 详情 + 操作按钮）
3. 04_已完成订单.html（绿色激活、追评卡片）
4. 05_物流追踪.html（时间轴布局）
5. 06_邮件模板.html（Tab + 三列 + JS 数据驱动）
```

> ❌ 禁止不参考直接凭记忆生成，会导致样式不一致。

### Step 3：create_file 生成完整 HTML

- 文件输出至：`D:\ETSY_Order_Automation\backend\tests\`
- 命名规则：`序号_页面名称.html`（如 `03_生产中订单.html`）
- 文件名序号与导航顺序对应：`01～06`

### Step 4：search_replace 增量修改

**修改原则**：
- 每次只修改原文件，不重写整个文件
- 使用 `search_replace` 精确定位唯一片段
- 一次改一处，验证后再改下一处

### Step 5：用户验证循环

```
用户打开 HTML → 提出修改意见 → AI 在原文件 search_replace → 再次验证
```

直到用户满意后，才进入下一阶段（Vue 组件化）。

---

## 6 个标准页面文件清单

| 序号 | 文件名 | 对应 Vue 视图 | 激活颜色 |
|------|-------|-------------|---------|
| 01 | `01_仪表盘总览.html` | Dashboard.vue | 蓝色 |
| 02 | `02_待确认订单.html` | PendingOrders.vue | 蓝色 |
| 03 | `03_生产中订单.html` | Production.vue | 蓝色 |
| 04 | `04_已完成订单.html` | CompletedOrders.vue | 绿色 |
| 05 | `05_物流追踪.html` | Logistics.vue | 蓝色 |
| 06 | `06_邮件模板.html` | EmailTemplates.vue | 蓝色 |

所有文件位于：`D:\ETSY_Order_Automation\backend\tests\`

---

## 常见踩坑与解决方案

### 1. 文字颜色不统一

**问题**：数据型文字（日期、金额、数量）误用橙色/红色  
**解决**：数据统一用 `text-slate-500`，仅状态关键词（"已逾期"、"须跟进"）保留警告色

### 2. 进度百分比文字与进度条颜色不一致

**问题**：进度条是橙色但百分比文字也是橙色，视觉杂乱  
**解决**：百分比文字改为 `text-slate-500`，进度条本身保留橙色

### 3. 页面右侧面板文字偏大、不够紧凑

**问题**：详情面板用 `text-xl`、`text-sm`，与表格区域不协调  
**解决**：详情标题用 `text-base`，正文用 `text-xs`，辅助信息用 `text-[11px]`

### 4. 时间轴图标圆圈过大

**问题**：时间轴节点用 `w-10 h-10`，图标用 `width="18"`  
**解决**：改为 `w-8 h-8`，图标 `width="14"`，padding 由 `p-6` → `p-4`

### 5. create_file 超过 1000 行限制

**问题**：复杂页面 HTML 超过工具行数限制  
**解决**：先用 create_file 生成基础结构（导航 + 主体框架），再用 search_replace 补充详细内容

### 6. JS 数据驱动页面的 onclick 引号冲突

**问题**：模板字符串中的 onclick 含双引号导致 HTML 属性解析错误  
**解决**：onclick 内部一律用单引号，如 `onclick="selectTemplate(${i})"`

---

## Vue 组件化迁移检查清单

静态 HTML 确认满意后，迁移为 Vue 组件时需要逐项核对：

- [ ] Tailwind 类名是否完整保留（特别是动态绑定部分）
- [ ] 左侧导航高亮状态改为 Vue Router `$route.name` 判断
- [ ] 统计数字改为 Pinia Store 真实数据（`orderStore.stats`）
- [ ] 表格数据改为 `v-for` 循环渲染
- [ ] 按钮 onclick 改为 Vue `@click` 事件方法
- [ ] 邮件模板页 JS 数据（`SECTIONS` 数组）可保留在组件 `data()` 中，不必连接 Supabase
- [ ] 滚动条样式写入全局 `style.css`，避免每个组件重复

---

## 版本记录

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-03 | 初始版本，基于 6 个页面原型实战提炼 |
