# Next.js 静态HTML模板集成

## 场景
购买的HTML模板（Webflow、Framer、纯HTML/CSS/JS）需要集成到Next.js项目中。

## 方案：next.config.mjs rewrite

### 1. 复制资源文件
```bash
# HTML放到public根目录
cp purchased-template.html frontend/public/template.html

# CSS和JS放到public子目录
cp -r template/css/ frontend/public/css/
cp -r template/js/ frontend/public/js/
cp -r template/fonts/ frontend/public/fonts/  # 如果有
```

### 2. 配置rewrite
```javascript
// frontend/next.config.mjs
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/',           // 访问根路径
        destination: '/template.html',  // 实际serve的文件
      },
    ];
  },
};
export default nextConfig;
```

### 3. 构建和部署
```bash
cd frontend && npm run build
npx vercel --prod --yes --force
```

## 注意事项
- rewrite不会改变URL（用户看到的是/，实际加载的是/template.html）
- 模板内的CSS/JS路径必须相对于public目录（如 `/css/style.css`、`/js/app.js`）
- CDN资源（如Webflow CDN的图片）可以直接使用，不需要下载
- Google Fonts需要在模板HTML中正确引用

## 不要用的方案
- ❌ 把HTML转成React组件（丢失JS交互）
- ❌ 用iframe嵌入（SEO不友好，样式隔离问题）
- ❌ 用dangerouslySetInnerHTML（XSS风险，JS不执行）
- ❌ 把CSS导入到globals.css（class名冲突）

## Antoken实际案例
- 模板：Cyrclo（Webflow模板，136KB HTML + 166KB CSS + 10个JS文件）
- 方案：`/` rewrite到 `/cyrclo.html`
- CSS: `/css/cyrclo.css`（从Webflow CDN下载的CSS）
- JS: `/js/`（GSAP、jQuery、ScrollTrigger、SplitText、Webflow交互JS）
- 结果：所有动画、交互、样式完美保留
