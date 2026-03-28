---
name: ui-grid-design
description: |
  系统化前端 UI 美化技能，基于 Grid 布局结构规则。像前端工程师一样思考设计：统一 Design Token（字体、间距、配色）、CSS Grid/Flexbox 精确布局、色彩分层背景、组件化视觉系统。
  
  任何涉及网站、网页、落地页、管理后台、组件库、数据看板、卡片列表等前端 UI 构建或美化任务时，必须调用此 Skill，确保输出具备：统一字体层级、精致间距系统、色彩分层背景、Grid 结构化布局、专业级视觉质感。
  
  触发关键词：网页美化、UI设计、前端布局、做一个网站、landing page、dashboard、网格布局、配色方案、组件美化、设计系统、视觉优化。
---

# UI Grid Design Skill — 前端美化系统

> 像前端工程师 + 设计师一样思考。每个 UI 都应有清晰的 Design Token 体系、Grid 骨架、色彩分层。

---

## 第一步：设计决策（开始写代码前必做）

```
1. 定义【场景基调】：商业/科技/创意/简约/沉浸？
2. 选择【主色调】：冷色系/暖色系/中性/高对比？
3. 确定【布局密度】：信息密集（Dashboard）/ 呼吸感（Landing）/ 卡片式（Product）？
4. 决定【明暗模式】：Light / Dark / Auto？
```

---

## 核心规则：Design Token 先行

在 `:root` 中定义所有 Token，**禁止在组件中硬编码颜色/间距/字号**。

```css
:root {
  /* ── 色彩系统 ── */
  --color-bg-base:    #0d0f14;   /* 最深背景层 */
  --color-bg-surface: #161920;   /* 卡片/面板层 */
  --color-bg-elevated:#1e2230;   /* 悬浮/高亮层 */
  --color-bg-overlay: #252a3a;   /* 模态/工具提示层 */

  --color-primary:    #4f8ef7;   /* 主品牌色 */
  --color-primary-dim:#2d5bbb;   /* 主色暗版（按钮 hover）*/
  --color-accent:     #7c3aed;   /* 强调色 */
  --color-success:    #22c55e;
  --color-warning:    #f59e0b;
  --color-danger:     #ef4444;

  --color-text-primary:   #f0f2f8;  /* 主文本 */
  --color-text-secondary: #8b93a8;  /* 辅助文本 */
  --color-text-muted:     #4a5068;  /* 弱化文本 */
  --color-border:         #252a3a;  /* 边框/分割线 */
  --color-border-strong:  #3a4155;

  /* ── 字体系统 ── */
  --font-display: 'Sora', 'PingFang SC', sans-serif;      /* 标题展示 */
  --font-body:    'DM Sans', 'PingFang SC', sans-serif;   /* 正文 */
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace;

  --text-xs:   0.75rem;   /* 12px */
  --text-sm:   0.875rem;  /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg:   1.125rem;  /* 18px */
  --text-xl:   1.25rem;   /* 20px */
  --text-2xl:  1.5rem;    /* 24px */
  --text-3xl:  1.875rem;  /* 30px */
  --text-4xl:  2.25rem;   /* 36px */
  --text-5xl:  3rem;      /* 48px */
  --text-hero: clamp(2.5rem, 6vw, 5rem); /* 响应式英雄字号 */

  --leading-tight:  1.2;
  --leading-normal: 1.6;
  --leading-loose:  1.8;

  /* ── 间距系统（基于 4px 网格）── */
  --space-1:  0.25rem;  /*  4px */
  --space-2:  0.5rem;   /*  8px */
  --space-3:  0.75rem;  /* 12px */
  --space-4:  1rem;     /* 16px */
  --space-5:  1.25rem;  /* 20px */
  --space-6:  1.5rem;   /* 24px */
  --space-8:  2rem;     /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
  --space-24: 6rem;     /* 96px */

  /* ── 圆角 ── */
  --radius-sm:  4px;
  --radius-md:  8px;
  --radius-lg:  12px;
  --radius-xl:  16px;
  --radius-2xl: 24px;
  --radius-full: 9999px;

  /* ── 阴影分层 ── */
  --shadow-sm:  0 1px 3px rgba(0,0,0,.3);
  --shadow-md:  0 4px 16px rgba(0,0,0,.35);
  --shadow-lg:  0 8px 32px rgba(0,0,0,.4);
  --shadow-glow: 0 0 24px rgba(79,142,247,.25);  /* 品牌色光晕 */

  /* ── 过渡 ── */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --duration-fast:   150ms;
  --duration-normal: 250ms;
  --duration-slow:   400ms;

  /* ── 布局常量 ── */
  --container-sm:  640px;
  --container-md:  768px;
  --container-lg:  1024px;
  --container-xl:  1280px;
  --container-2xl: 1536px;
}
```

> ⚠️ **亮色主题**：将 `--color-bg-base` 改为 `#f8f9fc`，`--color-bg-surface` 改为 `#ffffff`，文本色反转即可。详见 `references/light-theme.md`。

---

## Grid 布局系统

### 骨架：12列网格

```css
.grid-layout {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--space-6);
  max-width: var(--container-xl);
  margin: 0 auto;
  padding: 0 var(--space-8);
}

/* 列跨度工具类 */
.col-1  { grid-column: span 1; }
.col-2  { grid-column: span 2; }
.col-3  { grid-column: span 3; }   /* 1/4 */
.col-4  { grid-column: span 4; }   /* 1/3 */
.col-6  { grid-column: span 6; }   /* 1/2 */
.col-8  { grid-column: span 8; }   /* 2/3 */
.col-9  { grid-column: span 9; }   /* 3/4 */
.col-12 { grid-column: span 12; }  /* full */

/* 响应式 */
@media (max-width: 768px) {
  .col-3, .col-4, .col-6 { grid-column: span 12; }
  .col-8, .col-9          { grid-column: span 12; }
}
```

### 常用布局配方

```css
/* ① Dashboard 三列侧边栏布局 */
.layout-dashboard {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: 64px 1fr;
  min-height: 100vh;
}

/* ② 卡片瀑布流（自动填充）*/
.layout-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-6);
}

/* ③ 英雄区两栏（文字 + 图像）*/
.layout-hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: var(--space-16);
  min-height: 90vh;
}

/* ④ 功能特性 Bento Grid */
.layout-bento {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 200px;
  gap: var(--space-4);
}
.bento-wide  { grid-column: span 2; }
.bento-tall  { grid-row: span 2; }
.bento-large { grid-column: span 2; grid-row: span 2; }
```

---

## 色彩分层背景（必须实现）

背景不能是纯色，必须有**视觉深度**：

```css
/* 方案A：渐变噪点质感 */
body {
  background-color: var(--color-bg-base);
  background-image:
    radial-gradient(ellipse 80% 50% at 20% 10%, rgba(79,142,247,.08) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(124,58,237,.06) 0%, transparent 60%);
}

/* 方案B：细腻网格线背景 */
body {
  background-color: var(--color-bg-base);
  background-image: linear-gradient(rgba(255,255,255,.03) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,.03) 1px, transparent 1px);
  background-size: 40px 40px;
}

/* 方案C：点阵背景 */
body {
  background-color: var(--color-bg-base);
  background-image: radial-gradient(rgba(255,255,255,.06) 1px, transparent 1px);
  background-size: 24px 24px;
}

/* 卡片玻璃质感 */
.card-glass {
  background: rgba(255,255,255,.04);
  border: 1px solid var(--color-border);
  backdrop-filter: blur(12px);
  box-shadow: var(--shadow-md), inset 0 1px 0 rgba(255,255,255,.06);
}
```

---

## 组件样式规范

### 按钮层级

```css
/* 主按钮 */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
  background: var(--color-primary);
  color: #fff;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: 600;
  letter-spacing: .01em;
  transition: background var(--duration-fast) var(--ease-out),
              box-shadow var(--duration-fast) var(--ease-out),
              transform var(--duration-fast) var(--ease-out);
}
.btn-primary:hover {
  background: var(--color-primary-dim);
  box-shadow: var(--shadow-glow);
  transform: translateY(-1px);
}

/* 轮廓按钮 */
.btn-outline {
  padding: var(--space-3) var(--space-6);
  background: transparent;
  border: 1px solid var(--color-border-strong);
  color: var(--color-text-primary);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: 500;
  transition: border-color var(--duration-fast), background var(--duration-fast);
}
.btn-outline:hover {
  border-color: var(--color-primary);
  background: rgba(79,142,247,.08);
}

/* Ghost 幽灵按钮 */
.btn-ghost {
  padding: var(--space-2) var(--space-4);
  background: transparent;
  color: var(--color-text-secondary);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  transition: background var(--duration-fast), color var(--duration-fast);
}
.btn-ghost:hover {
  background: var(--color-bg-elevated);
  color: var(--color-text-primary);
}
```

### 卡片组件

```css
.card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
  transition: border-color var(--duration-normal), 
              box-shadow var(--duration-normal),
              transform var(--duration-normal) var(--ease-out);
}
.card:hover {
  border-color: var(--color-border-strong);
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

/* 数据指标卡 */
.card-metric .metric-value {
  font-size: var(--text-3xl);
  font-weight: 700;
  font-family: var(--font-display);
  color: var(--color-text-primary);
  line-height: var(--leading-tight);
}
.card-metric .metric-label {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  margin-top: var(--space-1);
}
.card-metric .metric-delta {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-xs);
  font-weight: 600;
  padding: 2px var(--space-2);
  border-radius: var(--radius-full);
}
.delta-up   { color: var(--color-success); background: rgba(34,197,94,.1); }
.delta-down { color: var(--color-danger);  background: rgba(239,68,68,.1); }
```

### 导航栏

```css
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 var(--space-8);
  background: rgba(13,15,20,.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.navbar-logo {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: -.02em;
}
.navbar-nav {
  display: flex;
  align-items: center;
  gap: var(--space-1);
}
.nav-link {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  border-radius: var(--radius-md);
  transition: color var(--duration-fast), background var(--duration-fast);
}
.nav-link:hover, .nav-link.active {
  color: var(--color-text-primary);
  background: var(--color-bg-elevated);
}
```

### 标签/Badge

```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: 2px var(--space-3);
  font-size: var(--text-xs);
  font-weight: 600;
  border-radius: var(--radius-full);
  letter-spacing: .04em;
  text-transform: uppercase;
}
.badge-primary { background: rgba(79,142,247,.15); color: var(--color-primary); }
.badge-success { background: rgba(34,197,94,.12);  color: var(--color-success); }
.badge-warning { background: rgba(245,158,11,.12); color: var(--color-warning); }
.badge-danger  { background: rgba(239,68,68,.12);  color: var(--color-danger);  }
```

---

## 字体加载（标准 Google Fonts 引入）

```html
<!-- Dark/Tech 风格 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<!-- 商务/简约 风格 -->
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">

<!-- 创意/编辑 风格 -->
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;400;700&family=Mona+Sans:wght@400;500;600&display=swap" rel="stylesheet">
```

---

## 动画规范

```css
/* 页面载入：元素渐入上移 */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0);    }
}
.animate-in {
  animation: fadeInUp var(--duration-slow) var(--ease-out) both;
}
/* 错开延迟：营造层叠节奏 */
.animate-in:nth-child(1) { animation-delay: 0ms;   }
.animate-in:nth-child(2) { animation-delay: 80ms;  }
.animate-in:nth-child(3) { animation-delay: 160ms; }
.animate-in:nth-child(4) { animation-delay: 240ms; }

/* 数字滚动计数器（JS） */
/* 参见 references/animations.md */

/* Skeleton 加载占位 */
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0;  }
}
.skeleton {
  background: linear-gradient(90deg,
    var(--color-bg-elevated) 25%,
    var(--color-bg-overlay)  50%,
    var(--color-bg-elevated) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-md);
}
```

---

## 输出质量检查清单

在完成 UI 前，逐项检查：

- [ ] `:root` 中定义了完整 Design Token（色彩、字号、间距）
- [ ] 布局使用 CSS Grid 或 Flexbox，无 float/table 布局
- [ ] 背景有分层深度（渐变/网格/点阵），非纯色
- [ ] 卡片有 border + 微阴影 + hover 状态
- [ ] 字体已通过 Google Fonts 引入，标题 / 正文 / 代码 分别使用不同字族
- [ ] 间距全部使用 `--space-*` Token
- [ ] 按钮有 3 种层级（Primary / Outline / Ghost）
- [ ] 颜色含语义化状态（success / warning / danger）
- [ ] 文本有 3 层层级（primary / secondary / muted）
- [ ] 有至少 1 个载入动画（fadeInUp / shimmer）
- [ ] 移动端响应式已处理（至少 breakpoint 768px）

---

## 参考文件索引

- `references/light-theme.md`   — 亮色主题 Token 覆盖
- `references/animations.md`    — 完整动画库（计数器/视差/滚动触发）
- `references/layout-recipes.md`— 更多布局模板（侧边栏/双栏/杂志式）
- `references/component-patterns.md` — 表单、表格、图表容器组件代码
