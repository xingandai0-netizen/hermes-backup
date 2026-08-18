# Asset Naming System - Best Practices (2026-06-15)

## Counter Strategy: Count Existing Nodes (Recommended)

Use the existing node count to determine the next asset number. This handles node deletion correctly and doesn't require cross-component synchronization.

```typescript
// In component, depends on nodes array
const getAssetName = (nodeType: string): string => {
  const type = nodeType.toUpperCase();
  const existingNames = nodes.map(n => (n.data as any)?.assetName || '');
  if (type === "IMAGE") {
    const count = existingNames.filter(n => n.startsWith('图素材')).length + 1;
    return `图素材${count}`;
  } else if (type === "VIDEO") {
    const count = existingNames.filter(n => n.startsWith('视频素材')).length + 1;
    return `视频素材${count}`;
  }
  return "素材";
};
```

## Old Approach: Window Global Counter (Deprecated)

```typescript
// ❌ DEPRECATED - Has multiple issues:
// 1. Deleting nodes doesn't reclaim numbers
// 2. Page refresh resets counter → duplicate names
// 3. NodePanel and CircleNavPanel maintain separate counters
const getGlobalCounter = (type: string) => {
  if (typeof window !== 'undefined') {
    const key = `__assetCounter_${type}`;
    (window as any)[key] = ((window as any)[key] || 0) + 1;
    return (window as any)[key];
  }
  return 1;
};
```

## Storage Location

`assetName` is stored at `node.data.assetName`, NOT `node.data.config.assetName`.

```typescript
// Creating node
data: { label, category, nodeType, config: {...}, assetName } as NodeData

// Reading - use d.assetName, NOT cfg.assetName
const d = props.data as unknown as NodeData;
<span>{d.assetName || "素材"}</span>  // ✅
<span>{cfg.assetName || "素材"}</span>  // ❌ undefined
```

## @Mention Default Options

When no upstream connections exist, show default mention options so @ always works:

```typescript
const defaultMentions: MentionItem[] = [
  { id: 'default-image-1', name: '图素材1', type: 'image' },
  { id: 'default-video-1', name: '视频素材1', type: 'video' },
];
const allMentions = mentions.length > 0 ? filteredMentions : defaultMentions.filter(...);
```

## Asset Name Display Position

Labels should be OUTSIDE the preview area (above it), not inside:

```tsx
<div style={{ position: "relative" }}>
  {/* Label - outside preview */}
  <div style={{ display: "flex", alignItems: "center", gap: 4, padding: "4px 8px", marginBottom: 4 }}>
    <svg ...>{/* icon */}</svg>
    <span>{d.assetName || "素材"}</span>
  </div>
  {/* Preview area */}
  <div style={{ ... }}>
    <VideoPreview ... />
  </div>
</div>
```
