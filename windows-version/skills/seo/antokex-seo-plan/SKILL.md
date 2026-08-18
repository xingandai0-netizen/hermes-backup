---
name: antokex-seo-plan
description: antokex.com SEO优化计划 - 技术SEO + 内容策略 + 执行清单
version: 1.0
tags: [seo, antokex, plan]
---

# antokex.com SEO 优化计划

## 目标
让 antokex.com 在搜索引擎中被目标用户找到，关键词覆盖 AI 工作流、AI 画布、AI 图片/视频生成等方向。

## 第一阶段：技术SEO基础（小黑执行）

### 1.1 sitemap.xml
- Next.js 生成动态 sitemap
- 包含所有页面：/、/workspace、/login、/blog/*
- 提交到 Google Search Console

### 1.2 robots.txt
- 允许爬取公开页面
- 禁止爬取 /workspace（需要登录）、/api/*
- 指向 sitemap.xml

### 1.3 Meta Tags 优化
```tsx
// 每个页面独立的 metadata
export const metadata: Metadata = {
  title: "Antoken - AI Workflow Editor | AI图片视频生成工作流",
  description: "可视化AI工作流编辑器，连接Gemini、DeepSeek、Seedance等模型，一站式完成图片和视频生成。",
  keywords: ["AI工作流", "AI图片生成", "AI视频生成", "可视化编辑器", "AI canvas"],
  openGraph: {
    title: "Antoken - AI Workflow Editor",
    description: "用AI连接创意与视觉输出",
    url: "https://antokex.com",
    siteName: "Antoken",
    images: [{ url: "https://antokex.com/og-image.png", width: 1200, height: 630 }],
  },
  twitter: { card: "summary_large_image" },
  alternates: { canonical: "https://antokex.com" },
};
```

### 1.4 结构化数据 (JSON-LD)
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Antoken",
  "applicationCategory": "DesignApplication",
  "description": "AI-powered visual workflow editor for image and video generation",
  "url": "https://antokex.com",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
  "operatingSystem": "Web"
}
```

### 1.5 页面速度
- Vercel Edge Network 已很快
- 优化：图片用 next/image、代码分割、预加载关键资源
- Core Web Vitals 目标：LCP < 2.5s, FID < 100ms, CLS < 0.1

### 1.6 Google Search Console
- 验证网站所有权
- 提交 sitemap
- 监控索引状态和搜索表现

## 第二阶段：关键词策略（小黑调研 + 阿戴确认）

### 2.1 核心关键词
| 关键词 | 搜索意图 | 优先级 |
|--------|----------|--------|
| AI workflow editor | 工具型 | 高 |
| AI图片生成工具 | 工具型 | 高 |
| AI视频生成工作流 | 工具型 | 高 |
| 可视化AI编辑器 | 工具型 | 中 |
| AI canvas editor | 工具型 | 中 |
| ComfyUI alternative | 竞品对比 | 中 |
| AI创作平台 | 信息型 | 中 |

### 2.2 长尾关键词机会
- "如何用AI生成图片教程"
- "AI视频生成工具对比"
- "Gemini图片生成怎么用"
- "Seedance视频生成教程"
- "AI工作流搭建指南"
- "免费AI图片生成平台"

### 2.3 竞品关键词分析
- TapNow.ai — 影视级AI创作
- Krea.ai — 实时AI生成
- ComfyUI — 节点式工作流
- Leonardo.ai — AI图片生成
- 分析竞品排名关键词，找差距和机会

> 📎 **详细竞品技术分析**：`references/competitor-website-technical-analysis.md`
> 包含11家竞品的技术栈、SEO结构化数据、性能优化对比、ROAS相关性分析、以及可复用的代码提取方法。

## 第三阶段：内容策略（小黑生成框架 + 阿戴审核发布）

### 3.1 博客文章计划
| 文章 | 目标关键词 | 类型 |
|------|-----------|------|
| Antoken：一站式AI工作流编辑器介绍 | AI workflow editor | 产品介绍 |
| 如何用AI生成高质量图片 | AI图片生成教程 | 教程 |
| AI视频生成工具对比：Seedance vs Kling vs Runway | AI视频生成对比 | 对比评测 |
| 从零搭建AI创作工作流 | AI工作流搭建 | 教程 |
| ComfyUI vs Antoken：节点式AI编辑器对比 | ComfyUI alternative | 竞品对比 |
| Gemini图片生成完全指南 | Gemini图片生成 | 教程 |
| AI图片视频生成：2026年最佳工具推荐 | AI生成工具推荐 | 列表文 |

### 3.2 内容SEO规则
- 每篇 1500-3000 字
- H1包含主关键词，H2/H3包含长尾词
- 首段100字内出现主关键词
- 图片alt text包含关键词
- 内链到产品页和其他文章
- 结尾CTA引导用户试用

### 3.3 Landing Page 优化
- 首页文案融入关键词
- Features页面每个功能单独描述
- 添加FAQ结构化数据
- 添加用户案例/使用场景页面

## 第四阶段：外链 + 持续运营（阿戴执行或外包）

### 4.1 外链建设
- Product Hunt 发布
- GitHub README 优化（star数、描述）
- AI工具目录提交（There's An AI For That、AI Tool Guru等）
- 社交媒体（Twitter/X、小红书、知乎）分享教程
- Guest posting 在 AI/SEO 相关博客

### 4.2 持续监控
- Google Search Console 周报
- Google Analytics 4 流量分析
- 关键词排名追踪（Ahrefs/SEMrush）
- 竞品动态监控

## 执行顺序

```
Phase 1（技术基础）→ 小黑可独立完成
  ├─ sitemap.xml + robots.txt
  ├─ Meta tags + Open Graph
  ├─ JSON-LD 结构化数据
  ├─ Google Search Console 提交
  └─ Core Web Vitals 优化

Phase 2（关键词）→ 小黑调研，阿戴确认
  ├─ 核心关键词确定
  ├─ 长尾词机会分析
  └─ 竞品关键词对比

Phase 3（内容）→ 小黑写框架，阿戴审核发布
  ├─ 博客系统搭建（Next.js MDX或类似）
  ├─ 首批7篇文章
  └─ Landing Page SEO优化

Phase 4（外链）→ 阿戴主导
  ├─ Product Hunt
  ├─ AI工具目录
  └─ 社交媒体推广
```

## 注意事项
- 不要用黑帽SEO手段（站群、关键词堆砌、隐藏文本）
- 内容质量优先，不要为了SEO写低质量文章
- 白帽SEO见效慢（3-6个月），需要耐心
- antokex.com 是.app 域名，Google对.app有HTTPS默认信任
- 当前维护页面状态下，等产品上线后再执行SEO
