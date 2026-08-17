# Canvas Context Menu & File Drop Patterns

## Right-Click Canvas Context Menu

Add `onPaneContextMenu` handler to ReactFlow for canvas right-click:

```tsx
// State for context menu
const [contextMenu, setContextMenu] = useState<{
  x: number; y: number; type: 'edge' | 'canvas'; edgeId?: string;
} | null>(null);

// Canvas right-click handler
const onPaneContextMenu = useCallback((e: MouseEvent | React.MouseEvent) => {
  e.preventDefault();
  setContextMenu({ x: e.clientX, y: e.clientY, type: 'canvas' });
}, []);

// Edge right-click handler  
const onEdgeContextMenu: EdgeMouseHandler = useCallback((e, edge) => {
  e.preventDefault();
  setContextMenu({ x: e.clientX, y: e.clientY, type: 'edge', edgeId: edge.id });
}, []);

// Add to ReactFlow component
<ReactFlow
  onPaneContextMenu={onPaneContextMenu}
  onEdgeContextMenu={onEdgeContextMenu}
  // ... other props
/>
```

## File Drag-and-Drop to Canvas

Support dropping image/video files directly onto canvas:

```tsx
const onDrop = useCallback(async (e: React.DragEvent) => {
  e.preventDefault();
  
  // Check for file drop
  const files = e.dataTransfer.files;
  if (files && files.length > 0) {
    const file = files[0];
    const isImage = file.type.startsWith('image/');
    const isVideo = file.type.startsWith('video/');
    
    if (isImage || isVideo) {
      const assetType = isImage ? 'IMAGE' : 'VIDEO';
      
      // Get original dimensions
      const fileUrl = URL.createObjectURL(file);
      let meta = { width: 0, height: 0, duration: 0 };
      
      if (isImage) {
        const img = new window.Image();
        await new Promise<void>((resolve) => {
          img.onload = () => {
            meta = { width: img.naturalWidth, height: img.naturalHeight, duration: 0 };
            resolve();
          };
          img.onerror = () => resolve();
          img.src = fileUrl;
        });
      } else {
        const video = document.createElement('video');
        await new Promise<void>((resolve) => {
          video.onloadedmetadata = () => {
            meta = { width: video.videoWidth, height: video.videoHeight, duration: video.duration };
            resolve();
          };
          video.onerror = () => resolve();
          video.src = fileUrl;
        });
      }
      
      URL.revokeObjectURL(fileUrl);
      
      // Upload to backend (returns publicly accessible URL)
      const backendUrl = await uploadToBackend(file);
      if (backendUrl) {
        createAssetNode(assetType, backendUrl, file.name, meta);
      }
      return;
    }
  }
  
  // Handle node type drops from sidebar...
}, [uploadToBackend, createAssetNode]);
```

## Important: `onPaneContextMenu` Type

The handler type must be `MouseEvent | React.MouseEvent` (not just `React.MouseEvent`):
```tsx
const onPaneContextMenu = useCallback((e: MouseEvent | React.MouseEvent) => {
  // ...
}, []);
```

## File Input for Right-Click Menu

Use hidden file input triggered by context menu selection:

```tsx
const fileInputRef = useRef<HTMLInputElement>(null);
const [addingAssetType, setAddingAssetType] = useState<'IMAGE' | 'VIDEO' | null>(null);

// Handle menu selection
const handleAddAsset = useCallback((assetType: 'IMAGE' | 'VIDEO') => {
  setAddingAssetType(assetType);
  setContextMenu(null);
  if (fileInputRef.current) {
    fileInputRef.current.accept = assetType === 'IMAGE' ? 'image/*' : 'video/*';
    fileInputRef.current.click();
  }
}, []);

// Hidden input
<input
  ref={fileInputRef}
  type="file"
  style={{ display: 'none' }}
  onChange={handleFileSelect}
/>
```

## Local Asset Display

For locally uploaded assets, use `objectFit: "contain"` instead of `"cover"` to preserve original dimensions:

```tsx
<img
  src={url}
  style={{ 
    objectFit: isLocalAsset ? "contain" : "cover",
    background: isLocalAsset ? "#1a1a1a" : "transparent",
  }}
/>
```
