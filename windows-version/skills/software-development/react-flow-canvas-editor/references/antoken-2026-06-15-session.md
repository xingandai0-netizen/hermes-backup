# Antoken Session 2026-06-15 - Critical Learnings

## Critical Pitfalls

### File Corruption via read_file/write_file
Using `read_file` + `write_file` for color replacement CORRUPTS files — it embeds line numbers like `1|1|1|"use client"`. **ALWAYS use `patch` tool for find-replace operations.** This happened 3 times in one session and required reverting to earlier commits.

### ReactFlow Double-Click Interception
ReactFlow's `onNodeDoubleClick` prop intercepts ALL double-click events on nodes. Setting it to `() => {}` does NOT let events pass through. Solution: remove the prop entirely if you need double-click on child elements.

### stopPropagation Breaks Node Selection
`stopPropagation()` on node child elements (preview areas, containers) prevents ReactFlow from selecting the node. This makes Delete key non-functional. **Only use stopPropagation on specific interactive controls (buttons, sliders, input fields), NOT on the entire preview area or node container.**

### Workflow Logic Changes Require User Approval
Never modify core workflow logic (API calls, asset processing, generation pipeline) without explicit user consultation. The user will get very frustrated if you break working logic while fixing UI issues.

## Node Naming Pattern

Use localStorage-based persistent counter for sequential node naming (图素材1, 图素材2, 视频素材1...):

```typescript
function getNextAssetNumber(type: 'IMAGE' | 'VIDEO'): number {
  const key = `antoken_asset_counter_${type}`;
  const current = parseInt(localStorage.getItem(key) || '0', 10);
  const next = current + 1;
  localStorage.setItem(key, next.toString());
  return next;
}
```

**Do NOT use:**
- Module-level variables (reset on page load)
- Count existing nodes (fails after deletion, produces duplicates)
- Global window variables (fragile)

## Video Preview Interaction Pattern (TapNow-style)

- **Hover** → play from start
- **Leave** → pause and reset to start
- **Click** → select node (do NOT stopPropagation)
- **Double-click** → open fullscreen preview
- **Controls bar** → show on hover, with progress bar, play/pause, time display
- Use `onMouseDown={(e) => e.stopPropagation()}` on controls bar to prevent drag while clicking controls

## Connection Handle Styling

- Size: 20x20px
- Distance from node: -28px (outside the node)
- Hover zone: 40px around node (use padding + margin trick on outer container)
- Delay hide: 10 seconds after mouse leave
- Hover effect: scale(1.5) with elastic curve `cubic-bezier(0.34, 1.56, 0.64, 1)`
- transform-origin: right center (left handle), left center (right handle) for outward expansion

## @Mention System for Asset Referencing

Components:
- `MentionInput.tsx` - textarea with @mention popup
- `getUpstreamAssets()` - collects all connected assets by node type
- Shows all connected assets in @popup, not just ones with URLs

Key fix: `getUpstreamAssets` should check `nodeType` property, not whether `url` exists.

## API Multi-Asset Support

### Image Generation (generate_image)
- `reference_image_urls: List[str]` - multiple images
- `reference_video_urls: List[str]` - multiple videos
- All combined into single `image_urls` array for API

### Video Generation (generate_video)
- `reference_image_urls: List[str]` - multiple images
- `reference_video_urls: List[str]` - multiple videos
- Each uploaded separately via asset system
- Uses `image_with_roles` and `video_with_roles` arrays

## Workflow Core Principle (DO NOT CHANGE WITHOUT CONSULTING)
All generation nodes must reference ALL upstream connected assets (multiple images + multiple videos). Supports: image→image, image+video→image, image+video→video, video→video.
