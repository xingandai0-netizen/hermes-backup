---
name: ascii-creative
description: "ASCII art and video generation. Text-to-ASCII (pyfiglet, cowsay, boxes, image-to-ascii) and video/audio-to-colored-ASCII conversion (MP4/GIF). Use when user wants ASCII art, text banners, image-to-ascii, or ASCII video."
version: 1.0
tags: [ascii, art, video, pyfiglet, cowsay, image-to-ascii, ffmpeg]
---

# ASCII Creative — Art & Video

## ASCII Art (Static)

### Tools
- **pyfiglet**: Text-to-ASCII banners (`pip install pyfiglet`)
- **cowsay**: ASCII cow with speech bubble
- **boxes**: Decorative ASCII boxes
- **image-to-ascii**: Convert images to ASCII art

### Quick Examples
```bash
# Text banner
pyfiglet "Hello World" -f slant

# Cow say
cowsay "Hello!"

# Boxes
echo "content" | boxes -d dog

# Image to ASCII (Python)
python3 -c "
from PIL import Image
img = Image.open('photo.jpg').resize((80, 40))
chars = ' .:-=+*#%@'
for y in range(img.height):
    row = ''
    for x in range(img.width):
        r, g, b = img.getpixel((x, y))[:3]
        gray = int(0.299*r + 0.587*g + 0.114*b)
        row += chars[gray * len(chars) // 256]
    print(row)
"
```

## ASCII Video (Animated)

### Conversion Pipeline
```bash
# Video → ASCII frames → colored ASCII MP4/GIF
ffmpeg -i input.mp4 -vf "scale=120:60" frames/%04d.png

# Process each frame to ASCII
python3 ascii_video.py frames/ --output ascii_output/

# Reassemble
ffmpeg -framerate 24 -i ascii_output/%04d.png -c:v libx264 ascii_video.mp4
```

### Key Parameters
- **Resolution**: 80-120 chars wide for video (balance detail vs readability)
- **FPS**: Match source or reduce to 15-24 for performance
- **Color**: ANSI 256-color or truecolor for colored output
- **Font**: Monospace required (Courier, Consolas, DejaVu Sans Mono)

### Output Formats
- **MP4**: Best for sharing, standard video format
- **GIF**: Best for web/social, supports animation
- **HTML**: Colored ASCII with CSS styling
- **Terminal**: Direct ANSI output

## Consolidated From
| Former Skill | Content |
|---|---|
| `ascii-art` | pyfiglet, cowsay, boxes, image-to-ascii |
| `ascii-video` | Video/audio to colored ASCII MP4/GIF conversion |
