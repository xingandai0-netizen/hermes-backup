---
name: nextjs-cache-troubleshooting
description: Next.js缓存问题排查和修复。当页面异常（CSS 404、JS加载失败、渲染异常但不报错）时，优先清除.next和.swc缓存。
triggers:
  - 页面卡住
  - 点击无反应
  - CSS 404
  - JS加载失败
  - 渲染异常
  - curl超时
  - 页面加载不出
  - dev server无响应
---

# Next.js 缓存问题排查

## 症状
- 页面加载但点击无反应
- CSS文件返回404
- JS chunks加载失败
- 渲染异常但控制台无错误
- 布局错乱
- **排版错误**（2026-06-27 反复出现）
- **Cannot find module './403.js'**（2026-07-06 出现，.next缓存损坏）

## 根本原因
多次修改代码后，`.next` 缓存目录积累旧编译结果，新旧代码冲突。**`.swc` 目录同样重要**——只清 `.next` 不清 `.swc` 仍然会出问题。

## 具体错误模式

### Cannot find module './403.js'（2026-07-06）
**症状**: Next.js报 `Error: Cannot find module './403.js'`，堆栈指向 `.next/server/webpack-runtime.js`
**原因**: `.next`缓存中残留了旧的chunk文件，热更新后引用了不存在的模块
**修复**: `rm -rf .next && npm run build`（只清.next即可，不需要清.swc）

## 解决方法

```bash
cd ~/antoken/frontend
rm -rf .next .swc node_modules/.cache
npm run dev
```

**注意：** 必须同时清除三个目录：
- `.next` — Next.js 编译输出
- `.swc` — SWC 编译器缓存
- `node_modules/.cache` — webpack/loader 缓存（2026-06-28 发现不清这个也会导致 CSS 编译失败）

## 预防措施
1. 每次大改代码后清缓存
2. 性能优化要逐步进行，每步验证
3. 出现异常先清缓存再排查

## 幻影语法错误（Phantom Syntax Error）

详见 `references/phantom-syntax-error-2026-06-14.md`。

**症状：** dev server报语法错误（如 `Expected ',', got '}'`），但实际文件内容完全正确。

**根因：** `.next` 缓存中的旧编译结果包含已修改/删除的代码，新编译时缓存版本与实际文件冲突。

**诊断步骤：**
1. 读取报错文件的实际内容，确认文件本身是否有语法错误
2. 如果文件正确但编译报错 → 100%是缓存问题
3. 清除 `.next` + `.swc` 缓存，重启dev server

**经验教训（2026-06-14）：** 不要假设编译报错=文件损坏。先验证文件，再清缓存。

## Dev Server 卡死（Hung Process）

**症状：** 页面完全加载不出来（curl 超时或返回空），浏览器也打不开，但 `lsof -i :3000` 显示进程还在 LISTEN。

**诊断：**
```bash
# 1. 确认端口有进程监听但无响应
lsof -i -P | grep LISTEN | grep node
curl -s -m 10 -o /dev/null -w "%{http_code}" http://localhost:3000

# 2. 检查 CPU/内存 — 卡死的 next-server 典型表现：CPU>100%, 内存>2GB
ps aux | grep next | grep -v grep
```

**典型指标（2026-06-28 实例）：** CPU 366%, 内存 42.9%（3.5GB），curl 返回空或超时。

**修复步骤：**
```bash
# 1. 杀掉卡死的进程（父子进程都要杀）
kill -9 <pid>

# 2. 清缓存（必须同时清 .next 和 .swc）
cd ~/antoken/frontend && rm -rf .next .swc

# 3. 重启
npm run dev
```

**与缓存问题的区别：**
- 缓存问题：页面能加载但渲染异常/JS报错
- 进程卡死：页面完全无法加载（curl超时/空响应），进程占用异常高的CPU和内存

## CSS 编译静默失败（Silent CSS Compilation Failure）

**症状：** 页面能加载但排版完全错乱，浏览器可能卡死。HTML 中有 `<link>` 引用 CSS 文件，但样式完全不生效。

**根因：** Next.js dev server 的 CSS 编译静默失败，`.next/static/css/` 目录存在但是空的。CSS URL 返回的是 404 HTML 页面而不是实际 CSS 内容。

**诊断步骤：**
```bash
# 1. 检查 CSS 目录是否有文件
find ~/antoken/frontend/.next/static/css -type f
# 如果输出为空 → CSS 编译失败

# 2. 直接请求 CSS 文件，看返回的是 CSS 还是 HTML
curl -s http://localhost:3000/_next/static/css/app/layout.css | head -5
# 如果以 <!DOCTYPE 或 <html 开头 → 返回的是 404 HTML，不是 CSS

# 3. 浏览器验证（如果能打开 DevTools）
# document.querySelectorAll('link[rel="stylesheet"]')[0].sheet.cssRules.length
# 如果返回 0 → CSS 没有生效
```

**浏览器控制台验证（2026-06-28）：**
```javascript
// 检查 CSS 规则数——如果返回 0，说明 CSS 没生效
const links = document.querySelectorAll('link[rel="stylesheet"]');
links.forEach(l => console.log(l.href, 'rules:', l.sheet ? l.sheet.cssRules.length : 0));
```

**修复：** 同上方解决方法（清三个缓存目录 + 重启 dev server）。

**与进程卡死的区别：**
- 进程卡死：curl 超时/空响应，CPU>100%，页面完全无法加载
- CSS 编译失败：curl 能返回 200 HTML，但 CSS 文件返回 404 HTML，页面能加载但无样式

## layout.tsx <head> 标签导致白屏（2026-07-15）

**症状：** 页面完全白屏，无任何错误提示

**根因：** 在 Next.js App Router 的 layout.tsx 中添加了 `<head>` 标签：
```tsx
// ❌ 错误写法 - 会导致白屏
<html lang="zh-CN">
  <head>
    <link href="https://fonts.googleapis.com/..." rel="stylesheet" />
  </head>
  <body>...</body>
</html>
```

**正确做法：** 使用 `metadata` 导出或在 `globals.css` 中导入字体：
```tsx
// ✅ 正确写法
export const metadata: Metadata = {
  title: '页面标题',
  description: '描述',
}

export default function RootLayout({ children }) {
  return (
    <html lang="zh-CN">
      <body style={{ fontFamily: "'Noto Sans SC', sans-serif" }}>
        {children}
      </body>
    </html>
  )
}
```

## 端口残留进程导致404（2026-07-15）

**症状：** `npm run dev` 启动后访问返回 Pages Router 风格的 404 页面（不是 App Router 的样式）

**根因：** 旧的 `next-server` 进程残留占用端口，新启动的 dev server 无法绑定

**诊断：**
```bash
# 检查端口占用
lsof -i :3000 | grep LISTEN
# 如果看到 next-server 进程，说明是旧进程
```

**修复：**
```bash
# 杀掉所有相关进程
pkill -f "next dev"
kill -9 $(lsof -t -i :3000) 2>/dev/null

# 清缓存
rm -rf .next

# 重启
npm run dev
```

## 浮点数数组索引导致 undefined（2026-07-15）

**症状：** 页面显示 "undefinedundefined" 而不是预期的值

**根因：** JavaScript 中用浮点数作为数组索引会返回 `undefined`：
```javascript
const index = (year / 4 + other) % 10  // 结果可能是 3.75
const value = array[index]  // undefined！
```

**修复：** 使用 `Math.floor()` 确保整数索引：
```javascript
const index = Math.floor(year / 4 + other) % 10
const value = array[index]  // 正确
```

## 验证
```bash
# 页面能加载
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000

# CSS 文件返回实际 CSS 内容（不是 HTML）
curl -s http://localhost:3000/_next/static/css/app/layout.css | head -3
# 应该看到 CSS 注释或规则，不是 <!DOCTYPE

# 关键词检查
curl -s http://localhost:3000 | grep -o "Antoken" | head -1
```
