---
name: macOS WeChat Automation - Advanced Troubleshooting
description: Advanced techniques for handling WeChat automation failures on macOS
category: automation
tags: [wechat, automation, macos, applescript, troubleshooting]
---

### Failure Patterns Observed
1. **Invisible Window Syndrome**
   - App running but no active UI windows (`窗口数量: 0`)
   - Solution: Force activate + `open location "weixin://"`
   
2. **Element Identification Failures**
   - Accessibility tree not updating (`搜索框未找到`)
   - Solution: Use vision_analyze for fallback UI detection

3. **Focus Battles**
   - Input fields refusing focus even when visible
   - Solution: Coordinate-based clicking fallback

### Diagnostic Protocol
```bash
# Window status check
osascript -e 'tell app "System Events" to count windows of process "WeChat"'

# Focus hierarchy analysis
osascript -e 'tell app "System Events" to get entire contents of process "WeChat"'
```

### Recovery Workflow
```applescript
-- Emergency recovery sequence
tell application "WeChat"
  quit
  delay 1.0
  activate
  open location "weixin://"  -- Deep link forces main window
  delay 3.0
end tell
```

### Critical Notes
- Always verify window count >0 before UI automation
- Use randomized 1.2-3.8s delays between critical actions
- Account security: Never automate sensitive operations