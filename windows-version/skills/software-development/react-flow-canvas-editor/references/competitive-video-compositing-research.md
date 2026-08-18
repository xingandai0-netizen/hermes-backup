# 竞品视频合成实现方式调研 (2026-06-08)

## 核心发现

**所有平台都不是直接传多个素材URL给AI模型。** 它们是Agent编排系统，把复杂任务拆分成多个步骤。

## TapNow

- 未公开API文档
- 可能整合多种模型（SVD/Stable Video Diffusion或自研模型）
- 多素材处理：通过Web UI上传素材 → 预处理 → prompt+参考素材驱动视频生成
- 可能使用图生视频+文生视频的组合流程

## Lovart

- **核心架构：Agent驱动的多模型编排**
- 不是自研模型，是AI设计Agent平台
- 接入的视频模型：可灵(Kling) 1.6/2.6、海螺(Hailuo) 01、Google Veo 2/3、Runway Gen-4、Seedance
- **视频合成工作流：**
  1. 脚本规划 — 根据prompt生成文案/脚本和故事板
  2. 图片生成 — 调用Flux、LibLib等图像模型生成分镜图片
  3. 图生视频 — 将图片作为输入传给可灵/Runway等视频模型（每段默认5秒）
  4. 视频拼接 — 通过内置"Video Clipper"工具将多个片段合并
  5. 配音配乐 — 自动生成音乐和配音
  6. 最终合成 — 将所有素材合并为成品
- **不提供公开API**
- 支持一次生成超过1分钟的完整视频

## LiblibAI (哩布哩布AI)

- 中国领先的AI创作平台，2000万+创作者
- 2026年3月推出子产品"LibTV"——一站式AI视频创作平台
- **采用"无限画布+节点式工作流"设计**
- 流程：剧本→分镜→图片→视频，全部在一个界面完成
- 接入的视频模型：
  - **Seedance 2.0**（字节跳动）—— 主推模型
  - 可灵(Kling)（快手）
  - 万相 Wan2.1/Wan2.2（阿里通义）—— 开源
  - Happy Horse 1.0（阿里最新）
  - SVD (Stable Video Diffusion)
- **提供开放API**（AccessKey+SecretKey签名认证）
- 支持ComfyUI工作流
- 图生视频需要上传图片作为首帧

## 对Antoken的启示

### 正确的合成逻辑

不是"把多个素材URL同时传给一个模型"，而是：

1. **图生视频模式**：图片作为首帧（image_urls），prompt描述效果
2. **视频编辑模式**：需要先上传素材到asset系统，用asset://格式引用

### toapis.com seedance-2 的正确用法

```json
{
  "model": "seedance-2",
  "prompt": "让人物手中拿着这支笔",
  "image_with_roles": [{"url": "asset://asset_img_xxx", "role": "reference_image"}],
  "video_with_roles": [{"url": "asset://asset_vid_xxx", "role": "reference_video"}]
}
```

**关键约束：**
- `image_urls` 和 `image_with_roles` 不能同时使用
- `image_with_roles` 必须用 `asset://` 格式（先上传获取asset_id）
- Asset上传后需要等待 `status=active` 才能使用

### 上传流程（4步）

1. 创建Group → `POST /v1/videos/doubao-seedance-2-0/private-avatar/groups`
2. 上传素材 → `POST /v1/videos/doubao-seedance-2-0/private-avatar/assets`
3. 轮询状态 → `GET /v1/videos/doubao-seedance-2-0/private-avatar/assets/{asset_id}`
4. 使用素材 → `asset://asset_id` 格式

详见 `api-model-discovery` skill 的 `references/seedance-2-composite-workflow.md`

## 关键教训

**"先调研竞品，再写代码"原则：**

当API不按预期工作时，不要猜测参数用法，应该：
1. 先查官方API文档
2. 研究竞品（tapnow/lovart/liblibai）是怎么实现的
3. 理解完整的参数规则和约束
4. 再写代码

**阿戴的原话："你要先明白目的逻辑，工作逻辑，代码运行逻辑，调用模型逻辑。再有问题给你删了"**
