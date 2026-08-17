# Connection Validation User Preference

## User Decision (2026-06-14)
阿戴明确要求：**移除所有连接类型限制，允许任意节点之间连接（和TapNow一致）**

## Implementation
```typescript
onConnect: (connection) => {
  // 只禁止自连接，允许所有其他连接（和TapNow一样）
  if (connection.source === connection.target) return;
  
  // 不做任何类型检查，直接创建连接
  get().saveSnapshot();
  set((s) => {
    const updated = addEdge({
      ...connection,
      animated: true,
      style: { stroke: "#ffffff", strokeWidth: 2 },
      type: "smoothstep",
    }, s.edges);
    return { edges: updated };
  });
},
```

## Rationale
- TapNow allows all connections without type restrictions
- Users may have creative workflow combinations not anticipated by type system
- Type validation at connection time is too restrictive
- Better to validate at execution time if needed

## DO NOT
- Add `isValidConnection` check in `onConnect`
- Block connections based on `assetType` or `nodeType`
- Show warnings for "type mismatches"

## DO
- Allow all connections (except self-connection)
- Let execution handle type compatibility if needed
- Keep the connection experience fluid like TapNow
