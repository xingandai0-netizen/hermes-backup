# Apple风格滚动渐变效果

> 基于小算项目实战经验，实现Apple官网风格的滚动渐变背景效果。

---

## 效果描述

- **初始状态**：米白色背景（245, 240, 230）
- **滚动过程**：背景逐渐变暗
- **最终状态**：黑色背景（10, 10, 15）

所有文字、按钮、卡片颜色都随滚动动态变化。

---

## 实现步骤

### 1. CSS设置（globals.css）

```css
/* 必须设置body背景为透明，否则会覆盖React inline style */
body {
  background: transparent;
}
```

**⚠️ 关键陷阱**：如果globals.css中设置了`body { background: #xxx }`，React的inline style会被覆盖！

### 2. React状态管理

```typescript
const [scrollProgress, setScrollProgress] = useState(0)

useEffect(() => {
  const handleScroll = () => {
    const scrollTop = window.scrollY
    const docHeight = document.documentElement.scrollHeight - window.innerHeight
    const progress = Math.min(scrollTop / docHeight, 1)
    setScrollProgress(progress)
  }

  window.addEventListener('scroll', handleScroll, { passive: true })
  return () => window.removeEventListener('scroll', handleScroll)
}, [])
```

### 3. 动态背景色计算

```typescript
// 米白色 (245, 240, 230) → 黑色 (10, 10, 15)
const bgColor = `rgb(${Math.round(245 - scrollProgress * 235)}, ${Math.round(240 - scrollProgress * 230)}, ${Math.round(230 - scrollProgress * 220)})`
```

### 4. 动态文字颜色

```typescript
// 深色文字（初始）→ 浅色文字（滚动后）
const textColor = scrollProgress > 0.5 ? '#fff' : '#1a1a2e'
const textColorLight = scrollProgress > 0.5 ? 'rgba(255,255,255,0.6)' : 'rgba(0,0,0,0.5)'

// 按钮背景
const btnBg = scrollProgress > 0.5 ? '#fff' : '#1a1a2e'
const btnText = scrollProgress > 0.5 ? '#0a1628' : '#fff'

// 半透明元素
const glassBg = `rgba(${scrollProgress > 0.5 ? 255 : 0}, ${scrollProgress > 0.5 ? 255 : 0}, ${scrollProgress > 0.5 ? 255 : 0}, 0.1)`
const glassBorder = `1px solid rgba(${scrollProgress > 0.5 ? 255 : 0}, ${scrollProgress > 0.5 ? 255 : 0}, ${scrollProgress > 0.5 ? 255 : 0}, 0.2)`
```

### 5. 应用到组件

```tsx
<div className="min-h-screen" style={{ backgroundColor: bgColor }}>
  <nav style={{ 
    backgroundColor: `rgba(${scrollProgress > 0.1 ? 10 : 245}, ${scrollProgress > 0.1 ? 22 : 240}, ${scrollProgress > 0.1 ? 40 : 230}, 0.8)` 
  }}>
    ...
  </nav>
  
  <h1 style={{ color: textColor }}>标题</h1>
  <p style={{ color: textColorLight }}>描述文字</p>
  
  <button style={{ backgroundColor: btnBg, color: btnText }}>
    按钮
  </button>
</div>
```

---

## 配色方案

| scrollProgress | 背景色 | 主文字 | 次文字 | 按钮背景 |
|---------------|--------|--------|--------|----------|
| 0 (初始) | rgb(245,240,230) 米白 | #1a1a2e 深蓝 | rgba(0,0,0,0.5) | #1a1a2e |
| 0.5 (中间) | rgb(128,125,120) 灰色 | #fff 白色 | rgba(255,255,255,0.6) | #fff |
| 1 (底部) | rgb(10,10,15) 黑色 | #fff 白色 | rgba(255,255,255,0.6) | #fff |

---

## Apple风格动画效果

### fadeInUp淡入动画
```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
```

使用方式：
```tsx
<div className="animate-[fadeInUp_1s_ease_0.2s_both]">延迟0.2s</div>
<div className="animate-[fadeInUp_1s_ease_0.4s_both]">延迟0.4s</div>
<div className="animate-[fadeInUp_1s_ease_0.6s_both]">延迟0.6s</div>
```

### 悬停效果
```tsx
<Link className="hover:scale-105 hover:shadow-2xl hover:-translate-y-1 active:scale-95 transition-all duration-300">
  按钮
</Link>
```

### 毛玻璃导航栏
```tsx
<nav className="bg-[#0a1628]/80 backdrop-blur-xl border-b border-white/10">
  ...
</nav>
```

---

## 背景散字装饰

```tsx
{bgCharacters.map((char, index) => (
  <div
    key={index}
    className="fixed font-brush select-none pointer-events-none"
    style={{
      top: `${10 + (index * 8) % 80}%`,
      left: `${5 + (index * 12) % 90}%`,
      fontSize: `${80 + (index * 20) % 100}px`,
      transform: `rotate(${-15 + (index * 10) % 30}deg)`,
      color: `rgba(${scrollProgress > 0.5 ? 255 : 0}, ${scrollProgress > 0.5 ? 255 : 0}, ${scrollProgress > 0.5 ? 255 : 0}, 0.03)`,
    }}
  >
    {char}
  </div>
))}
```

---

## 常见问题

### Q: 背景色不变化？
A: 检查globals.css中是否有`body { background: #xxx }`覆盖了inline style

### Q: 文字在某些区域不可见？
A: 确保所有文字颜色都随scrollProgress动态变化

### Q: 滚动不流畅？
A: 使用`{ passive: true }`监听滚动事件

---

**最后更新**: 2026-07-08
**基于项目**: 小算 v2
