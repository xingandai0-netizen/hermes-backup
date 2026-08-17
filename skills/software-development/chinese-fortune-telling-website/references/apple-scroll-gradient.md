# Apple风格滚动渐变背景实现

## 需求
页面顶部米白色，滚动时逐渐变暗，底部全黑。

## 完整实现模式

### 1. 状态管理
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

### 2. 背景色计算
```typescript
// 米白色(245,240,230) → 黑色(10,10,15)
const bgColor = `rgb(${Math.round(245 - scrollProgress * 235)}, ${Math.round(240 - scrollProgress * 230)}, ${Math.round(230 - scrollProgress * 220)})`
```

### 3. 文字颜色动态切换
```typescript
// 主文字
color: scrollProgress > 0.5 ? '#fff' : '#333'

// 次要文字
color: scrollProgress > 0.5 ? 'rgba(255,255,255,0.6)' : 'rgba(0,0,0,0.4)'

// 背景装饰字
color: `rgba(${scrollProgress > 0.5 ? 255 : 0}, ${scrollProgress > 0.5 ? 255 : 0}, ${scrollProgress > 0.5 ? 255 : 0}, 0.03)`
```

### 4. 按钮样式动态切换
```typescript
// 主按钮
style={{ 
  backgroundColor: scrollProgress > 0.5 ? '#fff' : '#1a1a2e',
  color: scrollProgress > 0.5 ? '#0a1628' : '#fff'
}}

// 次按钮
style={{ 
  backgroundColor: `rgba(${scrollProgress > 0.5 ? 255 : 0}, ${scrollProgress > 0.5 ? 255 : 0}, ${scrollProgress > 0.5 ? 255 : 0}, 0.1)`,
  color: scrollProgress > 0.5 ? '#fff' : '#333',
  border: `1px solid rgba(${scrollProgress > 0.5 ? 255 : 0}, ${scrollProgress > 0.5 ? 255 : 0}, ${scrollProgress > 0.5 ? 255 : 0}, 0.2)`
}}
```

### 5. 导航栏动态切换
```typescript
style={{ 
  backgroundColor: `rgba(${scrollProgress > 0.1 ? 10 : 245}, ${scrollProgress > 0.1 ? 22 : 240}, ${scrollProgress > 0.1 ? 40 : 230}, 0.8)`,
}}
```

## ⚠️ 关键Pitfall

**CSS body背景必须设为transparent**：
```css
body {
  background: transparent;  /* 不能是具体颜色 */
}
```

否则CSS会覆盖React的inline style，滚动渐变效果完全不生效。

## 调试方法

检查背景色是否生效：
```javascript
(() => {
  const div = document.querySelector('div');
  const computedStyle = window.getComputedStyle(div);
  return computedStyle.backgroundColor;
})()
```
