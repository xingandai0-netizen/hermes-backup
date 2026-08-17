# 节点视觉设计模式

## 设计原则
- 节点无边框，视觉更沉浸
- 预览区有柔和白光，突出素材内容
- 选中/悬停状态通过阴影变化体现
- 所有 AI 生成按钮纯白色，无蓝紫色

## BaseNode 样式

### 无边框 + 阴影
```tsx
<div style={{
  width: 320,
  background: "rgba(28, 28, 30, 0.95)",
  backdropFilter: "saturate(180%) blur(20px)",
  border: "none",  // 无边框
  borderRadius: 16,
  boxShadow: selected
    ? "0 0 0 1px rgba(255, 255, 255, 0.15), 0 12px 32px rgba(0, 0, 0, 0.5)"
    : isHovered
      ? "0 8px 24px rgba(0, 0, 0, 0.4)"
      : "0 4px 12px rgba(0, 0, 0, 0.3)",
}}>
```

### Handle 样式
```tsx
const handleStyle: React.CSSProperties = {
  width: 18,
  height: 18,
  background: categoryColor,
  border: "2px solid #0a0a0f",
  borderRadius: "50%",
  boxShadow: isHovered
    ? `0 0 16px ${categoryColor}, 0 0 8px ${categoryColor}80`
    : `0 0 8px ${categoryColor}70`,
  transition: "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
  transform: isHovered ? "scale(1.3)" : "scale(1)",
  opacity: isHovered ? 1 : 0,
  pointerEvents: isHovered ? "auto" : "none",
};
```

## 预览区泛光

### 图片预览
```tsx
<div style={{
  width: "100%",
  height: previewHeight,
  cursor: "pointer",
  background: "#1a1a1a",
  borderRadius: 12,
  boxShadow: "0 0 16px rgba(255, 255, 255, 0.2)",  // 淡泛光
  overflow: "hidden",
}}>
```

### 视频预览
```tsx
<div style={{
  cursor: "pointer",
  background: "#1a1a1a",
  borderRadius: 12,
  boxShadow: "0 0 16px rgba(255, 255, 255, 0.2)",
}}>
```

## 生成按钮样式

### 纯白色（替换蓝紫色）
```tsx
// ❌ 蓝紫色
color: "#0a84ff"
background: "rgba(10, 132, 255, 0.2)"

// ✅ 纯白色
color: loading ? "rgba(255,255,255,0.3)" : "#ffffff"
background: loading ? "rgba(255,255,255,0.08)" : "rgba(255,255,255,0.15)"
border: "1px solid rgba(255,255,255,0.2)"
```

### Hover 状态
```tsx
onMouseEnter={(e) => {
  e.currentTarget.style.background = "rgba(255,255,255,0.2)";
}}
onMouseLeave={(e) => {
  e.currentTarget.style.background = loading ? "rgba(255,255,255,0.08)" : "rgba(255,255,255,0.15)";
}}
```

## 画布背景
```tsx
const bgStyle = useMemo(() => ({ background: "#121215" }), []);
```

## 进度条样式
```tsx
// 亮白色进度条
<div style={{
  width: `${progress}%`,
  height: "100%",
  background: "linear-gradient(90deg, #ffffff, #e0e0e0)",
  transition: "width 0.3s ease",
}} />
```

## 生成体验优化

### 初始进度 5%
```tsx
setLoading(true);
setProgress(5);  // 立即显示进度条
```

### 轮询间隔 1.5s
```tsx
pollRef.current = setInterval(async () => {
  // ...
}, 1500);
```

### 完成停留 600ms
```tsx
if (pollData.status === "completed" && pollData.url) {
  clearInterval(pollRef.current!);
  setProgress(100);
  setTimeout(() => {
    updateResult(pollData.url, pollData.asset_id || "");
    setLoading(false);
  }, 600);
}
```

### 预览同步
```tsx
useEffect(() => {
  if (d.assetUrl && d.assetUrl !== previewUrl) {
    setPreviewUrl(d.assetUrl);
  }
}, [d.assetUrl]);
```
