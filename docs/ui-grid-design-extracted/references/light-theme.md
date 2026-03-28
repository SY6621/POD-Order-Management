# 亮色主题 Token 覆盖

在 `:root` 之后追加 `[data-theme="light"]` 或 `@media (prefers-color-scheme: light)`：

```css
[data-theme="light"], .theme-light {
  --color-bg-base:    #f4f6fb;
  --color-bg-surface: #ffffff;
  --color-bg-elevated:#eef1f8;
  --color-bg-overlay: #e4e9f4;

  --color-text-primary:   #0f1117;
  --color-text-secondary: #5a6478;
  --color-text-muted:     #9aa0b4;
  --color-border:         #dde1ed;
  --color-border-strong:  #c4cade;

  /* 主色保持一致，略微加深以保证对比度 */
  --color-primary:    #2563eb;
  --color-primary-dim:#1d4ed8;

  /* 卡片阴影在亮色下更柔和 */
  --shadow-sm: 0 1px 4px rgba(0,0,0,.06);
  --shadow-md: 0 4px 16px rgba(0,0,0,.08);
  --shadow-lg: 0 8px 32px rgba(0,0,0,.1);
  --shadow-glow: 0 0 24px rgba(37,99,235,.15);
}
```

## 亮色背景分层方案

```css
/* 亮色方案A：柔和渐变光斑 */
body[data-theme="light"] {
  background-color: var(--color-bg-base);
  background-image:
    radial-gradient(ellipse 70% 50% at 15% 10%, rgba(37,99,235,.05) 0%, transparent 60%),
    radial-gradient(ellipse 50% 40% at 85% 85%, rgba(124,58,237,.04) 0%, transparent 60%);
}

/* 亮色方案B：细线网格 */
body[data-theme="light"] {
  background-color: #f4f6fb;
  background-image: linear-gradient(rgba(0,0,0,.03) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(0,0,0,.03) 1px, transparent 1px);
  background-size: 40px 40px;
}
```

## 亮色卡片样式

```css
.card {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
}
.card:hover {
  border-color: var(--color-border-strong);
  box-shadow: var(--shadow-md);
}

/* 亮色无玻璃质感，改用纯白 + 轻阴影 */
.card-glass {
  background: rgba(255,255,255,.85);
  border: 1px solid rgba(255,255,255,.9);
  backdrop-filter: blur(12px);
}
```
