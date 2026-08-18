# Apple Glass Morphism — CSS 实现参考

## 核心效果

### 毛玻璃面板（顶栏/菜单/模态框）
```css
.glass-panel {
  background: rgba(28, 28, 30, 0.72);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 
              inset 0 1px 0 rgba(255, 255, 255, 0.06);
}
```

### 浮动按钮
```css
.glass-button {
  background: rgba(28, 28, 30, 0.72);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  color: rgba(235, 235, 245, 0.5);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-button:hover {
  color: #fff;
  background: rgba(58, 58, 60, 0.72);
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}
```

### 强调按钮（蓝色）
```css
.accent-button {
  background: rgba(10, 132, 255, 0.15);
  color: #0a84ff;
  border: 0.5px solid rgba(10, 132, 255, 0.2);
  border-radius: 8px;
}

.accent-button:hover {
  background: rgba(10, 132, 255, 0.25);
  border-color: rgba(10, 132, 255, 0.4);
}
```

## 色彩系统

### 背景层级
```css
:root {
  --bg-deep: #000000;
  --bg-panel: rgba(28, 28, 30, 0.8);
  --bg-surface: rgba(44, 44, 46, 0.6);
  --bg-elevated: rgba(58, 58, 60, 0.5);
  --bg-glass: rgba(255, 255, 255, 0.03);
}
```

### 文字层级
```css
:root {
  --text-primary: #ffffff;
  --text-secondary: rgba(235, 235, 245, 0.6);
  --text-tertiary: rgba(235, 235, 245, 0.3);
  --text-muted: rgba(235, 235, 245, 0.15);
}
```

### 语义色彩
```css
:root {
  --accent: #0a84ff;
  --success: #30d158;
  --error: #ff453a;
  --warning: #ff9f0a;
}
```

## 排版系统

### 字体栈
```css
:root {
  --font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 
                 'SF Pro Text', 'Helvetica Neue', 'Inter', sans-serif;
  --font-mono: 'SF Mono', 'Fira Code', 'Consolas', monospace;
}
```

### 字体层级
```css
:root {
  --text-xs: 11px;
  --text-sm: 13px;
  --text-base: 15px;
  --text-lg: 17px;
  --text-xl: 20px;
  --text-2xl: 24px;
}
```

## 圆角规范
```css
:root {
  --radius-sm: 8px;   /* 按钮、输入框 */
  --radius-md: 12px;  /* 菜单、卡片 */
  --radius-lg: 16px;  /* 面板 */
  --radius-xl: 20px;  /* 大容器 */
}
```

## 动效曲线
```css
/* Apple 标准曲线 */
--ease-apple: cubic-bezier(0.4, 0, 0.2, 1);

/* 弹性效果 */
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
```

## 交互反馈

### 按钮
- 悬停：`scale(1.05)` + 阴影
- 点击：`scale(0.98)`
- 过渡：`0.2s cubic-bezier(0.4, 0, 0.2, 1)`

### 菜单项
- 悬停背景：`rgba(255, 255, 255, 0.08)`
- 过渡：`0.15s ease`

### 分隔线
- 高度：`0.5px`
- 颜色：`rgba(255, 255, 255, 0.08)`
