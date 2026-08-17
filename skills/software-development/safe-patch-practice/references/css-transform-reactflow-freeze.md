# CSS Transform 覆盖导致页面卡死 - 2026-06-14

## 问题复现

在 `globals.css` 中添加了以下"高级感优化"：

```css
/* ❌ 这段代码导致页面完全卡死 */
.react-flow__node {
  transition: box-shadow 0.2s ease, transform 0.2s ease !important;
}
.react-flow__node:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
}
.react-flow__node.dragging {
  transform: scale(1.02) !important;
}
```

## 根因

React Flow 使用 `transform: translate(x, y)` 定位所有节点。CSS 中的 `transform` 覆盖会破坏定位系统，导致：
- 节点无法正确渲染
- 点击事件无法响应
- 拖拽完全失效

## 修复过程（错误方式）

1. 只移除了 `transform` 相关规则 → 页面仍然卡
2. 检查了 VideoNode 的 stopPropagation → 不是原因
3. 检查了 CompositeNode 语法错误 → 是旧缓存
4. 多次清除 `.next` 缓存重启 → 仍然卡

## 正确修复方式

**不要一个一个排查——直接 git 回退所有优化代码：**

```bash
cd ~/antoken/frontend
git log --oneline -5  # 找到最后一个正常的commit
git checkout <last-working> -- src/styles/globals.css src/components/canvas/WorkflowCanvas.tsx
rm -rf .next
npm run dev
```

确认页面恢复后，再一个一个重新加优化。

## 安全的 CSS 优化（不使用 transform）

```css
/* ✓ 安全 - 只改阴影和边框 */
.react-flow__node:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
}
.react-flow__node.selected {
  box-shadow: 0 0 0 2px var(--accent-bright), 0 4px 24px rgba(113, 112, 255, 0.2) !important;
}

/* ✓ 安全 - Handle 缩放（不影响节点定位） */
.react-flow__handle:hover {
  width: 14px !important;
  height: 14px !important;
  box-shadow: 0 0 8px var(--accent-bright) !important;
  transform: scale(1.3) !important;  /* Handle 上的 transform 是安全的 */
}
```

## 关键区别

| 元素 | transform 安全？ | 原因 |
|------|------------------|------|
| `.react-flow__node` | ❌ 绝对不安全 | React Flow 用 transform 定位节点 |
| `.react-flow__edge` | ❌ 不安全 | React Flow 用 transform 定位边 |
| `.react-flow__handle` | ✓ 安全 | Handle 定位不依赖 transform |
| `.react-flow__minimap` | ✓ 安全 | 独立组件 |
| `.react-flow__controls` | ✓ 安全 | 独立组件 |

## 教训

这是第二次发生同样的问题。第一次已经在 safe-patch-practice skill 中记录，但第二次仍然犯了同样的错误。

**原因：** 没有在修改前加载 skill。
**规则：** 任何 React Flow 相关的 CSS 修改，必须先加载 `safe-patch-practice` 和 `react-flow-css-pitfalls` skill。
