# ReactFlow 安全性能优化模式 - 2026-06-14

## 核心原则

ReactFlow 组件会比较 props 引用来决定是否需要内部更新。内联对象每次渲染都创建新引用，导致不必要的更新。

**安全优化：用 `useMemo`/`useCallback` 稳定引用**

## 可优化的 ReactFlow Props

| Prop | 类型 | 优化方式 |
|------|------|----------|
| `defaultEdgeOptions` | 对象 | `useMemo(() => ({...}), [])` |
| `connectionLineStyle` | 对象 | `useMemo(() => ({...}), [])` |
| `snapGrid` | 数组 | `useMemo(() => [16, 16], [])` |
| `defaultViewport` | 对象 | `useMemo(() => ({...}), [])` |
| `proOptions` | 对象 | `useMemo(() => ({...}), [])` |
| `nodeColor` | 函数 | `useCallback((node) => ..., [])` |

## 代码模板

```tsx
import { useCallback, useMemo } from "react";

function CanvasInner() {
  // 稳定引用 - 避免每次渲染创建新对象
  const snapGridValue: [number, number] = useMemo(() => [16, 16], []);
  
  const defaultEdgeOpts = useMemo(() => ({
    animated: true,
    style: { stroke: "#ffffff", strokeWidth: 2.5, strokeOpacity: 0.8 },
    type: "smoothstep" as const,
  }), []);

  const connLineStyle = useMemo(() => ({
    stroke: "#ffffff", strokeWidth: 3, strokeDasharray: "8 4"
  }), []);

  const defaultVP = useMemo(() => ({ x: 0, y: 0, zoom: 1 }), []);
  const proOpts = useMemo(() => ({ hideAttribution: true }), []);
  const bgStyle = useMemo(() => ({ background: "#000" }), []);
  const miniMapStyle = useMemo(() => ({
    background: "#0f1011",
    border: "1px solid rgba(255,255,255,0.08)",
    borderRadius: 8,
  }), []);

  const nodeColor = useCallback((node: Node) => {
    const d = node.data as unknown as NodeData;
    const colors: Record<string, string> = {
      INPUT: "#27a644",
      AI_GENERATION: "#7170ff",
      PROCESSING: "#3b82f6",
      OUTPUT: "#f59e0b",
    };
    return colors[d.category] ?? "rgba(255,255,255,0.05)";
  }, []);

  return (
    <ReactFlow
      snapToGrid={snapEnabled}  // 默认关闭，用户手动开启
      snapGrid={snapGridValue}
      defaultEdgeOptions={defaultEdgeOpts}
      connectionLineStyle={connLineStyle}
      proOptions={proOpts}
      defaultViewport={defaultVP}
      // ... 其他 props
    >
      <Background style={bgStyle} />
      <MiniMap nodeColor={nodeColor} style={miniMapStyle} />
    </ReactFlow>
  );
}
```

## 不需要优化的元素

以下内联样式在条件渲染区域，对性能影响极小，可以跳过：
- 右键菜单样式（只在右键时渲染）
- 空状态样式（只在无节点时渲染）
- 动态计算的样式（依赖状态的）

## 吸附网格 UX 决策

**默认关闭吸附**，原因：
- 用户要求"十分顺滑感"
- 吸附会导致移动时"跳跃"，不够流畅
- 添加开关按钮让用户手动开启

```tsx
const [snapEnabled, setSnapEnabled] = useState(false);

// 在 Controls 附近添加开关按钮
<button
  onClick={() => setSnapEnabled(!snapEnabled)}
  style={{
    position: "absolute",
    bottom: 80,
    left: 12,
    // ... 样式
  }}
  title={snapEnabled ? "关闭网格吸附" : "开启网格吸附"}
>
  {/* 网格图标 SVG */}
</button>
```

## 验证清单

优化后检查：
- [ ] 所有 useMemo/useCallback 依赖数组正确（通常为 `[]`）
- [ ] 没有遗漏的内联对象（搜索 `={{` 和 `={[`）
- [ ] 工作流逻辑未受影响（onConnect, onEdgesChange 等来自 store）
- [ ] 拖拽功能正常（onDrop, onDragOver）
- [ ] 右键菜单正常
- [ ] Cmd+Shift+R 刷新后测试
