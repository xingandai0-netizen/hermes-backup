# VideoPreview Component in ReactFlow Nodes

## Architecture
- Use native `<video>` element (Plyr doesn't work in Next.js)
- Custom controls: play/pause, seek bar, time display, speed, mute, fullscreen button
- Hover-to-play: `onMouseEnter` plays from start, `onMouseLeave` pauses and resets to 0
- Colors: white (#ffffff) accent, not blue-purple (#5e6ad2)

## Event Handling Rules (CRITICAL)

### Do NOTs
- Do NOT add `onClick` on VideoPreview's outer div — it blocks ReactFlow node selection
- Do NOT use `e.preventDefault()` on click handlers — breaks ReactFlow selection
- Do NOT rely on `onDoubleClick` — ReactFlow intercepts it (even empty handler doesn't work)

### DOs
- Use `onMouseDown={(e) => e.stopPropagation()}` on control panels/buttons inside VideoPreview
- Let single-click events bubble to ReactFlow naturally (no stopPropagation on outer div)
- Use `onExpand` callback prop for fullscreen button → opens PreviewModal

### Event Flow
```
User clicks video area
  → Event bubbles to ReactFlow
  → ReactFlow selects node
  → Node's onClick fires (e.g., setShowControls(true))
  → Control panel (对话交流框) appears with popup animation
```

## UI Interaction Model (阿戴's terminology — DO NOT confuse)

| Term | What it is | How to trigger |
|------|-----------|----------------|
| "对话交流框" / "对话框" | Control panel INSIDE node (prompt input, model select, generate button) | Click video area |
| "放大预览" | PreviewModal fullscreen overlay | Click expand button in controls |
| "属性面板" | Right-side PropertyPanel | ReactFlow node selection (auto) |

## Interaction Pattern
1. **Hover** → play video from start
2. **Leave** → pause + reset to 0
3. **Click** → show control panel (对话交流框)
4. **Right-click** → upload asset (file input)
5. **Expand button** → open PreviewModal (放大预览)

## Control Panel Animation
```css
@keyframes popUp {
  from { opacity: 0; transform: translateY(8px) scale(0.96); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
/* Use: animation: popUp 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) */
```

## Color Replacement Pitfall
- Use `patch` tool for color replacement, NOT `read_file` + `write_file`
- `read_file` output includes line numbers (e.g., `1|1|1|"use client"`) which corrupt files
- Replace `#5e6ad2` → `#ffffff`, `rgba(94,106,210,x)` → `rgba(255,255,255,x)`

## Complete Component Props
```typescript
interface VideoPreviewProps {
  src: string;
  poster?: string;
  width?: number | string;
  height?: number | string;
  autoPlay?: boolean;      // default: false
  loop?: boolean;           // default: true
  muted?: boolean;          // default: true
  controls?: boolean;       // default: true
  hoverToPlay?: boolean;    // default: true
  onExpand?: () => void;    // fullscreen button callback
  className?: string;
  style?: React.CSSProperties;
}
```
