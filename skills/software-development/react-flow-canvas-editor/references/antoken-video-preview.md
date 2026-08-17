# Antoken Video Preview Component Patterns

## Interaction Model (TapNow-style)
1. **Hover** → play video from start
2. **Leave** → pause and reset to start
3. **Click** → bubble to ReactFlow (select node → show PropertyPanel)
4. **Control panel (对话交流框)** → shown via parent node's onClick calling `setShowPreview(true)`
5. **Fullscreen button** → in controls area, opens PreviewModal
6. **Right-click** → upload file

## Component Props
```typescript
interface VideoPreviewProps {
  src: string;
  poster?: string;
  width?: number | string;
  height?: number | string;
  autoPlay?: boolean;  // default: false
  loop?: boolean;      // default: true
  muted?: boolean;     // default: true
  controls?: boolean;  // default: true
  hoverToPlay?: boolean; // default: true
  onExpand?: () => void; // fullscreen button callback
  className?: string;
  style?: React.CSSProperties;
}
```

## Key Implementation Details
- Do NOT add `onClick` to wrapper div — let events bubble to ReactFlow
- Use `onMouseDown={(e) => e.stopPropagation()}` on controls area only
- Controls show on hover (not just when playing)
- Progress bar: 4px height, #ffffff color
- Icons: 12-14px, compact spacing (gap: 6)
- No text labels on controls (removed for space)
- Smooth popup animation: `popUp 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)`

## Plyr Library Issue
- Plyr does NOT work in Next.js (CSS import issues)
- Use native `<video>` element + custom controls instead
- Custom controls: play/pause, skip ±5s, time, playback speed, mute, fullscreen

## Color Scheme
- Brand color: #ffffff (white, NOT #5e6ad2 blue-purple)
- Progress bar: #ffffff
- Loading spinner: #ffffff border-top
- All rgba(94,106,210,x) → rgba(255,255,255,x)

## File Corruption Warning
- NEVER use read_file + write_file for color replacement
- ALWAYS use `patch` tool for targeted string replacement
- read_file returns content with line numbers that get embedded in file if written back
