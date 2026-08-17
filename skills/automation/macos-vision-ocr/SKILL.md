---
name: macos-vision-ocr
description: Use macOS Vision framework to OCR screenshots when AI vision models are unavailable. Fallback for MiMo or other models that don't support image input.
tags: [ocr, vision, screenshot, macos, fallback]
triggers:
  - "analyze screenshot"
  - "read screenshot text"
  - "OCR screenshot"
  - "vision not supported"
  - "image input not available"
---

# macOS Vision OCR for Screenshots

When the AI model doesn't support image input (e.g., MiMo returns 404 for vision), use macOS's built-in Vision framework to extract text from screenshots.

## When to Use
- `vision_analyze` fails with "does not support vision" or "image input"
- `browser_vision` fails with "vision model not supported"
- Need to read text from a screenshot file on macOS

## Swift Approach (Preferred)

```bash
swift -e '
import Vision
import AppKit

let url = URL(fileURLWithPath: "/tmp/screenshot.png")
guard let image = NSImage(contentsOf: url),
      let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("Cannot load image")
    exit(1)
}

let request = VNRecognizeTextRequest()
request.recognitionLanguages = ["en-US", "zh-Hans"]
request.usesLanguageCorrection = true

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
try handler.perform([request])

if let results = request.results {
    for obs in results {
        if let candidate = obs.topCandidates(1).first {
            print(candidate.string)
        }
    }
}
'
```

## Screenshot Capture

```bash
# Full screen
screencapture -x /tmp/screen.png

# Specific window by PID
screencapture -l$(osascript -e 'tell application "System Events" to tell process "AppName" to get id of first window') /tmp/window.png
```

## Pitfalls
- `objc` Python module not available by default on macOS — use Swift instead
- `screencapture` without `-x` plays shutter sound
- Window capture requires the app to have a visible window
- OCR accuracy varies — UI text is usually good, code/fonts may have errors
- For large screenshots, pipe output through `head -80` to keep output manageable
