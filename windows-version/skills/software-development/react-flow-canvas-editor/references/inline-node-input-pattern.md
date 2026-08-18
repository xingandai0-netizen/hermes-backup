# Inline Node Input Pattern

## Problem
阿戴 complained: "素材框输入文本没有按键可以生成相应内容" — nodes displayed info but had no input fields or generate buttons. Users had to double-click to open property panel, which was unintuitive.

## Solution: Add textarea + button directly on node

AI generation nodes (ImageGen, VideoGen, Img2Video) need inline input:
- Textarea for prompt input (40px height, 9px font)
- Generate button with gradient background
- Config badges below (size, quality, duration, etc.)

### Implementation Pattern

```tsx
"use client";
import React, { useState } from "react";
import BaseNode from "./BaseNode";
import type { NodeProps } from "@xyflow/react";
import type { NodeData } from "@/types/workflow";
import { useSettingsStore } from "@/stores/settingsStore";
import { useWorkflowStore } from "@/stores/workflowStore";

export default function ImageGenNode(props: NodeProps) {
  const d = props.data as unknown as NodeData;
  const cfg = d.config as { prompt?: string; n?: number; size?: string; quality?: string };
  const { imageApi } = useSettingsStore();
  const { updateNodeData } = useWorkflowStore();
  const [prompt, setPrompt] = useState(cfg.prompt ?? "");

  const handleGenerate = () => {
    updateNodeData(props.id, {
      config: { ...cfg, prompt },
      status: "running",
    });
    // TODO: Call backend API
    console.log("Generate:", prompt, imageApi.modelName);
    // Simulate completion
    setTimeout(() => {
      updateNodeData(props.id, { status: "success", progress: 100 });
    }, 2000);
  };

  return (
    <BaseNode {...props}>
      <div style={{ padding: "0 8px 6px 10px" }}>
        {/* Prompt textarea */}
        <div style={{ marginBottom: 4 }}>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="输入图片描述..."
            style={{
              width: "100%", height: 40, fontSize: 9,
              color: "#d0d6e0",
              background: "rgba(255,255,255,0.03)",
              border: "1px solid rgba(255,255,255,0.08)",
              borderRadius: 4, padding: "4px 6px",
              resize: "none", outline: "none", fontFamily: "inherit",
            }}
            onFocus={(e) => { e.currentTarget.style.borderColor = "rgba(94,106,210,0.5)"; }}
            onBlur={(e) => { e.currentTarget.style.borderColor = "rgba(255,255,255,0.08)"; }}
          />
        </div>
        
        {/* Generate button */}
        <button
          onClick={handleGenerate}
          style={{
            width: "100%", fontSize: 9, fontWeight: 510,
            color: "#fff",
            background: "linear-gradient(135deg, #5e6ad2, #7170ff)",
            border: "none", borderRadius: 4, padding: "4px 8px",
            cursor: "pointer", transition: "all 0.15s ease",
          }}
        >
          生成图片
        </button>
        
        {/* Config badges */}
        <div style={{ display: "flex", gap: 4, marginTop: 4, flexWrap: "wrap" }}>
          <span style={{ fontSize: 7, padding: "1px 4px", borderRadius: 9999, color: "#3b82f6", background: "rgba(59,130,246,0.1)" }}>
            {cfg.size ?? "1024x1024"}
          </span>
          {/* ... more badges */}
        </div>
      </div>
    </BaseNode>
  );
}
```

### Button Color by Node Type
- Image Gen: `linear-gradient(135deg, #5e6ad2, #7170ff)` (indigo)
- Video Gen: `linear-gradient(135deg, #7170ff, #828fff)` (purple)
- Img2Video: `linear-gradient(135deg, #3b82f6, #60a5fa)` (blue)

### Placeholder Text by Node Type
- Image Gen: "输入图片描述..."
- Video Gen: "输入视频描述..."
- Img2Video: "输入视频风格描述..."

## Key Points
1. Use `useState` for local prompt state
2. Call `updateNodeData` to persist config changes
3. Set `status: "running"` on generate, `status: "success"` on complete
4. Textarea height: 40px (compact, fits in 160px wide node)
5. Font size: 9px (matches node styling)
6. Focus state: blue border highlight
7. Button hover: opacity 0.9 + scale(1.02)
