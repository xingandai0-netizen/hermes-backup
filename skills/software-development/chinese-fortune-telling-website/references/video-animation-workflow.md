# 视频动画集成工作流（已验证）

## 完整工作流：Canvas → Video → 删除

### 阶段1：Canvas动画实现
- 使用useRef + requestAnimationFrame
- 绘制角色（身体、头、帽子、手臂、腿、扫帚）
- 添加灰尘粒子效果

### 阶段2：替换为MP4视频
用户提供MP4动画文件时：
```tsx
<video autoPlay loop muted playsInline className="w-64 h-64 object-cover rounded-lg shadow-lg">
  <source src="/xiaodaoshi.mp4" type="video/mp4" />
</video>
```

删除Canvas相关代码：
- 删除useRef声明
- 删除useEffect中initAnimation调用
- 删除initAnimation函数
- 删除useRef import

### 阶段3：视频去背景（可选）
用户要求"只要人物，背景透明色"：

```bash
ffmpeg -i input.mp4 \
  -vf "colorkey=0x0a0a0f:0.1:0.2,format=yuva420p" \
  -c:v libvpx-vp9 -b:v 2M -an \
  -y output-transparent.webm
```

页面中使用：
```tsx
<video autoPlay loop muted playsInline className="w-64 h-64 object-cover">
  <source src="/output-transparent.webm" type="video/webm" />
  <source src="/input.mp4" type="video/mp4" />
</video>
```

### 阶段4：完全删除动画
用户说"移除这个动画"时：
- 删除video标签
- 删除相关CSS类
- 保留周围的HTML结构

## ⚠️ Pitfalls

### 1. mix-blend-multiply隐藏视频
视频背景是白色时，`mix-blend-multiply`会使视频与背景融合而不可见。
**解决**：先不加混合模式，确认可见后再调整。

### 2. 视频不自动播放
现代浏览器要求视频静音才能自动播放。
**解决**：必须同时添加`autoPlay`和`muted`属性。

### 3. 删除代码不完整
替换Canvas为Video时，容易遗漏：
- useRef声明
- useEffect中的初始化调用
- initAnimation函数定义
- useRef import

**解决**：系统性删除，检查每个相关代码块。

## 阿戴的动画偏好

**模式**：阿戴会反复调整动画
- 先要动画
- 然后要视频替换
- 然后要去背景
- 最后可能完全删除

**规则**：每次修改都要保留可回退的状态，不要一次性删除所有代码。
