# React Flow v12 TypeScript Pitfalls

Collected from Antoken project bootstrap (2026-06-07). All errors hit during `npx next build`.

## 1. NodeData must extend Record<string, unknown>

**Error:** Type 'NodeData' does not satisfy the constraint 'Record<string, unknown>'.

```typescript
// ✅ Correct
export interface NodeData extends Record<string, unknown> {
  label: string;
}
```

## 2. Void return functions can't chain with ||

```typescript
// ❌ Wrong
onChange={(v) => update("width", v.width) || update("height", v.height)}
// ✅ Correct
onChange={(v) => { update("width", v.width); update("height", v.height); }}
```

## 3. Unknown types can't render in JSX

```typescript
// ❌ Wrong
{cfg.fileName && <p>{cfg.fileName}</p>}
// ✅ Correct
{cfg.fileName ? <p>{String(cfg.fileName)}</p> : null}
```

## 4. nodeTypes at module level (not inside component)

## 5. useReactFlow() inside ReactFlowProvider

## 6. Handle visibility (CRITICAL)
- Minimum 12px with dark border `rgba(0,0,0,0.4)`
- Position half-outside node: `left: -6`
- Hover: 16px + glow

## 7. Edge visibility (CRITICAL)
- Use brand color `#5e6ad2`, NOT `rgba(255,255,255,0.1)`
- strokeWidth: 2 minimum

## 8. CSS variables in inline styles may not resolve
- Use literal color values: `stroke: "#7170ff"` not `stroke: "var(--accent)"`

## 9. BaseNode MUST accept and render {children}

## 10. Connection validation: warn but don't block

## 11. HTMLElement cast for event handlers
```typescript
const el = e.currentTarget as HTMLElement;
el.style.color = "red";
```

## 12. Click-to-add from sidebar (UX requirement)
Users expect clicking to add, not just drag. Add onClick alongside onDragStart.

## 13. Edge animated performance — use conditional animation for 100+ edges

## 14. Duplicate CSS imports — keep styles in one file only
