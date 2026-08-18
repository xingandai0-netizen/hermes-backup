# Safari AppleScript + base64 编码提取法

**验证日期**: 2026-07-05
**验证场景**: TapNow (app.tapnow.ai) 工作空间UI逆向

## 核心方法

当用户Safari已登录目标网站时，可通过AppleScript在Safari中执行JavaScript提取真实DOM/computed styles。

### base64编码绕过AppleScript引号问题

```bash
# 1. 将JS代码写入文件
cat > /tmp/extract.js << 'JSEOF'
(function() {
  var r = {};
  var el = document.querySelector('.target');
  if (el) {
    var cs = getComputedStyle(el);
    r.bg = cs.backgroundColor;
  }
  return JSON.stringify(r, null, 2);
})()
JSEOF

# 2. base64编码后通过AppleScript执行
B64=$(base64 -i /tmp/extract.js)
osascript -e "tell application \"Safari\" to tell window 3 to tell current tab to do JavaScript (do shell script \"echo $B64 | base64 -D\")"
```

## 前置检查

```bash
# 确认JS执行可用
osascript -e 'tell application "Safari" to tell window 3 to tell current tab to do JavaScript "document.title"'

# 定位正确的window/tab
osascript -e 'tell application "Safari" to get URL of every tab of window 1'

# 切到目标tab
osascript -e 'tell application "Safari" to set current tab of window 3 to tab 4 of window 3'
```

## 关键发现

1. getComputedStyle返回oklch/oklab格式，不是hex
2. execute_code有50 tool call上限，大文件拆分用terminal for循环
3. IIFE必须包裹所有JS代码，避免重复const/let声明
4. macOS中文系统Safari窗口名是"Safari浏览器"
5. computer_use可能无法capture Safari（返回0x0），改用screencapture
