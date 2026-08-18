# cfg 闭包问题模式

## 问题描述

`useCallback` 依赖数组包含 `cfg`，但函数体未使用 `cfg`，导致：
1. 不必要的重渲染（cfg 变化时函数重新创建）
2. 潜在的 stale closure 问题

## 错误模式

```tsx
const cfg = d.config as { model?: string; size?: string; assetUrl?: string };

const updateResult = useCallback((url: string, assetId: string) => {
  setPreviewUrl(url);
  updateNodeData(props.id, {
    status: "success",
    assetUrl: url,
    assetId,
  });
}, [props.id, cfg, updateNodeData]); // ❌ cfg 未使用但依赖
```

## 正确模式

```tsx
const updateResult = useCallback((url: string, assetId: string) => {
  setPreviewUrl(url);
  updateNodeData(props.id, {
    status: "success",
    assetUrl: url,
    assetId,
  });
}, [props.id, updateNodeData]); // ✅ 移除 cfg
```

## 检查方法

1. 搜索所有 `useCallback` 调用
2. 检查依赖数组中的每个变量是否在函数体中使用
3. 移除未使用的依赖

## DeepSeek 审查发现（2026-07-04）

DeepSeek 审查发现 image-node.tsx、video-node.tsx、composite-node.tsx 都有此问题。

**修复**：从所有 `updateResult` 的依赖数组中移除 `cfg`。
