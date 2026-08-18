# Antoken E-commerce Node Definitions

Complete node type registry for the Antoken AI workflow platform. Reference when building similar e-commerce workflow editors.

## Node Types (9 total)

### Input Group (输入)

| Type | Label | Inputs | Outputs | Config |
|------|-------|--------|---------|--------|
| skuImport | SKU导入 | none | TEXT (数据) | fileName, columnMapping, rowCount |
| imgImport | 图片导入 | none | IMAGE (图片) | fileName, format(PNG) |
| videoImport | 视频导入 | none | VIDEO (视频) | fileName, format(MP4) |

### AI Generation Group (AI生成)

| Type | Label | Inputs | Outputs | Config |
|------|-------|--------|---------|--------|
| imageGen | 图片生成 | TEXT (Prompt) | IMAGE (Output) | prompt, n, size, quality, resultUrl |
| videoGen | 文生视频 | TEXT (Prompt) | VIDEO (Output) | prompt, duration, resolution, resultUrl, thumbnailUrl |
| img2video | 图生视频 | IMAGE (图片) | VIDEO (视频) | prompt, duration, resolution, resultUrl, thumbnailUrl |

### Processing Group (处理)

| Type | Label | Inputs | Outputs | Config |
|------|-------|--------|---------|--------|
| imageProcess | 图片处理 | IMAGE (Input) | IMAGE (Output) | operation, quality, watermarkText |
| sizeAdapter | 尺寸适配 | IMAGE (Input) | IMAGE (Output) | preset, width, height, mode |
| videoComposite | 视频合成 | IMAGE + VIDEO | VIDEO (合成视频) | mode(overlay), duration, position(center) |

### Output Group (输出)

| Type | Label | Inputs | Outputs | Config |
|------|-------|--------|---------|--------|
| export | 导出 | IMAGE + VIDEO | none | format(PNG), quality, platform |

## Port Type Compatibility

```
TYPE_COMPAT = {
  IMAGE: ["IMAGE"],
  VIDEO: ["VIDEO", "IMAGE"],  // video can connect to image inputs
  TEXT: ["TEXT"],
  DATA: ["DATA", "TEXT"],
}
```

## Typical Workflows

### 1. Image + Video Composition (图片+视频合成)
```
imgImport(IMAGE) → videoComposite(IMAGE)
videoImport(VIDEO) → videoComposite(VIDEO)
videoComposite(VIDEO) → export(VIDEO)
```

### 2. Text-to-Image → Image-to-Video → Export
```
skuImport(TEXT) → imageGen(TEXT)
imageGen(IMAGE) → img2video(IMAGE)
img2video(VIDEO) → export(VIDEO)
```

### 3. Full E-commerce Pipeline
```
skuImport(TEXT) → imageGen(TEXT)
imageGen(IMAGE) → imageProcess(IMAGE)
imageProcess(IMAGE) → sizeAdapter(IMAGE)
sizeAdapter(IMAGE) → export(IMAGE)
```

## Node Letter Codes (for icons)

| Type | Code | Category Color |
|------|------|----------------|
| skuImport | SI | #27a644 (green) |
| imgImport | II | #27a644 |
| videoImport | VI | #27a644 |
| imageGen | IG | #7170ff (purple) |
| videoGen | VT | #7170ff |
| img2video | IV | #3b82f6 (blue) |
| imageProcess | IP | #3b82f6 |
| sizeAdapter | SA | #3b82f6 |
| videoComposite | VC | #3b82f6 |
| export | EX | #f59e0b (orange) |
