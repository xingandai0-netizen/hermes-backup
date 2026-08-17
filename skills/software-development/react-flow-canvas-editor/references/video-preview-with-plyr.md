# Video Preview Component (Custom Implementation)

## Problem
ReactFlow nodes with video elements have interaction conflicts:
- `stopPropagation` on containers breaks child button clicks
- Browser native `<video>` controls look inconsistent
- No loading states, error handling, or hover-to-play
- **Plyr library doesn't work well in Next.js App Router** (CSS import issues, initialization problems)

## Solution: Custom VideoPreview Component

### Why Not Plyr
**PITFALL**: Plyr has initialization issues in Next.js App Router:
- CSS import (`import 'plyr/dist/plyr.css'`) doesn't load properly
- Client-side initialization timing conflicts
- Style conflicts with Tailwind CSS

**Solution**: Use native `<video>` element with custom controls.

### Component Location
`/frontend/src/components/VideoPreview.tsx`

### Key Features
- **Custom controls** with brand-colored dark theme (#5e6ad2)
- **Loading state** with spinner animation
- **Error state** with icon + message
- **Hover-to-play** option (hoverToPlay prop)
- **Drag-to-seek** with time preview tooltip
- **Keyboard controls**: space/K=pause, arrows=seek, M=mute, F=fullscreen
- **Playback speed**: 0.5x-2x toggle
- **Volume control**: slider + mute button
- **Fullscreen support**
- **Auto-hide controls** (3 seconds during playback)

### Usage Pattern
```tsx
import VideoPreview from "@/components/VideoPreview";

// Full preview (with all controls)
<VideoPreview
  src={proxyUrl(videoUrl) || videoUrl}
  height={220}
  autoPlay
  loop
  muted
  controls
/>

// Thumbnail preview (no controls, smaller)
<VideoPreview
  src={proxyUrl(videoUrl) || videoUrl}
  height={60}
  autoPlay
  loop
  muted
  controls={false}
/>

// Hover-to-play mode
<VideoPreview
  src={videoUrl}
  hoverToPlay={true}
  controls
/>
```

### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| src | string | required | Video URL |
| poster | string | - | Thumbnail URL |
| width | number/string | '100%' | Container width |
| height | number/string | 220 | Container height |
| autoPlay | boolean | true | Auto-play on load |
| loop | boolean | true | Loop playback |
| muted | boolean | true | Muted by default |
| controls | boolean | true | Show custom controls |
| hoverToPlay | boolean | false | Play on hover |
| className | string | '' | Additional CSS class |
| style | CSSProperties | {} | Inline styles |

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| Space / K | Play / Pause |
| ← / → | Seek ±5 seconds |
| J / L | Seek ±10 seconds |
| ↑ / ↓ | Volume ±10% |
| M | Toggle mute |
| F | Toggle fullscreen |
| 0-9 | Jump to 0%-90% |

### Implementation Details

#### Loading Optimization
```tsx
// Use preload="auto" for faster loading
<video preload="auto" ... />

// Listen for canplay event (faster than loadeddata)
video.addEventListener('canplay', () => setIsLoading(false));
```

#### Drag-to-Seek
```tsx
// Mouse down starts seeking
const handleSeekStart = (e: React.MouseEvent) => {
  setIsSeeking(true);
  // Calculate position and update currentTime
  // Add mousemove/mouseup listeners for drag
};

// Time preview tooltip during drag
{isSeeking && (
  <div style={{ position: 'absolute', left: `${progress}%` }}>
    {formatTime((progress / 100) * duration)}
  </div>
)}
```

#### Auto-hide Controls
```tsx
// Hide controls after 3 seconds during playback
useEffect(() => {
  if (showControls && isPlaying) {
    timeout = setTimeout(() => setShowControls(false), 3000);
  }
  return () => clearTimeout(timeout);
}, [showControls, isPlaying]);
```

### Nodes Updated
- VideoNode: full preview with controls
- CompositeNode: video preview with controls
- VideoCompositeNode: thumbnail (controls=false) + result (controls=true)
- VideoGenNode: result preview
- VideoExportNode: result + input preview
- Img2VideoNode: fullscreen preview

### Pitfalls
1. **proxyUrl fallback**: Always `proxyUrl(url) || url` - proxyUrl can return null
2. **crossOrigin**: Add `crossOrigin="anonymous"` for CORS videos
3. **Stop propagation**: Put `onClick={(e) => e.stopPropagation()}` on controls div, not container
4. **Small previews**: Use `controls={false}` for thumbnails (< 100px height)
5. **Plyr doesn't work**: Don't use Plyr in Next.js App Router - use custom implementation
6. **preload strategy**: Use `preload="auto"` + `canplay` event for faster loading
7. **Keyboard focus**: Only capture keyboard events when `showControls` is true
