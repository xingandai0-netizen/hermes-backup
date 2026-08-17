# Node Data Field Location Pitfall

## Problem
Nodes store generated results at different locations depending on the component:
- `node.data.assetType` (top level of data)
- `node.data.assetUrl` (top level of data)
- `node.data.config.assetUrl` (inside config)

When downstream nodes read upstream data, they must check BOTH locations.

## Root Cause
The `updateNodeData` call in VideoNode/ImageNode/CompositeNode stores fields at the TOP level:
```typescript
updateNodeData(props.id, {
  status: "success",
  assetType: "VIDEO",    // ← at node.data level
  assetUrl: url,          // ← at node.data level
  config: { ...cfg, assetUrl: url }  // ← ALSO in config
});
```

But some nodes read from `node.data.config` only, missing the top-level fields.

## Fix Pattern
When reading upstream node data, always check both locations:
```typescript
const sourceData = sourceNode.data as unknown as NodeData;
const sourceConfig = sourceData?.config as Record<string, unknown> | undefined;

// Read URL from both locations
const url = (sourceConfig?.assetUrl || sourceConfig?.resultUrl || sourceData?.assetUrl) as string | undefined;

// Read assetType from both locations
const assetType = sourceData?.assetType || sourceConfig?.assetType;
```

## Verified Storage Locations

| Node | Field | Location |
|------|-------|----------|
| VideoNode | assetType | node.data.assetType |
| VideoNode | assetUrl | node.data.assetUrl AND node.data.config.assetUrl |
| ImageNode | assetType | node.data.assetType |
| ImageNode | assetUrl | node.data.assetUrl AND node.data.config.assetUrl |
| CompositeNode | assetType | node.data.assetType |
| CompositeNode | assetUrl | node.data.assetUrl AND node.data.config.assetUrl |

## Critical Rule
**ALWAYS read from `node.data` first, then fall back to `node.data.config`.** This prevents silent failures where downstream nodes can't see upstream results.
