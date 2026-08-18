# UI替换 vs UI修改 — 关键区分

## 阿戴2026-07-05的教训

### 用户原话
- "到底在几把改啥？" — 改了半天CSS但UI看起来没变化
- "都有代码了，我说了要一模一样有这么难吗？" — 用户给了目标UI的完整代码

### 根因
收到目标UI代码后，只修改CSS变量和样式值，而不是重写整个组件。没有检查同类型的其他组件（改了image-node但没改video-node）。

### 正确模式
1. 提取目标UI的完整DOM结构（outerHTML）和精确样式（getComputedStyle）
2. 直接用write_file重写整个组件文件
3. 保留原有业务逻辑（API调用、状态管理、事件处理）
4. **所有同类型组件一起改** — image-node改了，video-node、text-node也要改
5. 每个组件改完后build验证
6. 告诉用户Cmd+Shift+R硬刷新浏览器看效果

## 区分两种任务

| 任务类型 | 关键词 | 正确做法 |
|----------|--------|---------|
| UI修改 | "改一下颜色"、"调整间距"、"修个bug" | patch现有代码 |
| UI替换 | "原封不动替换"、"一比一复刻"、"照搬"、"和XX一样" | **重写整个组件** |

## Safari JS提取技术（已验证2026-07-05）

通过AppleScript在用户已登录的Safari中执行JavaScript提取DOM/CSS：

```bash
B64=$(base64 -i /tmp/extract.js)
osascript -e "tell application \"Safari\" to tell window 3 to tell current tab to do JavaScript (do shell script \"echo $B64 | base64 -D\")"
```

### 关键技巧
- 定位tab: `osascript -e 'tell application "Safari" to get URL of every tab of window N'`
- 切换tab: `osascript -e 'tell application "Safari" to set current tab of window N to tab M of window N'`
- base64必须: 直接传JS给osascript会因引号/特殊字符报错
- IIFE包裹: 所有JS用`(function(){...})()`避免重复声明const/let
- 输出截断: 复杂提取分多次执行（AppleScript返回有长度限制）

### 提取模板
```javascript
// CSS变量
var cssVars = {};
for (var i = 0; i < document.styleSheets.length; i++) {
  try {
    var rules = document.styleSheets[i].cssRules;
    for (var j = 0; j < rules.length; j++) {
      if (rules[j].selectorText === ':root') {
        for (var k = 0; k < rules[j].style.length; k++) {
          var prop = rules[j].style[k];
          if (prop.indexOf('--') === 0) cssVars[prop] = rules[j].style.getPropertyValue(prop).trim();
        }
      }
    }
  } catch(e) {}
}

// getComputedStyle精确值
var el = document.querySelector('.target');
var cs = getComputedStyle(el);
['backgroundColor','borderRadius','width','height','padding','boxShadow','backdropFilter','border','color','fontSize'].forEach(function(p){ r[p] = cs[p]; });
```
