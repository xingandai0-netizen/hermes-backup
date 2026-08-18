# Video Preview & Interactive Elements in React Flow Nodes

## Video Preview Attributes

When adding video preview to React Flow nodes, the `<video>` element needs specific attributes to work correctly.

### Main Preview (large, in node body)
```tsx
<video
  src={proxyUrl(videoUrl)}
  crossOrigin="anonymous"
  style={{ width: "100%", height: 220, objectFit: "cover", display: "block" }}
  muted       // Required for autoplay to work in most browsers
  playsInline // Required for iOS
  autoPlay    // Auto-play on load
  controls    // Show playback controls
  loop        // Loop for preview convenience
/>
```

### Small Thumbnail Preview (素材预览, 60px height)
```tsx
<video
  src={proxyUrl(videoUrl)}
  muted
  autoPlay
  loop
  style={{ width: '100%', height: 60, objectFit: 'cover' }}
/>
// No controls for small thumbnails - too small to be useful
```

### Result Preview (clickable, opens modal)
```tsx
<video
  src={proxyUrl(resultUrl)}
  autoPlay
  loop
  muted
  style={{ width: '100%', height: 140, objectFit: 'cover', display: 'block' }}
/>
// User clicks to open PreviewModal with full controls
```

### Common Mistakes
- **Missing `autoPlay`**: Video appears frozen/static image
- **Missing `muted`**: Browser blocks autoplay with sound
- **Missing `playsInline`**: iOS won't autoplay
- **`pointerEvents: 'none'`**: Prevents clicking - use only if click is handled by parent div

## Interactive Elements in Nodes (stopPropagation)

Any clickable/draggable element inside a React Flow node MUST have `onMouseDown` handler to prevent node dragging.

### On the interactive container
```tsx
<div onMouseDown={(e) => e.stopPropagation()}>
  {/* buttons, inputs, selects, draggable areas */}
</div>
```

### On individual interactive elements
```tsx
<button onClick={handleClick} onMouseDown={(e) => e.stopPropagation()}>
<input onClick={(e) => e.stopPropagation()}>
<textarea onClick={e => e.stopPropagation()}>
```

### Elements that need stopPropagation
- File upload zones (拖拽上传)
- Asset preview areas (素材预览)
- Input fields and textareas
- Select dropdowns
- Buttons inside nodes
- Any element that handles mouse events

### Common Symptoms without stopPropagation
- "粘鼠标" (sticky mouse) - node follows cursor after clicking element
- Can't click buttons without dragging the node
- File drop doesn't work
- Text selection triggers node drag

## Affected Nodes (Antoken)

### VideoNode
- Preview: `autoPlay`, `controls`, `loop`, `muted`, `playsInline`
- Upload area: needs `stopPropagation`

### CompositeNode
- Preview: `autoPlay`, `controls`, `loop`, `muted`, `playsInline`
- Input area: needs `stopPropagation`

### VideoCompositeNode
- Asset thumbnails (60px): `autoPlay`, `loop`, `muted` (no controls)
- Result preview (140px): `autoPlay`, `loop`, `muted` (no controls)
- Asset container: needs `stopPropagation`

### VideoExportNode
- Result preview: `autoPlay`, `loop`, `muted` (no controls)
- Input preview: `autoPlay`, `loop`, `muted` (no controls)

### VideoGenNode
- Preview: `autoPlay`, `loop`, `muted` (no controls)

### ImageExportNode
- Asset preview container: needs `stopPropagation`

### Img2VideoNode
- Full preview modal: `controls`, `autoPlay` (already working)

## Checklist

Before committing video preview changes:
- [ ] `muted` attribute present
- [ ] `autoPlay` attribute present
- [ ] `loop` attribute present (for previews)
- [ ] `playsInline` for main preview
- [ ] `controls` for main preview only
- [ ] `onMouseDown={(e) => e.stopPropagation()}` on interactive containers
