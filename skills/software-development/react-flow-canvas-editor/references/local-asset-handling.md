# Local Asset Handling (User-Uploaded Files)

When users upload their own files via right-click menu or drag-drop, the nodes must preserve original file properties.

## isLocalAsset Flag

Set `isLocalAsset: true` in node config when creating nodes from local files:

```tsx
config: {
  assetUrl: fileUrl,  // URL.createObjectURL(file)
  assetName,
  isLocalAsset: true,  // KEY FLAG
  originalWidth: ...,
  originalHeight: ...,
}
```

## Display Behavior

Local assets use `objectFit: contain` (preserves aspect ratio, no cropping).
Remote/API assets use `objectFit: cover` (fills container, may crop).

### ImageNode
```tsx
const cfg = d.config as {
  // ... other fields
  isLocalAsset?: boolean;
};

<img style={{ 
  objectFit: cfg.isLocalAsset ? "contain" : "cover",
  background: cfg.isLocalAsset ? "#1a1a1a" : "transparent",
}} />
```

### VideoPreview Component
Add `isLocalAsset` prop:

```tsx
interface VideoPreviewProps {
  // ... other props
  isLocalAsset?: boolean;
}

<video style={{
  objectFit: isLocalAsset ? 'contain' : 'cover',
  background: isLocalAsset ? '#1a1a1a' : 'transparent',
}} />
```

### VideoNode (passing the prop)
```tsx
const cfg = d.config as {
  // ... other fields
  isLocalAsset?: boolean;
};

<VideoPreview isLocalAsset={cfg.isLocalAsset} ... />
```

## File Type Detection

```tsx
const isImage = file.type.startsWith('image/');
const isVideo = file.type.startsWith('video/');
```

## Original Metadata Extraction

**Images:** Use `new Image()` + `onload` to get `naturalWidth`/`naturalHeight`
**Videos:** Use `document.createElement('video')` + `onloadedmetadata` to get `videoWidth`/`videoHeight`/`duration`

Both use `URL.createObjectURL(file)` which creates a blob: URL that doesn't need CORS proxy.

## Pitfalls

1. **Blob URLs don't need proxy** — `proxyUrl()` already handles this (checks for `blob:` prefix)
2. **objectFit cover crops content** — User-uploaded images/videos get cropped with `cover`. Always use `contain` for local assets.
3. **cfg type must include isLocalAsset** — Add `isLocalAsset?: boolean` to the cfg type assertion in both ImageNode and VideoNode
4. **VideoPreview prop drilling** — Must add `isLocalAsset` to VideoPreviewProps interface AND pass it from VideoNode
