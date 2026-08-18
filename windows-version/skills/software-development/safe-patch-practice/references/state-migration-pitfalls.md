# State Migration Pitfalls (2026-07-03)

## 双状态管理冲突

**场景**：从 Zustand 迁移到 Jotai，但保留了兼容层。

**问题**：
- PersistentCanvas 用 Jotai (nodesAtom)
- v1 组件用 Zustand (useWorkflowStore)
- 两边状态不同步 → 节点不显示、生成结果不更新

**正确做法**：一次性迁移，不留兼容层。

## v1→v2 字段缺失

**场景**：复制 v1 代码到 v2，但创建节点时缺少字段。

**问题**：
- v1 创建节点时设置 `assetType: 'IMAGE'`
- v2 只设置了 `nodeType: 'IMAGE'`
- `getUpstreamMentions` 检查 `assetType` → 找不到上游节点

**正确做法**：对比 v1 和 v2 数据结构，确保所有字段都设置。

## 代理端点缺失

**场景**：前端使用 `proxyUrl()` 获取图片，但后端没有代理端点。

**问题**：
- 前端调用 `/api/generate/proxy?url=xxx`
- 后端返回 404 → 图片不显示

**正确做法**：检查所有前端 API 调用，确保后端有对应端点。

## 内存泄漏 - 定时器未清理

**场景**：组件卸载后定时器继续运行。

**正确做法**：
```tsx
const timerRef = useRef<NodeJS.Timeout | null>(null);

useEffect(() => {
  return () => {
    if (timerRef.current) clearInterval(timerRef.current);
  };
}, []);

// 启动新定时器前清除旧的
if (timerRef.current) clearInterval(timerRef.current);
timerRef.current = setInterval(() => { ... }, 3000);
```

# Performance Pitfalls (2026-07-03)

## 全局状态订阅导致重渲染

**场景**：节点组件订阅全局 `nodesAtom`，任何节点变化都触发所有节点重渲染。

**正确做法**：使用 `useMemo` 缓存计算，或使用 `atomFamily` 为每个节点创建派生原子。

## viewportAtom 频繁更新

**场景**：侧边栏订阅 `viewportAtom`，画布每次平移都触发侧边栏重渲染。

**正确做法**：不直接订阅，只在函数中通过 `store.get()` 读取最新值。
