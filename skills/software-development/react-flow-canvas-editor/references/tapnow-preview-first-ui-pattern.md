# TapNow "Preview First" UI Pattern

## Core Design Philosophy

Nodes show ONLY the preview content by default. All controls appear in a floating panel on click.

## Node Structure (No Header)

```tsx
// BaseNode - minimal, no header
function BaseNodeComponent({ data, selected, children }: BaseNodeProps) {
  const d = data as unknown as NodeData;
  const categoryColor = CATEGORY_COLORS[d.category] ?? "#5e6ad2";
  const [isHovered, setIsHovered] = useState(false);

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
          : isHovered ? "0 8px 24px rgba(0,0,0,0.4)" : "0 2px 8px rgba(0,0,0,0.3)",
        transition: "all 0.2s ease",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {children}
      <Handle type="target" position={Position.Left} id="input" style={handleStyle} />
      <Handle type="source" position={Position.Right} id="output" style={handleStyle} />
    </div>
  );
}
```

**Key changes from traditional BaseNode:**
- NO header section (no node type label, no title)
- NO status dot in header
- NO progress bar at bottom
- Children fill the entire node area
- Smaller border radius (20px vs 28px)
- Subtler shadows

## Preview-Only Node Component

```tsx
export default function VideoNode(props: NodeProps) {
  const [showControls, setShowControls] = useState(false);
  // ... other state

  return (
    <BaseNode {...props}>
      <div style={{ position: "relative" }}>
        {/* Preview - fills entire node */}
        <div
          onClick={() => setShowControls(!showControls)}
          style={{
            cursor: "pointer",
            background: "#1a1a1a",
            transition: "all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
            position: "relative",
          }}
        >
          {previewUrl ? (
            <video
              src={proxyUrl(previewUrl)}
              style={{ width: "100%", height: 220, objectFit: "cover", display: "block" }}
              muted playsInline
            />
          ) : (
            <div style={{ height: 220, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 12 }}>
              {/* Placeholder icon */}
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">...</svg>
              <p style={{ fontSize: 13, color: "#62666d", margin: 0 }}>拖拽视频到这里，或点击上传</p>
            </div>
          )}

          {/* Loading indicator at bottom of preview */}
          {loading && (
            <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: 3, background: "rgba(255,255,255,0.04)" }}>
              <div style={{ width: `${progress}%`, height: "100%", background: "linear-gradient(90deg, #5e6ad2, #7c7cf8)", transition: "width 0.3s ease" }} />
            </div>
          )}
        </div>

        {/* Hidden file input */}
        <input ref={fileInputRef} type="file" accept="video/*" style={{ display: "none" }} />
      </div>

      {/* Floating control panel - OUTSIDE the node div */}
      {showControls && (
        <div style={{
          position: "absolute",
          top: 0,
          left: "100%",
          marginLeft: 12,
          width: 260,
          background: "#191a1b",
          border: "1px solid rgba(255,255,255,0.1)",
          borderRadius: 16,
          padding: 14,
          boxShadow: "0 8px 32px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.05)",
          zIndex: 100,
          animation: "fadeIn 0.15s ease",
        }}>
          {/* Controls here */}
        </div>
      )}
    </BaseNode>
  );
}
```

## Floating Panel Specs

| Property | Value |
|----------|-------|
| Position | `absolute`, `top: 0`, `left: "100%"`, `marginLeft: 12` |
| Width | 260px |
| Background | `#191a1b` |
| Border | `1px solid rgba(255,255,255,0.1)` |
| Border Radius | 16px |
| Padding | 14px |
| Box Shadow | `0 8px 32px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.05)` |
| Z-Index | 100 |
| Animation | `fadeIn 0.15s ease` |

## Control Panel Layout

```tsx
{/* Prompt input */}
<textarea style={{
  width: "100%", height: 40, padding: "8px 10px", fontSize: 12,
  color: "#d0d6e0", background: "rgba(255,255,255,0.04)",
  border: "1px solid rgba(255,255,255,0.08)", borderRadius: 8,
  marginBottom: 10,
}} />

{/* Parameters row */}
<div style={{ display: "flex", gap: 6, marginBottom: 10 }}>
  <select style={{ flex: 1, padding: "6px 8px", fontSize: 11, color: "#8a8f98", background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: 6 }} />
  <select style={{ width: 70, ... }} />
</div>

{/* Generate button */}
<button style={{
  width: "100%", padding: "8px 0", fontSize: 13, fontWeight: 600,
  color: "#000", background: "#fff", border: "none", borderRadius: 8,
}} />
```

## Hiding Node Types from Sidebar

```tsx
// components/sidebar/NodePanel.tsx
const categories: NodeCategory[] = ["INPUT", "GENERATION"]; // Remove "COMPOSITE"

// Filter out specific types
{NODE_DEFINITIONS.filter(d => d.type !== "COMPOSITE").map((def) => ...)}
```

## Pitfalls

1. **Floating panel must be OUTSIDE the node content div** - otherwise it clips with `overflow: hidden`
2. **Use `position: absolute` on the floating panel** - not fixed, not relative
3. **`left: "100%"` positions it to the right of the node** - adjust for left-side panels if needed
4. **`zIndex: 100` ensures it appears above other nodes**
5. **`onClick={(e) => e.stopPropagation()}` on the panel** - prevents closing when clicking inside
