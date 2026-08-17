# Apple 交互动效 — 实现参考

## 核心原则
- 克制、速度、有目的的动效
- 过渡时间：150-200ms
- 曲线：`cubic-bezier(0.4, 0, 0.2, 1)`（Apple 标准）

## 按钮动效

### 悬停效果
```typescript
// 放大 + 阴影
onMouseEnter: (e) => {
  e.currentTarget.style.transform = 'scale(1.05)';
  e.currentTarget.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.3)';
}
onMouseLeave: (e) => {
  e.currentTarget.style.transform = 'scale(1)';
  e.currentTarget.style.boxShadow = 'none';
}
```

### 点击反馈
```css
button:active {
  transform: scale(0.98);
}
```

### 统一过渡
```css
button {
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}
```

## 菜单/卡片动效

### 悬停背景变亮
```typescript
onMouseEnter: (e) => {
  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.08)';
}
onMouseLeave: (e) => {
  e.currentTarget.style.background = 'none';
}
```

### 卡片上浮
```typescript
onMouseEnter: (e) => {
  e.currentTarget.style.transform = 'translateY(-2px)';
  e.currentTarget.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.3)';
}
```

## 状态指示

### 加载脉冲
```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.loading {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

### 进入动画
```css
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

.animate-enter {
  animation: scaleIn 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
```

## 工具函数

### 创建悬停处理器
```typescript
export const createHoverHandlers = (
  baseStyle: CSSProperties,
  hoverStyle: CSSProperties
) => ({
  onMouseEnter: (e: React.MouseEvent<HTMLElement>) => {
    Object.assign(e.currentTarget.style, hoverStyle);
  },
  onMouseLeave: (e: React.MouseEvent<HTMLElement>) => {
    Object.assign(e.currentTarget.style, baseStyle);
  },
});
```

## 无障碍
- 使用 `prefers-reduced-motion` 媒体查询
- 禁用动画时保持功能可用
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
