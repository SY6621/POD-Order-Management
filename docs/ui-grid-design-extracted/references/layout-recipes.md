# 布局模板大全

## 1. SaaS Dashboard 布局

```css
.layout-app {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: 64px 1fr;
  grid-template-areas:
    "sidebar topbar"
    "sidebar main";
  min-height: 100vh;
}
.app-sidebar { grid-area: sidebar; border-right: 1px solid var(--color-border); }
.app-topbar  { grid-area: topbar;  border-bottom: 1px solid var(--color-border); }
.app-main    { grid-area: main; overflow-y: auto; padding: var(--space-8); }

/* 侧边栏导航项 */
.sidebar-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  margin: 2px var(--space-3);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  transition: all var(--duration-fast);
  cursor: pointer;
}
.sidebar-item:hover { background: var(--color-bg-elevated); color: var(--color-text-primary); }
.sidebar-item.active { background: rgba(79,142,247,.12); color: var(--color-primary); font-weight: 600; }
.sidebar-item .icon { width: 18px; height: 18px; flex-shrink: 0; }
```

## 2. Landing Page 结构

```html
<body>
  <nav class="navbar">...</nav>

  <!-- 英雄区：左文右图 -->
  <section class="hero">
    <div class="hero-content">
      <div class="badge badge-primary">New Release</div>
      <h1 class="hero-title">标题最多两行<br>清晰有力</h1>
      <p class="hero-sub">副标题一两句话，说清楚价值主张</p>
      <div class="hero-actions">
        <button class="btn-primary">立即开始</button>
        <button class="btn-outline">了解更多</button>
      </div>
    </div>
    <div class="hero-visual"><!-- 产品截图/插图 --></div>
  </section>

  <!-- 功能特性：Bento Grid -->
  <section class="features">
    <div class="layout-bento">
      <div class="card bento-large">主功能大卡</div>
      <div class="card">功能2</div>
      <div class="card">功能3</div>
      <div class="card bento-wide">功能4宽卡</div>
    </div>
  </section>

  <!-- 数据/社会证明 -->
  <section class="metrics">
    <div class="layout-cards">
      <div class="card card-metric">...</div>
    </div>
  </section>

  <!-- CTA 召唤行动 -->
  <section class="cta">...</section>

  <footer>...</footer>
</body>
```

```css
.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  gap: var(--space-16);
  min-height: 88vh;
  max-width: var(--container-xl);
  margin: 0 auto;
  padding: var(--space-20) var(--space-8);
}
.hero-title {
  font-family: var(--font-display);
  font-size: var(--text-hero);
  font-weight: 800;
  line-height: var(--leading-tight);
  letter-spacing: -.03em;
  color: var(--color-text-primary);
  margin: var(--space-4) 0;
}
.hero-sub {
  font-size: var(--text-lg);
  color: var(--color-text-secondary);
  line-height: var(--leading-loose);
  max-width: 48ch;
}
.hero-actions {
  display: flex;
  gap: var(--space-3);
  margin-top: var(--space-8);
}
```

## 3. 文章/文档 双栏布局

```css
.layout-docs {
  display: grid;
  grid-template-columns: 260px 1fr 220px;
  gap: var(--space-8);
  max-width: var(--container-2xl);
  margin: 0 auto;
  padding: var(--space-8);
}
/* 左侧目录 + 中间内容 + 右侧大纲 */

/* 文章正文排版 */
.prose { max-width: 72ch; }
.prose h1 { font-size: var(--text-4xl); font-weight: 800; margin-bottom: var(--space-4); }
.prose h2 { font-size: var(--text-2xl); font-weight: 700; margin: var(--space-10) 0 var(--space-4); }
.prose h3 { font-size: var(--text-xl);  font-weight: 600; margin: var(--space-8) 0 var(--space-3); }
.prose p  { line-height: var(--leading-loose); color: var(--color-text-secondary); margin-bottom: var(--space-4); }
.prose code {
  font-family: var(--font-mono);
  font-size: .875em;
  background: var(--color-bg-elevated);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  color: var(--color-primary);
}
```

## 4. 产品展示列表

```css
/* 图片 + 信息的水平卡片 */
.product-card {
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: var(--space-6);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
  transition: box-shadow var(--duration-normal);
}
.product-card:hover { box-shadow: var(--shadow-lg); }
.product-image { width: 100%; height: 100%; object-fit: cover; }
.product-info { padding: var(--space-6); display: flex; flex-direction: column; gap: var(--space-3); }
```

## 5. 模态框/弹出层

```css
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn var(--duration-fast) var(--ease-out);
}
.modal {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-2xl);
  padding: var(--space-8);
  width: min(560px, calc(100vw - var(--space-8)));
  box-shadow: var(--shadow-lg);
  animation: scaleIn var(--duration-normal) var(--ease-out);
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-6);
}
.modal-title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
}
```
