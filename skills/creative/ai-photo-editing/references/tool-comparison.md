# AI Photo Editing Tools — Detailed Comparison

## IOPaint
- **Repo**: https://github.com/Sanster/IOPaint
- **Stars**: 23k+
- **License**: Apache-2.0
- **Tech**: Python backend + React web UI
- **Models**: Lama, MAT, SD, SDXL, PowerPaint, etc.
- **Install**: `pip install iopaint`
- **Run**: `iopaint start --model lama --port 8080`
- **Strengths**: Most mature, active development, many models, web UI + CLI + API, batch processing
- **Weakness**: SD models need GPU for reasonable speed
- **macOS App**: OptiClean (App Store)

## inpaint-web
- **Repo**: https://github.com/lxfater/inpaint-web
- **License**: MIT
- **Tech**: WebGPU + WASM (pure browser)
- **Strengths**: Zero install, privacy (local processing), works offline
- **Weakness**: Less powerful models, limited to browser capabilities

## PhotoSense
- **Repo**: https://github.com/Gara-11/photosense
- **License**: GPL-3.0
- **Tech**: C# / .NET 4.8, Photoshop plugin
- **APIs**: GPT Image 2 compatible, Nano Banana / Gemini compatible
- **Workflow**: PS → Mask → AI Generation → Transparent Patch → Continue in PS
- **Strengths**: Professional non-destructive workflow, integrates with PS layers
- **Weakness**: Windows only, needs Photoshop, needs API key
- **Creator**: Lacrimosa1337 (Bilibili)

## text-inpainting
- **Repo**: https://github.com/nickersonj/text-inpainting
- **License**: MIT
- **Tech**: Python + CLIPSeg + Stable Diffusion
- **Strengths**: No manual mask needed, text-guided
- **Weakness**: Less precise than manual masks, needs torch

## Other Notable Tools

### lxfater/inpaint-web
- Browser-based, WebGPU
- Good for quick privacy-safe edits

### andreas128/RePaint
- Diffusion-based inpainting (CVPR 2022)
- Research-quality, not production-ready

### lkwq007/stablediffusion-infinity
- Outpainting on infinite canvas
- Niche use case: extending image boundaries

### zllrunning/video-object-removal
- Video object removal (draw bounding box)
- Separate category from still image editing

## API Services (No Local GPU)

| Service | Model | Pricing |
|---------|-------|---------|
| Replicate | Lama, SD, SDXL | Pay-per-use |
| Stability AI | SDXL inpainting | API credits |
| OpenAI | DALL-E inpainting | Per image |
| FLUX Fill | FLUX-based | Via Replicate/ fal.ai |

## Use Case → Tool Mapping

| Task | Best Tool | Why |
|------|-----------|-----|
| Remove watermark | IOPaint (Lama) | Fast, clean, local |
| Remove person from photo | IOPaint (Lama) | Good at structure fill |
| Replace background | IOPaint (SD) or API | Needs generative capability |
| Remove text/overlay | IOPaint (Lama) | Simple inpainting |
| Fix old photo damage | IOPaint (MAT) | Better for large areas |
| Change object in photo | PhotoSense + API | Precise mask control |
| Quick edit, no install | inpaint-web | Zero setup |
| Batch process 100+ images | IOPaint CLI | Scriptable, fast |
