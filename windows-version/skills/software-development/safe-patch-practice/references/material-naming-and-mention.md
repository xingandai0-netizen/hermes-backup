# Material Naming Dedup & @ Mention System

## Problem: Material Naming Duplicate Numbers

### Root Cause
Using module-level `let` variables or `window` global variables as counters leads to:
1. Module-level variables reset on page refresh
2. `window` global variables may be called twice in React strict mode
3. NodePanel and CircleNavPanel each have independent counters

### Solution: localStorage Persistent Counter

```typescript
function getNextAssetNumber(type: 'IMAGE' | 'VIDEO'): number {
  const key = `antoken_asset_counter_${type}`;
  const current = parseInt(localStorage.getItem(key) || '0', 10);
  const next = current + 1;
  localStorage.setItem(key, next.toString());
  return next;
}
```

**Benefits:**
- Persists across page refreshes
- Unique across all components
- Never resets (unless manually cleared)

### Alternative: Count Existing Nodes

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

**Benefits:**
- No external state needed
- Always accurate based on current nodes

**Drawbacks:**
- If nodes are deleted, numbers may have gaps
- Requires `nodes` array to be available

## @ Mention System (MentionInput)

### Component: `frontend/src/components/MentionInput.tsx`

### Features
- Input `@` to trigger material list popup
- Keyboard navigation (↑↓ arrows, Enter to select, Esc to close)
- Shows connected materials OR default options if none connected
- Filter by typing after `@`

### Default Options (when no connections)

```typescript
const defaultMentions: MentionItem[] = [
  { id: 'default-image-1', name: '图素材1', type: 'image' },
  { id: 'default-video-1', name: '视频素材1', type: 'video' },
];
const allMentions = mentions.length > 0 ? filteredMentions : defaultMentions.filter(m =>
  m.name.toLowerCase().includes(filterText.toLowerCase())
);
```

### Usage in Nodes

```tsx
<MentionInput
  value={prompt}
  onChange={setPrompt}
  mentions={[
    ...upstream.images.map(img => ({ id: img.assetName, name: img.assetName, type: 'image' })),
    ...upstream.videos.map(vid => ({ id: vid.assetName, name: vid.assetName, type: 'video' })),
  ]}
  placeholder="输入@引用素材，如：@图素材1中的什么替换成@视频素材1中的什么"
  disabled={loading}
/>
```

### Auto-inject Material Names into Prompt

```typescript
let fullPrompt = prompt;
const refs: string[] = [];
upstream.images.forEach(img => refs.push(`[图片素材: ${img.assetName}]`));
upstream.videos.forEach(vid => refs.push(`[视频素材: ${vid.assetName}]`));
if (refs.length > 0) fullPrompt = `${refs.join(' ')}\n${prompt}`;
```

## assetName Storage Location

**CRITICAL:** `assetName` is stored in `node.data`, NOT `node.data.config`.

```typescript
// ✅ Correct - read from data
const d = props.data as unknown as NodeData;
<span>{d.assetName || "素材"}</span>

// ❌ Wrong - cfg.assetName is undefined
const cfg = d.config as { assetName?: string; ... };
<span>{cfg.assetName || "素材"}</span>
```

### cfg Type Definition Must Include assetName

```typescript
const cfg = d.config as {
  content?: string;
  model?: string;
  assetName?: string;  // Must add this field
  // ...
};
```
