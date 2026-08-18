# 浏览器DevTools提取代码模板

**来源**: tapnow.ai UI逆向实战验证 (2026-07-05)
**用途**: 从运行中的网站提取真实CSS、动画、DOM结构

---

## 1. CSS变量提取

```javascript
// 找到包含主题变量的样式表
const sheet = Array.from(document.styleSheets).find(s => 
  s.href && s.href.includes('index-')  // 主样式表通常叫 index-xxx.css
);

if (sheet) {
  const rules = Array.from(sheet.cssRules || []);
  const rootRule = rules.find(r => 
    r.selectorText === ':root' || r.selectorText === ':root, :host'
  );
  
  if (rootRule) {
    const variables = {};
    for (let i = 0; i < rootRule.style.length; i++) {
      const prop = rootRule.style[i];
      if (prop.startsWith('--')) {
        variables[prop] = rootRule.style.getPropertyValue(prop);
      }
    }
    // 返回: { "--background": "#0f0f0f", "--primary": "#1fa2dc", ... }
  }
}
```

## 2. 动画关键帧提取

```javascript
const allSheets = Array.from(document.styleSheets);
const keyframes = [];

allSheets.forEach(sheet => {
  try {
    const rules = Array.from(sheet.cssRules || []);
    rules.forEach(rule => {
      if (rule.type === CSSRule.KEYFRAMES_RULE) {
        keyframes.push({
          name: rule.name,
          cssText: rule.cssText  // 完整的 @keyframes 定义
        });
      }
    });
  } catch (e) {
    // CORS限制，跳过跨域样式表
  }
});

// 返回: [{ name: "fadeIn", cssText: "@keyframes fadeIn { ... }" }, ...]
```

## 3. 组件库CSS提取（React Flow、Radix等）

```javascript
// 按文件名关键词找样式表
const canvasSheet = Array.from(document.styleSheets).find(s => 
  s.href && s.href.includes('vendor-pkg-canvas')  // React Flow
);

if (canvasSheet) {
  const rules = Array.from(canvasSheet.cssRules || []);
  // 过滤出React Flow相关的规则
  const flowRules = rules
    .filter(r => r.cssText.includes('react-flow') || r.cssText.includes('.xy-'))
    .map(r => r.cssText);
  
  // flowRules 包含所有 .react-flow__xxx 类的真实CSS
}
```

## 4. DOM元素HTML结构提取

```javascript
// 获取特定组件的完整HTML
const nodes = document.querySelectorAll('.react-flow__node');
const nodeHTMLs = [];

nodes.forEach((node, index) => {
  const dataId = node.getAttribute('data-id');
  const classes = typeof node.className === 'string' ? node.className : '';
  const style = node.getAttribute('style');
  
  // 获取所有子元素的类名
  const allClasses = [];
  node.querySelectorAll('*').forEach(el => {
    if (typeof el.className === 'string' && el.className.trim()) {
      allClasses.push(el.className.trim());
    }
  });
  
  nodeHTMLs.push({
    dataId,
    classes,
    style,
    html: node.outerHTML,           // 完整HTML（可直接复用）
    uniqueClasses: [...new Set(allClasses)]
  });
});
```

## 5. Sourcemap预检

```javascript
// 检查JS文件是否有sourcemap（有的话可以直接还原源码）
async function checkSourceMap(jsUrl) {
  const response = await fetch(jsUrl);
  const text = await response.text();
  const hasSourceMap = text.includes('//# sourceMappingURL=');
  const sourceMapMatch = text.match(/\/\/# sourceMappingURL=([^\s]+)/);
  
  return {
    hasSourceMap,
    sourceMapUrl: sourceMapMatch ? sourceMapMatch[1] : null,
    size: text.length
  };
}
```

## 6. 页面全局类名统计

```javascript
// 获取页面上所有CSS类名及使用次数
const allElements = document.querySelectorAll('*');
const classMap = {};

allElements.forEach(el => {
  if (el.className && typeof el.className === 'string' && el.className.trim()) {
    el.className.trim().split(/\s+/).forEach(cls => {
      if (!classMap[cls]) classMap[cls] = 0;
      classMap[cls]++;
    });
  }
});

// 按使用次数排序（高频类名通常是布局/工具类）
const sorted = Object.entries(classMap)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 50);
```

## 7. 技术栈识别

```javascript
// 检查构建工具
const scripts = document.querySelectorAll('script[src]');
const scriptSrcs = Array.from(scripts).map(s => s.src);

const isNextJs = scriptSrcs.some(s => s.includes('_next/static'));
const isVite = document.documentElement.outerHTML.includes('__vite__mapDeps');
const isWebpack = document.documentElement.outerHTML.includes('__webpack_require__');

// 检查框架
const isReact = !!document.querySelector('[data-reactroot]') || 
                !!window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
const isVue = !!window.__VUE__;
```

## 8. API端点提取

```javascript
// 从HTML中提取所有API路径
const html = document.documentElement.outerHTML;

// 方法1: 搜索/api/路径
const apiPaths = html.match(/\/api\/[a-zA-Z0-9_\-/]+/g) || [];

// 方法2: 搜索fetch调用
const fetchCalls = html.match(/fetch\(['"]([^'"]+)['"]/g) || [];

// 方法3: 搜索所有tapnow相关域名
const domains = html.match(/https?:\/\/[a-zA-Z0-9._-]+\.tapnow\.[a-zA-Z]+/g) || [];

// 方法4: 搜索端点变量
const endpoints = html.match(/endpoint['":\s]*['"]([^'"]+)['"]/gi) || [];
```

---

## 输出文件头部模板

每个提取的文件必须标注来源：

```css
/* ========================================
   [网站名] [组件名] - 真实爬取
   来源: https://example.com
   文件: index-xxx.css
   提取方法: document.styleSheets -> cssRules
   提取时间: YYYY-MM-DD
   ======================================== */
```

```html
<!-- 
  [网站名] [组件名] - 真实爬取
  来源: https://example.com
  提取方法: DOM直接读取 (querySelectorAll)
  提取时间: YYYY-MM-DD
-->
```
