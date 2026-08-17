# React Flow "Preview First" Node UI Pattern

## Overview
A UI pattern where nodes only show content preview (image/video) by default, and a floating dialog appears below on click. Based on TapNow's design.

## When to Use
- AI generation platforms with media preview
- When node content is the primary visual element
- When controls should be hidden until needed
- When you want clean, minimal canvas appearance

## Architecture

```
┌──────────────────────┐
│                      │  ← Node (BaseNode without Header)
│   [Preview Content]  │  ← Full bleed preview
│                      │
└──────────────────────┘
          │
          ▼ (on click)
┌──────────────────────┐
│ [★] [+]     [⤢]     │  ← Floating Dialog (absolute positioned)
│                      │
│  Input Area          │
│                      │
│ [Model] [Size] [↑]  │
└──────────────────────┘
```

## Implementation

### 1. BaseNode Simplification
Remove Header (label + title), keep only content area + handles:

```tsx
function BaseNodeComponent({ data, selected, children }: BaseNodeProps) {
  const d = data as unknown as NodeData;
  const categoryColor = CATEGORY_COLORS[d.category] ?? "#5e6ad2";
  const [isHovered, setIsHovered] = useState(false);

  const handleStyle = {
    width: 14,
    height: 14,
    background: categoryColor,
    border: "2px solid #0a0a0f",
    borderRadius: "50%",
    boxShadow: isHovered
      ? `0 0 12px ${categoryColor}, 0 0 4px ${categoryColor}60`
      : `0 0 6px ${categoryColor}50`,
    transition: "all 0.2s ease",
  };

  return (
    <div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        width: 280,
        background: "#0a0a0f",
        border: selected ? `2px solid ${categoryColor}` : "1px solid rgba(255,255,255,0.08)",
        borderRadius: 20,
        boxShadow: selected
          ? `0 0 0 3px ${categoryColor}40, 0 12px 32px rgba(0,0,0,0.6)`
          : isHovered
          ? "0 8px 24px rgba(0,0,0,0.4)"
          : "0 2px 8px rgba(0,0,0,0.3)",
        transition: "all 0.2s ease",
        position: "relative",
        // NO overflow: "hidden" - would clip floating dialog
      }}
    >
      {/* Content area - pure preview */}
      {children}

      {/* Handles */}
      <Handle type="target" position={Position.Left} id="input" style={{...handleStyle, left: -7}} />
      <Handle type="source" position={Position.Right} id="output" style={{...handleStyle, right: -7}} />
    </div>
  );
}
```

### 2. Node Component with Floating Dialog

```tsx
export default function VideoNode(props: NodeProps) {
  const [showControls, setShowControls] = useState(false);
  // ... other state

  return (
    <BaseNode {...props}>
      <div style={{ position: "relative" }}>
        {/* Preview Box - click to show dialog */}
        <div
          onClick={(e) => {
            e.stopPropagation();  // Prevent React Flow drag
            e.preventDefault();   // Prevent default behavior
            setShowControls(!showControls);
          }}
          style={{
            cursor: "pointer",
            background: "#1a1a1a",
            transition: "all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
            position: "relative",
          }}
        >
          {previewUrl ? (
            <video src={proxyUrl(previewUrl)} style={{ width: "100%", height: 220, objectFit: "cover", display: "block" }} muted playsInline />
          ) : (
            <div style={{ height: 220, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 12 }}>
              {/* Upload icon */}
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <rect x="6" y="10" width="36" height="28" rx="4" stroke="rgba(255,255,255,0.3)" strokeWidth="2"/>
                <path d="M20 18L32 24L20 30V18Z" fill="rgba(255,255,255,0.3)"/>
              </svg>
              <p style={{ fontSize: 13, color: "#62666d", margin: 0 }}>拖拽视频到这里，或点击上传</p>
            </div>
          )}

          {/* Progress indicator at bottom */}
          {loading && (
            <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: 3 }}>
              <div style={{ width: `${progress}%`, height: "100%", background: "linear-gradient(90deg, #5e6ad2, #7c7cf8)", transition: "width 0.3s ease" }} />
            </div>
          )}
        </div>

        {/* Error message */}
        {error && <div style={{ padding: "6px 14px", background: "#0a0a0f" }}><p style={{ fontSize: 11, color: "#ef4444", margin: 0 }}>{error}</p></div>}
      </div>

      {/* Floating Dialog - below node */}
      {showControls && (
        <div style={{
          position: "absolute",
          top: "100%",
          left: 0,
          right: 0,
          marginTop: 8,
          background: "rgba(51,51,51,0.95)",
          border: "1px solid rgba(255,255,255,0.08)",
          borderRadius: 16,
          padding: 0,
          boxShadow: "0 4px 8px rgba(0,0,0,0.3), 0 0 0 1px rgba(255,255,255,0.05)",
          zIndex: 100,
          animation: "fadeIn 0.2s ease",
          backdropFilter: "blur(20px)",
          // NO overflow: "hidden"
          // NO onClick: stopPropagation on container
        }}>
          {/* Top toolbar */}
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "8px 12px", borderBottom: "1px solid rgba(255,255,255,0.06)" }}>
            <div style={{ display: "flex", gap: 4 }}>
              <button style={{ width: 28, height: 28, display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(255,255,255,0.06)", border: "none", borderRadius: 6, cursor: "pointer", color: "#8a8f98" }}>
                {/* Star icon */}
              </button>
              <button style={{ width: 28, height: 28, display: "flex", alignItems: "center", justifyContent: "center", background: "rgba(255,255,255,0.06)", border: "none", borderRadius: 6, cursor: "pointer", color: "#8a8f98" }}>
                {/* Plus icon */}
              </button>
            </div>
            <button style={{ width: 28, height: 28, display: "flex", alignItems: "center", justifyContent: "center", background: "transparent", border: "none", cursor: "pointer", color: "#8a8f98" }}>
              {/* Fullscreen icon */}
            </button>
          </div>

          {/* Input area */}
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="描述任何你想要生成的内容"
            style={{
              width: "100%",
              height: 60,
              padding: "12px 16px",
              fontSize: 16,
              lineHeight: 1.5,
              color: "#fff",
              background: "transparent",
              border: "none",
              outline: "none",
              resize: "none",
              boxSizing: "border-box",
            }}
          />

          {/* Bottom toolbar */}
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "8px 12px", borderTop: "1px solid rgba(255,255,255,0.06)" }}>
            {/* Left: Model/size selectors - KEEP AS SELECT, NOT TEXT */}
            <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <select value={model} onChange={(e) => setModel(e.target.value)} style={{ padding: "4px 8px", fontSize: 12, color: "#fff", background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 6, outline: "none" }}>
                {MODELS.map((m) => <option key={m} value={m}>{m}</option>)}
              </select>
              <select value={size} onChange={(e) => setSize(e.target.value)} style={{ padding: "4px 6px", fontSize: 12, color: "#fff", background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 6, outline: "none" }}>
                {SIZES.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
              </select>
            </div>

            {/* Right: Mic + Send button */}
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <button style={{ width: 28, height: 28, display: "flex", alignItems: "center", justifyContent: "center", background: "transparent", border: "none", cursor: "pointer", color: "#8a8f98" }}>
                {/* Mic icon */}
              </button>
              <button
                onClick={() => handleGenerate()}
                disabled={loading || !prompt.trim()}
                style={{
                  width: 32,
                  height: 32,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  background: loading ? "rgba(255,255,255,0.3)" : "rgba(255,255,255,0.15)",
                  border: "none",
                  borderRadius: "50%",
                  cursor: loading ? "not-allowed" : "pointer",
                }}
              >
                {/* Arrow up icon */}
              </button>
            </div>
          </div>
        </div>
      )}
    </BaseNode>
  );
}
```

## Critical Pitfalls

### 1. overflow: hidden on BaseNode
**WRONG:** Adding `overflow: "hidden"` to BaseNode clips the floating dialog.
**FIX:** Do NOT add overflow hidden to the node container.

### 2. stopPropagation on Dialog Container
**WRONG:** Adding `onClick={(e) => e.stopPropagation()}` to the dialog container breaks ALL child buttons/selects.
**FIX:** Only add stopPropagation to specific child elements that need it.

### 3. Click vs Drag Conflict
**WRONG:** Simple `onClick={() => toggle()}` on preview box causes drag behavior.
**FIX:** Add both `e.stopPropagation()` and `e.preventDefault()` in the click handler.

### 4. Replacing Selects with Text
**WRONG:** Replacing `<select>` with `<span>` to simplify UI.
**FIX:** Keep all interactive controls functional.

## Design Tokens (from TapNow analysis)

| Token | Value | Usage |
|-------|-------|-------|
| Dialog BG | `rgba(51,51,51,0.95)` | Dialog background |
| Dialog Border | `rgba(255,255,255,0.08)` | 1px solid |
| Dialog Radius | `16px` | Border radius |
| Dialog Shadow | `0 4px 8px rgba(0,0,0,0.3)` | Box shadow |
| Input Font | `16px`, `line-height: 1.5` | Textarea |
| Button BG | `rgba(255,255,255,0.06)` | Toolbar buttons |
| Button Radius | `6px` | Button border radius |
| Send Button | `32px`, `50%` radius, `rgba(255,255,255,0.15)` | Circular send |

## Version History
- v1.0 (2026-06-15): Initial implementation based on TapNow analysis
