# Webflow Template Conversion Reference

## Cyrclo模板结构

文件位置: `/Users/macpro/Desktop/cyrclo_raw/`

```
index.html          136KB - 主页面(单HTML，所有内容)
css/                184KB - Webflow CSS(class命名系统)
js/                 ~500KB - jQuery + GSAP + ScrollTrigger + SplitText + Webflow运行时
```

## Webflow专有属性

- `data-w-id` - Webflow交互ID，驱动动画和交互
- `data-animation` - 动画类型(default, out, etc.)
- `data-collapse` - 导航栏折叠行为
- `data-duration` - 动画持续时间
- `w-nav`, `w-inline-block`, `w--current` - Webflow状态class
- `w-node-*` - 节点ID用于Flexbox/Grid布局

## 关键交互依赖

1. **GSAP + ScrollTrigger** - 滚动动画
2. **SplitText** - 文字拆分动画
3. **jQuery** - DOM操作和事件
4. **Webflow IX2** - 交互引擎(基于data属性)

## 内容替换清单

替换Cyrclo内容为Antoken内容时需要改的地方：
- 标题: "Cyrclo" → "Antoken"
- 描述: Marketing → 电商AI画布
- 导航: Home/About/Services → 工作空间/定价/功能
- CTA: Get Started → 免费开始创作
- FAQ: Marketing Q&A → 电商相关Q&A
- 定价: $1500/$3500 → Free/$9/$29
- Footer: cyrclo → Antoken
- 社交链接: Instagram/X/LinkedIn → GitHub/Twitter
- Logo: SVG logo → "A" + "Antoken"文字
