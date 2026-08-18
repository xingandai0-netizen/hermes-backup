---
name: ai-photo-editing
description: "AI无痕P图/图片编辑：对象移除、局部替换、修复、抠图、换背景。触发：无痕P图、去水印、去路人、修图、inpainting、object removal、photo editing、图片修复。"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [photo-editing, inpainting, object-removal, image-manipulation, AI-editing, 无痕P图]
    related_skills: [ai-art-workflow, stable-diffusion-image-generation]
---

# AI Photo Editing & Inpainting

AI-powered photo editing: seamless object removal, local replacement, background swap, watermark erasure, and image restoration.

**NOT for**: generating new images from scratch (→ `ai-art-workflow`), style transfer, or video editing.

## Decision Tree

| Need | Tool | Difficulty |
|------|------|------------|
| Quick object/people removal (local, no API) | **IOPaint** | Easy |
| Browser-only, no install | **inpaint-web** | Easiest |
| Photoshop workflow, professional retouching | **PhotoSense** | Medium |
| Text-guided editing (no manual mask) | **text-inpainting** | Medium |
| API-based, integrate into code | IOPaint API / Replicate | Medium |

## IOPaint (Recommended Default)

GitHub: https://github.com/Sanster/IOPaint (23k+ stars)

Best standalone tool for most use cases. Web UI + CLI + API.

### Install & Run

```bash
pip install iopaint
iopaint start --model lama --port 8080
# Open http://localhost:8080
```

### Key Models

| Model | Best For | Speed |
|-------|----------|-------|
| `lama` | Object removal, watermark erasure | Fast (CPU OK) |
| `mat` | High-quality fill for large areas | Medium |
| `sd` / `sdxl` | Content replacement with prompts | Slow (GPU recommended) |

### CLI Usage

```bash
# Remove object from image (mask = white areas to remove)
iopaint run --model lama --image input.png --mask mask.png --output output.png

# Batch process
iopaint run --model lama --image ./input/ --mask ./masks/ --output ./output/
```

### macOS App

OptiClean — native macOS/iOS app from same developer, App Store available.

## inpaint-web (No Install)

GitHub: https://github.com/lxfater/inpaint-web

- Pure browser (WebGPU + WASM), no server, no upload
- Good for quick edits, privacy-sensitive images
- Less powerful than IOPaint but zero setup

## PhotoSense (Photoshop Plugin)

GitHub: https://github.com/Gara-11/photosense

- Integrates into Adobe Photoshop workflow
- Mask-based generative editing via GPT Image 2 / Gemini APIs
- Returns transparent patch layer for non-destructive editing
- Requires: Windows + Photoshop + .NET 4.8 + user's own API key

## text-inpainting (No Manual Mask)

GitHub: https://github.com/nickersonj/text-inpainting

- Describe what to remove/replace via text prompt
- Uses CLIPSeg for automatic mask generation
- Good for: "remove the person on the left", "replace sky with sunset"
- Needs Python + torch

## Pitfalls

1. **Lama model is best for removal, not replacement.** For replacing content (e.g., swap background), use SD/SDXL models or API-based tools. Lama just fills with plausible texture.

2. **Large area removal = artifacts.** Removing a person covering 30%+ of the image will look unnatural. Consider: (a) crop instead, (b) use SD-based replacement, or (c) accept some blur.

3. **Watermark removal may need two passes.** Semi-transparent watermarks often require: first pass with Lama to remove structure, second pass to clean residual color shift.

4. **GPU vs CPU.** Lama runs fine on CPU (seconds per image). SD-based inpainting needs GPU or it's painfully slow (minutes per image). For SD without GPU, use API services (Replicate, Stability AI).

5. **Mask quality matters.** Soft-edged masks produce more natural results than hard-edged ones. If your tool supports mask feathering, use it.

6. **macOS pip install may need `--break-system-packages`.** If you get PEP 668 error: `pip3 install iopaint --break-system-packages`

## References

- See `references/tool-comparison.md` for detailed feature matrix and GitHub links
