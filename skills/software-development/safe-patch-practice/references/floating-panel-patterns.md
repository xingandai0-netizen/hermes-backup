# 悬浮面板设计模式

## TapNow风格对话框（2026-06-15验证）

### 设计规范
```tsx
<div style={{
  position: "absolute",
  top: "100%",      // 节点下方
  left: 0,
  right: 0,
  marginTop: 8,
  background: "rgba(51,51,51,0.95)",  // 毛玻璃深色
  border: "1px solid rgba(255,255,255,0.08)",
  borderRadius: 16,
  padding: 0,
  boxShadow: "0 4px 8px rgba(0,0,0,0.3), 0 0 0 1px rgba(255,255,255,0.05)",
  zIndex: 100,
  animation: "fadeIn 0.2s ease",
  backdropFilter: "blur(20px)",
}}>
```

### 结构
1. **顶部工具栏** - 功能按钮（AI优化、添加、全屏）+ 分隔线
2. **输入区域** - 透明背景textarea，16px字号，1.5行高
3. **底部工具栏** - 左侧参数显示、右侧麦克风+发送按钮

### 颜色规范
- 背景: `rgba(51,51,51,0.95)`
- 边框: `rgba(255,255,255,0.08)`
- 工具栏背景: `rgba(255,255,255,0.06)`
- 文字: `#fff` 主文字, `#8a8f98` 次文字
- 分隔线: `rgba(255,255,255,0.06)`

### 必须避免
1. ❌ 容器加 `overflow: hidden` - 会裁剪面板
2. ❌ 容器加 `onClick={stopPropagation}` - 阻止子元素点击
3. ❌ 使用 `transform` - 与React Flow冲突
4. ❌ 使用 `!important` 覆盖React Flow样式

### 必须检查
- [ ] 父容器无 `overflow: hidden`
- [ ] 按钮点击正常工作
- [ ] 面板不被裁剪
- [ ] 输入框可正常输入