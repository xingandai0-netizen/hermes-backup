# CSS/样式真实提取方法

## 前提条件
- 需要通过浏览器访问目标网站（browser_navigate + browser_console）
- 没有sourcemap时（Vite生产构建通常不开），只能提取运行时数据

## 提取顺序

### Step 1: 检查sourcemap
```javascript
const response = await fetch(jsUrl);
const text = await response.text();
text.includes('//# sourceMappingURL=');
```
有sourcemap → 下载.map文件 → 用source-map库还原
没有sourcemap → 继续Step 2

### Step 2: 枚举所有样式表
```javascript
const sheets = Array.from(document.styleSheets);
const info = sheets.map(s => ({
  href: s.href,
  ruleCount: (() => { try { return (s.cssRules||[]).length; } catch(e) { return 'CORS'; } })()
})).filter(s => s.href && s.href.includes('目标域名'));
```

### Step 3: 按类型提取

#### CSS变量（设计令牌）
```javascript
const rootRule = rules.find(r => r.selectorText === ':root' || r.selectorText === ':root, :host');
const style = rootRule.style;
const vars = {};
for (let i = 0; i < style.length; i++) {
  if (style[i].startsWith('--')) vars[style[i]] = style.getPropertyValue(style[i]);
}
```

#### 动画关键帧
```javascript
allSheets.forEach(sheet => {
  Array.from(sheet.cssRules || []).forEach(rule => {
    if (rule.type === CSSRule.KEYFRAMES_RULE) {
      // rule.name = 动画名, rule.cssText = 完整定义
    }
  });
});
```

#### 组件库CSS（React Flow, Radix等）
```javascript
const vendorSheet = sheets.find(s => s.href.includes('vendor-pkg-canvas'));
const rules = Array.from(vendorSheet.cssRules);
const targetRules = rules.filter(r => r.cssText.includes('react-flow'));
```

#### 特定选择器的样式
```javascript
const rules = Array.from(sheet.cssRules);
const matches = rules.filter(r => 
  r.selectorText && r.selectorText.includes('.target-class')
);
```

### Step 4: 保存并标注来源
每个文件头部：
```css
/* 来源: {url}
   文件: {filename}
   提取方法: document.styleSheets -> cssRules
   提取时间: {date} */
```

## 已知限制
- CORS跨域样式表无法读取cssRules（CDN域名不同）
- 内联样式无法通过此方法获取
- JS动态生成的样式（CSS-in-JS）需要在运行时提取
- 高度压缩的JS（如Vite生产构建）无法还原源码，只能提取CSS变量和样式

## TapNow实战结果（2026-07-05）
- CSS变量: 100个（index-ojNnE14B.css）
- 画布样式: React Flow完整CSS（vendor-pkg-canvas-B1dDS-3J.css）
- 动画关键帧: 57个（分散在多个样式表中）
- Sourcemap: 未开启
- JS源码: 无法还原（Vite压缩混淆）
