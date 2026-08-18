# Landing Page 最佳实践（2026-07-03 调研）

## 主流 AI 画布工具首页分析

| 工具 | 风格 | Hero | 特色 |
|------|------|------|------|
| TapNow | 暗色/影视感 | "Your Agentic Creative Canvas" | 产品演示+客户Logo |
| Krea.ai | 暗色/极简 | "AI Creative Suite" | 3000万用户+企业客户 |
| Midjourney | 暗色/哲学感 | 研究实验室宣言 | 社区驱动 |
| Runway | 暗色/研究感 | "Building AI to Simulate the World" | 企业合作 |
| Canva | 亮色/友好 | "Visual Suite for Everyone" | 大众市场 |

## 推荐区块结构（12个）

```
1.  Navbar（固定导航 + CTA）
2.  Hero（标题+副标题+CTA+产品演示）
3.  客户Logo（信任背书）
4.  功能亮点（3-4个核心功能，交替布局）
5.  产品演示（交互式展示）
6.  AI模型支持（Logo网格）
7.  使用场景（3步流程）
8.  定价表
9.  用户评价
10. FAQ
11. 最终CTA
12. Footer
```

## 设计原则

1. **暗色主题** — AI 工具标配（TapNow、Midjourney、Runway 都用暗色）
2. **产品演示 > 静态截图** — 交互式展示效果更好
3. **具体 CTA** — "免费开始创作" > "了解更多"
4. **信任背书** — 客户 Logo、用户数量、投资方
5. **简洁定价** — 3 档 > 6 档（TapNow 的 6 档太复杂）

## 推荐模板

| 模板 | Stars | 技术栈 | 暗色 |
|------|-------|--------|------|
| nobruf/shadcn-landing-page | 1.3k | Next.js + shadcn/ui | ✅ |
| launch-ui/launch-ui | 805 | Next.js 16 + Tailwind v4 | ✅ |

## SEO 配置

```typescript
// app/page.tsx
export const metadata: Metadata = {
  title: "Antoken — 电商人专属 AI 画布",
  description: "用 AI 一键生成电商主图、详情页、广告素材。",
  openGraph: {
    title: "Antoken — 电商人专属 AI 画布",
    description: "用 AI 一键生成电商主图、详情页、广告素材。",
    url: "https://antokex.com",
    siteName: "Antoken",
    locale: "zh_CN",
    type: "website",
  },
};

// app/sitemap.ts
export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: "https://antokex.com", lastModified: new Date(), priority: 1 },
    { url: "https://antokex.com/pricing", lastModified: new Date(), priority: 0.8 },
  ];
}

// app/robots.ts
export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: "*", allow: "/", disallow: ["/workspace", "/profile"] },
    sitemap: "https://antokex.com/sitemap.xml",
  };
}
```
