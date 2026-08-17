# React Flow Performance Optimizations (2026-06-14)

## ReactFlow Performance Props

```tsx
<ReactFlow
  onlyRenderVisibleElements={true}  // 关键：只渲染可见节点
  animated={false}                   // 禁用边动画减少重绘
  minZoom={0.2}
  maxZoom={3}
  elevateNodesOnSelect={false}       // 禁用选中提升
  deleteKeyCode={null}               // 禁用删除键
/>
```

## Node Memo (必须)

所有节点组件必须使用 `React.memo` 包装：
```tsx
const VideoNode = React.memo(function VideoNode(props: NodeProps) {
  // ... component code
});
export default VideoNode;
```

## Edge Animation

- `animated: true` 会导致大量边时性能问题
- 只在运行中的节点边启用动画
- 默认 `animated: false`

## AssetType存储位置Bug

**问题：** 节点存储assetType在 `node.data.assetType`，但读取时从 `node.data.config.assetType` 读取。

**修复：** 优先从 `node.data.assetType` 读取：
```typescript
const assetType = sourceData?.assetType || sourceConfig?.assetType;
```

## Video Proxy CORS Pattern

外部媒体URL需要通过代理绕过CORS：
```typescript
import { proxyUrl } from "@/lib/mediaProxy";

// 使用
<video src={proxyUrl(previewUrl)} crossOrigin="anonymous" />
<img src={proxyUrl(previewUrl)} />
```

## DAG Execution Engine

实现了并发执行引擎：
- `backend/app/services/dag_engine.py` - DAG拓扑排序+并发执行
- `backend/app/api/workflow.py` - 工作流执行API
- `frontend/src/hooks/useWorkflowExecution.ts` - 前端Hook

## WebSocket Progress

后端WebSocket端点用于实时进度推送：
- `backend/app/api/ws.py` - `/ws/workflow/{workflow_id}`
- 替代轮询模式，毫秒级更新
