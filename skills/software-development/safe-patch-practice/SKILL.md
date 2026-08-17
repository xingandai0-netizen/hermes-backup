---
name: safe-patch-practice
description: 安全修改代码的实践规范，避免误删或破坏现有功能。包含"先研究后动手"的工作流程。
triggers:
  - 修改代码
  - patch
  - 修复bug
  - 删除重复
  - 缝缝补补
  - 做事做一半
---

## 🔴 UI替换铁律：增量CSS修改 ≠ 1:1复刻

**场景**: 用户说"原封不动替换"、"一比一复刻"、"照搬"某个UI到当前项目。

**错误做法** (会导致用户极度不满并git回退):
- 只改CSS变量值（把oklch改成hex）
- 只改inline style（borderRadius: 12→16）
- 只改颜色、圆角、阴影等视觉属性
- 保留原有组件结构，只"美化"外观

**正确做法**:
1. 获取目标UI的完整DOM结构（outerHTML）
2. 获取每个元素的computed styles
3. **整个组件结构替换** — 不是改CSS，是用目标的DOM结构重写组件
4. 保留业务逻辑（事件处理、状态管理、API调用），替换视觉层

**判断标准**: 如果用户给你目标代码，你必须直接用那些代码替换组件，而不是"参考风格"修改现有组件。用户能一眼看出是"改了CSS"还是"换了组件"。

**教训来源**: 2026-07-05 阿戴要求1:1复刻TapNow UI到antoken-v2，小黑只改了CSS变量和inline style，阿戴说"改了个寂寞"并git reset --hard回退全部改动。

## ⚠️ CRITICAL: Claiming Changes Without Verification (2026-07-04 学到)

**NEVER claim a change is done without verifying it's actually in the code.** This session caused massive rework because I repeatedly said "已完成" when the patch didn't actually apply.

**Failure modes:**
1. **Patch silently fails** — `hermes_tools.patch()` returns success but the old text didn't match (whitespace, line breaks, encoding)
2. **Build passes but change wasn't applied** — TypeScript errors can mask missing changes
3. **"Deployed" without verifying file content** — Deploy succeeds but old code is still there

**Verification checklist (MANDATORY after every code change):**
1. Read the changed file at the specific line using `search_files` or `read_file`
2. Run `npm run build` / `python -m pytest`
3. Only then claim "done"

**User frustration signal:** "为什么没落实前面" / "你声称已修复但实际没有" = IMMEDIATELY re-verify all claimed changes

**问题**：我多次尝试"参考 v1 风格重写"代码，结果引入 bug。用户明确要求"v1 代码必须原样复制"。

**正确做法**：
1. 直接复制 v1 文件：`cp v1-file.tsx v2-file.tsx`
2. 只更新导入路径（camelCase → kebab-case）
3. 只更新状态管理（Zustand → Jotai）
4. 不改任何业务逻辑
5. **逐行对比确保一致** — 不能遗漏任何细节

**错误做法**：
- "参考 v1 风格重写" → 丢失细节
- "用 shadcn 组件替代原生 select" → 样式不兼容
- "用 CSS 变量替代内联样式" → 暗色模式问题
- "优化"或"改进" v1 代码 → 引入新 bug

**用户原话**（2026-07-03）：
> "v1代码必须原样复制不能'参考风格重写'"
> "左侧栏用v1风格"
> "Canvas必须复制v1不要重写"

**2026-07-04 补充**：
> "不是让你改回去风格，是要和之前未开始重构antoken项目前备份的所有ui一模一样"
> "你仔细检查一下v1和v2的代码区别，别有任何再遗漏的了"

**教训**：v1 代码是经过用户验证的，任何"改进"都可能引入 bug。必须原样复制，只更新必要的导入路径和状态管理。

### 0. 研究阶段（动手前必做）
- 阅读API文档，理解参数和返回值
- 检查现有代码的完整逻辑，不要只看局部
- 如果有多个相关组件，全部检查一遍
- 确认修改方案后再动手

**v1 代码必须原样复制（2026-07-03 确认）**：阿戴明确要求"v1 代码必须原样复制，不能参考风格重写"。正确做法：cp 直接复制 → 只更新导入路径 → 不改业务逻辑/样式/交互。错误做法：参考 v1 重写简化版（会丢失功能）、用 shadcn 组件替换原生组件（样式可能不兼容）。

**⚠️ v1/v2 代码迁移必须对比（2026-07-03 教训）**：
修改任何从 v1 复制的组件前，必须先对比 v1 和 v2 的差异。用 `diff` 或逐行对比，找出所有不同点。确认每个差异是有意的还是遗漏的。如果是遗漏，立即补上。
案例：Canvas 缺少右键菜单/文件拖拽/边高亮、代理端点缺失、后端返回字段不一致。

### 1. 修改前

**用户典型反馈**：
- "不要缝缝补补" → 说明你没理解完整逻辑就动手了
- "做事做一半" → 说明你只改了一个地方，没改其他相关地方
- "先搞明白再修改" → 说明你边改边猜，浪费时间

### 1. 修改前
- 读取完整文件，理解所有条目/组件的关系
- 确认要修改的内容不会影响其他部分
- 如果是删除操作，先列出所有要保留的项目

### 2. 修改时
- 使用精确匹配，不用模糊替换
- patch内容要包含足够的上下文，确保唯一性
- 删除重复条目时，逐个检查每个条目，不要批量删除

### 3. 修改后
- 读取修改后的文件，验证所有条目完整
- 检查是否有意外删除或遗漏
- 确认功能正常后再告诉用户

## 典型错误案例

### 错误1: read_file/write_file 导致文件损坏

**场景**: 使用 `read_file` 读取文件后，用 `write_file` 写回修改。

**问题**: `read_file` 返回的内容包含行号前缀（如 `1|content`），`write_file` 会把这些行号也写入文件，导致文件损坏。

**错误表现**:
```
1|"use client";
2|
3|import React from "react";
```

**正确做法**: 使用 `patch` 工具而不是 `read_file` + `write_file`。

```typescript
// ❌ 错误做法
const result = read_file("file.tsx");
write_file("file.tsx", result["content"]);  // 行号也被写入

// ✅ 正确做法
patch({
  mode: "patch",
  patch: `*** Begin Patch
*** Update File: file.tsx
@@ context @@
-old line
+new line
*** End Patch`
});
```

**如果必须用 read_file**: 先去除行号再写入。

### 错误2: CSS !important 覆盖内联样式

**场景**: 修改React组件的内联样式（如边颜色），但页面没有变化。

**原因**: globals.css中使用了 `!important`，会覆盖内联样式。

**正确做法**: 必须同时修改CSS和内联样式。

```css
/* globals.css */
.react-flow__edge-path {
  stroke: #ffffff !important;  /* 必须改这里 */
}
```

```typescript
// workflowStore.ts
style: { stroke: "#ffffff", strokeWidth: 2 }  /* 也要改 */
```

## 检查清单
```javascript
// 原始文件有：
{ type: "img2video", ... },  // 重复
{ type: "videoComposite", ... },  // 需要保留
{ type: "img2video", ... },  // 重复

// 错误做法：直接删除整个块，导致videoComposite也被删
// 正确做法：只删除重复的img2video行，保留videoComposite
```

### 错误2：修复一个问题时破坏另一个功能
```javascript
// 修复img2video重复时，不小心把videoComposite也删了
// 用户反馈："为什么没经过我同意给他删了？"

// 根因：patch的old_string匹配范围太大，包含了不需要修改的内容
// 正确做法：精确匹配，只修改目标行
```

### 正确的删除方式
1. 先读取文件，列出所有条目
2. 确定哪些要删除，哪些要保留
3. 使用精确的old_string匹配，只删除目标行
4. 修改后重新读取文件验证

## 检查清单

- [ ] 修改前读取完整文件
- [ ] 列出所有要保留的项目
- [ ] 确认修改范围
- [ ] 修改后读取修改后的文件
- [ ] 验证所有项目完整
- [ ] 测试功能正常

## toapis.com API 文本生成格式（2026-07-05 教训）

**问题**：文本生成 API 返回 500 错误，因为使用了错误的请求格式。

**错误格式**：
```python
body = {"prompt": "写一段产品描述", "model": "gemini-3.5-flash"}
```

**正确格式**（OpenAI 兼容）：
```python
body = {
    "messages": [{"role": "user", "content": "写一段产品描述"}],
    "model": "gemini-3.5-flash"
}
```

**规则**：toapis.com 的 `/chat/completions` 端点使用 OpenAI 兼容格式，必须用 `messages` 数组，不是 `prompt` 字段。

## 图片预览优化模式（2026-07-05）

**问题**：AI 生成的 2K/4K 图片（2-5MB）直接在 320px 预览框中显示，导致"从上到下慢慢加载"。

**解决方案**：后端代理增加图片缩放能力，前端请求时传入预览尺寸。

**前端修改**：
```typescript
// lib/media-proxy.ts
export function proxyUrl(url: string, width?: number, height?: number): string {
  const base = `${getApiBase()}/api/generate/proxy?url=${encodeURIComponent(url)}`;
  if (width && height) {
    return `${base}&width=${width}&height=${height}`;
  }
  return base;
}

// 使用
<img src={proxyUrl(previewUrl, 320, previewHeight)} />
```

**后端修改**（Pillow 缩放 + 本地缓存）：
```python
@router.get("/generate/proxy")
async def proxy_media(url: str, width: int = None, height: int = None):
    # ... 获取原图 ...
    if width and height and content_type.startswith("image/"):
        cache_key = hashlib.md5(f"{url}_{width}_{height}".encode()).hexdigest()
        # 缩放并缓存
```

**规则**：预览图应使用缩略图代理，不直接下载原图。

## Python 文件修改验证规则（2026-07-05 教训）

**问题**：Python 文件的 patch 可能静默失败，特别是当字符串包含特殊字符（引号、花括号）时。

**正确做法**：
```bash
# 修改后必须验证
grep -n "raise ValueError\|logger.warning" app/config.py
# 确认输出中只有 raise ValueError，没有 logger.warning
```

**规则**：Python 文件修改后必须用 grep 验证修改生效。

**详细的安全/不安全优化清单：** 参见 `references/reactflow-performance-optimization.md`

## Testing Changes Individually

**CRITICAL (2026-06-14):** When making multiple "optimization" changes, NEVER batch them together. Test each change individually before adding the next.

**Problem Pattern:**
1. Add `onlyRenderVisibleElements={true}` — page freezes
2. Add `elevateNodesOnSelect={false}` — clicks stop working
3. Add `deleteKeyCode={null}` — keyboard events break
4. All three changes together = completely broken UI

**Correct Pattern:**
1. Add `onlyRenderVisibleElements={true}` → refresh browser → test
2. If works, add `elevateNodesOnSelect={false}` → refresh browser → test
3. If works, add `deleteKeyCode={null}` → refresh browser → test
4. If any step fails, revert that change and investigate

**Rule:** When optimizing ReactFlow, CSS, or any UI framework, change ONE option at a time, refresh browser, test interactions. Never batch multiple "optimization" options.

## Testing Changes Individually (CRITICAL 2026-06-14)

**When making multiple "optimization" changes, NEVER batch them together. Test each change individually before adding the next.**

**Problem Pattern:**
1. Add `onlyRenderVisibleElements={true}` → page freezes
2. Add `elevateNodesOnSelect={false}` → clicks stop working
3. Add `deleteKeyCode={null}` → keyboard events break
4. All three changes together = completely broken UI

**Correct Pattern:**
1. Add ONE option → refresh browser → test interactions
2. If works, add next option → refresh browser → test
3. If any step fails, revert that change and investigate
4. Never batch multiple "optimization" options

**Rule:** When optimizing ReactFlow, CSS, or any UI framework, change ONE option at a time, refresh browser, test interactions.

## React.memo on ReactFlow Nodes (CRITICAL 2026-06-14)

**DO NOT use React.memo on ReactFlow node components.**

```tsx
// ❌ DANGEROUS - breaks ReactFlow event handling
const VideoNode = React.memo(function VideoNode(props: NodeProps) { ... });
export default VideoNode;

// ✅ SAFE - use function export
export default function VideoNode(props: NodeProps) { ... }
```

**Symptoms:** Page loads, nodes render, but clicks don't work on nodes.

**Root cause:** React.memo's comparison function prevents necessary re-renders for ReactFlow's internal event handling.

**2026-06-14 教训追加：** 只移除一个transform不够——如果页面还卡，说明有其他优化也在造成问题。不要一个一个排查，直接 **git checkout 回到最后一个能用的commit**，把所有优化全部撤掉。

```bash
# 查看最近commit
cd ~/antoken/frontend
git log --oneline -5

# 回到最后一个正常工作的commit
git checkout <last-working-commit> -- src/
rm -rf .next
npm run dev
```

**原则：** 优化导致回归时，不要试图"修好"优化——直接回退所有优化代码，确认页面恢复正常后，再一个一个重新加。用户原话："没性能优化前是正常的"。

## UI重构模式：批量修改同类组件（2026-06-15）

**场景：** 需要修改多个相似组件的UI（如所有节点的预览框）

**正确流程：**
1. 先修改一个组件作为模板（如VideoNode）
2. 测试通过后，再应用到其他组件
3. 每个组件修改后都要验证
4. 保持底层逻辑不变，只改UI

**关键原则：**
- 所有相似组件使用相同的UI模式
- 状态变量命名一致（如`showControls`）
- 样式值一致（圆角、颜色、间距）
- 动画效果一致（transition、animation）

**Antoken节点UI重构示例：**
```tsx
// 1. 添加状态
const [showControls, setShowControls] = useState(false);

// 2. 预览框 - 点击展开
<div onClick={() => setShowControls(!showControls)} style={{...}}>
  {/* 预览内容 */}
</div>

// 3. 控制面板 - 条件渲染
{showControls && (
  <div style={{...}}>
    {/* 控制内容 */}
  </div>
)}
```

## Viewport-Based Node Positioning (2026-06-15)

**问题：** 新创建的节点出现在画布固定位置 (300, 150)，而不是当前视口中心。

**解决方案：** 在 Zustand store 中存储 viewport 状态，创建节点时计算当前视口中心位置。

```typescript
// 1. Store 中添加 viewport 状态
interface WorkflowState {
  viewport: { x: number; y: number; zoom: number };
  updateViewport: (viewport: { x: number; y: number; zoom: number }) => void;
}

// 2. Canvas 监听 onMove 事件
const onMove = useCallback((_, viewport) => {
  updateViewport(viewport);
}, [updateViewport]);

<ReactFlow onMove={onMove} />

// 3. 创建节点时计算中心位置
const centerX = (-viewport.x + window.innerWidth / 2) / viewport.zoom;
const centerY = (-viewport.y + window.innerHeight / 2) / viewport.zoom;

const newNode = {
  position: { x: centerX - 140, y: centerY - 100 },
};
```

## Handle Styling Optimization (2026-06-15)

**问题：** 连接线节点（Handle）太小，不好选中。

**解决方案：**
1. 放大到 16×16px（原 14×14px）
2. 位置外移到 -10px（原 -7px）
3. 3层 glow 效果增强可见性

```typescript
const handleStyle = {
  width: 16,
  height: 16,
  background: categoryColor,
  border: "2px solid #0a0a0f",
  borderRadius: "50%",
  boxShadow: isHovered
    ? `0 0 14px ${categoryColor}, 0 0 6px ${categoryColor}80, 0 0 3px ${categoryColor}60`
    : `0 0 10px ${categoryColor}70, 0 0 4px ${categoryColor}50`,
  transition: "all 0.2s ease",
};

<Handle style={{ ...handleStyle, left: -10 }} />
<Handle style={{ ...handleStyle, right: -10 }} />
```

## Delete Key Smart Handling (2026-06-15)

**问题：** 焦点在输入框时，Delete 键无法删除节点。

**解决方案：** 检查输入框是否有内容，只有输入框为空时才删除节点。

```typescript
if ((e.key === "Delete" || e.key === "Backspace") && selectedNodeId) {
  if (isInputFocused) {
    const inputValue = (target as HTMLInputElement | HTMLTextAreaElement).value;
    if (inputValue && inputValue.length > 0) {
      return; // 输入框有内容，不删除节点
    }
  }
  e.preventDefault();
  removeNode(selectedNodeId);
}
```

## Handle (Connection Point) 最终优化配置 (2026-06-15)

**用户反复要求：** 连接线节点要大、离素材框远、hover放大、向外扩展不贴素材框。

```typescript
const handleStyle = {
  width: 20,
  height: 20,
  background: categoryColor,
  border: "2px solid #0a0a0f",
  borderRadius: "50%",
  boxShadow: isHovered
    ? `0 0 20px ${color}, 0 0 10px ${color}80, 0 0 5px ${color}60`
    : `0 0 10px ${color}70, 0 0 4px ${color}50`,
  transition: "all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)",
  transform: isHovered ? "scale(1.5)" : "scale(1)",
};

// 左侧handle - transform-origin: right center（向左扩展）
<Handle style={{ ...handleStyle, left: -20, zIndex: 20, transformOrigin: "right center" }} />
// 右侧handle - transform-origin: left center（向右扩展）
<Handle style={{ ...handleStyle, right: -20, zIndex: 20, transformOrigin: "left center" }} />
```

**关键参数：**
- 大小：20×20px（14太小，16勉强，20合适）
- 距离：-20px（-7太近，-14还贴着，-20刚好）
- Hover缩放：1.5倍 + 弹性曲线
- 虚光：3层box-shadow

### Handle Hover Zone 扩展（2026-06-15）

**问题：** Handle 需要在素材框周围 40px 内都能被 hover 触发显示，但不能改变素材框本身的布局。

**错误做法：** 用透明 div 做 hover 检测区域（z-index 问题导致素材框内的 hover 不触发）

**正确做法：** 在外层容器上用 padding + margin 技巧扩展 hover 检测范围

```tsx
const HOVER_ZONE = 40;

<div
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}
  style={{
    position: "relative",
    width: 280,
    padding: HOVER_ZONE,    // 扩展 hover 检测范围
    margin: -HOVER_ZONE,    // 补偿布局偏移
  }}
>
  {/* 素材框本体 - 保持不变 */}
  <div style={{ width: 280, ... }}>
    {children}
  </div>

  {/* Handle 位置需要加上 HOVER_ZONE 偏移 */}
  <Handle style={{ ...handleStyle, left: HOVER_ZONE - 28 }} />
  <Handle style={{ ...handleStyle, right: HOVER_ZONE - 28 }} />
</div>
```

**关键点：**
- padding 扩展外层容器的 hover 检测区域
- margin 负值补偿，不影响 ReactFlow 的节点定位
- Handle 位置需要加上 HOVER_ZONE 偏移（因为 padding 改变了内容区域的起点）
- 素材框本身不需要任何修改

### Handle 延迟隐藏（2026-06-15）

**问题：** 用户在使用连接线时，鼠标移开素材框区域后连接节点立即消失，导致无法完成连接。

**解决方案：** 鼠标离开后延迟 10 秒才隐藏连接节点。

```tsx
const hideTimerRef = useRef<NodeJS.Timeout | null>(null);

const handleMouseEnter = useCallback(() => {
  if (hideTimerRef.current) {
    clearTimeout(hideTimerRef.current);
    hideTimerRef.current = null;
  }
  setIsHovered(true);
}, []);

const handleMouseLeave = useCallback(() => {
  hideTimerRef.current = setTimeout(() => {
    setIsHovered(false);
  }, 10000); // 10秒后隐藏
}, []);
```

**规则：** 连接节点的显示/隐藏使用延迟机制，给用户足够时间完成连接操作。

## Viewport-Aware Node Placement (2026-06-15)

**问题：** 新节点总是出现在画布固定位置(300,150)，不在当前视口中心。

**解决方案：** Zustand store存储viewport，创建节点时计算视口中心。

```typescript
// Store
viewport: { x: 0, y: 0, zoom: 1 },
updateViewport: (viewport) => set({ viewport }),

// Canvas - 监听onMove
const onMove = useCallback((_, viewport) => updateViewport(viewport), [updateViewport]);
<ReactFlow onMove={onMove} />

// Sidebar - 计算中心
const centerX = (-viewport.x + window.innerWidth / 2) / viewport.zoom;
const centerY = (-viewport.y + window.innerHeight / 2) / viewport.zoom;
newNode.position = { x: centerX - 140, y: centerY - 100 };
```

## Delete Key Smart Handling (2026-06-15)

**问题：** 焦点在输入框时Delete键无法删除节点。

**解决方案：** 输入框为空时仍可删除节点。

```typescript
if ((e.key === "Delete" || e.key === "Backspace") && selectedNodeId) {
  if (isInputFocused) {
    const inputValue = (target as HTMLInputElement | HTMLTextAreaElement).value;
    if (inputValue && inputValue.length > 0) return; // 有内容不删节点
  }
  e.preventDefault();
  removeNode(selectedNodeId);
}
```

## VideoPreview TapNow-style 交互 (2026-06-15)

**详细模式见 `references/video-preview-interaction-pattern.md`**

核心规则：
1. Hover播放/Leave暂停
2. 单击显示控制面板（对话交流框）
3. 全屏按钮打开PreviewModal
4. **外层div绝对不能有onClick**（会阻止冒泡）
5. 控件区域用onMouseDown阻止拖拽，不用onClick

## 多参考架构模式（2026-07-05）

**问题**：上游素材被简单收集为 URL 列表，没有角色区分。

**解决方案**：
```typescript
// types/workflow-v1.ts
export type ReferenceRole = 'style' | 'subject' | 'composition' | 'content';

// hooks/use-upstream-data.ts
export interface UpstreamNode {
  node: Node<NodeData>;
  edge: Edge;
  assetName: string;
  assetType?: string;
  assetUrl?: string;
  role: ReferenceRole; // 从 edge.targetHandle 获取
}
```

**规则**：参考素材必须有角色（style/subject/composition/content），不能只是 URL 列表。

## 参数透传规则（2026-07-05）

**核心原则**：用户设置的每个参数都必须 100% 传递到 AI API。

**常见断裂点**：
1. 字段名不匹配：前端 `ratio` vs 后端 `aspect_ratio`
2. Schema 缺失字段：前端发送 `video_mode`，后端未定义
3. 参数位置错误：`resolution` 包装在 `metadata` 中
4. 参考数据丢失：`reference_images` 未在 Schema 中定义

**规则**：前端发送的每个字段都必须有对应的后端 Schema 定义，字段名必须一致或后端做映射。

## JSX中引用未定义的ref导致构建失败（2026-07-04）

**问题**：在JSX中添加了 `fileInputRef.current` 的引用（如上传按钮的onClick），但忘记在组件中定义 `const fileInputRef = useRef<HTMLInputElement>(null)`。

**症状**：`npm run build` 报 `Type error: Cannot find name 'fileInputRef'`

**根因**：从指令复制代码时，只复制了JSX部分（按钮+隐藏input），忘记复制ref定义行。

**修复**：在组件的 `useRef` 声明区域添加：
```tsx
const fileInputRef = useRef<HTMLInputElement>(null);
```

**规则**：添加任何 ref 引用时，必须同时确认 ref 已定义。检查清单：
- [ ] `useRef` 声明存在
- [ ] 类型泛型正确（`HTMLInputElement`、`HTMLVideoElement` 等）
- [ ] JSX中的ref名称和声明名称完全一致

## execute_code 50 tool call limit（2026-07-04 教训）

**问题**：`execute_code` 有 50 tool call 限制。当脚本中调用超过 50 次工具时，后续调用**静默失败**——不报错，不写入文件，脚本继续执行。

**实际案例**：用 execute_code 循环读取 70+ 个源文件并写入模块文件。前 50 个文件成功，后面的文件静默跳过，导致模块文件不完整。

**正确做法**：
- 超过 30 个文件操作时，用 `terminal` + shell 命令代替 `execute_code`
- 或将任务拆分为多个 execute_code 调用（每个 < 40 次工具调用）
- 写入后必须验证文件大小和行数

**验证**：
```bash
wc -l /tmp/output-file.txt  # 检查行数是否合理
head -5 /tmp/output-file.txt  # 检查内容
tail -5 /tmp/output-file.txt  # 检查结尾是否完整
```

## tail -n +N 空文件陷阱（2026-07-04 教训）

**问题**：`tail -n +N` 当 N 大于文件总行数时，输出为空（0 bytes），不报错。

**实际案例**：
```bash
# 文件只有 797 行
head -415 file.tsx > before.tsx   # ✅ 415 行
tail -n +826 file.tsx > after.tsx  # ❌ 0 行（文件只有 797 行！）
cat before.tsx new-controls.tsx after.tsx > file.tsx  # 丢失了 showPreview 部分
```

**根因**：添加状态变量后行号偏移，但 tail 的行号没有更新。

**正确做法**：
1. 用 `wc -l` 确认文件总行数
2. 用 `grep -n` 确认目标行号
3. tail 的起始行必须 < 文件总行数
4. 组合后验证：`wc -l` + `tail -5` 检查结尾是否完整

**验证清单**：
```bash
wc -l before.tsx after.tsx  # 两个都必须 > 0
tail -3 after.tsx  # 必须包含文件的结尾内容（export, }, 等）
```

## sed追加合并行陷阱（2026-07-04）

**问题**：`sed -i '' '/pattern/a\` 追加多行时，内容可能和已有行合并到同一行。

**修复**：追加后验证行结构，或直接用 patch 工具代替 sed。

## ⚠️ 1:1复刻 vs 风格参考（2026-07-05 教训，最严重）

**用户说"原封不动"、"1:1复刻"、"照搬"、"一比一"时，意思是用目标代码直接替换现有代码，不是"参考风格修改现有代码"。**

**本session严重失败**：用户给了TapNow的真实逆向代码（CSS变量、DOM结构、computed styles），我却用这些数据作为"参考"去修改现有antoken组件的CSS值。结果：
- 用户反馈"改了个寂寞"、"到底在几把改啥"
- 节点卡片、控制面板、侧边栏都没有真正改变
- 浪费了大量时间做无效的CSS微调

**正确做法**：当有目标代码时，直接用目标代码替换现有组件，不要"参考"着改。
- 如果目标代码是React组件 → 直接替换对应组件文件
- 如果目标代码是CSS → 直接替换CSS文件
- 如果目标代码是DOM结构 → 按DOM结构重写组件
- **不要**"把现有组件的borderRadius从12改成16" → 而是"用目标组件替换现有组件"

**用户原话**（2026-07-05）：
> "都有代码了，我说了要一模一样有这么难吗？"
> "不是只有风格一样"
> "你先别管现有的，我直接让另一个ai逆向出全部的你要用的到的"

**区分**：
| 用户说法 | 含义 | 做法 |
|---------|------|------|
| "参考风格" | 学习设计语言 | 提取设计规范，自己实现 |
| "照搬/套用" | 原样复制 | 直接复制代码，只改导入路径 |
| "1:1复刻/原封不动" | 逐像素复制 | 用目标代码完全替换现有代码 |

**当有目标代码时的正确流程**：
1. 读取目标代码的完整结构
2. 读取现有代码的完整结构
3. 用目标代码替换现有代码（不是修改！）
4. 只更新必要的集成点（导入路径、状态管理绑定）
5. 验证构建通过

## Safari DOM逆向提取方法（2026-07-05 验证通过）

**当需要从已登录的网站提取真实UI代码时**，用AppleScript在Safari中执行JavaScript：

```bash
# 方法：base64编码JS → AppleScript执行 → 获取结果
B64=$(base64 -i /tmp/extract.js) && osascript -e "tell application \"Safari\" to tell window N to tell current tab to do JavaScript (do shell script \"echo $B64 | base64 -D\")"
```

**前提**：Safari必须已登录目标网站，且"允许Apple Events执行JavaScript"已开启（Safari → 开发 → 允许JavaScript from Apple Events）。

**提取内容**：
- CSS变量：`document.styleSheets` → `:root` 选择器
- @keyframes动画：`CSSRule.KEYFRAMES_RULE` 类型
- computed styles：`getComputedStyle(element)` 所有属性
- DOM结构：`element.outerHTML` 完整HTML
- 组件定位：`getBoundingClientRect()` 精确位置

**输出格式**：提取的数据直接写入markdown文件，标注来源和提取方法。

## Git回退+部署工作流（2026-07-05 验证通过）

**当需要回退到之前的版本并部署时**：

```bash
# 1. 找到目标commit
git log --format="%h %ai %s" -20

# 2. 回退到目标commit
git reset --hard <commit-hash>

# 3. 推送到GitHub（需要force因为历史 diverged）
git push --force-with-lease origin main

# 4. 手动部署到Vercel（如果GitHub webhook没触发）
cd frontend && npx vercel --prod --yes
```

**关键**：
- `--force-with-lease` 比 `--force` 安全（检查远程是否被他人更新）
- Vercel可能不会自动部署force push，需要手动触发
- 回退后本地的未提交修改会丢失，确保先stash或commit

## 购买模板集成规则（2026-07-04 教训）

**核心教训：当用户说"照搬"、"套用"、"直接用"时，意思是原样复制，不是"参考风格重写"。**

### 错误模式（本session实际发生）
1. 用户给了一套购买的Webflow模板(Cyrclo)，要求"套用"
2. 我理解为"参考风格重新做一个" → 用户说"完全不一样"
3. 我尝试把HTML转成React组件 → 结构丢失，CSS不生效，页面乱码
4. 用户最终说"你直接把这个首页网站照搬上去即可"

### 正确方案：静态HTML + Next.js rewrite

对于购买的HTML模板（Webflow、Framer等），不要尝试转成React组件。直接serve静态HTML：

```javascript
// next.config.mjs
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/',
        destination: '/purchased-template.html',
      },
    ];
  },
};
export default nextConfig;
```

步骤：
1. 复制HTML到 `frontend/public/` 目录
2. 复制CSS到 `frontend/public/css/`
3. 复制JS到 `frontend/public/js/`
4. 在 `next.config.mjs` 添加rewrite规则
5. 构建、部署

### 为什么不能转React
- Webflow模板的JS依赖特定DOM结构和data属性（data-w-id等）
- CSS class名是Webflow生成的，和JS交互绑定
- 转React会丢失：旋转动画、滚动触发、视差效果、交互状态
- 子agent也无法可靠解析136KB的单行HTML

### 用户术语辨别
- "套用" = 原样复制上去
- "照搬" = 原样复制上去
- "参考风格" = 参考设计风格但自己实现
- "基于XX改" = 以XX为基础修改内容

## 禁止事项

1. **禁止模糊删除**：不要用大块文本替换，容易误删
2. **禁止批量操作**：多个修改要分开执行，逐个验证
3. **禁止跳过验证**：修改后必须重新读取文件确认
4. **禁止未经确认就提交**：告诉用户修改了什么，让用户确认
5. **禁止删除功能不告知**：删除任何功能前必须告知用户并获得确认
6. **禁止批量优化**：性能优化必须一个一个加，测试通过再加下一个。用户原话："没性能优化前是正常的"

## v1/v2 代码迁移系统性对比规则（2026-07-03 教训）

**问题**：逐个 bug 修复导致修一个引入另一个，没有系统性对比 v1 和 v2 的差异。

**阿戴纠正原话**：
- "不要这个bug那个bug，这个修改完就出现别的bug"
- "你仔细检查一下v1和v2代码区别，要全面，仔细"

**正确流程**：

### Step 1: 全面对比（动手前必做）
```bash
# 使用 delegate_task 让子 agent 做完整对比
delegate_task({
  goal: "Compare v1 and v2 code for ALL differences",
  context: "List: functions in v1 missing from v2, data structure differences, import differences, state management differences"
})
```

### Step 2: 分类差异
| 类型 | 处理方式 |
|------|---------|
| 导入路径差异 | 批量替换 |
| 状态管理差异 | 重写调用方式 |
| 数据结构差异 | 补全缺失字段 |
| 功能缺失 | 复制 v1 代码 |
| 样式差异 | 复制 v1 样式 |

### Step 3: 一次性修复
- 不要逐个修，要一次性修复所有相关问题
- 修复后必须运行完整测试套件
- 必须在浏览器中实际测试所有功能

### Step 4: 验证清单
- [ ] 所有节点类型都能正常显示
- [ ] 所有交互功能正常（点击、拖拽、右键）
- [ ] 所有生成流程正常（图片、视频、文本）
- [ ] 上下游数据传递正常
- [ ] 没有引入新的 bug

## 定时器内存泄漏规则（2026-07-03 新增）

**规则**：所有 `setInterval`/`setTimeout` 必须有对应的清理逻辑。

```tsx
// ✅ 正确 - 有清理逻辑
const timerRef = useRef<NodeJS.Timeout | null>(null);

useEffect(() => {
  return () => {
    if (timerRef.current) {
      clearInterval(timerRef.current);
    }
  };
}, []);

// 启动新定时器前清除旧的
if (timerRef.current) clearInterval(timerRef.current);
timerRef.current = setInterval(() => { ... }, 3000);
```

## 异步轮询中断规则（2026-07-03 新增）

**规则**：所有异步轮询必须支持中断，使用 `usePollPublicUrl` Hook。

```tsx
// hooks/use-poll-public-url.ts
export function usePollPublicUrl() {
  const abortControllerRef = useRef<AbortController | null>(null);

  const startPolling = useCallback((assetId: string, nodeId: string) => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    const controller = new AbortController();
    abortControllerRef.current = controller;

    (async () => {
      for (let i = 0; i < 30; i++) {
        if (controller.signal.aborted) return;
        await new Promise(r => setTimeout(r, 2000));
        if (controller.signal.aborted) return;
        // ... poll logic
      }
    })();
  }, []);

  useEffect(() => {
    return () => {
      abortControllerRef.current?.abort();
    };
  }, []);

  return startPolling;
}
```

## 数据结构字段完整性规则（2026-07-03 新增）

**问题**：v1 创建节点时同时设置 `nodeType` 和 `assetType`，v2 只设置了 `nodeType`。

**规则**：创建节点时必须设置所有必要字段，参考 v1 的数据结构。

```tsx
// ✅ 正确 - 和 v1 一致
const newNode = {
  id: `${type}_${Date.now()}`,
  type,
  data: {
    label,
    category,
    nodeType: type,
    assetType: type === 'IMAGE' ? 'IMAGE' : type === 'VIDEO' ? 'VIDEO' : 'TEXT',
    config: {},
    assetName,
  },
};
```

**验证清单**：
- [ ] 对比 v1 的 `NodeData` 类型定义
- [ ] 确认所有字段都有设置
- [ ] 确认字段名称一致（不是 `nodeType` vs `assetType` 混用）

当修复一个节点/组件的问题后，必须：
1. 检查所有其他节点/组件是否有同样的问题
2. 统一应用相同的修复模式
3. 不要只修一个就报告完成

**"做事做一半"** — 用户期望所有相关地方都修好，不是只修一个。

## 性能优化陷阱（2026-06-14 教训）

**"没性能优化前是正常的"** — 用户说这句话时，说明优化导致了回归。

**立即回退**，不要试图修复：
```bash
git checkout <last-working-commit> -- <affected-files>
git add -A && git commit -m "revert: restore working state" && git push
```

**ReactFlow特定陷阱**：
- `onlyRenderVisibleElements={true}` → 页面卡死
- `elevateNodesOnSelect={false}` → 点击无响应
- `deleteKeyCode={null}` → 键盘事件异常
- `React.memo` on nodes → 数据更新时节点不刷新
- CSS `!important` → 干扰ReactFlow内部样式

**原则**：用户体验 > 性能。稍微慢一点但能用的页面，比快但坏了的页面好一万倍。

## 系统性工作原则

**"不要缝缝补补"** — 先完整理解工作逻辑和目的，再一次性修改。

步骤：
1. 读取所有相关源文件，理解完整数据流
2. 识别所有问题点（不是一个一个发现）
3. 一次性修复所有问题
4. 验证所有修复

**"先搞明白所有的合成逻辑，再一次性修改代码"** — 不要边做边发现新问题。
5. **禁止只改一处**：如果功能在多个节点/组件中使用，所有地方都要改
6. **禁止边改边猜**：先研究清楚再动手，不要边写代码边发现问题
5. **禁止删除用户功能不告知**：用户原话"为什么没经过我同意给他删了？"——删除任何功能前必须告知用户并获得确认

## 典型错误案例（本session）

### 错误：assetType存储位置不一致导致工作流失败
VideoNode存储assetType在`node.data.assetType`，但ImageNode从`node.data.config.assetType`读取。
结果：视频→图片工作流无法识别上游是视频还是图片。

**根因：** 没有检查所有节点的存储位置是否一致。
**修复：** 读取时兼容两层：`sourceData?.assetType || sourceConfig?.assetType`

**教训：** 修改React Flow节点时，必须检查所有相关节点的存储位置是否一致。

### 错误：删除重复条目时误删videoComposite节点
在修复img2video重复条目时，使用了模糊匹配，把videoComposite也一起删了。
用户反馈："为什么没经过我同意给他删了？"

教训：
- 删除操作必须逐行确认
- 修改后必须重新读取文件验证完整性
- 涉及用户功能的删除必须告知用户

### 错误2：sed多行替换失败导致文件损坏
使用sed进行多行替换时，命令格式不正确导致文件损坏（行号重复）。

**症状：** 文件内容变成 `1|"use client";` `2|` `3|import React...` 格式

**原因：** sed的多行替换语法在macOS上不稳定，特别是包含换行符的替换

**解决方案：**
```bash
# ❌ 不可靠 - sed多行替换
sed -i '' 's/old_line1\nold_line2/new_line1\nnew_line2/' file.tsx

# ✅ 可靠 - 使用Python脚本
python3 -c "
with open('file.tsx', 'r') as f:
    content = f.read()
content = content.replace('old', 'new')
with open('file.tsx', 'w') as f:
    f.write(content)
"

# ✅ 最佳 - 使用patch工具
# 通过skill_manage(action='patch')或直接使用patch命令
```

**教训：**
- 避免使用sed进行多行替换
- 优先使用Python脚本或patch工具
- 修改后必须验证文件完整性（检查前几行是否有行号前缀）
5. **禁止未经同意删除功能**：即使是"修复"，也不能删除用户正在使用的功能

## 阿戴核心原则

**"你做完一步你自己也要全面检查一下代码不要出错，特别是工作流逻辑，连接逻辑一点不能乱改"** (2026-06-14) — 每次修改后，必须自己先全面检查代码：
- 语法正确（无 TS 错误）
- 工作流逻辑未被改动（onConnect, onEdgesChange, onNodesChange 等来自 store 的函数）
- 连接逻辑未被改动（handleDeleteEdge, onEdgeContextMenu 等）
- 拖拽逻辑未被改动（onDrop, onDragOver）
- 然后再让用户测试

**"不要缝缝补补"** — 先完整理解工作逻辑和目的，再一次性修改。不要一个一个修，修一个漏一个。

**"先搞明白所有合成逻辑，再一次性修改"** — 遇到问题时，先研究清楚所有相关逻辑，然后统一修改。不要边改边发现新问题。

**"为什么没经过我同意给他删了？"** — 删除任何功能前必须告知用户并获得确认。即使是为了"修复"也不能静默删除。

**"先说明情况再修改"** (2026-06-11) — 修改任何东西之前，必须先说明：
1. 当前情况是什么（现状）
2. 为什么要改（原因）
3. 打算怎么改（方案）

然后再执行。这适用于所有操作——改仓库可见性、改配置、改文件、改权限。不是只对"删除"或"破坏性操作"才这样，而是所有修改都要先说明。用户原话："以后记得先说明情况再修改"。

**区别于"先研究后动手"**：
- "先研究后动手" = 自己先搞明白再做（内部流程）
- "先说明情况再修改" = 做之前告诉用户现状和计划（外部沟通）

两者都要做。先研究明白，然后告诉用户情况和方案，最后执行。

## 侧边栏节点类型修改陷阱（2026-06-14）

**问题：** 删除或添加节点类型时，只改了一处，另一处没改，导致侧边栏仍显示旧节点。

**Antoken有两个侧边栏组件：**
1. `components/sidebar/NodePanel.tsx` — 旧版列表式侧边栏
2. `components/sidebar/CircleNavPanel.tsx` — 新版卡片式侧边栏（CircleNav）

两者都从 `NODE_DEFINITIONS`（types/workflow.ts）读取节点列表，但各自有过滤/渲染逻辑。

**正确做法：** 修改节点类型时，必须同时检查两个组件：
1. `NodePanel.tsx` 的 `categories` 数组和 `defs` 数组
2. `CircleNavPanel.tsx` 的 `NODE_DEFINITIONS.map()` 调用（可能需要 `.filter()`）

```tsx
// CircleNavPanel.tsx - 过滤掉不需要的节点类型
{NODE_DEFINITIONS.filter(d => d.type !== "COMPOSITE").map((def) => { ... })}
```

**教训：** 用户说"还有XXX啊"时，说明你只改了一处。搜索所有引用该节点类型的文件。

## BaseNode 修改规则（2026-06-15 教训）

**修改BaseNode时必须检查所有子组件的依赖：**

当移除BaseNode的Header时，确保：
1. 子组件不依赖 `d.label`（标题显示）
2. 子组件不依赖 `d.status`（状态点显示）
3. 子组件不依赖 `d.progress`（进度条显示）

**安全做法：** 在子组件中自行处理这些状态，不依赖BaseNode。

## 悬浮面板实现规则（2026-06-15 教训）

**悬浮控制面板必须放在节点内容div外面：**

```tsx
// ❌ 错误 - 面板在节点内部，会被overflow: hidden裁剪
<BaseNode>
  <div style={{ position: "relative" }}>
    <div className="preview">...</div>
    {showControls && <div className="floating-panel">...</div>}  {/* 被裁剪 */}
  </div>
</BaseNode>

// ✅ 正确 - 面板在节点外部
<BaseNode>
  <div style={{ position: "relative" }}>
    <div className="preview">...</div>
  </div>
  {showControls && <div className="floating-panel">...</div>}  {/* 正常显示 */}
</BaseNode>
```

**面板定位：**
- `position: "absolute"` + `top: 0` + `left: "100%"` + `marginLeft: 12`
- `zIndex: 100` 确保在其他节点之上
- `onClick={(e) => e.stopPropagation()}` 防止点击面板时关闭

## 编译报错时先验证文件（2026-06-14 教训）

**场景：** dev server报语法错误（如`Expected ',', got '}'`），但实际文件内容完全正确。

**错误做法：** 直接假设文件有语法错误，花时间检查/修改文件。

**正确做法：**
1. 用 `read_file` 读取报错文件的实际内容
2. 确认文件本身是否有语法错误
3. 如果文件正确 → 100%是缓存问题，清除 `.next` + `.swc` 重启

**根因：** Next.js缓存中保留了旧版本的编译结果，与新代码冲突。

**教训：** 编译报错 ≠ 文件损坏。先验证文件，再清缓存，最后才考虑修改代码。

## 研究阶段必查：字段命名一致性

**NEW PITFALL (2026-06-14)**: 修复bug时，必须先确认所有相关组件使用的字段名是否一致。

**案例**：ImageNode读取上游视频节点的assetType失败
- VideoNode存储：`node.data.assetType` (正确位置)
- ImageNode读取：`node.data.config.assetType` (错误位置)
- 结果：连接视频→图片时，图片节点无法识别上游是视频

**修复前检查清单**：
1. 搜索所有使用该字段的组件
2. 确认存储位置和读取位置是否一致
3. 如果不一致，统一为一种方式

**教训**：不要假设字段位置，必须实际搜索确认。

## write_file Line Number Corruption (NEW PITFALL)

**PITFALL**: `read_file` returns content with line numbers (e.g., `1|content`). If this output is passed to `write_file`, the file gets corrupted with line numbers embedded.

**Symptoms**: TypeScript errors like `TS1109: Expression expected` at line 1, 2, 3...

**Fix**: Always strip line numbers before writing, or use `patch` tool instead.

```python
# Wrong: read_file output has line numbers
content = read_file("path.tsx")["content"]  # "1|\"use client\";\n2|..."
write_file("path.tsx", content)  # CORRUPTS FILE

# Correct: strip line numbers first
lines = content.split("\n")
fixed = [line.split("|", 2)[2] if "|" in line else line for line in lines]
write_file("path.tsx", "\n".join(fixed))

# Better: just use patch tool for targeted edits
```

## CSS !important Override Pitfall

**CRITICAL (2026-06-14):** Adding CSS with `!important` for React Flow overrides can break Tailwind utility classes and cause layout issues.

**Problem:**
```css
/* This broke the entire page layout */
.react-flow {
  width: 100% !important;
  height: 100% !important;
}
```

**Why it fails:** The `!important` declarations override Tailwind's utility classes, causing unexpected layout behavior. The flex container's `h-screen` class was being overridden.

**Fix:** Use ReactFlow's built-in sizing props instead of CSS overrides:
```typescript
<ReactFlow
  style={{ width: '100%', height: '100%' }}
  // or rely on parent container having proper dimensions
/>
```

**Rule:** NEVER use `!important` for React Flow styling. Use ReactFlow's style prop or ensure parent containers have proper dimensions.

## Next.js Cache Corruption Pitfall (CRITICAL 2026-06-14)

**Symptoms:**
- Page loads but clicks don't respond
- CSS files return 404
- JS chunks fail to load
- Layout broken but no console errors
- "Compiled successfully" but page doesn't work

**Root Cause:** After multiple code changes, `.next` cache directory accumulates stale compiled results that conflict with new code.

**Fix:**
```bash
cd ~/antoken/frontend
rm -rf .next
npm run dev
```

**Prevention:**
- Clear cache after major code changes
- If page acts weird, clear cache FIRST before investigating
- Performance optimizations should be done incrementally with cache clears between each

**Rule:** When user says "页面卡住" or "点击无反应", FIRST clear Next.js cache, THEN investigate.

## React Flow 节点内可交互元素拖拽冲突 (CRITICAL 2026-06-15)

**问题：** 节点内的可交互元素（按钮、选择器、输入框）点击时会触发节点拖拽，节点"粘着鼠标"。

**根因：** React Flow 通过 `mousedown` 事件启动拖拽。节点内的任何可交互元素的 mousedown 事件会冒泡到节点层，触发拖拽。

**修复：** 在可交互元素的容器上添加 `onMouseDown` 阻止传播：

```tsx
{/* ❌ 错误 - 点击会触发拖拽 */}
<div style={{ position: "absolute", top: "100%" }}>
  <button onClick={handleClick}>Click</button>
  <select onChange={handleChange}>...</select>
</div>

{/* ✓ 正确 - 阻止 mousedown 传播 */}
<div 
  onMouseDown={(e) => e.stopPropagation()}
  style={{ position: "absolute", top: "100%" }}
>
  <button onClick={handleClick}>Click</button>
  <select onChange={handleChange}>...</select>
</div>
```

**关键点：**
- 只需在容器上加一次 `onMouseDown`，所有子元素都会继承
- 不需要给每个按钮/选择器单独加
- `onClick` 的 `stopPropagation` 不能阻止拖拽，必须是 `onMouseDown`

## StopPropagation 双刃剑 (2026-06-15)

**问题：** 在对话框容器上加 `onClick={(e) => e.stopPropagation()}` 会导致内部所有点击失效。

**NEW PITFALL (2026-06-15):** `stopPropagation()` on node child elements (preview areas, containers) prevents ReactFlow from selecting the node. This makes Delete key non-functional. **Only use stopPropagation on specific interactive controls (buttons, sliders, input fields), NOT on the entire preview area or node container.**

**错误模式：**
```tsx
{/* ❌ 这会导致内部按钮无法点击 */}
<div onClick={(e) => e.stopPropagation()}>
  <button onClick={handleGenerate}>生成</button>  {/* 无法点击！ */}
</div>
```

**正确模式：**
```tsx
{/* ✓ 只在 mousedown 上阻止，不影响 click */}
<div onMouseDown={(e) => e.stopPropagation()}>
  <button onClick={handleGenerate}>生成</button>  {/* 正常工作 */}
</div>
```

**区别：**
- `onClick` 的 `stopPropagation` 会阻止所有子元素的 click 事件
- `onMouseDown` 的 `stopPropagation` 只阻止拖拽，不影响 click

## React.memo on ReactFlow Nodes (NUANCED 2026-06-14)

The skill previously said "DO NOT use React.memo". This is **too strict**.

**Real issue:** React.memo CAN work on ReactFlow nodes, but the syntax must be perfect:

```tsx
// ✅ CORRECT - proper closing
export default React.memo(function VideoNode(props: NodeProps) {
  // ... component code ...
});

// ❌ WRONG - missing semicolon or extra bracket
export default React.memo(function VideoNode(props: NodeProps) {
  // ... component code ...
})  // missing ;
export default VideoNode;  // this line causes error

// ❌ WRONG - helper function inside memo wrapper
export default React.memo(function CompositeNode(props: NodeProps) {
  // ... component code ...
  function helper() { ... }  // WRONG - must be outside
});
```

**Key rules:**
1. Close with `});` not `})`
2. Helper functions must be OUTSIDE the memo wrapper
3. Test TypeScript compilation after adding memo
4. If memo causes issues, revert immediately

## Video-to-Image Workflow Pitfall (2026-06-14)

**Problem:** API returns "base64 image is not allowed" when trying to use video reference for image generation.

**Wrong approach:** Extract video frame → convert to base64 → pass to API

**Why wrong:** 
1. External APIs can't access localhost URLs
2. Video URLs passed as image_urls cause "no images in generateContent response"

**Correct approach:** Pass video URL directly to API, let API handle it.

## Multi-Asset Collection Pitfall

**Problem:** Using `elif` logic when collecting multiple assets misses some assets.

**Wrong:** `if video: urls = [video] elif images: urls = images`

**Correct:** Collect all assets separately, then combine:
```python
all_urls = []
if videos: all_urls.extend(videos)
if images: all_urls.extend(images)
```

## ReactFlow Event Handling Pitfalls

1. **Double-click intercepted by ReactFlow** — Use single click for control panel, button for fullscreen
2. **stopPropagation on parent div breaks child buttons** — Use `onMouseDown` stopPropagation instead
3. **e.preventDefault() on click blocks all behavior** — Don't use on preview containers
4. **VideoPreview onClick on outer div prevents node selection** — Don't add click handlers on VideoPreview outer div

### Detailed Migration Steps (2026-07-04)

1. Copy file: `cp v1-file.tsx v2-file.tsx`
2. Update imports:
   - `@/stores/workflowStore` → `@/stores/workflow-store-jotai`
   - `@/lib/api` → `@/lib/api-base`
   - `./BaseNode` → `./base-node`
   - `@/types/workflow` → `@/types/workflow-v1`
   - `@/stores/settingsStore` → `@/stores/settings-store`
   - `@/components/PreviewModal` → `@/components/preview-modal`
   - `@/components/MentionInput` → `@/components/mention-input`
   - `@/lib/mediaProxy` → `@/lib/media-proxy`
   - `@/lib/assetUpload` → `@/lib/asset-upload`
3. Replace store usage:
   - `const { nodes, edges, ... } = useWorkflowStore()` → individual `useAtom` calls
   - `selectNodeQuietly(id); setShowControlPanel(true)` → `selectNode(id)`
4. Add `/* eslint-disable */` at top

### Critical Pitfall
v1 code has hardcoded default mentions in MentionInput. Do NOT remove them - they're intentional fallback behavior.

## File Corruption Pitfall

**Never use `read_file` + `write_file` for edits.** read_file returns content with line numbers (e.g., `1|1|"use client";`). Writing this back corrupts the file. Always use the `patch` tool.
**Correct approach:** Pass video URL directly to API, let API handle it

**Update (2026-06-15):** 错误 "call upstream API failed: no images in AIX generateContent response" 表示API期望图片URL但收到视频URL。正确做法：用 `extract_video_frame()` 提取首帧图片URL再传给API。

```python
# 错误：直接传视频URL给图片API
payload["image_urls"] = [req.reference_video_url]  # ❌

# 正确：先提取首帧
frame_url = await extract_video_frame(req.reference_video_url)
payload["image_urls"] = [frame_url]  # ✅
```

```python
# ❌ Wrong - extract frame and pass base64
frame_url = await extract_video_frame(video_url)  # returns base64
payload["image_urls"] = [frame_url]

# ✅ Correct - pass video URL directly
payload["image_urls"] = [video_url]
```

**Why:** Most AI APIs (like toapis.com) can process video URLs directly. They extract frames internally. Passing localhost URLs or base64 doesn't work because the API can't access them.

## Asset Type Propagation Pattern (2026-06-14)

**Problem:** Downstream nodes can't read upstream node's asset type.

**Root cause:** Different nodes store assetType at different levels:
- VideoNode: `node.data.assetType` (correct)
- ImageNode reads: `node.data.config.assetType` (wrong location)

**Fix:** Read from both locations:
```typescript
const sourceData = sourceNode.data as unknown as NodeData;
const sourceConfig = sourceData?.config as Record<string, unknown>;
const assetType = sourceData?.assetType || sourceConfig?.assetType;
```

**Rule:** When adding new fields to node data, check ALL nodes that read this field to ensure they read from the correct location.

## Proxy URL for CORS (2026-06-14)

**Problem:** External media URLs (from API CDNs) can't be played in browser due to CORS.

**Solution:** Use backend proxy endpoint:
```typescript
// frontend/src/lib/mediaProxy.ts
const PROXY_BASE = 'http://localhost:8000/api/generate/proxy';

export function proxyUrl(url: string | null): string {
  if (!url) return '';
  if (url.startsWith('http://localhost') || url.startsWith('blob:') || url.startsWith('data:')) {
    return url;  // Local URLs don't need proxy
  }
  return `${PROXY_BASE}?url=${encodeURIComponent(url)}`;
}
```

**Usage in components:**
```tsx
<video src={proxyUrl(previewUrl)} crossOrigin="anonymous" />
<img src={proxyUrl(previewUrl)} />
```

**Backend proxy must:**
1. Allow the domain (or use wildcard for dev)
2. Return proper CORS headers
3. Support Content-Range for video playback

## BaseNode overflow:hidden 遮挡悬浮面板 (2026-06-15)

**Problem:** BaseNode has `overflow: hidden` which clips the floating control panel that extends below the node.

**Solution:** Remove `overflow: hidden` from BaseNode, or use `overflow: visible` and handle content clipping differently.

## Handle Styling and Hover Zone (2026-06-15)

**详细模式见 `references/handle-styling-hover-zone.md`**

核心要点：
- `margin: -40` + `padding: 40` 创建隐形hover检测区域
- Handle大小20×20px，距离-20px
- Hover时scale(1.5) + 弹性曲线
- 延迟10秒隐藏，方便连接操作

## 素材自动命名 + @提及系统 (2026-06-15)

**详细模式见 `references/asset-naming-and-mention.md`**

核心要点：
- assetName存储在 `node.data.assetName`，不是 `node.data.config.assetName`
- 使用localStorage持久化计数器
- MentionInput组件支持@提及
- 提示词自动注入素材引用

## Related References

- `references/video-preview-interaction.md` — Video preview interaction patterns (TapNow style)
- `references/multi-line-edit-pitfalls.md` — Multi-line edit pitfalls and solutions
- `references/deepseek-review-workflow.md` — DeepSeek 代码审查工作流（分模块审查+TDD修复）
- `references/parameter-passthrough-rules.md` — 参数透传规则（前端→后端→AI API）
- `references/multi-reference-architecture.md` — 多参考架构模式（角色系统+结构化数据）
- `references/jotai-atomfamily-patterns.md` — Jotai atomFamily 性能优化模式
- `references/node-visual-design.md` — 节点视觉设计模式（无边框+泛光+白色按钮）
- `references/large-block-replacement-patterns.md` — 大块JSX替换(head/tail拆分) + sed批量样式替换
- `references/video-node-spacious-panel.md` — 视频节点舒展布局面板设计参数+弹窗遮罩模式

**修复：** 从BaseNode的style中移除 `overflow: "hidden"`。

**规则：** 如果节点需要有悬浮/弹出面板（如控制面板、下拉菜单），BaseNode不能设置 `overflow: "hidden"`。需要在视觉设计和功能之间权衡。

## ReactFlow 性能优化安全清单 (2026-06-15)

**安全的优化（可以用useMemo/useCallback）：**
- `defaultEdgeOptions` — 每次渲染创建新对象，用useMemo稳定引用
- `connectionLineStyle` — 同上
- `snapGrid` — 同上
- `proOptions` — 同上
- `defaultViewport` — 同上
- `nodeColor` — 回调函数用useCallback
- `nodeTypes` — 已经是模块级常量，引用天然稳定

**不安全的优化（会导致页面卡死/点击失效）：**
- `onlyRenderVisibleElements={true}` → 页面卡死
- `elevateNodesOnSelect={false}` → 点击无响应
- `deleteKeyCode={null}` → 键盘事件异常
- `React.memo` on node components → 数据更新时节点不刷新
- CSS `transform` on `.react-flow__node` → 破坏定位系统

**规则：** 优化ReactFlow时，只改props引用（useMemo），不改行为配置。

## 网格吸附应默认关闭 (2026-06-15)

**问题：** `snapToGrid` 一直开启，导致节点移动有明显的"跳跃感"，不够顺滑。

**修复：** 
1. 添加 `const [snapEnabled, setSnapEnabled] = useState(false);`
2. `<ReactFlow snapToGrid={snapEnabled}>`
3. 添加网格吸附开关按钮（左下角Controls下方）

**规则：** 默认关闭吸附，用户需要时手动开启。

## CSS transform 覆盖破坏 React Flow 定位 (CRITICAL 2026-06-14)

**这个问题发生了两次。** 改之前没加载 skill，又犯了同样的错误。

## CSS transform 覆盖破坏 React Flow 定位 (CRITICAL 2026-06-14)

**问题：** 添加CSS `transform` 覆盖到 `.react-flow__node` 会导致页面卡住。

```css
/* ❌ 错误 - 破坏React Flow定位系统 */
.react-flow__node:hover {
  transform: translateY(-1px) !important;
}
```

**原因：** React Flow 使用 `transform: translate(x, y)` 定位节点。

**安全替代方案：** 只用 `box-shadow`、`border`。

**规则：** 绝对不要对 `.react-flow__node` 使用 `transform` 覆盖。

## 悬浮面板陷阱 (CRITICAL 2026-06-15)

**问题1：overflow:hidden 裁剪悬浮面板**

BaseNode有 `overflow: hidden` 时，用 `position: absolute` + `left: 100%` 或 `top: "100%"` 的悬浮面板会被裁剪不可见。

```tsx
// ❌ 悬浮面板被裁剪
<div style={{ overflow: "hidden" }}>  // BaseNode
  <div style={{ position: "absolute", top: "100%" }}>  // 被裁剪
```

**修复：** 移除父容器的 `overflow: hidden`。

**问题2：e.stopPropagation() 阻止子元素点击**

在悬浮面板容器上加 `onClick={(e) => e.stopPropagation()}` 会导致面板内所有按钮失效。

```tsx
// ❌ 所有按钮失效
<div onClick={(e) => e.stopPropagation()}>
  <button onClick={handleGenerate}>生成</button>  // 不触发
</div>
```

**修复：** 不要在面板容器上用 stopPropagation。如果需要阻止冒泡，只在具体按钮上用。

**规则：**
1. 悬浮面板的父容器不能有 `overflow: hidden`
2. 悬浮面板容器不要加 `onClick={stopPropagation}`
3. 需要阻止冒泡时，只在具体交互元素上加

## ReactFlow 安全优化模式（2026-06-14 验证通过）

**已验证安全的优化**（不会破坏渲染/事件/定位）：

### 1. useMemo 稳定 ReactFlow props 引用

ReactFlow 的 `defaultEdgeOptions`、`connectionLineStyle`、`snapGrid` 等 props 如果传入内联对象，每次渲染都会创建新引用，触发 ReactFlow 内部不必要的更新。

```tsx
// ✅ 安全 - useMemo 稳定引用
const defaultEdgeOpts = useMemo(() => ({
  animated: true,
  style: { stroke: "#ffffff", strokeWidth: 2.5, strokeOpacity: 0.8 },
  type: "smoothstep" as const,
}), []);

const connLineStyle = useMemo(() => ({
  stroke: "#ffffff", strokeWidth: 3, strokeDasharray: "8 4"
}), []);

const snapGridValue: [number, number] = useMemo(() => [16, 16], []);

<ReactFlow
  defaultEdgeOptions={defaultEdgeOpts}
  connectionLineStyle={connLineStyle}
  snapGrid={snapGridValue}
/>
```

### 2. nodeTypes 模块级常量

`nodeTypes` 如果定义在模块顶层（不在组件内），引用天然稳定，不需要额外处理：

```tsx
// nodes/index.ts - 模块级常量，引用稳定
export const nodeTypes: NodeTypes = {
  video: VideoNode,
  image: ImageNode,
  // ...
};
```

### 3. CSS box-shadow 动画（不碰 transform）

```css
/* ✅ 安全 - 只改阴影 */
.react-flow__node:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
}
.react-flow__node.selected {
  box-shadow: 0 0 0 2px var(--accent-bright) !important;
}
```

### 绝对禁止的优化（已验证会破坏页面）

- `onlyRenderVisibleElements={true}` → 页面卡死
- `elevateNodesOnSelect={false}` → 点击无响应
- `deleteKeyCode={null}` → 键盘事件异常
- `React.memo` on node components → 节点不刷新
- CSS `transform` on `.react-flow__node` → 定位系统崩溃
- CSS `!important` on layout props (width/height) → 破坏 Tailwind

**原则：** 只优化引用稳定性（useMemo），不优化渲染行为（memo/visibility/transform）。

## Safe ReactFlow Performance Optimization (2026-06-14)

**用户要求：** "全做了吧，但要慢慢来一步步来，做完一步检查一步" + "你做完一步你自己也要全面检查一下代码不要出错，特别是工作流逻辑，连接逻辑一点不能乱改"

### 可安全优化的 ReactFlow props（用 useMemo/useCallback）

这些 props 每次渲染创建新对象引用，会导致 ReactFlow 认为 props 变了触发内部更新：

| 优先级 | Prop | 原因 |
|--------|------|------|
| 高 | `defaultEdgeOptions` | 每次创建新对象，影响所有边 |
| 高 | `connectionLineStyle` | 每次创建新对象，影响连线渲染 |
| 高 | `snapGrid` | 每次创建新数组 |
| 中 | `defaultViewport` | 每次创建新对象 |
| 中 | `proOptions` | 每次创建新对象 |
| 中 | Background/MiniMap `style` | 每次创建新对象 |
| 低 | 右键菜单/空状态 `style` | 条件渲染，几乎不影响 |

### 正确模式

```tsx
// ✅ 在组件内用 useMemo 稳定引用
const defaultEdgeOpts = useMemo(() => ({
  animated: true,
  style: { stroke: "#ffffff", strokeWidth: 2.5, strokeOpacity: 0.8 },
  type: "smoothstep" as const,
}), []);

const connLineStyle = useMemo(() => ({
  stroke: "#ffffff", strokeWidth: 3, strokeDasharray: "8 4"
}), []);

const snapGridValue: [number, number] = useMemo(() => [16, 16], []);

// ✅ nodeTypes 如果是模块级常量，不需要 useMemo（引用已稳定）
// ✅ nodeColor 如果不依赖状态，用 useCallback([], [])
const nodeColor = useCallback((node: Node) => {
  const d = node.data as unknown as NodeData;
  return colors[d.category] ?? "rgba(255,255,255,0.05)";
}, []);
```

### 工作流程（必须遵守）

1. **一次只改一个 prop** — 改完刷新浏览器测试
2. **每步验证整个文件** — 不只看改动处，检查所有 props 是否正确引用
3. **绝不碰工作流逻辑** — onConnect, onEdgesChange, onNodesChange 等来自 store 的回调不能改
4. **绝不碰连接逻辑** — handleDeleteEdge, onEdgeContextMenu 等不能改
5. **验证完再做下一步** — 用户原话："做完一步检查一步"

### 绝对不能碰的优化（已知会导致页面卡死）

- `onlyRenderVisibleElements={true}` → 页面卡死
- `elevateNodesOnSelect={false}` → 点击无响应
- `deleteKeyCode={null}` → 键盘事件异常
- `React.memo` on nodes → 数据更新时节点不刷新
- CSS `transform` on `.react-flow__node` → 定位系统崩溃
- CSS `!important` on React Flow 内部样式 → 干扰渲染

## ReactFlow 安全性能优化（2026-06-14 验证）

**详细模式见 `references/reactflow-safe-optimization.md`**

核心要点：
1. 用 `useMemo` 稳定 ReactFlow props 引用（defaultEdgeOptions, connectionLineStyle, snapGrid 等）
2. 用 `useCallback` 稳定 nodeColor 函数引用
3. **不要动**：nodes, edges, onNodesChange, onEdgesChange, onConnect（来自 store，必须实时更新）
4. 吸附网格默认关闭，添加开关按钮

**用户确认的优化流程：**
- 一个一个改，改完一步让用户测试
- 每步自己检查代码（特别是工作流逻辑、连接逻辑）
- 改完所有优化后，搜索 `={{` 确认没有遗漏的内联对象

## Multiple Sidebar Components Pitfall (2026-06-14)

**Problem:** User asked to remove "融合" from sidebar. I edited `NodePanel.tsx` but the actual UI was `CircleNavPanel.tsx`.

**Root cause:** Antoken has TWO sidebar components that render node definitions:
1. `NodePanel.tsx` — Simple list-style sidebar
2. `CircleNavPanel.tsx` — Card-style selection panel with icons (the one user sees)

**Fix:** Always check BOTH files when modifying which nodes appear in the sidebar.

**Filtering pattern:** Use `.filter()` on `NODE_DEFINITIONS` rather than modifying source data:
```tsx
{NODE_DEFINITIONS.filter(d => d.type !== "COMPOSITE").map((def) => {
  // render card
})}
```

## overflow:hidden 裁剪浮动元素 (CRITICAL 2026-06-15)

**问题：** 在 React Flow 节点的容器 div 上添加 `overflow: "hidden"` 会导致浮动对话框被裁剪。

```tsx
// ❌ 错误 - 浮动对话框被裁剪
<div style={{ overflow: "hidden" }}>
  <PreviewBox />
  {/* 这个对话框在节点外部，会被裁剪 */}
  {showDialog && <div style={{ position: "absolute", top: "100%" }}>Dialog</div>}
</div>
```

**原因：** `overflow: "hidden"` 会裁剪所有超出容器边界的内容，包括 `position: "absolute"` 的浮动元素。

**修复：** 移除 `overflow: "hidden"`，或只在需要裁剪的子元素上添加。

```tsx
// ✓ 正确 - 只在预览框上裁剪
<div style={{ position: "relative" }}>
  <div style={{ overflow: "hidden", borderRadius: 16 }}>
    <PreviewBox />
  </div>
  {showDialog && <div style={{ position: "absolute", top: "100%" }}>Dialog</div>}
</div>
```

## e.stopPropagation() 在对话框容器上破坏子按钮 (CRITICAL 2026-06-15)

**问题：** 在对话框容器 div 上添加 `onClick={(e) => e.stopPropagation()}` 会导致内部所有按钮失效。

```tsx
// ❌ 错误 - 所有按钮都失效
<div onClick={(e) => e.stopPropagation()}>
  <button onClick={() => console.log("clicked")}>Click Me</button>
  <select onChange={(e) => setModel(e.target.value)}>...</select>
</div>
```

**原因：** `stopPropagation()` 阻止了事件冒泡，但也干扰了某些浏览器的事件处理机制，特别是对于 select 元素。

**修复：** 只在需要阻止冒泡的特定元素上添加，不要在容器上添加。

```tsx
// ✓ 正确 - 只在特定元素上阻止冒泡
<div>
  <button onClick={(e) => { e.stopPropagation(); doSomething(); }}>Click Me</button>
  <select onChange={(e) => setModel(e.target.value)}>...</select>
</div>
```

**规则：** 永远不要在对话框/弹窗容器上添加 `stopPropagation`，只在需要的子元素上添加。

## React Flow 点击 vs 拖拽冲突 (2026-06-15)

**问题：** 点击节点内容时，React Flow 把它当成拖拽操作，节点"粘着"鼠标。

```tsx
// ❌ 错误 - 点击被当成拖拽
<div onClick={() => setShowDialog(!showDialog)}>
  Preview Content
</div>
```

**原因：** React Flow 的拖拽处理器会捕获 mousedown 事件，如果 click 事件没有正确阻止传播，会被当成拖拽。

**修复：** 在 click handler 中添加 `e.stopPropagation()` 和 `e.preventDefault()`。

```tsx
// ✓ 正确 - 阻止拖拽
<div onClick={(e) => { e.stopPropagation(); e.preventDefault(); setShowDialog(!showDialog); }}>
  Preview Content
</div>
```

**注意：** 这里在 click handler 上使用 stopPropagation 是安全的（不是在容器上）。

## 不要用文本显示替换交互控件 (2026-06-15)

**问题：** 把 select 下拉框替换成纯文本显示，导致用户无法修改参数。

```tsx
// ❌ 错误 - 用户无法修改
<span style={{ fontSize: 14, color: "#fff" }}>{model}</span>
<span style={{ fontSize: 14, color: "#fff" }}>{size}·{duration}s</span>
```

**修复：** 保持交互控件，只调整样式。

```tsx
// ✓ 正确 - 保持可交互
<select value={model} onChange={(e) => setModel(e.target.value)} style={{...}}>
  {MODELS.map((m) => <option key={m} value={m}>{m}</option>)}
</select>
```

**规则：** UI 简化不能牺牲功能性。用户必须能修改所有参数。

## 常见陷阱：CSS !important覆盖内联样式

修改React组件样式时，如果CSS文件中使用了`!important`，内联样式会被覆盖。

**典型场景**：修改React Flow边颜色
- 只改组件内联样式 → 不生效（被CSS覆盖）
- 必须同时改CSS全局样式中的`!important`规则

**检查清单：**
- [ ] 搜索`globals.css`或全局CSS中是否有`!important`覆盖
- [ ] 如果有，必须同时修改CSS和内联样式
- [ ] 修改后强制刷新浏览器（Cmd+Shift+R）清除缓存

## 代码审查检查清单（阿戴要求 2026-06-14）

> "做完一步你自己也要全面检查一下代码不要出错，特别是工作流逻辑，连接逻辑一点不能乱改"

每次改完必须 read_file 全文，确认：
- [ ] import 正确
- [ ] useCallback/useMemo 依赖正确
- [ ] onConnect, onEdgesChange, onNodesChange 等工作流函数未被改动
- [ ] 连接逻辑（handleDeleteEdge, onEdgeContextMenu）未被改动
- [ ] 拖拽逻辑（onDrop, onDragOver）未被改动

## 视频预览组件实现陷阱 (2026-06-15)

**详细交互模式见 `references/video-preview-interaction-pattern.md`**

### Plyr 库在 Next.js 中不工作

**问题：** Plyr 视频播放器库在 Next.js 环境中初始化失败，CSS 导入冲突。

**症状：** 视频不显示，控件不工作，控制台无明显错误。

**根因：** Plyr 是客户端库，依赖特定的 DOM 结构和 CSS 加载顺序，与 Next.js 的 SSR/SSG 机制冲突。

**正确做法：** 使用原生 `<video>` 元素 + 自定义控件组件。

```tsx
// ❌ 错误 - Plyr 在 Next.js 中不工作
import Plyr from 'plyr';
import 'plyr/dist/plyr.css';

// ✅ 正确 - 使用原生 video + 自定义控件
<video
  ref={videoRef}
  autoPlay
  loop
  muted
  playsInline
  preload="auto"
  crossOrigin="anonymous"
>
  <source src={src} type="video/mp4" />
</video>
```

### 视频预览 UX 最佳实践

**阿戴要求：** 控件区域不要太占空间，移除文字提示。

```tsx
// 紧凑型控件设计
- 播放按钮：36px（不要48px太大）
- 进度条：底部 3-4px 细条
- 时间显示：悬停时右下角显示
- 图标大小：12-14px
- 不要快捷键提示文字
```

### 加载优化

```tsx
// 使用 preload="auto" + canplay 事件
video.preload = 'auto';

video.addEventListener('canplay', () => {
  setIsLoading(false);  // 更快显示视频
});
```

### 进度条拖拽实现

```tsx
const handleSeekStart = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
  setIsSeeking(true);
  
  const handleMouseMove = (moveEvent: MouseEvent) => {
    // 实时更新进度
  };
  
  const handleMouseUp = () => {
    setIsSeeking(false);
    window.removeEventListener('mousemove', handleMouseMove);
    window.removeEventListener('mouseup', handleMouseUp);
  };
  
  window.addEventListener('mousemove', handleMouseMove);
  window.addEventListener('mouseup', handleMouseUp);
}, [duration]);
```

## 颜色替换陷阱（详细模式见 `references/batch-color-replacement.md`）

**问题：** 批量替换颜色时，使用 read_file + write_file 会导致文件损坏。

**正确做法：** 使用 patch 工具进行精确替换。

```python
# ❌ 错误 - 会损坏文件
content = read_file("file.tsx")["content"]
content = content.replace("#5e6ad2", "#ffffff")
write_file("file.tsx", content)

# ✅ 正确 - 使用 patch
patch(
    path="file.tsx",
    old_string='color: "#5e6ad2"',
    new_string='color: "#ffffff"'
)
```

**批量替换后必须：**
1. 运行 `npm run build` 验证编译通过
2. 检查前几行文件内容是否有行号前缀

## ReactFlow ConnectionMode.Loose (CRITICAL 2026-06-15)

**问题：** ReactFlow v12 默认 `ConnectionMode.Strict`，一个 target handle 只允许一个 incoming connection。连接第二个 source 时，第一个 edge 被静默替换。

**症状：** 用户连接了3个素材节点到视频生成节点，但只有最后1个素材被参考。

**修复：**
```tsx
import { ConnectionMode } from "@xyflow/react";

<ReactFlow
  connectionMode={ConnectionMode.Loose}
  ...
/>
```

**Edge ID 唯一性：** `addEdge()` 可能生成重复 ID 导致边被替换。使用直接数组追加：
```tsx
const edgeId = `edge-${source}-${sourceHandle}-${target}-${targetHandle}-${Date.now()}`;
const newEdge = { id: edgeId, ...connection, animated: true, style: {...}, type: "smoothstep" };
const updated = [...s.edges, newEdge]; // 不用 addEdge()
```

**规则：** 多素材连接时必须设置 `ConnectionMode.Loose`，否则边会被静默替换。

## 素材编号去重 - localStorage 持久化 (2026-06-15)

**问题：** 模块级变量或 window 全局变量在页面刷新后重置，导致编号重复。

**正确做法：** 使用 localStorage 持久化计数器：
```typescript
function getNextAssetNumber(type: 'IMAGE' | 'VIDEO'): number {
  const key = `antoken_asset_counter_${type}`;
  const current = parseInt(localStorage.getItem(key) || '0', 10);
  const next = current + 1;
  localStorage.setItem(key, next.toString());
  return next;
}
```

**或者用 max+1 逻辑（更可靠）：**
```typescript
const existingNames = nodes.map(n => (n.data as any)?.assetName || '');
const existingNumbers = existingNames
  .filter(n => n.startsWith('图素材'))
  .map(n => parseInt(n.replace('图素材', '')) || 0);
const maxNum = existingNumbers.length > 0 ? Math.max(...existingNumbers) : 0;
assetName = `图素材${maxNum + 1}`;
```

**规则：** 素材编号必须使用持久化方式（localStorage 或 max+1），不能用模块级变量。

## 阿戴核心要求（2026-06-15 反复确认）

1. **不要缝缝补补** — 先完整理解工作逻辑和目的，再一次性修改
2. **绝不未经同意删除任何东西** — 误删素材融合节点被严厉批评
3. **修改前先保存当前稳定版本** — 写进skills
4. **修改后必须验证完整性** — 每个功能实际测试验证
5. **不要引入新错误** — 用户原话："让你改东西的时候不要有别的错误怎么又犯"
6. **先检查自己** — 用户原话："你先检查自己"，在回答前先排除自己的错误
7. **先说明情况再修改** — 用户原话：以后记得先说明情况再修改
8. **禁止修改工作逻辑代码** — generate.py等后端API调用逻辑、视频/图片处理流程等核心业务代码不要动。只修改UI/前端代码。用户原话：我不是之前让你改东西不要碰工作逻辑代码吗？怎么工作逻辑代码又出现这么多问题！！！！

## 禁止修改工作逻辑代码（2026-06-15 教训）

**用户原话：** "我不是之前让你改东西不要碰工作逻辑代码吗？怎么工作逻辑代码又出现这么多问题！！！！"

**规则：** 只修改UI/前端代码，不要修改以下内容：
- `backend/app/api/generate.py` — API调用逻辑
- `backend/app/services/` — 业务逻辑服务
- 任何涉及API请求、数据处理、文件上传的核心逻辑

**错误案例：** 修改 `generate_image` 函数，将视频URL改为提取首帧图片URL后传递给API。结果：
1. 提取的首帧URL是 `http://localhost:8000/...`，外部API无法访问
2. 导致 "call upstream API failed: connection refused" 错误

**教训：** 已经修复过的工作逻辑代码不要动。如果发现bug，先检查是否是之前修改导致的，然后回退到原始逻辑。

**详细工作流逻辑和API传递方式见 `references/antoken-workflow-logic.md`**

**错误案例：** 修改 `generate_image` 函数，将视频URL改为提取首帧图片URL后传递给API。结果：
1. 提取的首帧URL是 `http://localhost:8000/...`，外部API无法访问
2. 导致 "call upstream API failed: connection refused" 错误

**教训：** 已经修复过的工作逻辑代码不要动。如果发现bug，先检查是否是之前修改导致的，然后回退到原始逻辑。

**详细工作流逻辑和API传递方式见 `references/antoken-workflow-logic.md`**

## 本地URL外部API无法访问陷阱（2026-06-15 教训）

**问题：** 从视频提取首帧后，生成的URL是 `http://localhost:8000/api/generate/temp-file/frame_xxx.jpg`，但外部API（如toapis.com）无法访问localhost。

**错误信息：** `call upstream API failed: failed to mirror external image at index 0 from http://localhost:8000/... dial tcp [::1]:8000: connect: connection refused`

**根因：** 外部API服务器无法访问开发机的localhost。

**正确做法：** 不要修改已有的API调用逻辑。原来的代码直接传递视频URL给API，让API自己处理视频转图片。

**规则：** 
- 生成的临时文件URL只能在本地使用，不能传给外部API
- 外部API需要的是可公开访问的URL（如CDN URL）
- 不要假设外部API能访问localhost

## Antoken工作流核心原则（2026-06-15确立，不咨询不改）

**所有生成节点必须参考所有上游连接线素材（多个图片+多个视频）：**
- 图图生图：多个图片作为参考
- 图视频生图：图片+视频同时作为参考
- 图视频生视频：图片+视频同时作为参考
- 视频视频生视频：多个视频作为参考

**API传递方式：**
- 图片生成：用 `image_urls` 传递所有素材
- 视频生成：用 `image_with_roles` 和 `video_with_roles` 分别传递

**前端收集模式：** 使用数组收集所有上游素材，不是单个值
```typescript
// ❌ 错误 - 只支持单个
let referenceVideoUrl: string | null = null;

// ✅ 正确 - 支持多个
let referenceVideoUrls: string[] = [];
```

**详细API传递方式和错误归档见 `references/antoken-workflow-logic.md`**

## 素材自动命名 + @提及系统（2026-06-15）

**功能：** 每个素材节点自动命名（图素材1、视频素材2），提示词中可用@引用素材。

### 自动命名规则
- 按创建时间递增编号
- 图片节点：图素材1、图素材2...
- 视频节点：视频素材1、视频素材2...
- 名称存储在 `node.data.assetName`

### @提及输入组件
文件：`frontend/src/components/MentionInput.tsx`

```tsx
<MentionInput
  value={prompt}
  onChange={setPrompt}
  mentions={[
    ...upstream.images.map(img => ({ id: img.assetName, name: img.assetName, type: 'image' })),
    ...upstream.videos.map(vid => ({ id: vid.assetName, name: vid.assetName, type: 'video' })),
  ]}
  placeholder="输入@引用素材，如：@图素材1中的什么替换成@视频素材1中的什么"
/>
```

### 提示词自动注入素材名称
生成时自动在提示词前添加素材引用：
```typescript
let fullPrompt = prompt;
const refs: string[] = [];
upstream.images.forEach(img => refs.push(`[图片素材: ${img.assetName}]`));
upstream.videos.forEach(vid => refs.push(`[视频素材: ${vid.assetName}]`));
if (refs.length > 0) fullPrompt = `${refs.join(' ')}\n${prompt}`;
```

### 素材名称标签显示
在素材框左上角显示名称标签：
```tsx
<div style={{
  position: "absolute", top: 8, left: 8, zIndex: 10,
  background: "rgba(0,0,0,0.6)", padding: "2px 8px", borderRadius: 4,
  pointerEvents: "none",
}}>
  <svg ...>{/* 图片/视频图标 */}</svg>
  <span style={{ fontSize: 11, color: "white", fontWeight: 500 }}>{cfg.assetName || "素材"}</span>
</div>
```

**cfg类型定义必须包含assetName：**
```typescript
const cfg = d.config as {
  content?: string;
  model?: string;
  assetName?: string;  // 必须加这个字段
  // ...
};
```

## 弹出动画偏好（2026-06-15）

**阿戴喜欢的动画效果：**

**阿戴喜欢的动画效果：**
```css
/* 从下方弹出 + 缩放 + 弹性曲线 */
animation: popUp 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);

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

**规则：** 对话框/控制面板弹出时使用 `popUp` 动画，不要用简单的 `fadeIn`。

## 完整性原则（阿戴核心要求）

**问题：** 父容器有 `onClick={(e) => { e.stopPropagation(); e.preventDefault(); }}` 时，子元素的点击事件被阻止，导致子元素（如VideoPreview）点击无效。

```tsx
// ❌ 错误 - 父容器的 e.preventDefault() 阻止子元素点击
<div onClick={(e) => { e.stopPropagation(); e.preventDefault(); setShowControls(!showControls); }}>
  <VideoPreview onDoubleClick={() => setShowPreview(true)} />  {/* 点击无效 */}
</div>

// ✅ 正确 - 父容器只用 stopPropagation，不用 preventDefault
<div onClick={(e) => { e.stopPropagation(); }}>
  <VideoPreview onDoubleClick={() => setShowPreview(true)} />  {/* 正常工作 */}
</div>
```

**规则：** 在父容器的 onClick 中，`e.preventDefault()` 会阻止所有子元素的点击事件。只在需要阻止冒泡时用 `e.stopPropagation()`，不要用 `e.preventDefault()`。

## ReactFlow 节点内子组件点击事件设计 (CRITICAL 2026-06-15)

### 核心区分：三种"框"（阿戴UI术语）

1. **"对话交流框"** = 节点内的控制面板（输入提示词、选择模型、生成按钮），通过 `showControls` 状态控制显示
2. **"属性面板"** = 右侧 PropertyPanel（ReactFlow选中节点后自动显示）
3. **"放大预览"/"预览对话框"** = PreviewModal 全屏模态框（点击放大按钮触发）

**这三个是完全不同的东西，绝对不要混淆！**

### 点击事件设计规则

**核心原则：单击视频区域 → 显示"对话交流框"（控制面板）**

```tsx
// ✅ 正确 - 单击显示控制面板（对话交流框）
<div onClick={(e) => { e.stopPropagation(); setShowControls(true); }}>
  <VideoPreview ... />
</div>

// 控制面板（对话交流框）包含：输入提示词、模型选择、生成按钮
{showControls && (
  <div onMouseDown={(e) => e.stopPropagation()}>
    <textarea placeholder="描述任何你想要生成的内容" ... />
    <select>模型选择</select>
    <button onClick={handleGenerate}>生成</button>
  </div>
)}
```

### 交互设计模式

| 用户操作 | 期望效果 | 实现方式 |
|---------|---------|---------|
| 鼠标悬停 | 播放视频 | `onMouseEnter` + `video.play()` |
| 鼠标移开 | 暂停视频 | `onMouseLeave` + `video.pause()` |
| 单击预览区 | 显示"对话交流框"（控制面板） | `onClick={(e) => { e.stopPropagation(); setShowControls(true); }}` |
| 点击放大按钮 | 打开PreviewModal全屏预览 | `onClick={(e) => { e.stopPropagation(); onExpand(); }}` |

### 控件区域防止拖拽

控件区域（播放/暂停、进度条等）需要阻止 `onMouseDown` 冒泡防止节点拖拽，但不要阻止 `onClick`：

```tsx
// ✅ 正确 - 用onMouseDown阻止拖拽，onClick正常工作
<div onMouseDown={(e) => e.stopPropagation()}>
  <button onClick={togglePlay}>Play/Pause</button>
  <div onClick={handleSeek}>Progress Bar</div>
</div>

// ❌ 错误 - 用onClick阻止冒泡会导致子按钮失效
<div onClick={(e) => e.stopPropagation()}>
  <button onClick={togglePlay}>不工作！</button>
</div>
```

### 放大预览仅通过按钮触发

```tsx
// ✅ 放大按钮 - 唯一触发PreviewModal的方式
<button
  onClick={(e) => {
    e.stopPropagation();  // 阻止冒泡，避免选中节点
    if (onExpand) onExpand();
  }}
  onMouseDown={(e) => e.stopPropagation()}  // 防止拖拽
>
  <FullscreenIcon />
</button>
```

### 双击事件的坑

**不要在ReactFlow节点中使用双击（onDoubleClick）打开预览：**
1. ReactFlow 的 `onNodeDoubleClick` 会拦截双击事件
2. 即使传空函数 `() => {}` 也不能阻止拦截
3. 完全移除 `onNodeDoubleClick` prop 才能让双击冒泡到节点

**结论：放弃双击，用单击显示控制面板 + 放大按钮打开预览。**

**详细案例见 `references/reactflow-doubleclick-interception.md`**

## 阿戴设计偏好（2026-06-15）

**主色调变更：** 从蓝紫色 #5e6ad2 改为白色 #ffffff

**替换清单：**
- `#5e6ad2` → `#ffffff`
- `#7c7cf8` → `#e0e0e0`
- `#828fff` → `#ffffff`
- `rgba(94,106,210,x)` → `rgba(255,255,255,x)`

**涉及文件：**
- globals.css (CSS变量)
- 所有节点组件 (进度条)
- BaseNode.tsx (类别颜色)
- NodePanel.tsx / PropertyPanel.tsx (侧边栏)
- VideoPreview.tsx (播放器)
- WorkflowCanvas.tsx (画布)

**视频预览控件偏好：**
- 不要文字提示（快捷键说明等）
- 控件紧凑（36px按钮、12-14px图标）
- 进度条细（3-4px）
- 时间显示在悬停时右下角
- 播放按钮不要太大的圆圈

## VideoPreview 外层 div 绝对不能有 onClick (CRITICAL 2026-06-15)

**问题：** VideoPreview 组件的外层 div 有 `onClick={togglePlay}`，会阻止事件冒泡到父容器（VideoNode），导致父容器的 onClick（显示控制面板）不触发。

**错误模式（反复出现3次）：**
```tsx
// ❌ 错误 - 阻止冒泡，父容器收不到点击
<div onClick={togglePlay}>
  <video ... />
</div>

// ❌ 错误 - 改成其他handler也不行，只要onClick存在就会阻止冒泡
<div onClick={(e) => { e.stopPropagation(); /* 任何逻辑 */ }}>
```

**正确做法：外层div完全不放onClick**
```tsx
// ✅ 正确 - 让事件正常冒泡到父容器
<div
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}
  // 没有onClick！
>
  <video ... />
</div>
```

**规则：** VideoPreview 组件只负责预览和控件显示，不处理单击逻辑。单击逻辑由父容器（VideoNode/ImageNode等）处理。

## 阿戴UI术语区分（CRITICAL 2026-06-15）

**三种"框"是完全不同的东西，绝对不要混淆！**

1. **"对话交流框"** = 节点内的控制面板（输入提示词、选择模型、生成按钮），通过 `showControls` 状态控制显示
2. **"属性面板"** = 右侧 PropertyPanel（ReactFlow选中节点后自动显示）
3. **"放大预览"/"预览对话框"** = PreviewModal 全屏模态框（点击放大按钮触发）

**当用户说"单击出现对话框"时，指的是"对话交流框"（控制面板），不是PreviewModal！**

**详细交互模式见 `references/video-preview-interaction-pattern.md`**

## 文件损坏时用 git checkout 恢复（2026-06-15 教训）

**场景：** 批量修改导致文件损坏（行号嵌入、语法错误），无法修复。

**正确做法：** 从 git 恢复到最后一个正常版本，然后用 patch 重新应用修改。

```bash
# 1. 找到最后一个正常版本
git log --oneline -10

# 2. 恢复特定文件
git checkout <commit> -- path/to/file.tsx

# 3. 恢复多个文件
git checkout <commit> -- src/components/nodes/VideoNode.tsx src/components/nodes/ImageNode.tsx

# 4. 或者恢复整个目录
git checkout <commit> -- src/components/

# 5. 然后用 patch 重新应用修改（不用 read_file + write_file）
```

**规则：** 文件损坏时，不要试图"修复"损坏内容——直接从 git 恢复，然后用 patch 重新做。

## 素材自动命名系统（2026-06-15）

**问题：** 使用模块级变量做计数器，页面刷新后重置，所有素材都叫同一个名字。

**正确做法：** 使用 `window` 全局变量存储计数器，跨组件共享且持久。

```typescript
const getGlobalCounter = (type: string) => {
  if (typeof window !== 'undefined') {
    const key = `__assetCounter_${type}`;
    (window as any)[key] = ((window as any)[key] || 0) + 1;
    return (window as any)[key];
  }
  return 1;
};

function getAssetName(nodeType: string): string {
  const type = nodeType.toUpperCase();
  if (type === "IMAGE") return `图素材${getGlobalCounter("IMAGE")}`;
  if (type === "VIDEO") return `视频素材${getGlobalCounter("VIDEO")}`;
  return "素材";
}
```

**存储位置陷阱：** `assetName` 存储在 `node.data.assetName`，不是 `node.data.config.assetName`。

```typescript
// 创建节点时
data: { label, category, nodeType, config: {...}, assetName } as NodeData

// 读取时 - 从 data 读取，不是 cfg
const d = props.data as unknown as NodeData;
const cfg = d.config as { assetName?: string; ... };

// ❌ 错误 - cfg.assetName 是 undefined
<span>{cfg.assetName || "素材"}</span>

// ✅ 正确 - 从 d.assetName 读取
<span>{d.assetName || "素材"}</span>
```

**cfg 类型定义必须包含 assetName：**
```typescript
const cfg = d.config as {
  content?: string;
  model?: string;
  assetName?: string;  // 必须加
  // ...
};
```

### 素材编号去重（2026-06-15 修复）

**问题：** 使用模块级变量或window全局变量做计数器，导致编号重复（所有素材都叫"素材2"）。

**根因：** 
1. 模块级变量在页面刷新后重置
2. window全局变量在React严格模式下可能被调用两次
3. NodePanel和CircleNavPanel各自有独立计数器

**正确做法：** 根据已有节点数量计算编号，不使用独立计数器。

```typescript
// ✅ 正确 - 根据已有节点数量计算
const getAssetName = (nodeType: string): string => {
  const type = nodeType.toUpperCase();
  const existingNames = nodes.map(n => (n.data as any)?.assetName || '');
  if (type === "IMAGE") {
    const count = existingNames.filter(n => n.startsWith('图素材')).length + 1;
    return `图素材${count}`;
  } else if (type === "VIDEO") {
    const count = existingNames.filter(n => n.startsWith('视频素材')).length + 1;
    return `视频素材${count}`;
  }
  return "素材";
};
```

**关键点：**
- `getAssetName` 函数必须在 `handleAddNode` 回调内部定义（可以访问 `nodes`）
- 不要在组件外部定义（无法访问最新的 nodes 状态）
- NodePanel 和 CircleNavPanel 都要用相同的逻辑

## @提及输入组件（2026-06-15）

**文件：** `frontend/src/components/MentionInput.tsx`

**功能：** 输入 `@` 弹出素材列表，支持键盘导航（↑↓箭头、回车选择、ESC关闭）。

**使用方式：**
```tsx
<MentionInput
  value={prompt}
  onChange={setPrompt}
  mentions={[
    ...upstream.images.map(img => ({ id: img.assetName, name: img.assetName, type: 'image' })),
    ...upstream.videos.map(vid => ({ id: vid.assetName, name: vid.assetName, type: 'video' })),
  ]}
  placeholder="输入@引用素材，如：@图素材1中的什么替换成@视频素材1中的什么"
/>
```

**默认选项（没有连接素材时）：**
```typescript
// 如果没有连接的素材，显示默认选项（带编号）
const defaultMentions: MentionItem[] = [
  { id: 'default-image-1', name: '图素材1', type: 'image' },
  { id: 'default-video-1', name: '视频素材1', type: 'video' },
];
const allMentions = mentions.length > 0 ? filteredMentions : defaultMentions.filter(m =>
  m.name.toLowerCase().includes(filterText.toLowerCase())
);
```

**提示词自动注入素材名称：**
```typescript
let fullPrompt = prompt;
const refs: string[] = [];
upstream.images.forEach(img => refs.push(`[图片素材: ${img.assetName}]`));
upstream.videos.forEach(vid => refs.push(`[视频素材: ${vid.assetName}]`));
if (refs.length > 0) fullPrompt = `${refs.join(' ')}\n${prompt}`;
```

## 素材名称标签位置（2026-06-15）

**用户要求：** 素材名称标签在预览区外面（左上角），不是在预览区内部。

```tsx
// ✅ 正确 - 在预览区外面
<div style={{ position: "relative" }}>
  {/* 素材名称标签 - 在预览区外面 */}
  <div style={{
    display: "flex",
    alignItems: "center",
    gap: 4,
    padding: "4px 8px 4px 4px",
    marginBottom: 4,
  }}>
    <svg ...>{/* 图标 */}</svg>
    <span style={{ fontSize: 11, color: "rgba(255,255,255,0.8)", fontWeight: 500 }}>
      {d.assetName || "素材"}
    </span>
  </div>
  
  {/* 预览框 */}
  <div style={{ ... }}>
    <VideoPreview ... />
  </div>
</div>

// ❌ 错误 - 在预览区内部（会被遮挡）
<div style={{ position: "relative" }}>
  <div style={{ position: "absolute", top: 8, left: 8, zIndex: 10 }}>
    <span>{cfg.assetName || "素材"}</span>  {/* cfg 读取位置也错了 */}
  </div>
  <VideoPreview ... />
</div>
```

## 上游素材收集模式（2026-06-15）

**所有生成节点必须收集所有上游素材（多图+多视频）：**

```typescript
const getUpstreamAssets = useCallback(() => {
  const incomingEdges = edges.filter((e) => e.target === props.id);
  const assets: { 
    images: Array<{ url: string; assetId: string; assetName: string }>; 
    videos: Array<{ url: string; assetId: string; assetName: string }> 
  } = { images: [], videos: [] };

  for (const edge of incomingEdges) {
    const sourceNode = nodes.find((n) => n.id === edge.source);
    if (sourceNode) {
      const nodeData = sourceNode.data as unknown as NodeData;
      const url = nodeData.assetUrl || (nodeData.config as any)?.assetUrl;
      const assetId = nodeData.assetId || (nodeData.config as any)?.assetId;
      const assetName = nodeData.assetName || (nodeData.config as any)?.assetName || "素材";

      if (url) {
        const assetType = nodeData.assetType || (url.match(/\.(mp4|mov|avi)$/i) ? "VIDEO" : "IMAGE");
        if (assetType === "IMAGE") {
          assets.images.push({ url, assetId: assetId || "", assetName });
        } else if (assetType === "VIDEO") {
          assets.videos.push({ url, assetId: assetId || "", assetName });
        }
      }
    }
  }
  return assets;
}, [edges, nodes, props.id]);
```

**关键：** `assetName` 读取时兼容两层位置：`nodeData.assetName || nodeData.config.assetName`

## ⚠️ CRITICAL: 不要声称修改已完成但实际未落实（2026-07-04 教训，反复出现）

**问题**：我多次声称"已修复"、"已部署"、"已推送到GitHub"，但实际上代码并没有真正修改。DeepSeek 每次审查都发现了这个问题。这个问题在同一个session中反复出现5次以上。

**用户纠正原话**：
- "不是他妈的才修改到模块3吗刚刚"
- "为什么没落实前面，把改完的代码给我"
- "必须严格按照要求修改"
- "按照要求改！注意原则bdd和tdd，别蒙头乱改"

**错误模式**（每个都实际发生过）：
1. 说"已修复"但代码中仍有旧代码（如 `#0a84ff` 蓝色按钮）
2. 说"已部署"但构建可能失败
3. 说"已推送"但Git可能超时
4. 声称"类型安全"但仍有 `as NodeData` 断言
5. 说"config.assetUrl已移除"但代码中仍有
6. 说"fileInputRef已删除"但代码中仍有

**正确做法**：
1. **修改后必须验证** - 用 `search_files` 确认修改确实生效
2. **构建后必须检查** - 用 `npm run build` 确认无错误
3. **测试后必须确认** - 用 `npm test` 确认测试通过
4. **部署后必须验证** - 检查 Vercel 输出确认部署成功
5. **不要声称"已完成"除非真正验证过**

**强制验证清单**（每次修改后必须执行）：
```bash
# 1. 修改后验证 - 确认旧代码已移除
search_files("old_code_pattern")  # 应返回 0 结果
# 确认新代码已添加
search_files("new_code_pattern")  # 应返回 >0 结果

# 2. 构建验证
npm run build 2>&1 | tail -5  # 必须显示 "Ready in"

# 3. 测试验证
npm test 2>&1 | tail -10  # 必须显示 "Tests X passed"

# 4. 部署验证
npx vercel --prod --yes --force 2>&1 | tail -5  # 必须显示 "Ready in"
```

**关键教训**：用户能看出来你说谎了。不要为了"看起来完成了"而声称完成。诚实地说"还在修改中"比说"已完成"但实际没改好要好得多。

## ⚠️ CRITICAL: TDD/BDD 必须严格执行（2026-07-04 教训，反复出现）

**问题**：我多次跳过 TDD/BDD 流程，直接修改代码再测试。用户反复纠正，但我仍然偷懒。

**用户纠正原话**：
- "先测试，再继续。你先检查一下你每次完成任务都遵守了bdd和tdd原则吗"
- "为什么没有遵守"
- "慢慢来。不着急。每一步都完善好"
- "一定要慢，一定要遵守btt和tdd原则，一定要尽可能完善"
- "继续p1，一定要慢，一定要遵守btt和tdd原则"

**正确流程**（每次修改必须走完）：
1. **写 BDD 场景** - 描述用户行为和期望结果
2. **写 failing test** - 测试应该失败（因为功能未实现）
3. **实现代码** - 让测试通过
4. **运行测试** - 确认测试通过
5. **构建验证** - 确认无 TypeScript 错误
6. **部署验证** - 确认线上正常

**错误做法**（实际发生过）：
- 直接修改代码再测试
- 跳过 BDD 场景
- 声称"已修复"但未运行测试
- 说"构建通过"但实际有错误
- 说"测试通过"但实际未运行

**教训**：用户说"慢慢来不着急"时，意思是"每一步都要完善好"，不是"可以慢慢来不用着急"。这是对质量的要求，不是对速度的宽容。

## ⚠️ DeepSeek 代码审查工作流（2026-07-04 建立）

**模式**：将代码分模块发送给 DeepSeek 审查，然后根据反馈逐个修复。

**步骤**：
1. **分模块** - 将代码按功能分为6个模块：
   - 模块1：状态管理（workflow-store-jotai.ts, settings-store-*.ts）
   - 模块2：Hooks（use-upstream-data.ts, use-poll-public-url.ts, use-asset-upload.ts, use-keyboard-shortcuts.ts）
   - 模块3：节点组件（base-node.tsx, image-node.tsx, video-node.tsx, text-node.tsx, composite-node.tsx）
   - 模块4：Canvas和UI（persistent-canvas.tsx, node-sidebar.tsx, error-boundary.tsx, workspace-content.tsx）
   - 模块5：后端（main.py, config.py, database.py, api/*.py, services/*.py）
   - 模块6：账号系统和云端存储（auth-context.tsx, route.ts, supabase.ts, asset-management.ts）

2. **生成文件** - 使用 `execute_code` 将每个模块的代码写入 `/tmp/antoken-module{N}.txt`

3. **用户粘贴给 DeepSeek** - 用户复制文件内容粘贴给 DeepSeek

4. **DeepSeek 返回审查报告** - 包含问题列表和修复建议

5. **逐个修复** - 按照 TDD/BDD 流程逐个修复问题

6. **验证修复** - 构建、测试、部署

7. **再次发送给 DeepSeek** - 确认修复正确

**关键原则**：
- 不要声称"已完成"除非真正验证过
- 每个修复都要走 TDD/BDD 流程
- 修复后要再次发送给 DeepSeek 确认

## React Flow NodeProps 类型限制（2026-07-04 教训）

**问题**：`NodeProps<NodeData>` 不直接工作，因为 React Flow 的 `NodeProps` 期望 `Node` 类型，不是 `NodeData`。

**错误尝试**：
```tsx
// ❌ 不工作
interface BaseNodeProps extends NodeProps<NodeData> { ... }

// ❌ 也不工作
interface BaseNodeProps extends NodeProps<Node<NodeData>> { ... }
```

**正确做法**：使用 `NodeProps` + 类型断言
```tsx
// ✅ 工作
interface BaseNodeProps extends NodeProps { ... }

function BaseNodeComponent({ data, selected, children, className }: BaseNodeProps) {
  const d = data as NodeData;
  // 使用 d.xxx
}
```

**原因**：React Flow 的 `NodeProps` 类型定义期望 `Node` 类型（包含 id, position, data 等），不是 `NodeData`（只有 data 字段）。

**规则**：不要尝试用 `NodeProps<NodeData>` 或 `NodeProps<Node<NodeData>>`，直接用 `NodeProps` + `as NodeData` 断言。
