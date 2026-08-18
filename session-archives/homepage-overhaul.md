# antokex首页改版+Bug修复 — 2026-05-09

## Task 2: 首页进后台"渲染出错" Bug ✅ 已修复

### 根因
brand-replace.js的injectHomePage()用`main.innerHTML = html`完全替换main的DOM内容，销毁React SPA的虚拟DOM引用。从`/`导航到`/login`时React找不到DOM → Error Boundary → "页面渲染出错"。

### 修复（brand-replace.js v17→v25，6个fix）
- FIX #11: injectHomePage用hide+append替代innerHTML替换（保护React DOM）
- FIX #11b: callback内race condition防重复注入wrapper
- FIX #12: innerHTML注入的`<script>`标签手动createElement执行
- FIX #13: 遍历main到document.documentElement所有祖先，修复overflow:hidden→visible + height:auto

### 关键代码
```javascript
// injectHomePage - 新方案
_hiddenReactChildren = [];
var children = Array.from(m.children);
for (var i = 0; i < children.length; i++) {
  _hiddenReactChildren.push(children[i]);
  children[i].style.display = 'none';
}
var wrapper = document.createElement('div');
wrapper.id = _homeWrapperId;
wrapper.innerHTML = html;
m.appendChild(wrapper);

// FIX #12: script手动执行
var scripts = wrapper.querySelectorAll('script');
for (var s = 0; s < scripts.length; s++) {
  var newScript = document.createElement('script');
  newScript.textContent = scripts[s].textContent;
  scripts[s].parentNode.replaceChild(newScript, scripts[s]);
}

// FIX #13: 修复SPA祖先overflow+height
var ancestor = m;
while (ancestor && ancestor !== document.documentElement) {
  var cs = window.getComputedStyle(ancestor);
  if (cs.overflow !== 'visible' || cs.overflowY !== 'visible') {
    ancestor.style.overflow = 'visible';
    ancestor.style.overflowY = 'visible';
  }
  var hPx = parseInt(cs.height, 10);
  if (hPx > 0 && hPx < 5000) {
    ancestor.style.height = 'auto';
    ancestor.style.minHeight = hPx + 'px';
  }
  ancestor = ancestor.parentElement;
}
```

### 踩坑
- SPA的DOM祖先层级多（app-layout→semi-layout→main→body），必须遍历到document.documentElement
- body的overflow:'auto hidden'需要匹配为非visible才修复
- body有height:100px(720px)固定值，必须改成auto
- main overflow:auto会创建内滚动容器，不应该设置main的overflow

---

## Task 1: 首页改版

### 最终页面结构
1. Hero区（标题+聊天框+模型ticker）
2. 最新支持ANTOKEX（padding-top:60px, max-width:1100px）
   - 左列：标题在上(21px, font-weight:500) + cover大图片在下(min-height:420px)
   - 右列：3个竖向卡片（gap:20px, padding-top:37px对齐大卡片）
3. 最新动态（padding:80px 40px 60px）
   - OpenAI风格：2列横向小卡片，左小图(64x64圆角) + 右文字(15px标题+13px灰色日期)
   - 底部分割线，hover opacity:0.7
4. 为什么选择ANTOKEX（4个pf-row，图文交替）
5. FAQ（details/summary原生手风琴）
6. Footer

### 品牌替换JS (brand-replace.js)
- 当前版本: v=25
- 核心变更: injectHomePage用hide+append策略，FIX #11/#11b/#12/#13
- Nginx配置: /etc/nginx/snippets/brand-replace.conf
- home-content HTML通过`<link rel="stylesheet" href="/assets/antokex-home.css">`引用外部CSS

### 图片规范
- news图片: 200x200正方形，JPEG q88，中心裁切，~5KB
- side-card配图: 600x400，JPEG q90，中心裁切去3%白边，~30KB
- cover图片: 1200x600，JPEG q90，~47KB
- pf图片: 800x450，JPEG q90，中心裁切去3%白边，~35KB
- 所有图片源: ~/Desktop/图片池/（用完删除原图）

### CSS架构
- 外部CSS: /assets/antokex-home.css (9866 bytes, 来自index.html.bak的<style>块)
- 内联CSS: home-content.html的`<style>`块（featured-grid, side-card等新样式）
- 两个CSS都用`#antokex-home`作用域隔离

### 三个新页面（占位，内容待定）
- /letter-to-users — 给用户的一封信
- /assistant — 个人客户助理
- /transparency — 透明查看后台模型数据
- Nginx: location = /xxx { try_files /xxx.html =404; }

### 服务器文件
| 文件 | 路径 | 说明 |
|------|------|------|
| brand-replace.js | /var/www/antokex/assets/antokex-brand-replace.js | v=25 |
| home-content.html | /var/www/antokex/assets/antokex-home-content.html | ~58KB |
| home.css | /var/www/antokex/assets/antokex-home.css | 9866 bytes |
| Nginx | /etc/nginx/sites-available/antokex-v14.conf | 含3个新location |
| brand-replace.conf | /etc/nginx/snippets/brand-replace.conf | ?v=25 |

### 已删除的PNG巨文件
pf_warm_orange.png, pf_purple.png, pf_cool_blue.png, pf_pink.png, cover-antokex.png, flower_cyan.png
（已有JPG替代品，PNG是冗余）

### 团队协作
- Phase 1方案由小黄（Claude Desktop GUI）输出
- 小黄免费额度用完后，小黑独立完成编码+部署
- 粘贴脚本: /tmp/team-collab/paste.swift
