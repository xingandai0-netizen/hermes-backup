# Antoken UI Conventions

## Node Dialog Sizing (Verified 2026-06-15)

Standard dimensions for node inline dialogs (VideoNode, ImageNode, CompositeNode):

```css
.node-dialog {
  width: 400px;
  min-width: 400px;
  border-radius: 18px;
  left: -60px;  /* Center offset */
}

.dialog-button {
  width: 30px;
  height: 30px;
}

.dialog-icon {
  width: 15px;
  height: 15px;
}

.send-button {
  width: 44px;
  height: 44px;
}
```

### Why These Sizes
- **400px width**: Fits comfortably in 280px nodes with overflow visible, prevents text truncation
- **18px radius**: Matches TapNow reference design
- **-60px left offset**: Centers dialog relative to node
- **30px buttons**: Touch-friendly, visually balanced
- **44px send button**: Primary action, larger for emphasis

## Design Reference: TapNow

UI style guide follows TapNow (https://tapnow.ai):
- Dark theme: #2a2a2a dialog background
- Border radius: 16-18px
- Backdrop blur on overlays
- No emoji in UI (use CSS squares/icons)
- Linear/Vercel dark aesthetic

## Anti-Patterns (Lessons Learned)

1. **Don't use `width: 100%`** — dialogs inherit node width (280px), too small
2. **Don't use `overflow: hidden`** — clips dialogs that extend beyond node bounds
3. **Don't add `transform`** — breaks React Flow positioning
4. **Always `stopPropagation` on dialog** — prevents node drag when clicking inputs

## Material Name Label (2026-06-15)

每个素材节点左上角显示素材名称标签：

```tsx
<div style={{
  position: "absolute",
  top: 8,
  left: 8,
  zIndex: 10,
  display: "flex",
  alignItems: "center",
  gap: 4,
  background: "rgba(0,0,0,0.6)",
  padding: "2px 8px",
  borderRadius: 4,
  pointerEvents: "none",
}}>
  {/* 图片用 rect+circle+polyline, 视频用 polygon play */}
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
    <polygon points="5 3 19 12 5 21 5 3" />
  </svg>
  <span style={{ fontSize: 11, color: "white", fontWeight: 500 }}>
    {cfg.assetName || "素材"}
  </span>
</div>
```

**cfg类型必须包含assetName字段：**
```typescript
const cfg = d.config as {
  content?: string;
  model?: string;
  assetName?: string;  // 必须加
  // ...
};
```

## @Mention Input Component (2026-06-15)

文件：`frontend/src/components/MentionInput.tsx`

在对话框中输入@弹出素材列表，支持键盘导航：

```tsx
import MentionInput from "@/components/MentionInput";

<MentionInput
  value={prompt}
  onChange={setPrompt}
  mentions={[
    ...upstream.images.map(img => ({ 
      id: img.assetName, name: img.assetName, type: 'image' as const 
    })),
    ...upstream.videos.map(vid => ({ 
      id: vid.assetName, name: vid.assetName, type: 'video' as const 
    })),
  ]}
  placeholder="输入@引用素材，如：@图素材1中的什么替换成@视频素材1中的什么"
  disabled={loading}
/>
```

### 功能特性
- 输入@弹出素材列表
- 键盘导航：↑↓箭头、回车选择、ESC关闭
- 按类型显示不同图标（图片/视频）
- 选择后自动插入 `@素材名 `

## Handle Styling (Final Config 2026-06-15)

```typescript
const HOVER_ZONE = 40;

const handleStyle = {
  width: 20,
  height: 20,
  background: categoryColor,
  border: "2px solid #0a0a0f",
  borderRadius: "50%",
  boxShadow: isHovered
    ? `0 0 20px ${color}, 0 0 10px ${color}80, 0 0 5px ${color}60`
    : `0 0 10px ${color}70, 0 0 4px ${color}50`,
  transition: "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
  transform: isHovered ? "scale(1.5)" : "scale(1)",
  opacity: isHovered ? 1 : 0,
  pointerEvents: (isHovered ? "auto" : "none") as React.CSSProperties["pointerEvents"],
};

// 外层容器用 padding+margin 扩展 hover 检测范围
<div
  onMouseEnter={handleMouseEnter}
  onMouseLeave={handleMouseLeave}
  style={{ position: "relative", width: 280, padding: HOVER_ZONE, margin: -HOVER_ZONE }}
>
  {/* Handle 位置需要加上 HOVER_ZONE 偏移 */}
  <Handle style={{ ...handleStyle, left: HOVER_ZONE - 28, transformOrigin: "right center" }} />
  <Handle style={{ ...handleStyle, right: HOVER_ZONE - 28, transformOrigin: "left center" }} />
</div>
```

### Handle 延迟隐藏
鼠标离开后延迟10秒才隐藏，方便连接操作：
```typescript
const hideTimerRef = useRef<NodeJS.Timeout | null>(null);

const handleMouseEnter = useCallback(() => {
  if (hideTimerRef.current) { clearTimeout(hideTimerRef.current); hideTimerRef.current = null; }
  setIsHovered(true);
}, []);

const handleMouseLeave = useCallback(() => {
  hideTimerRef.current = setTimeout(() => setIsHovered(false), 10000);
}, []);
```

## Iteration History

| Version | Width | Issue |
|---------|-------|-------|
| v1 | 100% | Too small, text truncated |
| v2 | 300px | Still cramped |
| v3 | 400px | ✅ Optimal |

## CSS Variables (globals.css)

```css
:root {
  --node-width: 280px;
  --dialog-width: 400px;
  --dialog-radius: 18px;
  --dialog-bg: #2a2a2a;
  --dialog-border: rgba(255, 255, 255, 0.1);
}
```
