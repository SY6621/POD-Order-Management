# 组件模式库

## 表单组件

```css
.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}
.form-label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text-secondary);
  letter-spacing: .01em;
}
.form-input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  color: var(--color-text-primary);
  font-family: var(--font-body);
  transition: border-color var(--duration-fast), box-shadow var(--duration-fast);
  outline: none;
}
.form-input::placeholder { color: var(--color-text-muted); }
.form-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(79,142,247,.15);
}
.form-input:invalid:not(:placeholder-shown) {
  border-color: var(--color-danger);
  box-shadow: 0 0 0 3px rgba(239,68,68,.12);
}
.form-hint  { font-size: var(--text-xs); color: var(--color-text-muted); }
.form-error { font-size: var(--text-xs); color: var(--color-danger); }
```

## 数据表格

```css
.data-table { width: 100%; border-collapse: collapse; }
.data-table thead th {
  padding: var(--space-3) var(--space-4);
  text-align: left;
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: .08em;
  border-bottom: 1px solid var(--color-border);
  white-space: nowrap;
}
.data-table tbody tr {
  border-bottom: 1px solid var(--color-border);
  transition: background var(--duration-fast);
}
.data-table tbody tr:last-child { border-bottom: none; }
.data-table tbody tr:hover { background: var(--color-bg-elevated); }
.data-table tbody td {
  padding: var(--space-4);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  vertical-align: middle;
}
.data-table tbody td:first-child { color: var(--color-text-primary); font-weight: 500; }
```

## 选项卡 (Tabs)

```css
.tabs {
  display: flex;
  gap: var(--space-1);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--space-6);
}
.tab-item {
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text-muted);
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  cursor: pointer;
  transition: color var(--duration-fast), border-color var(--duration-fast);
}
.tab-item:hover { color: var(--color-text-secondary); }
.tab-item.active {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

/* 胶囊式 Tabs */
.tabs-pill {
  display: flex;
  gap: var(--space-1);
  background: var(--color-bg-elevated);
  padding: var(--space-1);
  border-radius: var(--radius-lg);
  width: fit-content;
}
.tab-pill {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  font-weight: 500;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--duration-fast);
}
.tab-pill.active {
  background: var(--color-bg-surface);
  color: var(--color-text-primary);
  box-shadow: var(--shadow-sm);
}
```

## 进度条

```css
.progress-bar {
  height: 6px;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-full);
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  border-radius: var(--radius-full);
  background: linear-gradient(90deg, var(--color-primary), var(--color-accent));
  transition: width .8s var(--ease-out);
}
```

## 通知提示 (Toast/Alert)

```css
.alert {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-radius: var(--radius-lg);
  font-size: var(--text-sm);
  border-left: 3px solid currentColor;
}
.alert-info    { background: rgba(79,142,247,.08);  color: var(--color-primary); }
.alert-success { background: rgba(34,197,94,.08);   color: var(--color-success); }
.alert-warning { background: rgba(245,158,11,.08);  color: var(--color-warning); }
.alert-danger  { background: rgba(239,68,68,.08);   color: var(--color-danger);  }

.alert-title { font-weight: 600; margin-bottom: var(--space-1); color: inherit; }
.alert-body  { color: var(--color-text-secondary); line-height: var(--leading-normal); }
```

## 图表容器（Chart.js / D3 通用）

```css
.chart-container {
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
}
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}
.chart-title {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--color-text-primary);
}
.chart-legend {
  display: flex;
  gap: var(--space-4);
}
.legend-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}
.legend-dot {
  width: 8px; height: 8px;
  border-radius: var(--radius-full);
  flex-shrink: 0;
}

/* Chart.js 颜色建议 */
/*
  primary:  rgba(79, 142, 247, .8)
  accent:   rgba(124, 58, 237, .8)
  success:  rgba(34, 197, 94, .8)
  warning:  rgba(245, 158, 11, .8)
  gridColor: rgba(255,255,255,.05)  (dark) / rgba(0,0,0,.05) (light)
*/
```

## 头像 (Avatar)

```css
.avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-full);
  overflow: hidden;
  flex-shrink: 0;
  font-weight: 600;
  color: #fff;
}
.avatar-sm  { width: 28px; height: 28px; font-size: var(--text-xs); }
.avatar-md  { width: 36px; height: 36px; font-size: var(--text-sm); }
.avatar-lg  { width: 48px; height: 48px; font-size: var(--text-base); }
.avatar-xl  { width: 64px; height: 64px; font-size: var(--text-xl); }

/* 头像组叠加 */
.avatar-stack { display: flex; }
.avatar-stack .avatar { margin-left: -8px; border: 2px solid var(--color-bg-surface); }
.avatar-stack .avatar:first-child { margin-left: 0; }
```
