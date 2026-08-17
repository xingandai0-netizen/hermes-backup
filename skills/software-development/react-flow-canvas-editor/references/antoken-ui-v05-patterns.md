# Antoken UI v0.5 Patterns (2026-06-15)

## VideoPreview 组件规范

### 交互行为
- **悬停播放**：鼠标进入从头播放，离开暂停重置
- **控件区域**：悬停时显示，包含进度条、播放/暂停、时间、全屏按钮
- **单击**：只阻止冒泡，不执行操作（让ReactFlow选中节点）
- **全屏按钮**：点击打开PreviewModal

### 关键代码模式
```typescript
// 悬停播放
useEffect(() => {
  if (!hoverToPlay || !videoRef.current) return;
  if (isHovered) {
    videoRef.current.currentTime = 0;
    videoRef.current.play().catch(() => {});
  } else {
    videoRef.current.pause();
    videoRef.current.currentTime = 0;
  }
}, [isHovered, hoverToPlay]);

// 单击只阻止冒泡
const handleClick = useCallback((e: React.MouseEvent) => {
  e.stopPropagation();
}, []);
```

---

## Handle 连接节点规范

### 样式配置
```typescript
const handleStyle = {
  width: 20,
  height: 20,
  background: categoryColor,
  border: "2px solid #0a0a0f",
  borderRadius: "50%",
  boxShadow: isHovered
    ? `0 0 20px ${categoryColor}, 0 0 10px ${categoryColor}80, 0 0 5px ${categoryColor}60`
    : `0 0 10px ${categoryColor}70, 0 0 4px ${categoryColor}50`,
  transition: "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
  transform: isHovered ? "scale(1.5)" : "scale(1)",
  opacity: isHovered ? 1 : 0,
  pointerEvents: (isHovered ? "auto" : "none") as React.CSSProperties["pointerEvents"],
};
```

### 位置配置
```typescript
// 左侧Handle
<Handle
  type="target"
  position={Position.Left}
  id="input"
  style={{
    ...handleStyle,
    left: -28,  // 距离素材框28px
    zIndex: 20,
    transformOrigin: "right center",  // 向外扩展
  }}
/>

// 右侧Handle
<Handle
  type="source"
  position={Position.Right}
  id="output"
  style={{
    ...handleStyle,
    right: -28,
    zIndex: 20,
    transformOrigin: "left center",
  }}
/>
```

### Hover区域扩展
```typescript
// 使用padding扩展hover检测范围
<div
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}
  style={{
    position: "relative",
    width: 280,
    padding: 40,      // 扩展40px
    margin: -40,       // 补偿布局偏移
    boxSizing: "content-box",
  }}
>
```

### 延迟隐藏
```typescript
const hideTimerRef = useRef<NodeJS.Timeout | null>(null);

const handleMouseEnter = useCallback(() => {
  if (hideTimerRef.current) {
    clearTimeout(hideTimerRef.current);
    hideTimerRef.current = null;
  }
  setIsHovered(true);
}, []);

const handleMouseLeave = useCallback(() => {
  hideTimerRef.current = setTimeout(() => {
    setIsHovered(false);
  }, 10000); // 10秒后隐藏
}, []);
```

---

## 素材名称标签规范

### 位置：预览区外面左上角
```typescript
{/* 素材名称标签 - 在预览区外面 */}
<div
  style={{
    display: "flex",
    alignItems: "center",
    gap: 4,
    padding: "4px 8px 4px 4px",
    marginBottom: 4,
  }}
>
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.6)" strokeWidth="2">
    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
    <circle cx="8.5" cy="8.5" r="1.5" />
    <polyline points="21 15 16 10 5 21" />
  </svg>
  <span style={{ fontSize: 11, color: "rgba(255,255,255,0.8)", fontWeight: 500 }}>
    {d.assetName || "图素材"}
  </span>
</div>
```

### 编号逻辑：最大编号+1
```typescript
// 根据已有节点的最大编号+1生成素材名称
const type = def.type.toUpperCase();
const existingNames = nodes.map(n => (n.data as any)?.assetName || '');
let assetName = '素材';
if (type === "IMAGE") {
  const existingNumbers = existingNames
    .filter(n => n.startsWith('图素材'))
    .map(n => parseInt(n.replace('图素材', '')) || 0);
  const maxNum = existingNumbers.length > 0 ? Math.max(...existingNumbers) : 0;
  assetName = `图素材${maxNum + 1}`;
}
```

---

## @提及功能

### MentionInput组件
- 输入@弹出素材列表
- 支持键盘导航（↑↓箭头、回车选择、ESC关闭）
- 按类型显示不同图标（图片/视频）
- 没有连接素材时显示默认选项

### 使用方式
```typescript
<MentionInput
  value={prompt}
  onChange={setPrompt}
  mentions={[
    ...upstream.images.map(img => ({ id: img.assetName, name: img.assetName, type: 'image' })),
    ...upstream.videos.map(vid => ({ id: vid.assetName, name: vid.assetName, type: 'video' })),
  ]}
  placeholder="输入@引用素材"
/>
```

---

## 节点选中规范

### 点击预览区也要选中节点
```typescript
// 移除stopPropagation，让事件冒泡到ReactFlow
<div
  onClick={() => setShowControls(true)}  // 只设置状态，不阻止冒泡
  style={{...}}
>
```

### Delete键优化
```typescript
// 即使焦点在输入框上，如果输入框为空也可以删除节点
if ((e.key === "Delete" || e.key === "Backspace") && selectedNodeId) {
  if (isInputFocused) {
    const inputValue = (target as HTMLInputElement | HTMLTextAreaElement).value;
    if (inputValue && inputValue.length > 0) {
      return; // 输入框有内容，不删除节点
    }
  }
  e.preventDefault();
  removeNode(selectedNodeId);
}
```

---

## 常见陷阱

### ❌ 不要修改工作逻辑代码
- generate.py 中的API调用逻辑不要动
- 视频/图片处理流程不要改
- 只修改UI/前端代码

### ❌ 不要用read_file+write_file替换颜色
- 会损坏文件（带入行号）
- 必须用patch工具

### ❌ 不要在VideoPreview添加onClick阻止冒泡
- 会导致ReactFlow无法选中节点
- 属性面板不显示

### ✅ 正确的做法
- 点击预览区：只设置状态（如setShowControls）
- 不要调用e.stopPropagation()
- 让事件自然冒泡到ReactFlow
