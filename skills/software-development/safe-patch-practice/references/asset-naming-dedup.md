# 素材编号去重修复（2026-06-15）

## 问题
使用模块级变量或window全局变量做计数器，导致编号重复（所有素材都叫"素材2"）。

## 根因
1. 模块级变量在页面刷新后重置
2. window全局变量在React严格模式下可能被调用两次
3. NodePanel和CircleNavPanel各自有独立计数器

## 正确做法
根据已有节点的最大编号+1，不使用独立计数器。

```typescript
// ✅ 正确 - 根据已有节点的最大编号+1
const getAssetName = (nodeType: string): string => {
  const type = nodeType.toUpperCase();
  const existingNames = nodes.map(n => (n.data as any)?.assetName || '');
  if (type === "IMAGE") {
    const existingNumbers = existingNames
      .filter(n => n.startsWith('图素材'))
      .map(n => parseInt(n.replace('图素材', '')) || 0);
    const maxNum = existingNumbers.length > 0 ? Math.max(...existingNumbers) : 0;
    return `图素材${maxNum + 1}`;
  } else if (type === "VIDEO") {
    const existingNumbers = existingNames
      .filter(n => n.startsWith('视频素材'))
      .map(n => parseInt(n.replace('视频素材', '')) || 0);
    const maxNum = existingNumbers.length > 0 ? Math.max(...existingNumbers) : 0;
    return `视频素材${maxNum + 1}`;
  }
  return "素材";
};
```

## 关键点
- `getAssetName` 函数必须在 `handleAddNode` 回调内部定义（可以访问 `nodes`）
- 不要在组件外部定义（无法访问最新的 nodes 状态）
- NodePanel 和 CircleNavPanel 都要用相同的逻辑

## 错误案例

### 错误1：模块级变量
```typescript
// ❌ 错误 - 页面刷新后重置
let imageCounter = 0;
function getAssetName(nodeType: string): string {
  if (type === "IMAGE") {
    imageCounter++;
    return `图素材${imageCounter}`;
  }
}
```

### 错误2：window全局变量
```typescript
// ❌ 错误 - React严格模式下可能被调用两次
const getGlobalCounter = (type: string) => {
  if (typeof window !== 'undefined') {
    const key = `__assetCounter_${type}`;
    (window as any)[key] = ((window as any)[key] || 0) + 1;
    return (window as any)[key];
  }
  return 1;
};
```

### 错误3：简单计数+1
```typescript
// ❌ 错误 - 删除节点后会导致编号重复
const count = existingNames.filter(n => n.startsWith('图素材')).length + 1;
return `图素材${count}`;
```
