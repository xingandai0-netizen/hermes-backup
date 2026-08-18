# Error Cases from 2026-06-14 Session

## Case 1: assetType Storage Location Mismatch

**Symptom**: Video→Image workflow fails. Image node cannot detect that upstream is a video.

**Root Cause**: 
- VideoNode stores `assetType` at `node.data.assetType` (correct)
- ImageNode reads from `node.data.config.assetType` (wrong location)

**Fix**:
```typescript
// Read from both locations
const sourceData = sourceNode.data as unknown as NodeData;
const sourceConfig = sourceData?.config as Record<string, unknown> | undefined;
const assetType = sourceData?.assetType || sourceConfig?.assetType;
```

**Lesson**: Always search all components for field usage before assuming consistency.

## Case 2: CSS !important Overrides Inline Styles

**Symptom**: Changed edge color in ReactFlow props but color didn't change.

**Root Cause**: `globals.css` had `stroke: #5e6ad2 !important` which overrides inline styles.

**Fix**: Must update BOTH:
1. CSS: `.react-flow__edge-path { stroke: #ffffff !important; }`
2. Inline: `style: { stroke: "#ffffff" }`

**Lesson**: When CSS uses `!important`, inline styles cannot override.

## Case 3: read_file/write_file Line Number Corruption

**Symptom**: TypeScript errors `TS1109: Expression expected` at lines 1-10.

**Root Cause**: `read_file` returns `"1|\"use client\";\n2|..."` with line numbers. Passing this to `write_file` corrupts the file.

**Fix**: Use `patch` tool instead, or strip line numbers before writing.

**Lesson**: Never pass `read_file` output directly to `write_file`.

## Case 4: onlyRenderVisibleElements Freezes Page

**Symptom**: Page completely frozen after adding `onlyRenderVisibleElements={true}`.

**Root Cause**: Unknown - this ReactFlow option can cause freezing in some configurations.

**Fix**: Remove the option entirely.

**Lesson**: Test performance options carefully before committing.

## Case 5: Video Reference - base64 Not Accepted by API

**Symptom**: API error "base64 image is not allowed".

**Root Cause**: `extract_video_frame` returned base64 data URL, but API doesn't accept base64.

**Fix**: Pass video URL directly to API, let it handle video-to-image internally.

**Lesson**: Always check API format requirements before implementing.

## Case 6: Localhost URLs Not Accessible from External API

**Symptom**: API error "connection refused" when trying to download from `http://localhost:8000/...`.

**Root Cause**: Local proxy URLs are only accessible from the user's machine, not from external API servers.

**Fix**: Pass public URLs directly to API instead of proxying through localhost.

**Lesson**: External APIs cannot access localhost URLs.

## Case 7: Layout Completely Broken by CSS Changes

**Symptom**: Sidebar disappeared, canvas at top, controls at bottom.

**Root Cause**: CSS additions conflicted with Tailwind utility classes.

**Fix**: Revert CSS changes, keep minimal styling.

**Lesson**: Never add CSS that conflicts with Tailwind's layout utilities.

## Case 8: Multiple Node Files Not Using memo

**Symptom**: Sluggish performance when moving nodes.

**Root Cause**: VideoNode, ImageNode, CompositeNode, TextNode not wrapped in `React.memo`.

**Fix**: 
```typescript
const VideoNode = React.memo(function VideoNode(props: NodeProps) { ... });
export default VideoNode;
```

**Lesson**: Always memo node components in React Flow.
