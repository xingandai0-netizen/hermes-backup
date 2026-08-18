# 视频动画集成

## 基本用法

```tsx
<video
  autoPlay
  loop
  muted
  playsInline
  className="w-64 h-64 object-cover rounded-lg shadow-lg"
>
  <source src="/animation.mp4" type="video/mp4" />
</video>
```

## 关键属性

| 属性 | 作用 | 必需 |
|------|------|------|
| autoPlay | 自动播放 | ✅ |
| muted | 静音（浏览器要求） | ✅ |
| loop | 循环播放 | ✅ |
| playsInline | iOS内联播放 | ✅ |

## 文件位置

视频文件放在`/public/`目录下，通过`/filename.mp4`访问。

## 样式选项

```tsx
// 基础样式
className="w-64 h-64 object-cover rounded-lg shadow-lg"

// 背景融合（白色背景变透明）
className="w-64 h-64 object-contain mix-blend-multiply"

// 带滤镜
style={{ filter: 'contrast(1.2) brightness(1.1)' }}
```

## ⚠️ Pitfalls

1. **mix-blend-multiply可能隐藏视频**：如果视频背景是白色的，混合后会与页面背景融合而不可见。先不加混合模式测试。

2. **浏览器自动播放策略**：现代浏览器要求视频muted才能autoplay。如果不加muted属性，视频不会自动播放。

3. **视频尺寸**：video标签的width/height CSS属性控制显示大小，不影响视频原始分辨率。用object-cover/object-contain控制裁剪方式。

## 检查视频状态（浏览器控制台）

```javascript
const video = document.querySelector('video');
console.log({
  width: video.videoWidth,
  height: video.videoHeight,
  duration: video.duration,
  currentTime: video.currentTime,
  paused: video.paused,
  readyState: video.readyState  // 4 = 已加载
});
```

## Canvas vs Video 选择

| 场景 | 推荐 |
|------|------|
| 简单几何动画（线条、圆形） | Canvas |
| 复杂角色动画（用户提供视频） | Video |
| 需要交互（点击、拖拽） | Canvas |
| 循环播放装饰动画 | Video |
| 需要动态改变参数 | Canvas |
