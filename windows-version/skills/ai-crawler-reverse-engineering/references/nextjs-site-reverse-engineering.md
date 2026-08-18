# Next.js站点逆向工程实战记录

> 验证日期：2026-07-08
> 目标：suanlemeai.cn（算了么 - 东方命理推演云台）

## 技术栈确认

从curl获取的HTML源码中确认：
- **框架**：Next.js 14.2.29（从meta注释和chunk命名模式确认）
- **CSS文件**：`/_next/static/css/[hash].css`（单文件，360KB）
- **JS文件**：`/_next/static/chunks/[name]-[hash].js`（15个chunks，~830KB总计）
- **主题系统**：通过`data-theme`属性切换（ocean/dark/light）
- **本地存储**：`localStorage.getItem("suanle-me-store")`保存用户偏好

## 提取结果

### 文件清单
```
index.html (148KB) - 完整HTML，包含：
  - <link rel="stylesheet" href="/_next/static/css/e8020b2c73be30c9.css">
  - 15个<script src="/_next/static/chunks/xxx.js">标签
  - JSON-LD结构化数据（Schema.org）
  - 主题初始化内联脚本

css/e8020b2c73be30c9.css (360KB) - 完整样式
js/ (15个文件, ~830KB):
  - acfafb44-*.js (169KB) - 核心chunk
  - 8920-*.js (170KB) - 核心chunk
  - main-app-*.js - 主应用入口
  - layout-*.js - 布局组件
  - page-*.js - 首页组件
  - webpack-*.js - Webpack运行时
  - polyfills-*.js - Polyfills
  - 3327/399/5759-*.js - 工具页面chunks
  - 761/8898/193/5890-*.js - 共享chunks
```

### 关键发现
1. **Next.js App Router**：使用`app/`目录结构（不是pages/）
2. **React Server Components**：部分HTML由服务端生成
3. **代码分割**：每个工具页面独立chunk
4. **CSS变量系统**：`:root` + `[data-theme="ocean"]` + `[data-theme="dark"]`
5. **组件名（从HTML注释和chunk名推断）**：
   - ThemeProvider, LanguageProvider, ParticleBackground
   - Navbar, Footer, Hero, FeatureGrid
   - GlassCard, QuoteCard, DailyPractice

## 局限性

1. **不能直接静态serve**：Next.js需要SSR，纯静态文件服务会报"Application error"
2. **JS代码压缩混淆**：变量名被替换为短名称，需要beautify后分析
3. **组件分散**：React组件分布在多个chunk中，需要AST分析才能完整提取
4. **部分功能依赖后端API**：如用户登录、会员支付、AI解读

## 创建demo页面的技巧

由于Next.js不能直接静态serve，创建demo.html时：
1. **引用原始CSS**：`<link rel="stylesheet" href="/css/xxx.css">`
2. **复制Tailwind类名**：从HTML源码中提取class属性
3. **内联主题脚本**：复制`<script>`标签中的主题初始化代码
4. **手写HTML结构**：根据原始DOM结构重建页面骨架
5. **添加说明横幅**：标注"逆向复刻版本"避免混淆

## 与天机阁项目的关系

天机阁（/Users/macpro/tianji-ge）是阿戴自有的算命网站项目：
- 已有：八字排盘、紫微斗数、梅花易数、奇门遁甲
- 技术栈：Next.js 14 + React 18 + TypeScript + Tailwind CSS
- 排盘引擎：iztro（紫微）+ lunar-javascript（八字）

本次逆向的目的是**提取suanlemeai.cn的真实代码作为参考**，不是替代天机阁项目。
