# Antoken-Specific Development Patterns

> Absorbed from `antoken-development` skill (archived 2026-06-21). Project-specific knowledge for the Antoken AI workflow platform.

## Project Architecture
- **Frontend**: Next.js 14 + React Flow (@xyflow/react v12) + Zustand + Tailwind CSS
- **Backend**: FastAPI (Python)
- **API**: toapis.com/v1
- **Repo**: xingandai0-netizen/antoken

## Critical: toapis.com API Endpoints (Verified 2026-06-27)

**Correct endpoints:**
- Video generation: `POST /v1/video/generations` or `/v1/videos/generations`
- Image generation: `POST /v1/images/generations`
- Task polling: `GET /v1/video/generations/{task_id}` or `/v1/images/generations/{task_id}`

**Wrong (do not use):** `/v1/generate/video`, `/v1/generate/image`, `/v1/task/video/{id}`

API uses `aspect_ratio` parameter (NOT `ratio` or `size`). Value must be ratio format:
```json
{"aspect_ratio": "1:1"}, {"aspect_ratio": "3:4"}, {"aspect_ratio": "9:16"}
```
Wrong parameters are silently ignored, returning default 1:1 1024x1024.

## Workflow Logic

All generation nodes must reference ALL upstream connected assets (multiple images + videos).

Data flow:
```
Frontend: reference_image_urls: [url1, url2] / reference_video_urls: [url3]
Backend: Upload to asset system → image_with_roles / video_with_roles
API: Prompt uses [素材1:名称] [素材2:名称] corresponding to array order
```

**Image generation API does NOT support video URLs!** `reference_image_urls` can only contain image URLs. Video URLs cause Vertex AI `INVALID_ARGUMENT` error.

## Asset Naming System

```typescript
function getNextAssetNumber(type: 'IMAGE' | 'VIDEO'): number {
  const key = `antoken_asset_counter_${type}`;
  const current = parseInt(localStorage.getItem(key) || '0', 10);
  const next = current + 1;
  localStorage.setItem(key, next.toString());
  return next;
}
```
- `assetName` stored in `data` (not `config`)
- Read with `d.assetName` (not `cfg.assetName`)

## UI Design Standards
- Linear/Vercel dark theme
- No emoji — CSS block icons
- Primary color: #ffffff (bright white)
- Node width: 280px
- Handle: 20px, offset -28px, hover scale 1.5x
- Pop animation: popUp + cubic-bezier(0.34, 1.56, 0.64, 1)

## Size Presets Must Sync Across Files

When updating size presets, must update ALL node files:
- `src/lib/constants.ts` → `IMAGE_SIZE_PRESETS`
- `src/components/nodes/ImageNode.tsx` → `IMAGE_SIZES`
- `src/components/nodes/VideoNode.tsx` → `VIDEO_RATIOS` + `VIDEO_RESOLUTIONS` + `VIDEO_DURATIONS`
- Same for VideoGenNode, VideoExportNode, VideoCompositeNode

## Dynamic Preview Height

```typescript
const getPreviewHeight = (ratio: string) => {
  const [w, h] = ratio.split(':').map(Number);
  return Math.round(280 * h / w);
};
```
| Ratio | Height (280px width) |
|-------|---------------------|
| 1:1   | 280px |
| 3:4   | 373px |
| 9:16  | 497px |
| 16:9  | 157px |

## Frontend Dev Server Crash Recovery

```bash
pkill -f "next dev" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
cd ~/antoken/frontend && rm -rf .next node_modules/.cache
npm run dev
```

## Video Node: Ratio/Resolution/Duration Separation

User explicitly requires: size selection and resolution must be separate controls.
```typescript
const VIDEO_RATIOS = [
  { label: "9:16 竖版", value: "9:16" },
  { label: "3:4 竖版", value: "3:4" },
  { label: "1:1 方版", value: "1:1" },
  { label: "16:9 横版", value: "16:9" },
];
const VIDEO_RESOLUTIONS = [
  { label: "480p", value: "480p" },
  { label: "720p", value: "720p" },
  { label: "1080p", value: "1080p" },
  { label: "2K", value: "2k" },
  { label: "4K", value: "4k" },
];
```
