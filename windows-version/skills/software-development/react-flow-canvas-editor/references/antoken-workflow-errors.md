# Antoken Workflow Logic — Error Archive & Solutions

## Critical: "no images in AIX generateContent response"
- **Cause:** Video URL passed as `image_urls` to image generation API
- **Fix:** API handles video URLs natively — just pass them directly in `image_urls`, API extracts frames internally
- **Wrong approach:** Extracting frames locally with ffmpeg → localhost URLs not accessible from external API

## Critical: elif Logic Only Selects One Material
- **Cause:** `if video: ... elif images: ...` means only one type gets passed
- **Fix:** Use `all_urls = []` + `if video: all_urls.extend()` + `if images: all_urls.extend()` pattern
- **Applied to:** Both generate_image (image_urls) and generate_video (image_with_roles/video_with_roles)

## Critical: quota_not_enough
- **Cause:** toapis.com account balance depleted
- **Fix:** User must recharge account — not a code issue

## API Constraints (toapis.com)
1. `image_urls` and `image_with_roles` cannot be used simultaneously
2. Reference images must be uploaded via `/assets/upload` to get `asset_id`, then passed as `asset://asset_id` format
3. Direct URLs as reference images cause `UnsupportedImageFormat` error

## Workflow Logic Principle (DO NOT CHANGE WITHOUT CONSULTING)
All generation nodes MUST reference ALL upstream connected materials:
- 图图生图 (image-image-to-image)
- 图视频生图 (image-video-to-image)
- 图视频生视频 (image-video-to-video)
- 视频视频生视频 (video-video-to-video)

Data flow: `reference_image_urls: List[str]` + `reference_video_urls: List[str]`
Video generation uses `image_with_roles` + `video_with_roles` arrays
