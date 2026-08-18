# Node Naming Deduplication - Session 2026-06-15

## Problem
Multiple approaches to node naming were tried and failed:

### Attempt 1: Module-level variables
```typescript
let imageCounter = 0;
let videoCounter = 0;
```
**Failed:** Variables reset on page refresh, causing all nodes to get "素材1".

### Attempt 2: Window global variables
```typescript
const getGlobalCounter = (type: string) => {
  if (typeof window !== 'undefined') {
    const key = `__assetCounter_${type}`;
    (window as any)[key] = ((window as any)[key] || 0) + 1;
    return (window as any)[key];
  }
  return 1;
};
```
**Failed:** React strict mode may call twice, causing duplicates.

### Attempt 3: Count existing nodes
```typescript
const existingNames = nodes.map(n => (n.data as any)?.assetName || '');
const count = existingNames.filter(n => n.startsWith('图素材')).length + 1;
return `图素材${count}`;
```
**Failed:** After deletion, count doesn't match expected next number.

### Attempt 4: Find max number + 1
```typescript
const existingNumbers = existingNames
  .filter(n => n.startsWith('图素材'))
  .map(n => parseInt(n.replace('图素材', '')) || 0);
const maxNum = existingNumbers.length > 0 ? Math.max(...existingNumbers) : 0;
assetName = `图素材${maxNum + 1}`;
```
**Failed:** Same issue - after deletion, numbers don't increment correctly.

### Attempt 5: localStorage persistent counter (WORKING)
```typescript
function getNextAssetNumber(type: 'IMAGE' | 'VIDEO'): number {
  const key = `antoken_asset_counter_${type}`;
  const current = parseInt(localStorage.getItem(key) || '0', 10);
  const next = current + 1;
  localStorage.setItem(key, next.toString());
  return next;
}
```
**Working:** Persists across page refreshes and deletions.

## Key Lessons
1. **Don't use module-level variables** - reset on refresh
2. **Don't count existing nodes** - fails after deletion
3. **Don't use window globals** - fragile with React strict mode
4. **Use localStorage** - persistent and reliable

## Asset Name Storage
Store in `node.data.assetName`, NOT in `node.data.config.assetName`.

```typescript
// Create node
data: { label, category, nodeType, config: {...}, assetName } as NodeData

// Read node
const d = props.data as unknown as NodeData;
d.assetName  // ✅ Correct
cfg.assetName  // ❌ Wrong - cfg is config, not data
```
