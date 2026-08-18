# 竞品网站技术分析（2026-07-03）

> 分析方法：browser_navigate + browser_console 提取 meta tags、JSON-LD、script tags、图片优化情况
> 使用 delegate_task 并行分析（3批次×3-4个站点）

## 竞品列表

| 竞品 | 定位 | 投放时间 | ROAS | 近期ROAS | 日耗 |
|------|------|---------|------|---------|------|
| LumeFlow AI | AI视频+图片聚合 | 25年初 | 2+ | 1.6+ | $1,400 |
| TopMediai | AI视频+音乐+语音 | 24年初 | 2+ | 2+ | $7,000 |
| Morphic | Canvas画布+AI视频 | 25年9月 | 1.9 | 0.6(6月) | $2,000 |
| InVideo | Canva-like AI视频 | 22年 | 1.7 | 2.5+ | $15,000 |
| HeyGen | AI虚拟人+场景画布 | 21年 | 3.3 | 4.0 | $50,000 |
| Descript | AI视频编辑 | 22年 | 2.0 | 2.8 | $25,000 |
| Skywork | AI超级智能体 | - | - | - | - |
| Krea | AI创意套件 | 26年5月 | 2.0 | 2.0 | $1,500 |
| Storyboarder | AI故事板 | 24年 | 2.0 | 2.0 | €1,100 |
| Higgsfield | AI创意套件+LLM | 26年4月 | 12 | 12 | $32,000 |

## 技术栈

| 竞品 | 框架 | 托管 | 状态管理 | UI库 | CMS |
|------|------|------|---------|------|-----|
| LumeFlow | 原生HTML+jQuery | 自建 | - | - | - |
| TopMediai | 原生HTML+jQuery | 自建 | - | - | - |
| Morphic | Next.js (Turbopack) | Vercel | - | - | - |
| InVideo | Next.js (Turbopack) | 自建CDN | - | - | - |
| HeyGen | Next.js (App Router) | Cloudflare | - | - | Sanity |
| Descript | Next.js (App Router) | Cloudflare | - | - | Builder.io |
| Skywork | Vue.js 3 SPA | 阿里云S3 | Vuex/Pinia | Element Plus | - |
| Krea | SvelteKit SSR/SSG | 自建 | Svelte stores | 自定义 | - |
| Storyboarder | Astro SSG | 自建 | - | 自定义CSS | - |
| Higgsfield | Next.js (React SSR) | Cloudflare | Valtio | Radix UI+Framer Motion | - |
| **Antoken** | **Next.js 14** | **Vercel** | **Jotai** | **shadcn/ui** | - |

**结论：Next.js 是绝对主流（7/11）**

## SEO & 结构化数据

| 竞品 | JSON-LD | OG标签 | Twitter卡片 | hreflang | 评分 |
|------|---------|--------|------------|---------|------|
| HeyGen | WebSite+Organization+FAQPage+HowTo+16VideoObject+AggregateRating | 完整 | 完整 | 30+语言 | ⭐5 |
| Higgsfield | Organization+WebPage+WebSite+SearchAction+7SiteNavigationElement | 完整 | 完整 | - | ⭐5 |
| Krea | Organization+WebSite+SoftwareApplication+BreadcrumbList | 完整+图片尺寸 | 完整 | - | ⭐4 |
| Storyboarder | Organization+SoftwareApplication+AggregateRating(4.8/5,1200评) | 完整 | 完整 | - | ⭐4 |
| TopMediai | WebSite+Organization+WebApplication+FAQPage | 部分(仅og:image) | ❌ | 12语言 | ⭐3 |
| Descript | BreadcrumbList+Organization+21VideoObject | 部分 | 完整 | - | ⭐3 |
| Morphic | Organization+WebSite(多语言alt) | 完整 | 完整 | 5语言 | ⭐3 |
| InVideo | WebPage+SoftwareApplication | ❌缺og:image | summary(小图) | ❌ | ⭐2 |
| LumeFlow | WebSite | 部分(仅og:image) | ❌ | 3语言 | ⭐2 |
| Skywork | ❌无 | 完整 | 完整 | ❌ | ⭐2 |

## 性能优化

| 竞品 | 图片懒加载 | 图片格式 | 字体预加载 | Preconnect | Service Worker |
|------|-----------|---------|-----------|-----------|---------------|
| Morphic | 100% (57/57) | WebP (Next.js Image) | ❌ | ✅5个 | ❌ |
| HeyGen | 96% (131/137) | WebP (ImageKit) | ✅2个 | ✅5个 | ❌ |
| TopMediai | 95% (84/88) | PNG为主 | ❌ | ❌ | ❌ |
| InVideo | 91% (53/58) | PNG/JPG | ✅4个 | ✅3个 | ❌ |
| Krea | 83% (20/24) | WebP | ✅4个 | ❌ | ✅ |
| LumeFlow | 80% (117/147) | SVG为主 | ❌ | ❌ | ✅ |
| Higgsfield | 59% (33/56) | JPG | ✅15个 | ✅3个 | ❌ |
| Descript | 33% (86/263) | PNG/JPG | ❌ | ❌ | ❌ |
| Storyboarder | 30% (30/100) | PNG/JPG | ❌ | ✅Google Fonts | ❌ |
| Skywork | 0% (0/50) | WebP | ❌ | ✅ | ❌ |

## 分析方法（可复用）

### 提取 Tech Stack
```javascript
// 在 browser_console 中执行
JSON.stringify({
  framework: document.querySelector('[id="__next"]') ? 'Next.js' : 
             document.querySelector('[id="__nuxt"]') ? 'Nuxt' :
             document.querySelector('meta[name="generator"]')?.content || 'unknown',
  scripts: [...document.querySelectorAll('script[src]')].map(s => s.src).filter(s => !s.startsWith('data:')),
  meta: [...document.querySelectorAll('meta')].map(m => ({name: m.name, content: m.content, property: m.getAttribute('property')})),
  links: [...document.querySelectorAll('link[rel]')].map(l => ({rel: l.rel, href: l.href})),
})
```

### 提取 JSON-LD
```javascript
JSON.stringify([...document.querySelectorAll('script[type="application/ld+json"]')].map(s => JSON.parse(s.textContent)))
```

### 提取图片优化情况
```javascript
JSON.stringify({
  total: document.querySelectorAll('img').length,
  lazy: document.querySelectorAll('img[loading="lazy"]').length,
  webp: document.querySelectorAll('img[src*=".webp"]').length,
  avif: document.querySelectorAll('img[src*=".avif"]').length,
  srcset: document.querySelectorAll('img[srcset]').length,
  nextImage: document.querySelectorAll('img[src*="/_next/image"]').length,
})
```

### 提取 Preconnect/DNS-Prefetch
```javascript
JSON.stringify([...document.querySelectorAll('link[rel="preconnect"], link[rel="dns-prefetch"]')].map(l => ({rel: l.rel, href: l.href})))
```

## ROAS 与技术实现的相关性

**ROAS 最高的两个（HeyGen 4.0, Higgsfield 12）共同点：**
1. JSON-LD 结构化数据最丰富（FAQPage+HowTo+VideoObject/SearchAction）
2. 完整的 OG + Twitter 标签
3. 图片懒加载覆盖率高（96%+）
4. 多语言 hreflang
5. 多元化追踪系统（10+个）

**ROAS 最低的（Morphic 0.6, Descript 0.8）问题：**
- Morphic：70个视频在首页（太重）
- Descript：懒加载仅33%，无preconnect
