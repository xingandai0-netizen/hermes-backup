# Safari AppleScript JavaScript Extraction (实战验证 2026-07-05)

## 核心方法

当浏览器已登录目标网站时，通过AppleScript在Safari的当前tab中执行JavaScript，提取真实DOM/CSS/动画数据。

### 前提条件
- Safari已打开目标页面（需要登录态）
- Safari → Develop → 勾选"Allow JavaScript from Apple Events"

### 基本语法

```bash
# 简单JS执行
osascript -e 'tell application "Safari" to tell window 3 to tell current tab to do JavaScript "document.title"'

# 获取页面URL
osascript -e 'tell application "Safari" to get URL of every tab of window 3'
```

### 复杂JS注入（base64编码）

当JS代码包含引号、换行、特殊字符时，AppleScript的字符串转义极其麻烦。**用base64编码绕过**：

```bash
# 1. 写JS到文件
cat > /tmp/extract.js << 'EOF'
(function() {
  var r = {};
  var nodes = document.querySelectorAll('.react-flow__node');
  // ... 复杂逻辑
  return JSON.stringify(r, null, 2);
})()
EOF

# 2. base64编码后通过AppleScript注入执行
B64=$(base64 -i /tmp/extract.js)
osascript -e "tell application \"Safari\" to tell window 3 to tell current tab to do JavaScript (do shell script \"echo $B64 | base64 -D\")"
```

**⚠️ 关键**：`do shell script "echo $B64 | base64 -D"` 会先解码base64得到原始JS，再传给Safari执行。这比直接在AppleScript里转义引号可靠100倍。

### 找到正确的window和tab

Safari可能有多个window和tab，需要先定位：

```bash
# 列出所有window的tab URL
osascript -e 'tell application "Safari" to get URL of every tab of window 1'
osascript -e 'tell application "Safari" to get URL of every tab of window 2'
osascript -e 'tell application "Safari" to get URL of every tab of window 3'

# 切换到指定tab
osascript -e 'tell application "Safari" to set current tab of window 3 to tab 4 of window 3'

# 验证当前页面
osascript -e 'tell application "Safari" to tell window 3 to tell current tab to do JavaScript "document.title"'
```

## 实战提取模板

### CSS变量提取
```javascript
(function() {
  var cssVars = {};
  for (var i = 0; i < document.styleSheets.length; i++) {
    try {
      var sheet = document.styleSheets[i];
      var rules = sheet.cssRules || sheet.rules;
      for (var j = 0; j < rules.length; j++) {
        var rule = rules[j];
        if (rule.selectorText === ":root" || rule.selectorText === "*") {
          for (var k = 0; k < rule.style.length; k++) {
            var prop = rule.style[k];
            if (prop.indexOf("--") === 0) {
              cssVars[prop] = rule.style.getPropertyValue(prop).trim();
            }
          }
        }
      }
    } catch(e) {}
  }
  return JSON.stringify(cssVars);
})()
```

### @keyframes动画提取
```javascript
(function() {
  var kf = [];
  for (var i = 0; i < document.styleSheets.length; i++) {
    try {
      var sheet = document.styleSheets[i];
      var rules = sheet.cssRules || sheet.rules;
      for (var j = 0; j < rules.length; j++) {
        if (rules[j].type === CSSRule.KEYFRAMES_RULE) {
          kf.push(rules[j].name + "|||" + rules[j].cssText);
        }
      }
    } catch(e) {}
  }
  return kf.join("===KF===");
})()
```

### Computed Styles提取
```javascript
(function() {
  var r = {};
  var el = document.querySelector('.target-element');
  if (el) {
    var cs = getComputedStyle(el);
    r = {
      bg: cs.backgroundColor,
      borderRadius: cs.borderRadius,
      border: cs.border,
      boxShadow: cs.boxShadow,
      // ... 所有需要的属性
    };
  }
  return JSON.stringify(r, null, 2);
})()
```

### DOM结构提取
```javascript
(function() {
  var nodes = document.querySelectorAll('.react-flow__node');
  var result = [];
  for (var i = 0; i < nodes.length; i++) {
    var n = nodes[i];
    result.push({
      id: n.getAttribute("data-id") || "",
      type: n.getAttribute("data-type") || "",
      selected: n.classList.contains("selected"),
      outerHTML: n.outerHTML.substring(0, 3000),
      transform: n.style.transform || ""
    });
  }
  return JSON.stringify(result);
})()
```

## 已验证的提取结果（TapNow 2026-07-05）

从 app.tapnow.ai 提取了：
- 148个CSS变量（:root选择器）
- 40+个@keyframes动画
- 节点卡片、Handle、控制面板、生成按钮等20+组件的computed styles
- 侧边栏、右键菜单、模型下拉框的完整DOM结构
- 画布面板布局（5个react-flow__panel）

完整提取数据：`/Users/macpro/Desktop/tapnow-real-extraction.md`

## 注意事项

1. **不截图**：用户明确要求"不能截图"，要从DOM提取真实代码，不要从截图猜样式值
2. **IIFE包裹**：所有多行JS必须用`(function(){...})()`包裹，避免重复声明const/let导致SyntaxError
3. **window定位**：Safari的window编号不是固定的，每次都要先用`get URL of every tab`确认
4. **输出截断**：osascript输出超长时会被截断，分多次提取不同组件
5. **页面交互**：需要用户在Safari中操作（点击节点、打开菜单等）才能提取交互状态的DOM
