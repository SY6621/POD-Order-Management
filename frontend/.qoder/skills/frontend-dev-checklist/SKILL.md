---
name: frontend-dev-checklist
description: 前端代码修改后的强制验证闭环规范。每次修改前端Vue组件后必须执行此检查清单，确保改动真正生效。适用于修改OrdersPending.vue、任何Vue页面组件、Tailwind样式、前端逻辑时自动触发。
---

# 前端开发验证闭环规范

## 修改前：检查数据源陷阱

以下已知问题会导致"代码改了但页面没变"，修改前必须确认：

| 陷阱 | 说明 | 解决方式 |
|------|------|---------|
| API旧数据覆盖本地 | `email_templates` 表存有旧的错误模板，API数据会优先于本地硬编码 | 首封邮件区域直接用 `defaultFirstEmailTemplates`，不走API |
| Vite未运行 | 修改了源文件但dev server没启动，页面加载的是旧的dist编译文件 | 必须确认 `npm run dev` 在运行 |
| 浏览器缓存 | 旧的JS/CSS被缓存 | Ctrl+Shift+Delete 清缓存，或用无痕模式 |
| 编译时序 | `npm run build` 在代码修改之前执行 | 修改后重新 build 或使用 dev server |

## 修改后：强制验证流程（不可跳过）

```
步骤1 → 确认dev server运行中
         cd d:\ETSY_Order_Automation\frontend; npm run dev

步骤2 → 浏览器打开页面，实际操作验证每一个改动点
         不接受"代码看起来对"的说法，必须在页面上看到效果

步骤3 → 如果页面未变化，按以下顺序排查：
         ① dev server是否在运行？终端是否显示编译成功？
         ② 文件是否已保存？（检查文件修改时间）
         ③ 是否有API/数据库旧数据覆盖了本地修改？
         ④ 浏览器是否有缓存？尝试强制刷新（Ctrl+F5）
         ⑤ 是否修改了正确的文件？（检查文件路径）

步骤4 → 验证通过后，提交Git：
         cd d:\ETSY_Order_Automation
         git add -A; git commit -m "描述本次改动"
```

## 验证标准

- 必须在浏览器中实际看到改动效果
- 如有UI改动，描述页面实际显示内容作为证据
- 控制台（F12）无红色报错
- 涉及多个功能点时，逐项验证并逐项报告

## 已知数据源规则

| 功能区域 | 数据源 | 说明 |
|---------|--------|------|
| 首封邮件模板 | 本地硬编码 `defaultFirstEmailTemplates` | 不走API，数据库旧模板已弃用 |
| 邮件撰写Tab模板 | `email_templates` API | 正常走API |
| 订单数据 | Supabase `orders` 表 | 正常走API |
| 效果图 | Supabase Storage | 正常走API |

## 效果图设计器保护

OrdersPending.vue 中的效果图设计器区域（iframe嵌入）已完成开发且用户满意。
任何任务如果涉及 OrdersPending.vue 的修改，**禁止改动设计器相关代码**。

## 布局比例规则

OrdersPending.vue 左右分栏比例为 **65:35**（左65%右35%）。
- 左侧 `w-[65%]`：订单列表 + 效果图设计器
- 右侧 `w-[35%]`：订单详情 + 首封邮件 + 模板编辑
修改时不得随意调整此比例。
