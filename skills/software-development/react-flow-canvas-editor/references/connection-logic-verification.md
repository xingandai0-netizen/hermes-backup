# Connection Logic Verification Checklist

## When User Says "检查连接逻辑"
Run this systematic check with `execute_code`.

## 1. Node Port Definitions
Extract from NodePanel.tsx NODE_DEFINITIONS:
```
| Node | Inputs | Outputs |
|------|--------|---------|
| SKU导入 | — | TEXT |
| 图片导入 | — | IMAGE |
| 视频导入 | — | VIDEO |
| 图片生成 | TEXT | IMAGE |
| 文生视频 | TEXT | VIDEO |
| 图生视频 | IMAGE | VIDEO |
| 图片处理 | IMAGE | IMAGE |
| 尺寸适配 | IMAGE | IMAGE |
| 视频合成 | IMAGE+VIDEO | VIDEO |
| 导出 | IMAGE+VIDEO | — |
```

## 2. TYPE_COMPAT Matrix (validation.ts)
```typescript
const TYPE_COMPAT = {
  IMAGE: ["IMAGE"],           // IMAGE → IMAGE
  VIDEO: ["VIDEO", "IMAGE"],  // VIDEO → VIDEO or IMAGE
  TEXT: ["TEXT"],              // TEXT → TEXT
  DATA: ["DATA", "TEXT"],     // DATA → DATA or TEXT
};
```

## 3. Verified Workflow Chains

### 图片+视频合成 (阿戴's primary use case)
```
imgImport(IMAGE) → videoComposite(IMAGE) ✅
videoImport(VIDEO) → videoComposite(VIDEO) ✅
videoComposite(VIDEO) → export(VIDEO) ✅
```

### 文生图→图生视频→导出
```
imageGen(IMAGE) → img2video(IMAGE) ✅
img2video(VIDEO) → export(VIDEO) ✅
```

### SKU→图片生成→处理→导出
```
skuImport(TEXT) → imageGen(TEXT) ✅
imageGen(IMAGE) → imageProcess(IMAGE) ✅
imageProcess(IMAGE) → sizeAdapter(IMAGE) ✅
sizeAdapter(IMAGE) → export(IMAGE) ✅
```

## 4. onConnect Handler Checks
- ✅ Self-connection blocked: `if (source === target) return`
- ✅ Type mismatch: warn but allow (don't block)
- ✅ Edge style: `{stroke: "#5e6ad2", strokeWidth: 2, type: "smoothstep", animated: true}`

## 5. Common Issues Found
- SKU Import output was DATA → changed to TEXT (connects to prompt inputs)
- Export node only accepted IMAGE → added VIDEO input port
- Type mismatch was blocking connections → changed to warn-only
