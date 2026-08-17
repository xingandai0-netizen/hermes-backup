# Safari AppleScript JavaScript执行方法

## 背景
当需要从用户已登录的Safari浏览器中提取实时DOM数据（CSS变量、computed styles、DOM结构）时，
无法使用browser工具（agent的浏览器没有登录态），必须通过AppleScript驱动用户的Safari。

## 前提条件
- Safari已打开目标页面
- Safari的"开发"菜单中已启用"允许来自Apple Events的JavaScript"
  （Safari → 设置 → 高级 → 勾选"在菜单栏中显示开发菜单"，然后开发菜单 → 勾选"允许来自Apple Events的JavaScript"）

## 核心方法：base64编码 + osascript

直接传大段JS到osascript会因为引号/换行导致 `-2741` 语法错误。
**必须用base64编码绕过**：

```bash
# 1. 将JS代码写入文件
cat > /tmp/extract.js << 'JSEOF'
(function() {
  var r = {};
  var canvas = document.querySelector('.react-flow');
  if (canvas) {
    var cs = getComputedStyle(canvas);
    r.canvas = { bg: cs.backgroundColor, width: cs.width };
  }
  return JSON.stringify(r, null, 2);
})()
JSEOF

# 2. base64编码后通过osascript执行
B64=$(base64 -i /tmp/extract.js)
osascript -e "tell application \"Safari\" to tell window 3 to tell current tab to do JavaScript (do shell script \"echo $B64 | base64 -D\")"
```

## 查找正确的Safari窗口和Tab

```bash
# 列出所有窗口的Tab URL
osascript -e 'tell application "Safari" to get URL of every tab of window 1'
osascript -e 'tell application "Safari" to get URL of every tab of window 2'
# ...直到找到目标URL

# 切换到目标Tab
osascript -e 'tell application "Safari" to set current tab of window 3 to tab 4 of window 3'

# 验证页面标题
osascript -e 'tell application "Safari" to tell window 3 to tell current tab to do JavaScript "document.title"'
```

## 分批提取策略（避免输出过大）

JS执行结果通过AppleScript返回，输出有大小限制。分批提取：

1. **第一批**: CSS变量 (`:root`选择器中的`--`变量)
2. **第二批**: `@keyframes`动画 (`CSSRule.KEYFRAMES_RULE`)
3. **第三批**: 节点DOM结构 (`.react-flow__node` 的 `outerHTML`)
4. **第四批**: computed styles (`getComputedStyle` 对关键元素)
5. **第五批**: 组件HTML (侧边栏、右键菜单、下拉框等)

每批写一个独立的JS文件，分别执行。

## 提取CSS变量的JS模板

```javascript
(function() {
  var cssVars = {};
  for (var i = 0; i < document.styleSheets.length; i++) {
    try {
      var sheet = document.styleSheets[i];
      var rules = sheet.cssRules || sheet.rules;
      for (var j = 0; j < rules.length; j++) {
        var rule = rules[j];
        if (rule.selectorText === ":root") {
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

## 提取@keyframes动画的JS模板

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

## 提取Computed Styles的JS模板

```javascript
(function() {
  var r = {};
  var el = document.querySelector('.target-selector');
  if (el) {
    var cs = getComputedStyle(el);
    r.element = {
      bg: cs.backgroundColor,
      borderRadius: cs.borderRadius,
      border: cs.border,
      boxShadow: cs.boxShadow,
      // ...需要的属性
    };
  }
  return JSON.stringify(r, null, 2);
})()
```

## 查找动态弹出层（侧边栏、下拉框、菜单）

弹出层可能在执行JS时还未出现或已关闭。策略：
- 用户操作后立即执行（保持弹出层打开）
- 用宽泛选择器搜索：`[role="dialog"], [role="listbox"], [data-state="open"]`
- 用坐标+尺寸过滤：检查`getBoundingClientRect()`的width/height > 100
- 用文本内容匹配：检查`textContent`包含预期关键词

## 常见问题

- **"missing value"**: Safari没有打开的窗口，或JavaScript from Apple Events未启用
- **空输出**: JS代码执行出错，或AppleScript转义问题（用base64方法）
- **Safari窗口名 "xxx — (null)"**: 正常，这只是窗口标题格式
- **弹出层找不到**: 用户可能已关闭，或选择器不匹配。用更宽泛的搜索。

## 禁止事项
- **不要截图猜样式** — 用户明确要求逆向真实代码时，必须用getComputedStyle提取精确值
- **不要编造CSS值** — 所有值必须来自真实DOM，标注提取方法和来源
- **不要声称"已完成"但实际没改** — 提取后必须验证输出非空且包含预期数据
