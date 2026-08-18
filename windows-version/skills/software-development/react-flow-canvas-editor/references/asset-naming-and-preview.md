# Asset Naming, Preview, and Download Patterns

## Asset Naming (assetName)
Every generation node stores a `config.assetName` field. Users type a descriptive name (e.g., "折扇", "海边人物") that downstream synthesis nodes read and embed into the AI prompt.

### Generation nodes save assetName
```typescript
const [assetName, setAssetName] = useState(cfg.assetName ?? "");
// On generation complete:
updateNodeData(id, { config: { ...cfg, assetName, resultUrl: data.url } });
```

### Synthesis nodes read assetName from upstream
```typescript
const incomingEdges = edges.filter(e => e.target === id);
let imgName = "图片素材";
let videoName = "视频素材";
for (const edge of incomingEdges) {
  const sourceNode = nodes.find(n => n.id === edge.source);
  const sourceConfig = sourceNode?.data?.config;
  if (edge.targetHandle === 'image') imgName = sourceConfig?.assetName || "图片素材";
  if (edge.targetHandle === 'video') videoName = sourceConfig?.assetName || "视频素材";
}
```

### Prompt construction with asset names
```typescript
let fullPrompt = prompt;
const refs = [];
if (imgUrl) refs.push(`[图片素材: ${imgName}]`);
if (videoUrl) refs.push(`[视频素材: ${videoName}]`);
if (refs.length) fullPrompt = `${refs.join(' ')}\n${prompt}`;
// Result: "[图片素材: 折扇] [视频素材: 海边人物] 让人物手中拿着折扇"
```

## Download Button Pattern
ALL nodes that generate content MUST have a download button. This is a user requirement ("只要是在我们这里生成的都要提供下载").

```tsx
{resultUrl && (
  <a
    href={proxyUrl(resultUrl)}
    download
    target="_blank"
    rel="noopener noreferrer"
    style={{
      display: "block", width: "100%", textAlign: "center",
      fontSize: 11, marginTop: 4, padding: "4px 0", borderRadius: 4,
      background: "rgba(255,255,255,0.05)", color: "rgba(255,255,255,0.6)",
      textDecoration: "none",
    }}
  >
    下载图片  {/* or 下载视频 */}
  </a>
)}
```
**Critical**: Download links MUST also use `proxyUrl()` to bypass CORS.

## PreviewModal Pattern (Click-to-Expand)
All preview images/videos support click-to-expand in a fullscreen modal.

### PreviewModal component
```tsx
// components/PreviewModal.tsx
interface PreviewModalProps {
  url: string;
  type: 'image' | 'video';
  onClose: () => void;
}

export default function PreviewModal({ url, type, onClose }: PreviewModalProps) {
  const proxiedUrl = proxyUrl(url) || url;
  return (
    <div
      onClick={onClose}
      onWheel={e => e.stopPropagation()}
      onMouseDown={e => e.stopPropagation()}
      style={{
        position: 'fixed', inset: 0, zIndex: 9999,
        background: 'rgba(0,0,0,0.85)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        cursor: 'pointer',
      }}
    >
      <div
        onClick={e => e.stopPropagation()}
        onWheel={e => e.stopPropagation()}
        onMouseDown={e => e.stopPropagation()}
        style={{ maxWidth: '90vw', maxHeight: '90vh', position: 'relative' }}
      >
        {type === 'image' ? (
          <img src={proxiedUrl} style={{ maxWidth: '90vw', maxHeight: '90vh', objectFit: 'contain', borderRadius: 8 }} />
        ) : (
          <video src={proxiedUrl} controls autoPlay style={{ maxWidth: '90vw', maxHeight: '90vh', objectFit: 'contain', borderRadius: 8 }} />
        )}
        <button onClick={onClose} style={{ position: 'absolute', top: -12, right: -12, width: 28, height: 28, borderRadius: '50%', background: '#1a1a2e', border: '1px solid rgba(255,255,255,0.2)', color: '#fff', fontSize: 14, cursor: 'pointer' }}>
          X
        </button>
      </div>
    </div>
  );
}
```

### Usage in nodes
```tsx
import PreviewModal from "@/components/PreviewModal";

const [showPreview, setShowPreview] = useState(false);

// Preview area (clickable)
<div onClick={() => setShowPreview(true)} style={{ cursor: "pointer" }}>
  <img src={proxyUrl(url)} style={{ width: "100%", height: 100, objectFit: "cover" }} />
</div>

// Modal
{showPreview && <PreviewModal url={url} type="image" onClose={() => setShowPreview(false)} />}
```

### Critical: Stop event propagation
The modal MUST stop `wheel` and `mouseDown` events from propagating to the React Flow canvas. Otherwise, scrolling/zooming inside the modal will also move/zoom the canvas underneath.

## Size Selection Pattern
All 6 generation/compositing nodes have size selection dropdowns:

### Image sizes
```typescript
const IMAGE_SIZES = [
  { label: "1:1 方形 (1024x1024)", value: "1024x1024" },
  { label: "16:9 横屏 (1920x1080)", value: "1920x1080" },
  { label: "9:16 竖屏 (1080x1920)", value: "1080x1920" },
  { label: "4:3 标准 (1024x768)", value: "1024x768" },
  { label: "3:4 竖版 (768x1024)", value: "768x1024" },
];
```

### Video sizes
```typescript
const VIDEO_SIZES = [
  { label: "16:9 横屏 720p (1280x720)", value: "720p" },
  { label: "16:9 横屏 1080p (1920x1080)", value: "1080p" },
  { label: "9:16 竖屏 720p (720x1280)", value: "720p_vertical" },
  { label: "9:16 竖屏 1080p (1080x1920)", value: "1080p_vertical" },
  { label: "1:1 方形 720p (720x720)", value: "720p_square" },
];
```

### Size selector UI (after model selector, before prompt)
```tsx
<select
  value={selectedSize}
  onChange={e => setSelectedSize(e.target.value)}
  disabled={loading}
  style={{
    width: "100%", marginBottom: 4, fontSize: 11, color: "#d0d6e0",
    background: "#0a0a0f", border: "1px solid rgba(255,255,255,0.12)",
    borderRadius: 4, padding: "4px 6px", outline: "none",
  }}
>
  {IMAGE_SIZES.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
</select>
```

### API call includes size
```typescript
// Image: size parameter
body: JSON.stringify({ prompt, model, size: selectedSize, ... })

// Video: resolution parameter
body: JSON.stringify({ prompt, model, resolution: selectedSize, ... })
```
