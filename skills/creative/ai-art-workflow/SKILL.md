---
name: ai-art-workflow
description: >-
  AI艺术创作工作流，支持多种模型（Stable Diffusion、FLUX、DALL-E等）。
  提供拖拽式工作流设计，自动化图像生成和处理。
  当用户需要创建艺术作品、图像生成或设计工作流时自动激活。
version: 1.0.0
author: Hermes Agent (基于 DahnM20/ai-flow)
activation: /art
license: MIT
metadata:
  created: 2026-04-17
  sources:
    - https://github.com/DahnM20/ai-flow
    - https://github.com/stability-ai/stability-sdk
---

# /art

AI艺术创作工作流系统，支持多种图像生成模型和自动化处理管道。

## 触发条件

当用户提到以下内容时激活：
- "生成图片"
- "AI绘图"
- "艺术创作"
- "图像设计"
- "create image"
- "generate art"

## 支持的模型

### 文本到图像
| 模型 | 特点 | 适用场景 |
|------|------|---------|
| Stable Diffusion XL | 高质量、开源 | 通用图像生成 |
| FLUX | 最新、细节好 | 精细控制 |
| DALL-E 3 | OpenAI出品 | 创意表达 |
| Midjourney风格 | 艺术感强 | 艺术创作 |

### 图像处理
| 功能 | 描述 |
|------|------|
| 图像修复 | 移除不需要的元素 |
| 图像扩展 | 扩展画布边界 |
| 风格转换 | 转换艺术风格 |
| 图像放大 | 提高分辨率 |

## 工作流设计

### 基础工作流
```
输入提示词 → 模型选择 → 参数配置 → 生成 → 后处理 → 输出
```

### 高级工作流
```
1. 初始生成 (Stable Diffusion)
   ↓
2. 细节增强 (FLUX)
   ↓
3. 风格调整 (Style Transfer)
   ↓
4. 质量提升 (Upscaler)
   ↓
5. 输出保存
```

## 使用方法

### 快速生成
```python
# 使用现有工具生成图像
from hermes_tools import generate_image

result = generate_image(
    prompt="一只可爱的猫咪，赛博朋克风格",
    model="stable-diffusion-xl",
    width=1024,
    height=1024
)
```

### 批量生成
```python
# 批量生成多张图像
prompts = [
    "未来城市",
    "太空站",
    "机器人花园"
]

for prompt in prompts:
    generate_image(prompt, output_dir="./generated")
```

## 参数配置

### 常用参数
```yaml
generation:
  width: 1024
  height: 1024
  steps: 30
  cfg_scale: 7.5
  sampler: "DPM++ 2M Karras"
  
style:
  preset: "digital-art"  # 或 photographic, anime, etc.
  quality: "hd"
```

### 风格预设
| 预设 | 描述 |
|------|------|
| digital-art | 数字艺术风格 |
| photographic | 照片写实风格 |
| anime | 动漫风格 |
| oil-painting | 油画风格 |
| watercolor | 水彩风格 |

## 集成的API

### 本地运行
```bash
# 使用Stable Diffusion WebUI
python -m accelerate.commands.launch scripts/txt2img.py

# 或使用ComfyUI
python main.py --listen
```

### 云端API
```bash
# Replicate API
export REPLICATE_API_TOKEN="your-token"

# Stability AI API
export STABILITY_API_KEY="your-key"

# OpenAI DALL-E
export OPENAI_API_KEY="your-key"
```

## 输出管理

### 文件命名
```
{日期}_{提示词摘要}_{模型}_{序号}.png
示例: 20260417_cyberpunk-cat_sdxl_001.png
```

### 元数据保存
```json
{
  "prompt": "cyberpunk cat",
  "model": "stable-diffusion-xl",
  "parameters": {...},
  "timestamp": "2026-04-17T15:00:00Z"
}
```
