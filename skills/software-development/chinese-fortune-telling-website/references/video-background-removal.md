# 视频去背景技术（ffmpeg colorkey）

## 使用场景

用户要求"只要人物，背景透明色"时，需要去除视频的纯色背景。

## 实现方法

### 1. 分析视频背景颜色

```bash
# 提取第一帧
ffmpeg -i input.mp4 -vframes 1 -y /tmp/frame1.png

# 用vision_analyze查看背景颜色
# 或用ImageMagick获取主要颜色
convert /tmp/frame1.png -colors 5 -unique-colors txt:-
```

### 2. 使用colorkey滤镜去除背景

```bash
ffmpeg -i input.mp4 \
  -vf "colorkey=0x0a0a0f:0.1:0.2,format=yuva420p" \
  -c:v libvpx-vp9 -b:v 2M -an \
  -y output-transparent.webm
```

**参数说明**：
- `colorkey=0x0a0a0f:0.1:0.2`
  - `0x0a0a0f`：要去除的颜色（十六进制RGB）
  - `0.1`：相似度（0-1），越大去除范围越广
  - `0.2`：混合度（0-1），边缘过渡
- `format=yuva420p`：带alpha通道的像素格式
- `libvpx-vp9`：VP9编码器，WebM格式支持透明通道
- `-an`：去除音频
- `-b:v 2M`：视频比特率

### 3. 页面中使用

```tsx
<video autoPlay loop muted playsInline className="w-64 h-64 object-cover">
  <source src="/xiaodaoshi-transparent.webm" type="video/webm" />
  <source src="/xiaodaoshi.mp4" type="video/mp4" />  {/* 回退 */}
</video>
```

## 关键点

1. **WebM VP9是唯一支持透明通道的Web视频格式**
2. 优先加载WebM透明版本，回退到MP4原版
3. `colorkey`的颜色值需要从视频中提取
4. 相似度和混合度需要根据实际效果调整
5. 处理时间较长（5秒视频约25秒）

## 调整参数

如果去除效果不理想：

```bash
# 增大相似度（去除更多相似颜色）
-vf "colorkey=0x0a0a0f:0.2:0.3"

# 减小相似度（只去除精确匹配）
-vf "colorkey=0x0a0a0f:0.05:0.1"

# 调整混合度（边缘更柔和/更锐利）
-vf "colorkey=0x0a0a0f:0.1:0.5"
```

## 已验证案例

- 小道童扫地动画：MP4(1.3MB) → WebM(2MB)，黑色背景透明化
- 颜色：0x0a0a0f（深灰黑色）
- 相似度：0.1，混合度：0.2
