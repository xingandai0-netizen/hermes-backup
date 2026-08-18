---
name: template-adaptation
description: "模板集成与网站逆向完整指南：照搬优先原则、静态HTML serve（rewrite方式）、Webflow→React转换、Next.js集成陷阱、从活网站提取源码。合并了 html-template-integration、static-html-template-integration、webflow-template-to-react、website-reverse-engineering。触发：套用模板、照搬、用这个模板、集成HTML模板、Webflow模板、逆向网站、提取网站源码、复刻网站。"
tags: [template, ui, landing-page, webflow, adaptation]
---

# 模板适配模式

## 触发条件
- 用户提供HTML模板/设计稿/竞品页面
- 用户说"套用模板"、"用这个模板"、"根据这个改"
- 用户发截图说"按照这个做"

## 核心原则

**直接复用模板代码/结构/样式，只替换内容文字。不要"参考风格重新做一个"。**

阿戴在2026-07-04明确纠正：
> "啥意思，我都给你模版了，我让你套进去，不是自己按照这个做一个首页"

## 常见错误

```
用户: "这是首页模板，套进去"
❌ 做法: 参考模板风格，用React组件重写一个"类似"的首页
✅ 做法: 把模板HTML/CSS直接搬过来，替换文字和链接
```

## Webflow模板处理

Webflow模板的特点：
- 单HTML文件（100KB+），内联大量Webflow专有属性（data-w-id, w-node等）
- CSS在单独文件（100KB+），用Webflow class命名系统
- JS依赖：GSAP + ScrollTrigger + SplitText + jQuery
- 动画交互：Webflow的data属性驱动，非标准JS

### 处理方案

**方案1: 静态页面（快速上线）**
- 把HTML/CSS/JS放到 `public/` 目录
- 替换文字内容和链接
- 导航栏链接指向Next.js路由（/workspace, /login等）
- 缺点：不走Next.js路由，auth需要单独处理

**方案2: React组件（工程化）**
- 提取HTML结构为React组件
- CSS提取为全局样式文件
- JS交互用React hooks重新实现
- 能集成auth系统
- 工作量大，但长期可维护

### Webflow → React转换要点
1. `data-w-id` 属性 → React state + onClick
2. `.w-inline-block` → CSS display: inline-block
3. Webflow动画 → CSS transitions + GSAP (如保留)
4. 响应式断点 → media queries（Webflow用class控制）
5. Webflow CMS → Next.js数据获取

## 静态页面方案（推荐首选）

当用户说"照搬"、"直接搬上去"、"不要改"时，用静态页面方案最快最稳：

```bash
# 1. 复制HTML到public/
cp template/index.html frontend/public/template.html

# 2. 复制CSS（⚠️ 保持原文件名！）
cp template/css/*.css frontend/public/css/
# 不要改名！HTML中的href="css/xxx.css"必须匹配

# 3. 复制JS
cp template/js/*.js frontend/public/js/

# 4. next.config.mjs 添加rewrite
# async rewrites() { return [{ source: '/', destination: '/template.html' }] }
```

### ⚠️ CSS文件名必须完全匹配（2026-07-04教训）
HTML引用 `href="css/cyrclo.app.shared.8a67f88a8.css"`，如果复制时改名为 `cyrclo.css`，页面会白屏（CSS不加载）。
**必须保持原文件名**，或者更新HTML中的引用。

### 静态HTML集成详细步骤（from html-template-integration + static-html-template-integration）

#### Step 1: 复制资源到 public/
```bash
cp template.html frontend/public/template.html
cp template.css frontend/public/css/  # ⚠️ 保持原文件名！
cp -r template/js/ frontend/public/js/
```

#### Step 2: 配置 Next.js rewrite
```js
// frontend/next.config.mjs
const nextConfig = {
  async rewrites() {
    return [{ source: '/', destination: '/template.html' }];
  },
};
export default nextConfig;
```

#### Step 3: layout.tsx 中加载 CSS/JS
```tsx
import Script from "next/script";
// head 中:
<link rel="stylesheet" href="/css/original-name.css" />
// body 末尾:
<Script src="/js/library.js" strategy="beforeInteractive" />
<Script src="/js/app.js" strategy="afterInteractive" />
```

#### Step 4: 验证
```bash
curl -s -o /dev/null -w "%{http_code}" https://domain.com/css/xxx.css  # 200
curl -s -o /dev/null -w "%{http_code}" https://domain.com/js/xxx.js    # 200
curl -s -o /dev/null -w "%{http_code}" https://domain.com/              # 200
```

### 详细陷阱清单（from html-template-integration）

1. **CSS 文件名必须完全匹配** — HTML 引用 `css/cyrclo.app.shared.8a67f88a8.css`，文件就必须叫这个名字，改名→404→白屏
2. **JS 文件路径必须匹配** — 所有 `<script src="...">` 路径必须在 public/ 中存在
3. **相对 vs 绝对路径** — rewrite 从 `/` 到 `/template.html` 时，浏览器认为在 `/`，相对路径 `css/file.css` 正确解析为 `/css/file.css`
4. **Layout 包装** — rewrite serve 原始 HTML（有自己的 `<html>` 和 `<body>`），Next.js layout 不会应用
5. **Font 加载** — 模板通过 `<script>` 加载字体（如 WebFont.js），这些 JS 必须在 public/js/
6. **page.tsx redirect + rewrite = 307 循环** — 删除 page.tsx，只用 rewrite
7. **小屏幕缩放** — Webflow 模板为大屏设计，`<body style="zoom: 0.8">` 缩放

### Cloudflare CDN 缓存导致 404

**症状**：Vercel 部署成功（curl 200），用户浏览器看到 404。
**根因**：Cloudflare 缓存了旧的 404 响应。
**诊断**：`curl -s -I https://domain.com/ | grep -i "server\|cf-"` — "server: cloudflare" = 有 CDN。
**修复**：Cloudflare → 缓存 → 清除所有文件，或开启 Development Mode。

### Webflow → React 转换工作流（from webflow-template-to-react）

**⚠️ 只在用户明确要求"转换为React"/"工程化集成auth"时使用。"照搬"="直接放HTML"。**

#### Step 1: 分析模板结构
```bash
python3 -c "
import re
with open('template/index.html', 'r') as f:
    html = f.read()
classes = re.findall(r'class=\"([^\"]+)\"', html)
for c in classes: print(c)
"
```

#### Step 2: 逐 Section 转换
- 每个 section 一个文件
- `class` → `className`，`for` → `htmlFor`
- 保留所有 data 属性（data-w-id, data-animation, data-collapse）
- 保留所有嵌套层级（Webflow 的 circle-container > circle-wrapper > circle-block 有严格层级）
- 只替换文本内容

#### Webflow 特有结构
- `.w-nav` — 导航
- `.w-inline-block` — 内联块
- `.w-layout-grid` — 网格布局
- `data-w-id` — Webflow 元素 ID
- `data-animation` — 动画类型
- `data-collapse` — 折叠行为

#### 子 Agent 指令质量
给子 agent 的指令必须：
1. 明确说"保留所有原始 HTML 结构，不要简化任何嵌套"
2. 提供 python3 脚本提取 class 层级
3. 要求写完后 `npm run build` 验证
4. 子 agent 无法运行 build 时必须在主 agent 中验证

#### head+tail 文件操作陷阱
`head -N` 和 `tail -n +M` 拆分文件时，行号偏移会导致 after 文件为空。每次修改后重新计算行号，用 `wc -l` 确认。

## 从活网站提取源码（逆向工程）

当用户说"逆向网站"、"提取网站源码"、"复刻网站"时，从目标网站提取真实代码并整理为项目。

### 核心原则
1. **真实代码优先**：用curl获取真实HTML源码，不是web_extract（返回markdown格式）
2. **不编造代码**：所有代码必须有可验证来源
3. **按工程结构整理**：按标准项目结构组织（见下方标准结构）

### Phase 1: 侦察（5分钟）

```bash
# 1. 获取真实HTML源码（关键！web_extract返回markdown，不要用它）
curl -s -L "https://target.com/" -o /tmp/index.html

# 2. 提取资源URL
grep -oE '(src|href)="[^"]*\.(js|css)"' /tmp/index.html

# 3. 识别技术栈
grep -oE '_next/static|__webpack_require__|__vite__mapDeps' /tmp/index.html
```

**技术栈识别**：
- `_next/static` → Next.js
- `__webpack_require__` → Webpack
- `__vite__mapDeps` → Vite

### Phase 2: 资源文件下载（10分钟）

```bash
# 1. 下载CSS文件
curl -s -L "https://target.com/_next/static/css/xxx.css" -o css/main.css

# 2. 批量下载JS文件
for js in $(grep -oE '/_next/static/chunks/[^"]+\.js' /tmp/index.html); do
  curl -s -L "https://target.com$js" -o "js/$(basename $js)"
done

# 3. 下载图片等静态资源
for img in $(grep -oE 'src="[^"]*\.(jpg|png|svg)"' /tmp/index.html); do
  curl -s -L "$img" -o "images/$(basename $img)"
done
```

### Phase 3: 项目结构整理

整理为标准Next.js项目结构（与模板集成相同）：

```
项目名/
├── frontend/
│   ├── src/
│   │   ├── app/                # Next.js App Router
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── globals.css
│   │   ├── components/         # 组件
│   │   ├── contexts/          # Context
│   │   ├── hooks/             # Hooks
│   │   ├── stores/            # 状态管理
│   │   └── lib/               # 工具函数
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── tailwind.config.ts
└── backend/
    ├── main.py
    └── requirements.txt
```

**关键原则**：
- ❌ 不要按模块拆分（module1-state、module2-hooks等）
- ✅ 按功能分类（contexts、hooks、stores、components等）
- ✅ 保持标准的Next.js目录结构

### 逆向工程特有陷阱

1. **web_extract返回markdown格式** — 用 `curl -s -L` 获取真实HTML
2. **按模块拆分代码** — ❌ module1-state/、module2-hooks/ → ✅ src/stores/、src/hooks/
3. **编造代码** — ❌ 根据"常见模式"推测CSS变量值 → ✅ 从真实源码中提取
4. **忽略配置文件** — ❌ 只复制.tsx/.ts文件 → ✅ 包含package.json、tsconfig.json等
5. **遗漏字体和本地资源文件** — 检查所有 `next/font/local`、`@font-face` 引用的本地文件是否齐全

### Word文档图片查看

当用户给的Word文档中有UI设计图时：

```bash
# 方法1：textutil转换为HTML
textutil -convert html -stdout document.doc > /tmp/doc.html

# 方法2：用Preview打开后截图
open -a "Preview" document.doc
sleep 2
screencapture -x /tmp/screenshot.png

# 方法3：用vision_analyze查看截图
vision_analyze /tmp/screenshot.png "描述UI设计细节"
```

### 代码整理检查清单

- [ ] 所有源码文件按标准结构组织
- [ ] 包含完整的配置文件（package.json、tsconfig.json等）
- [ ] 包含README文档和启动说明
- [ ] 路径别名配置正确（@/指向src/）
- [ ] 字体和本地资源文件完整（grep检查localFont/@font-face引用）
- [ ] 依赖列表完整
- [ ] `npm run build` 验证通过

---

## 竞品UI 1:1复刻（非模板集成）

**区别于模板集成**：模板集成是"用户给你一个HTML文件，你放到项目里"。竞品复刻是"用户要你把现有项目的UI改成和另一个产品一模一样"。

**2026-07-05教训（阿戴极度不满）**:
用户要求把antoken-v2的工作空间UI替换为TapNow的UI。我做了CSS变量替换+样式修改，结果"改了个寂寞"——因为TapNow和antoken的组件结构完全不同（嵌套层次、组件拆分、DOM布局），只改颜色和间距无法达到1:1。

**正确做法**:
1. 获取目标产品的真实代码（逆向或用户提供）
2. 写全新组件，完全匹配目标的DOM结构
3. 用新组件替换旧组件（不是修改旧组件的CSS）
4. 保留现有组件的业务逻辑（API调用、状态管理），UI层全部重写

**判断标准**: 如果目标产品和现有产品的DOM结构差异 > 30%，必须整体替换，不能增量修改。

**阿戴术语辨别（已在ai-crawler-reverse-engineering中记录）**:
- "照搬"/"套用"/"直接用"/"原封不动"/"一比一复刻" = 整体替换
- "风格一样" = 只是视觉相似，不等于结构一致
- "都有代码了" = 用户已准备好目标代码，直接使用

## 截图对比UI修改

当用户发截图对比时，必须**逐像素对比**，不能只看大致风格。关键对比维度：
- 按钮填充色（透明 vs 填充#2a2a2a）
- 圆角大小（4px vs 8px vs 20px）
- 间距（紧凑 vs 松散）
- 边框（有无、粗细、颜色）
- 图标样式（线条粗细、图标类型）
- 文字层级（大小、颜色、字重）
- 背景透明度（0.75 vs 0.95 vs solid）

## Webflow → React 转换流程

详见 `references/conversion-checklist.md` 和 `references/webflow-template-conversion.md`。
