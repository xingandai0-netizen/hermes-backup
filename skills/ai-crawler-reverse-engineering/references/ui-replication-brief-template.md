# 竞品UI 1:1复刻逆向简报模板

**用途**: 当用户要求"原封不动"、"一比一复刻"、"照搬"竞品UI时，用此模板生成逆向简报交给另一个AI执行。

**关键**: 不是风格参考，是逐像素复制。所有样式值必须是getComputedStyle获取的真实值。

---

## 简报开头（必须包含）

```markdown
# [竞品名] 工作空间 UI 1:1 逆向指令

**目标**: 从 [URL] 完整逆向工作空间UI代码，用于1:1复刻到另一个项目。
**要求**: 不是"风格参考"，是逐像素复制。所有样式值、DOM结构、动画参数、交互逻辑必须是真实的。

**登录后进入工作空间页面**（需要有项目才能看到完整UI）。
```

---

## 逆向方法论（必须包含在简报中）

对每个组件，必须获取以下全部信息：

1. **DOM结构** — `element.outerHTML`，保留所有class、data属性、嵌套关系
2. **Computed Styles** — `getComputedStyle(element)`，每个元素的所有计算后样式
3. **CSS动画** — `element.getAnimations()` 或检查 `@keyframes` 规则
4. **事件监听** — `getEventListeners?.(element)`（DevTools）或通过行为推断
5. **动态状态** — hover/selected/active/disabled 各状态的样式变化
6. **响应式** — 不同窗口尺寸下的布局变化

---

## 8类组件清单

### 一、节点系统（最高优先级）

#### 1.1 基础节点结构
- 节点最外层容器的完整HTML + 所有computed styles
- 节点内容区域（图片/视频预览区）的完整HTML + styles
- 节点标题栏（icon + 文字）的完整HTML + styles
- 左右连接点（Handle/PlusIcon）的完整HTML + styles + 位置计算
- 节点的border-radius、box-shadow、backdrop-filter精确值
- 节点宽度

**提取方法**:
1. 在画布上创建一个图片节点
2. 用DevTools选中该节点的最外层div
3. console运行: `copy(getComputedStyle($0))` 获取全部样式
4. 对hover状态: DevTools中强制:hover，再次获取样式
5. 对selected状态: 点击节点选中，获取样式

#### 1.2 Image节点
- 完整DOM结构（从外层到最内层每个元素）
- 图片预览区的样式（object-fit、border-radius、尺寸）
- 左上角类型标签的样式
- 右上角上传胶囊按钮的样式（圆角、背景色、hover效果）
- 无素材时的空状态UI
- 有素材时的预览UI

#### 1.3 Video节点
- 视频缩略图的显示方式（尺寸、object-fit、圆角）
- 视频播放按钮（居中的三角形）的样式
- 视频时长标签的样式
- hover时播放预览的效果
- 视频节点和图片节点的尺寸差异

#### 1.4 Text节点
- 文本内容区域的样式（字体、颜色、行高、padding）
- 文本截断方式（几行后ellipsis?）

#### 1.5 Composite节点（如果有）
- 输入输出Handle的数量和位置
- 合成模式选择器的UI

#### 1.6 连线（Edges）
- 连线的颜色、宽度、样式（实线/虚线）
- 连线的SVG path属性
- animated状态的动画
- 选中连线的颜色/宽度变化
- 连线hover时的变化

---

### 二、控制面板/对话框（最高优先级）

#### 2.1 节点内联控制面板（PromptPanel）
- 面板的完整DOM结构
- 面板的打开/关闭动画（CSS transition/animation完整定义）
- 提示词输入框的完整样式（高度、padding、字体、placeholder颜色、focus边框）
- 模型选择下拉框的样式（按钮 + 下拉列表 + 选项hover）
- 比例/清晰度/时长选择器的样式
- 生成按钮的所有状态样式（默认、hover、click、loading）
- 生成进度条的样式
- 面板中每个元素之间的间距精确值

**提取方法**:
1. 点击节点展开控制面板
2. 逐层展开子元素，记录outerHTML和computedStyles
3. 展开模型下拉框 → 获取下拉列表DOM + 选项样式
4. 模拟生成 → 获取loading/progress状态

#### 2.2 全屏预览对话框（Preview Dialog）
- 遮罩层样式（背景色、模糊度、透明度）
- 对话框容器样式（尺寸、圆角、阴影、最大宽高）
- 打开/关闭动画（scale? fade? slide? 具体参数）
- 图片预览显示方式
- 视频播放器UI（播放/暂停、进度条、音量、全屏、时间显示）
- 关闭按钮样式
- 底部操作栏（下载等）
- ESC关闭行为

---

### 三、画布组件

#### 3.1 画布背景
- 背景色精确值
- 背景点阵的颜色、间距、大小
- cursor样式

#### 3.2 缩放控件（Zoom Controls）
- 位置（左下? 右下?）
- 容器样式（背景、圆角、阴影、padding）
- +/- 按钮样式
- zoom百分比文字样式

#### 3.3 左侧节点面板（NodeSidebar）
- 宽度、背景色、毛玻璃效果
- 展开/收起动画
- 节点类型卡片样式
- 拖拽交互样式

#### 3.4 右键菜单（ContextMenu）
- 容器样式（背景、圆角、阴影、min-width）
- 菜单项样式 + hover
- 分割线样式
- 打开动画

#### 3.5 顶部工具栏（Toolbar）
- 高度、背景色、毛玻璃效果
- Logo/项目名/用户头像样式

---

### 四、动画系统

#### 4.1 CSS动画关键帧
提取所有 @keyframes：
```javascript
const allKeyframes = [];
for (const sheet of document.styleSheets) {
  try {
    for (const rule of sheet.cssRules) {
      if (rule.type === CSSRule.KEYFRAMES_RULE) {
        allKeyframes.push({ name: rule.name, cssText: rule.cssText });
      }
    }
  } catch(e) {}
}
copy(JSON.stringify(allKeyframes, null, 2));
```

#### 4.2 CSS Transition
对每个交互元素获取 transition 属性的精确值：
- transition-duration（0.15s? 0.2s? 0.3s?）
- transition-timing-function（cubic-bezier参数）
- transition-delay

---

### 五、全局样式

#### 5.1 CSS变量
```javascript
const cssVars = {};
for (const sheet of document.styleSheets) {
  try {
    for (const rule of sheet.cssRules) {
      if (rule.selectorText === ':root') {
        for (const prop of rule.style) {
          if (prop.startsWith('--')) {
            cssVars[prop] = rule.style.getPropertyValue(prop);
          }
        }
      }
    }
  } catch(e) {}
}
copy(JSON.stringify(cssVars, null, 2));
```

#### 5.2 字体
- font-family精确值
- 引入方式（@font-face? Google Fonts? CDN?）
- 不同元素的字体大小/粗细/行高/letter-spacing

#### 5.3 滚动条
```css
::-webkit-scrollbar { /* 宽度 */ }
::-webkit-scrollbar-track { /* 背景 */ }
::-webkit-scrollbar-thumb { /* 颜色、圆角 */ }
```

#### 5.4 全局重置
- body的margin/padding/background
- box-sizing设置

---

### 六、交互行为记录

对以下每个交互，记录完整的事件序列和视觉变化：

#### 6.1 节点交互
1. **创建节点**: ghost样式、drop动画、出现动画
2. **选中节点**: 视觉变化、控制面板展开
3. **拖拽节点**: 视觉反馈、释放吸附
4. **删除节点**: 确认、动画、连线处理
5. **连线**: 临时连线样式、可连接Handle高亮、成功/失败反馈

#### 6.2 生成交互
1. **点击生成**: 按钮反馈、loading状态
2. **生成中**: 进度指示、节点内容变化
3. **生成完成**: 结果出现动画、按钮恢复
4. **生成失败**: 错误信息、重试按钮

#### 6.3 画布交互
1. **缩放**: 滚轮行为、控件行为、视觉反馈
2. **平移**: 拖拽行为、cursor变化
3. **框选**: 框选框样式

---

### 七、输出格式要求

每个组件输出为一个完整的React组件（TSX），样式用内联style对象：

```tsx
// 文件: [组件名].tsx
// 来源: [URL] 真实逆向
// 逆向时间: [日期]
// 逆向方法: DevTools + getComputedStyle + getAnimations

/*
 * 原始DOM结构（outerHTML）:
 * [粘贴完整的outerHTML]
 *
 * 原始CSS（相关@keyframes和class规则）:
 * [粘贴相关的CSS规则]
 */

import React, { memo, useState, useCallback } from 'react';

// 精确的样式值（从getComputedStyle获取）
const STYLES = {
  container: {
    width: 252, // 实际测量值
    background: 'rgba(28, 28, 30, 0.7)', // 实际计算值
    backdropFilter: 'blur(12px) saturate(180%)',
    borderRadius: 10.8,
    // ... 所有样式属性
  },
} as const;

// 动画关键帧（完整复制）
const KEYFRAMES = `
  @keyframes nodeNewHighlight {
    0% { ... }
    100% { ... }
  }
`;

export const TapNowNode = memo(function TapNowNode({ ... }) {
  // ...
});
```

---

### 八、验证清单

逆向完成后逐项确认：

- [ ] 节点默认样式（尺寸、颜色、圆角、阴影、backdrop-filter）
- [ ] 节点hover/selected样式变化
- [ ] Handle/PlusIcon的精确样式和位置
- [ ] 控制面板完整DOM + 样式 + 动画
- [ ] 提示词输入框完整样式
- [ ] 模型下拉框完整样式（按钮 + 列表 + 选项）
- [ ] 生成按钮所有状态样式
- [ ] 预览对话框完整DOM + 样式 + 动画
- [ ] 视频播放器UI完整样式
- [ ] 连线样式 + 动画
- [ ] 画布背景样式
- [ ] 缩放控件完整样式
- [ ] 左侧面板完整样式
- [ ] 右键菜单完整样式
- [ ] 顶部工具栏完整样式
- [ ] 所有 @keyframes 动画
- [ ] 所有 CSS 变量
- [ ] 字体引入方式
- [ ] 滚动条样式
- [ ] 所有交互状态变化记录
