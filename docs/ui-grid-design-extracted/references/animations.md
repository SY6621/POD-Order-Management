# 动画库参考

## CSS 动画集

```css
/* ─── 基础入场 ─── */
@keyframes fadeIn       { from { opacity: 0 }           to { opacity: 1 } }
@keyframes fadeInUp     { from { opacity: 0; transform: translateY(24px) }  to { opacity: 1; transform: none } }
@keyframes fadeInDown   { from { opacity: 0; transform: translateY(-24px) } to { opacity: 1; transform: none } }
@keyframes fadeInLeft   { from { opacity: 0; transform: translateX(-24px) } to { opacity: 1; transform: none } }
@keyframes fadeInRight  { from { opacity: 0; transform: translateX(24px) }  to { opacity: 1; transform: none } }
@keyframes scaleIn      { from { opacity: 0; transform: scale(.92) }         to { opacity: 1; transform: scale(1) } }
@keyframes slideInLeft  { from { transform: translateX(-100%) }               to { transform: none } }

/* ─── 持续循环 ─── */
@keyframes spin    { to { transform: rotate(360deg) } }
@keyframes ping    { 0%,100% { transform: scale(1); opacity: 1 } 50% { transform: scale(1.4); opacity: .6 } }
@keyframes pulse   { 0%,100% { opacity: 1 } 50% { opacity: .5 } }
@keyframes bounce  { 0%,100% { transform: translateY(0) } 50% { transform: translateY(-8px) } }
@keyframes float   { 0%,100% { transform: translateY(0) }  50% { transform: translateY(-12px) } }
@keyframes shimmer {
  0%   { background-position: -200% 0 }
  100% { background-position:  200% 0 }
}

/* ─── 使用工具类 ─── */
.anim-fade-in-up { animation: fadeInUp var(--duration-slow) var(--ease-out) both }
.anim-scale-in   { animation: scaleIn  var(--duration-slow) var(--ease-out) both }
.anim-float      { animation: float 4s ease-in-out infinite }
.anim-pulse      { animation: pulse 2s ease-in-out infinite }

/* 错开延迟：最多 6 个子元素 */
.stagger > *:nth-child(1) { animation-delay:   0ms }
.stagger > *:nth-child(2) { animation-delay:  80ms }
.stagger > *:nth-child(3) { animation-delay: 160ms }
.stagger > *:nth-child(4) { animation-delay: 240ms }
.stagger > *:nth-child(5) { animation-delay: 320ms }
.stagger > *:nth-child(6) { animation-delay: 400ms }
```

## Scroll-triggered 动画（Intersection Observer）

```javascript
const io = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      io.unobserve(entry.target); // 只触发一次
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('[data-animate]').forEach(el => io.observe(el));
```

```css
[data-animate] {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity .6s var(--ease-out), transform .6s var(--ease-out);
}
[data-animate].visible {
  opacity: 1;
  transform: none;
}
```

## 数字计数器动画

```javascript
function animateCounter(el) {
  const target = parseInt(el.dataset.target, 10);
  const duration = 1800;
  const start = performance.now();

  function step(now) {
    const progress = Math.min((now - start) / duration, 1);
    // easeOutExpo
    const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
    el.textContent = Math.floor(eased * target).toLocaleString();
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// 当进入视窗时触发
const counterObserver = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) animateCounter(e.target) });
}, { threshold: 0.5 });

document.querySelectorAll('[data-target]').forEach(el => counterObserver.observe(el));
```

```html
<span data-target="12847">0</span>
```

## 视差背景（轻量版）

```javascript
window.addEventListener('scroll', () => {
  const y = window.scrollY;
  document.querySelector('.hero-bg')
    ?.style.setProperty('transform', `translateY(${y * 0.3}px)`);
});
```
