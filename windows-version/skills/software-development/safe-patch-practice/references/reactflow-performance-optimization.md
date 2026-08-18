# ReactFlow 性能优化安全清单 - 2026-06-15

## 安全的优化（useMemo/useCallback）

### ReactFlow Props 引用稳定化
```tsx
// 每次渲染创建新对象 → 用useMemo稳定
const defaultEdgeOpts = useMemo(() => ({
  animated: true,
  style: { stroke: "#ffffff", strokeWidth: 2.5, strokeOpacity: 0.8 },
  type: "smoothstep" as const,
}), []);

const connLineStyle = useMemo(() => ({
  stroke: "#ffffff", strokeWidth: 3, strokeDasharray: "8 4"
}), []);

const snapGridValue: [number, number] = useMemo(() => [16, 16], []);
const proOpts = useMemo(() => ({ hideAttribution: true }), []);
const defaultVP = useMemo(() => ({ x: 0, y: 0, zoom: 1 }), []);

// 回调函数
const nodeColor = useCallback((node: Node) => {
  // ...
}, []);

// 模块级常量天然稳定，不需要useMemo
// nodeTypes 从 @/components/nodes 导入，引用不变
```

### 安全的 CSS 优化
```css
/* ✓ 安全 - 只改阴影 */
.react-flow__node:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
}
.react-flow__node.selected {
  box-shadow: 0 0 0 2px var(--accent-bright) !important;
}

/* ✓ 安全 - Handle 缩放（不影响节点定位） */
.react-flow__handle:hover {
  transform: scale(1.3) !important;  /* Handle 上的 transform 是安全的 */
}
```

## 不安全的优化（会导致页面卡死/点击失效）

### ReactFlow 行为配置
```tsx
// ❌ 页面卡死
<ReactFlow onlyRenderVisibleElements={true} />

// ❌ 点击无响应
<ReactFlow elevateNodesOnSelect={false} />

// ❌ 键盘事件异常
<ReactFlow deleteKeyCode={null} />

// ❌ 数据更新时节点不刷新
const VideoNode = React.memo(function VideoNode(props: NodeProps) { ... });
```

### CSS 覆盖
```css
/* ❌ 破坏React Flow定位系统 */
.react-flow__node {
  transform: translateY(-1px) !important;
}
.react-flow__node:hover {
  transform: scale(1.02) !important;
}
```

### BaseNode 配置
```tsx
/* ❌ 会裁剪下方悬浮面板 */
<div style={{ overflow: "hidden" }}>
  {children}
  {/* 悬浮面板用 position: absolute; top: 100% 会被裁剪 */}
</div>
```

## 网格吸附

```tsx
// 默认关闭，用户需要时手动开启
const [snapEnabled, setSnapEnabled] = useState(false);

<ReactFlow
  snapToGrid={snapEnabled}
  snapGrid={snapGridValue}
>

// 添加开关按钮（左下角Controls下方）
<button onClick={() => setSnapEnabled(!snapEnabled)}>
  网格吸附
</button>
```

## 总结

| 优化方式 | 安全？ | 说明 |
|---------|--------|------|
| useMemo 稳定 props 引用 | ✓ | 避免不必要的重渲染 |
| useCallback 稳定回调 | ✓ | 避免子组件重渲染 |
| box-shadow hover/selected | ✓ | 视觉反馈 |
| Handle transform | ✓ | 不影响节点定位 |
| onlyRenderVisibleElements | ❌ | 页面卡死 |
| elevateNodesOnSelect | ❌ | 点击无响应 |
| deleteKeyCode={null} | ❌ | 键盘异常 |
| React.memo on nodes | ❌ | 数据不刷新 |
| CSS transform on nodes | ❌ | 定位破坏 |
| overflow: hidden on BaseNode | ❌ | 悬浮面板被裁剪 |
