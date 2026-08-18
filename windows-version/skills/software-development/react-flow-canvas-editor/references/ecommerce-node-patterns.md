# E-commerce Workflow Node Patterns (Antoken)

## Correct Port Type Assignments

Learned through multiple rounds of user correction. The key insight: **distinguish between AI generation nodes (text→media) and material import nodes (file→media) and composition nodes (media+media→media)**.

### Input Nodes (No inputs, one output)
| Node | Type ID | Output | Chinese Label | Purpose |
|------|---------|--------|---------------|---------|
| SKU导入 | `skuImport` | TEXT | 数据 | Text data from CSV/Excel |
| 图片导入 | `imgImport` | IMAGE | 图片 | Local image file |
| 视频导入 | `videoImport` | VIDEO | 视频 | Local video file |

**CRITICAL**: SKU导入 outputs TEXT (not DATA), because it feeds into prompt fields.

### AI Generation Nodes (TEXT input → media output)
| Node | Type ID | Input | Output | Chinese Label |
|------|---------|-------|--------|---------------|
| 图片生成 | `imageGen` | TEXT (Prompt) | IMAGE | Output |
| 文生视频 | `videoGen` | TEXT (Prompt) | VIDEO | Output |

### Material Composition Nodes (media input → media output)
| Node | Type ID | Inputs | Output | Chinese Label |
|------|---------|--------|--------|---------------|
| 图生视频 | `img2video` | IMAGE | VIDEO | 视频 |
| 视频合成 | `videoComposite` | IMAGE + VIDEO | VIDEO | 合成视频 |
| 图片处理 | `imageProcess` | IMAGE | IMAGE | Output |
| 尺寸适配 | `sizeAdapter` | IMAGE | IMAGE | Output |

### Output Nodes (media inputs, no outputs)
| Node | Type ID | Inputs | Chinese Labels |
|------|---------|--------|----------------|
| 导出 | `export` | IMAGE + VIDEO | 图片, 视频 |

**CRITICAL**: 导出 must accept BOTH IMAGE and VIDEO inputs. Don't make separate export nodes for each type.

## TYPE_COMPAT Validation Rules

```typescript
const TYPE_COMPAT: Record<PortType, PortType[]> = {
  IMAGE: ["IMAGE"],           // IMAGE → IMAGE only
  VIDEO: ["VIDEO", "IMAGE"],  // VIDEO → VIDEO or IMAGE (video can export as image frame)
  TEXT: ["TEXT"],              // TEXT → TEXT only
  DATA: ["DATA", "TEXT"],     // DATA → DATA or TEXT (legacy, prefer TEXT)
};
```

## Common Workflow Patterns

### Pattern 1: 文生图 (Text-to-Image)
```
SKU导入(TEXT) → 图片生成(IMAGE) → 图片处理(IMAGE) → 尺寸适配(IMAGE) → 导出
```

### Pattern 2: 图生视频 (Image-to-Video)
```
图片生成(IMAGE) → 图生视频(VIDEO) → 导出
```

### Pattern 3: 图片+视频合成 (Material Composition) ← User's primary use case
```
图片导入(IMAGE) ─┐
                 ├→ 视频合成(VIDEO) → 导出
视频导入(VIDEO) ─┘
```

### Pattern 4: Full Pipeline
```
SKU导入(TEXT) → 图片生成(IMAGE) → 图生视频(VIDEO) → 导出
                                    ↑
视频导入(VIDEO) ────────────────────┘
```

## Node Component Template

Every node component must:
1. Import and wrap `BaseNode` with children
2. Read from `useSettingsStore` for model info
3. Use inline styles (not CSS vars) for colors
4. Use compact sizing (9px font for details)

```tsx
"use client";
import React from "react";
import BaseNode from "./BaseNode";
import type { NodeProps } from "@xyflow/react";
import type { NodeData } from "@/types/workflow";

export default function XxxNode(props: NodeProps) {
  const d = props.data as unknown as NodeData;
  const cfg = d.config as { ... };

  return (
    <BaseNode {...props}>
      <div style={{ fontSize: 9, color: "#62666d", padding: "0 8px 4px 10px" }}>
        {/* Compact details here */}
      </div>
    </BaseNode>
  );
}
```

## Node Registration (index.ts)

```typescript
import type { NodeTypes } from "@xyflow/react";
import BaseNode from "./BaseNode";
// ... import all nodes ...

export const nodeTypes: NodeTypes = {
  baseNode: BaseNode,
  skuImport: SKUImportNode,
  imgImport: ImgImportNode,
  videoImport: VideoImportNode,
  imageGen: ImageGenNode,
  videoGen: VideoGenNode,
  img2video: Img2VideoNode,
  videoComposite: VideoCompositeNode,
  imageProcess: ImageProcessNode,
  sizeAdapter: SizeAdapterNode,
  export: ExportNode,
};
```

## Pitfalls

1. **Don't use DATA type for text outputs** — Use TEXT. DATA is confusing and breaks validation.
2. **Don't create separate export nodes per media type** — One export node with multiple inputs.
3. **Don't auto-load localStorage** — User expects clean canvas on first visit.
4. **Don't use h-screen** — Use min-h-[100dvh].
5. **Don't use CSS vars in inline styles** — Use literal color values.
