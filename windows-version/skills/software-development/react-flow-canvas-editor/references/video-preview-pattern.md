# Video Preview Component Pattern

## Overview

Custom video preview component for React Flow nodes. Uses native `<video>` element with custom controls - NO Plyr library (fails in Next.js SSR environment).

## Component Structure

```tsx
// ~/antoken/frontend/src/components/VideoPreview.tsx
'use client';

import { useEffect, useRef, useState, useCallback } from 'react';

interface VideoPreviewProps {
  src: string;
  poster?: string;
  width?: number | string;
  height?: number | string;
  autoPlay?: boolean;
  loop?: boolean;
  muted?: boolean;
  controls?: boolean;
  hoverToPlay?: boolean;
  className?: string;
  style?: React.CSSProperties;
}

export default function VideoPreview({ ... }: VideoPreviewProps) {
  // Native video element + custom controls
  // Hover to show controls
  // Progress bar at bottom (3px)
  // Time display on hover (bottom-right)
  // Play/pause button overlay
}
```

## Key Features

1. **Loading State**: Spinner animation while video loads
2. **Error State**: "加载失败" message on error
3. **Play/Pause**: Click video or button to toggle
4. **Progress Bar**: Bottom 3px bar, click to seek
5. **Time Display**: Shows on hover, bottom-right corner
6. **Controls**: Show on hover, hide when playing

## Integration with Nodes

```tsx
// In VideoNode, ImageNode, CompositeNode, etc.
import VideoPreview from "@/components/VideoPreview";
import { proxyUrl } from "@/lib/mediaProxy";

// Usage
<VideoPreview
  src={proxyUrl(videoUrl) || videoUrl}
  height={220}
  autoPlay
  loop
  muted
  controls
/>
```

## Pitfalls

### ❌ DON'T Use Plyr
```bash
npm install plyr  # FAILS in Next.js
```
- Plyr CSS doesn't load properly in Next.js SSR
- Initialization timing issues
- **Use native video + custom controls instead**

### ✅ DO Use preload="auto"
```tsx
<video preload="auto" ...>
```
- Faster loading for short videos
- Better user experience

### ✅ DO Handle proxyUrl
```tsx
src={proxyUrl(videoUrl) || videoUrl}
```
- Always proxy external URLs through backend
- Fallback to original URL if proxy fails

## User Preferences (阿戴)

1. **No descriptive text** - Remove keyboard shortcuts hints, feature descriptions
2. **Icon-only controls** - Use SVG icons, no text labels
3. **Compact controls** - Small icons (12-14px), tight spacing
4. **Hover to show** - Controls appear on hover, disappear when playing
5. **Color scheme** - Use white (#ffffff) accent, not blue-purple

## Complete Example

See `~/antoken/frontend/src/components/VideoPreview.tsx` for full implementation.
