# Asset Naming System (2026-06-15)

## Auto-Naming Pattern

Each asset node gets an automatic name based on type and creation order:
- Image nodes: 图素材1, 图素材2, 图素材3...
- Video nodes: 视频素材1, 视频素材2, 视频素材3...

## Storage Location

**Critical:** `assetName` is stored in `node.data.assetName`, NOT in `node.data.config.assetName`.

```typescript
// Creating node
data: {
  label: def.label,
  category: def.category,
  nodeType: def.type,
  config: def.defaultConfig ?? {},
  assetName,  // ← in data, not in config
} as NodeData

// Reading node - use d.assetName, not cfg.assetName
const d = props.data as unknown as NodeData;
const cfg = d.config as { assetName?: string; ... };

// ❌ Wrong - cfg.assetName is undefined
<span>{cfg.assetName || "素材"}</span>

// ✅ Correct - from d.assetName
<span>{d.assetName || "素材"}</span>
```

## Numbering with localStorage Counter

**Problem:** Module-level counters reset on page refresh. Using `nodes.length` causes duplicates after deletion.

**Solution:** Use localStorage for persistent numbering:

```typescript
function getNextAssetNumber(type: 'IMAGE' | 'VIDEO'): number {
  const key = `antoken_asset_counter_${type}`;
  const current = parseInt(localStorage.getItem(key) || '0', 10);
  const next = current + 1;
  localStorage.setItem(key, next.toString());
  return next;
}
```

**Alternative (simpler but less robust):** Use max+1 from existing nodes:

```typescript
const getAssetName = (nodeType: string): string => {
  const type = nodeType.toUpperCase();
  const existingNames = nodes.map(n => (n.data as any)?.assetName || '');
  if (type === "IMAGE") {
    const existingNumbers = existingNames
      .filter(n => n.startsWith('图素材'))
      .map(n => parseInt(n.replace('图素材', '')) || 0);
    const maxNum = existingNumbers.length > 0 ? Math.max(...existingNumbers) : 0;
    return `图素材${maxNum + 1}`;
  }
  // ... same for VIDEO
};
```

## @Mention Input Component

**File:** `frontend/src/components/MentionInput.tsx`

**Usage:**
```tsx
<MentionInput
  value={prompt}
  onChange={setPrompt}
  mentions={[
    ...upstream.images.map(img => ({ 
      id: img.assetName, 
      name: img.assetName, 
      type: 'image' as const 
    })),
    ...upstream.videos.map(vid => ({ 
      id: vid.assetName, 
      name: vid.assetName, 
      type: 'video' as const 
    })),
  ]}
  placeholder="输入@引用素材，如：@图素材1中的什么替换成@视频素材1中的什么"
/>
```

**Features:**
- Input `@` to trigger menu
- Keyboard navigation (↑↓ arrows, Enter to select, ESC to close)
- Filter by typing after `@
- Default options when no connections exist

## Prompt Auto-Injection

When generating, automatically prepend asset references to prompt:

```typescript
let fullPrompt = prompt;
const refs: string[] = [];
upstream.images.forEach((img, i) => {
  refs.push(`[图片素材${i + 1}: ${img.assetName}]`);
});
upstream.videos.forEach((vid, i) => {
  refs.push(`[视频素材${i + 1}: ${vid.assetName}]`);
});
if (refs.length > 0) {
  fullPrompt = `${refs.join(' ')}\n${prompt}`;
}
```

This tells the model which asset corresponds to which reference in the prompt.

## Asset Name Label Display

Display asset name outside the preview area (top-left corner):

```tsx
<div style={{ position: "relative" }}>
  {/* Asset name label - outside preview */}
  <div style={{
    display: "flex",
    alignItems: "center",
    gap: 4,
    padding: "4px 8px 4px 4px",
    marginBottom: 4,
  }}>
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" 
         stroke="rgba(255,255,255,0.6)" strokeWidth="2">
      {/* Image or video icon */}
    </svg>
    <span style={{ fontSize: 11, color: "rgba(255,255,255,0.8)", fontWeight: 500 }}>
      {d.assetName || "素材"}
    </span>
  </div>
  
  {/* Preview area */}
  <div style={{ ... }}>
    <VideoPreview ... />
  </div>
</div>
```
