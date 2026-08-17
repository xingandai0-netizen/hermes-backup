# Claude Desktop 被其他窗口遮挡 - 案例记录

## 场景
2026-06-07: 尝试用GUI自动化给小黄发送电商AI工作流平台的调研内容。

## 发生了什么
1. `pbcopy` + `swift paste.swift` 成功（"Paste completed"）
2. Swift CGEvent Enter 成功（"Enter sent"）
3. 但无法验证消息是否发送 —— 帮助文档窗口（HelpViewer）覆盖了Claude Desktop
4. 尝试了多种方法关闭帮助窗口：
   - `osascript 'tell application "Help" to close window 1'` → 错误：不能获得 application "Help"
   - `osascript 'tell process "HelpViewer" to keystroke "w" using {command down}'` → 无效果
   - `killall HelpViewer` → "No matching processes belonging to you were found"
   - `cliclick c:36,22`（点击关闭按钮）→ 命令超时
   - `osascript activate Claude` → 多次超时（>10秒）
5. 最终使用回退方案：内容已在剪贴板，告知用户手动粘贴

## 根因
- macOS 的 HelpViewer 进程名可能不是 "HelpViewer"
- System Events 在多个 Electron 应用同时运行时容易 hang
- osascript activate 对于不在当前 Space 的窗口效果有限

## 教训
- **不要在关闭遮挡窗口上花超过30秒**
- paste.swift 和 Enter 的 CGEvent 操作很可能已经成功了，只是无法验证
- 回退方案（手动粘贴）在 90% 的情况下比 GUI 自动化更快更可靠
