# 视频预览交互陷阱 (2026-06-15)

## 核心问题：stopPropagation 阻止节点选中

### 症状
- 单击视频预览区域，节点不被选中
- 属性面板（PropertyPanel）不显示
- 对话交流框（控制面板）不弹出

### 根因
在 VideoPreview 组件外层 div 添加了 `onClick={(e) => e.stopPropagation()}`，阻止了事件冒泡到 ReactFlow。

### 解决方案
```tsx
// ❌ 错误
<div onClick={(e) => e.stopPropagation()}>

// ✅ 正确 - 不添加 onClick
<div onMouseEnter={() => setIsHovered(true)} onMouseLeave={() => setIsHovered(false)}>

// ✅ 控件区域使用 onMouseDown 阻止冒泡
<div onMouseDown={(e) => e.stopPropagation()}>
```

## 用户术语区分（重要）

| 用户说的 | 实际含义 | 触发方式 |
|---------|---------|---------|
| 对话交流框 / 对话框 | 控制面板（输入提示词、选择模型、生成按钮） | 单击节点 |
| 放大预览 | PreviewModal 全屏预览 | 控件区域的全屏按钮 |
| 属性面板 | PropertyPanel 右侧面板 | 单击选中节点后自动显示 |

## 交互设计规范

### 悬停行为
- 鼠标进入 → 从头播放视频
- 鼠标移开 → 暂停并重置到开头

### 单击行为
- 单击视频区域 → 显示控制面板（对话交流框）
- 单击空白素材框 → 显示控制面板
- 右键素材框 → 触发文件上传

### 控件区域
- 悬停时显示底部控件
- 包含：播放/暂停、快进快退、时间、速度、静音、全屏按钮
- 使用 `onMouseDown` 阻止冒泡，不影响节点选中

## 动画规范

控制面板弹出动画：
```css
@keyframes popUp {
  from {
    opacity: 0;
    transform: translateY(8px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

animation: popUp 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
```

## 相关文件
- `frontend/src/components/VideoPreview.tsx`
- `frontend/src/components/nodes/VideoNode.tsx`
- `frontend/src/components/nodes/ImageNode.tsx`
- `frontend/src/styles/globals.css`
