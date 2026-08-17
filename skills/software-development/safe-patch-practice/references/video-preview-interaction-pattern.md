# Video Preview Interaction Pattern (TapNow Style)

## 交互设计

### 悬停播放
- 鼠标进入 → 从头播放视频
- 鼠标移开 → 暂停并重置到开头

### 控件区域（悬停时显示）
- 进度条（可拖拽）
- 播放/暂停按钮
- 时间显示
- 播放速度切换
- 静音控制
- 全屏按钮（打开PreviewModal）

### 点击行为
- 单击视频区域 → 显示控制面板（对话交流框）
- 单击全屏按钮 → 打开PreviewModal（放大预览）

## 事件处理规则

### 1. VideoPreview外层div不要放onClick

```tsx
// ❌ 错误 - 阻止事件冒泡到父容器
<div onClick={togglePlay}>
  <video ... />
</div>

// ✅ 正确 - 让事件正常冒泡
<div>
  <video ... />
</div>
```

**原因：** 父容器（VideoNode）需要捕获单击事件来显示控制面板。

### 2. 控件区域用onMouseDown阻止冒泡

```tsx
// ❌ 错误 - onClick阻止会导致子按钮失效
<div onClick={(e) => e.stopPropagation()}>
  <button onClick={togglePlay}>不工作！</button>
</div>

// ✅ 正确 - onMouseDown只阻止拖拽，不影响click
<div onMouseDown={(e) => e.stopPropagation()}>
  <button onClick={togglePlay}>正常工作</button>
</div>
```

### 3. 控件按钮也用onMouseDown

```tsx
<button
  onClick={togglePlay}
  onMouseDown={(e) => e.stopPropagation()}
>
  Play/Pause
</button>
```

## 父容器（VideoNode）实现

```tsx
// 预览框 - 单击显示控制面板
<div
  onClick={(e) => {
    e.stopPropagation();
    setShowControls(true);
  }}
  style={{
    cursor: "pointer",
    background: "#1a1a1a",
    position: "relative",
  }}
>
  <VideoPreview
    src={proxyUrl(previewUrl)}
    hoverToPlay
    onExpand={() => setShowPreview(true)}
  />
</div>

// 控制面板 - 条件渲染
{showControls && (
  <div onMouseDown={(e) => e.stopPropagation()}>
    <textarea placeholder="描述任何你想要生成的内容" />
    <select>模型选择</select>
    <button onClick={handleGenerate}>生成</button>
  </div>
)}
```

## 常见错误

### 错误1：单击变成暂停视频
**原因：** VideoPreview外层div有onClick={togglePlay}
**修复：** 移除外层div的onClick

### 错误2：单击不显示控制面板
**原因：** VideoPreview的onClick阻止了事件冒泡
**修复：** 让事件正常冒泡到父容器

### 错误3：控件区域按钮不工作
**原因：** 控件区域用onClick阻止冒泡
**修复：** 改用onMouseDown阻止冒泡

### 错误4：放大预览和对话交流框混淆
**区分：**
- "对话交流框" = 控制面板（输入提示词、选择模型）
- "放大预览" = PreviewModal全屏模态框
- 单击 → 显示控制面板
- 全屏按钮 → 打开PreviewModal

### 错误5：单击变成暂停视频（VideoPreview外层div残留onClick）
**原因：** VideoPreview外层div有`onClick={togglePlay}`，阻止了事件冒泡
**修复：** 完全移除外层div的onClick，不要改成其他handler
**验证：** 检查VideoPreview组件的return中第一个div是否还有onClick

### 错误6：ReactFlow空的onNodeDoubleClick仍然拦截
**尝试：** `onNodeDoubleClick={() => {}}` → 仍然拦截双击
**修复：** 完全移除onNodeDoubleClick prop和handler，不要传空函数

## 控制面板弹出动画

```css
/* globals.css */
@keyframes popUp {
  from {
    opacity: 0;
    transform: translateY(8px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
```

```tsx
// 控制面板使用弹性动画
<div style={{
  animation: "popUp 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
}}>
  {/* 输入框、模型选择、生成按钮 */}
</div>
```

**动画参数说明：**
- `cubic-bezier(0.34, 1.56, 0.64, 1)` — 弹性曲线，有轻微回弹效果
- `0.25s` — 速度适中，不会太快也不会太慢
- `translateY(8px)` — 从下方滑入
- `scale(0.96)` — 带轻微缩放，增加"弹出"感
