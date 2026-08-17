---
name: xiaohuang-claude-desktop-gui
description: 通过GUI自动化对接小黄（Claude Desktop app）的完整流程。包括激活窗口、粘贴文本、发送消息、截取回复、提取完整响应。macOS专用。
version: 1.1
triggers:
  - 对接小黄
  - Claude Desktop GUI
  - 小黄方案
  - 小黄回复
  - claude desktop automation
---

# 小黄（Claude Desktop）GUI自动化对接技能

## 适用场景
当需要通过GUI控制小黄（Claude Desktop app，bundle: `com.anthropic.claudefordesktop`）发送任务并获取回复时使用。

## 前置条件
- macOS系统
- Claude Desktop已安装并登录
- 终端有辅助功能权限（System Settings → Privacy & Security → Accessibility）
- 工具已安装：cliclick（`brew install cliclick`）、Swift编译器

## 核心脚本文件
所有脚本位于 `/tmp/team-collab/`：
- `ocr-file.swift` — Swift Vision OCR，用法: `swift ocr-file.swift <image.png>`
- `paste.swift` — 激活Claude并Cmd+V粘贴
- `clear-input.swift` — Cmd+A全选+Delete清空输入框
- `scroll.swift` — CGEvent滚动（已废弃，见下方替代方案）

## 关键发现和踩坑记录

### 1. Electron App特性
- Claude Desktop是Electron应用，AX Accessibility API极简（只有AXGroup），无法通过AXSetAttributeValue设置文本
- osascript的`keystroke`对Electron不可靠，必须用Swift CGEvent

### 2. Retina坐标系
- 屏幕物理分辨率2880x1800，逻辑分辨率1440x900
- cliclick使用逻辑坐标
- OCR截图需要缩放到1440x900才能正确识别

### 3. 剪贴板竞争
- Terminal和Claude之间存在剪贴板竞争
- 必须用`pbcopy`设置剪贴板后**立即**运行Swift CGEvent paste脚本
- paste脚本用`NSPasteboard.general`独立读取剪贴板，不依赖系统Cmd+V

### 4. 滚动方案
- CGEvent scrollWheel在Claude中不生效（Electron渲染层拦截）
- **正确方案：不滚动，用Cmd+A + Cmd+C + pbpaste提取全部文本**

## 标准操作流程

### Step 1: 激活小黄窗口
```bash
osascript -e 'tell application id "com.anthropic.claudefordesktop" to activate'
sleep 2
```

### Step 2: 清空输入框（可选，如果是新对话则不需要）
```bash
# 窗口通常在 (98,28) 大小 (1200,800)
# 输入框在窗口底部中间，大约 (698, 770)
cliclick c:698,770   # 点击输入框区域
sleep 0.3
swift /tmp/team-collab/clear-input.swift
```

### Step 3: 粘贴任务文本
```bash
# 1. 将任务文本写入剪贴板
cat /tmp/team-collab/short-task.md | pbcopy
sleep 0.2

# 2. 激活Claude并粘贴（Swift CGEvent方式）
swift /tmp/team-collab/paste.swift
```

**paste.swift 核心逻辑：**
```swift
import Cocoa
// 激活Claude
NSRunningApplication.runningApplications(withBundleIdentifier:
    "com.anthropic.claudefordesktop").first?.activate()
usleep(500000)

// 从剪贴板读取
let pasteboard = NSPasteboard.general
let content = pasteboard.string(forType: .string) ?? ""

// Cmd+A 全选（清空旧内容）
let src = CGEventSource(stateID: .hidSystemState)
let cmdA = CGEvent(keyboardEventSource: src, virtualKey: 0x00, keyDown: true)!
cmdA.flags = .maskCommand
cmdA.post(tap: .cghidEventTap)
usleep(100000)
// ... keyUp ...

// Cmd+V 粘贴
let cmdV = CGEvent(keyboardEventSource: src, virtualKey: 0x09, keyDown: true)!
cmdV.flags = .maskCommand
cmdV.post(tap: .cghidEventTap)
```

### Step 4: 发送消息（Enter键）
```swift
// CGEvent发送Enter
let enter = CGEvent(keyboardEventSource: src, virtualKey: 0x24, keyDown: true)!
enter.post(tap: .cghidEventTap)
usleep(50000)
let enterUp = CGEvent(keyboardEventSource: src, virtualKey: 0x24, keyDown: false)!
enterUp.post(tap: .cghidEventTap)
```

**⚠️ CRITICAL PITFALL — Enter键可能失效（2026-06-03 确认）：**
在某些Claude Desktop版本中，所有Enter键方法都会被当作文字输入而非发送消息：
- `osascript key code 36` → 输入文字"return"
- `osascript keystroke return` → 输入文字"return"
- Swift CGEvent `virtualKey: 0x24` → 输入文字"return"
- Swift CGEvent `virtualKey: 0x4C` → 无效果
- `cliclick t:return` → 输入文字"return"

**如果Enter键失效，回退方案：**
1. `osascript keystroke` 可以正常输入普通文字（只有Enter/Return失败）
2. 对于短消息，用 `osascript -e 'tell application "System Events" to keystroke "你的消息"'` 逐段输入
3. 输入完成后，让用户手动在Claude Desktop中按Enter发送
4. 或者点击Claude输入框右侧的发送按钮（如果可见）

### Step 5: 等待小黄生成回复
- Claude Sonnet生成详细方案通常需要1-3分钟
- 复杂任务可能需要3-5分钟
- 可以轮询检查（每30秒截图OCR一次）

### Step 6a: 截图+OCR预览（快速检查是否在生成）
```bash
osascript -e 'tell application id "com.anthropic.claudefordesktop" to activate'
sleep 2
screencapture -x /tmp/team-collab/shot.png
osascript -e 'tell application "Terminal" to activate'
sleep 1
sips -z 900 1440 /tmp/team-collab/shot.png --out /tmp/team-collab/shot-s.png 2>&1 | tail -1
swift /tmp/team-collab/ocr-file.swift /tmp/team-collab/shot-s.png 2>&1
```

### Step 6b: 提取完整响应（推荐方式 — Cmd+A/C + pbpaste）
```bash
# 1. 激活Claude
osascript -e 'tell application id "com.anthropic.claudefordesktop" to activate'
sleep 1

# 2. 点击响应内容区域
cliclick c:700,400
sleep 0.3

# 3. Cmd+A 全选 + Cmd+C 复制（Swift CGEvent）
swift -e '
import Cocoa
let src = CGEventSource(stateID: .hidSystemState)
// Cmd+A
let keyA = CGEvent(keyboardEventSource: src, virtualKey: 0x00, keyDown: true)!
keyA.flags = .maskCommand
keyA.post(tap: .cghidEventTap)
usleep(100000)
let keyAUp = CGEvent(keyboardEventSource: src, virtualKey: 0x00, keyDown: false)!
keyAUp.flags = .maskCommand
keyAUp.post(tap: .cghidEventTap)
// Cmd+C
usleep(200000)
let keyC = CGEvent(keyboardEventSource: src, virtualKey: 0x08, keyDown: true)!
keyC.flags = .maskCommand
keyC.post(tap: .cghidEventTap)
usleep(100000)
let keyCUp = CGEvent(keyboardEventSource: src, virtualKey: 0x08, keyDown: false)!
keyCUp.flags = .maskCommand
keyCUp.post(tap: .cghidEventTap)
print("Cmd+A Cmd+C done")
' 2>&1

sleep 1

# 4. 切回终端，读取剪贴板
osascript -e 'tell application "Terminal" to activate'
sleep 0.5
pbpaste > /tmp/team-collab/claude-response-full.md
wc -l /tmp/team-collab/claude-response-full.md
```

**重要注意：** Cmd+A会选中Claude界面中所有可选文本（包括chat历史和当前响应），需要后续清理提取目标内容。

### Step 7: 清理提取的文本
pbpaste输出包含：
- Claude UI文本（"Claude finished the response"、"You said:"等）
- 历史消息中的pasted内容（重复出现）
- 实际响应内容
- 页脚文本（"Next time, try this in Cowork"等）

需要程序化清理：
```python
# 找到实际响应的起始（第一个独立的标题行）
# 去掉重复的pasted内容
# 去掉UI干扰文本
```

## 完整一键脚本模板

```bash
#!/bin/bash
# send-to-xiaohuang.sh — 发送任务给小黄并提取回复
# 用法: bash send-to-xiaohuang.sh <task-file.md>

TASK_FILE="$1"
WAIT_SECONDS=120  # 等待Claude生成的时间

# Step 1: 发送任务
cat "$TASK_FILE" | pbcopy
sleep 0.2

osascript -e 'tell application id "com.anthropic.claudefordesktop" to activate'
sleep 2

swift /tmp/team-collab/paste.swift
sleep 1

# Step 2: 发送Enter
swift -e '
import Cocoa
let src = CGEventSource(stateID: .hidSystemState)
let enter = CGEvent(keyboardEventSource: src, virtualKey: 0x24, keyDown: true)!
enter.post(tap: .cghidEventTap)
usleep(50000)
let enterUp = CGEvent(keyboardEventSource: src, virtualKey: 0x24, keyDown: false)!
enterUp.post(tap: .cghidEventTap)
print("Enter sent")
'

echo "等待${WAIT_SECONDS}秒让Claude生成回复..."
sleep "$WAIT_SECONDS"

# Step 3: 提取回复
osascript -e 'tell application id "com.anthropic.claudefordesktop" to activate'
sleep 1
cliclick c:700,400
sleep 0.3

# Cmd+A + Cmd+C
swift -e '
import Cocoa
let src = CGEventSource(stateID: .hidSystemState)
let keyA = CGEvent(keyboardEventSource: src, virtualKey: 0x00, keyDown: true)!
keyA.flags = .maskCommand; keyA.post(tap: .cghidEventTap)
usleep(100000)
let keyAUp = CGEvent(keyboardEventSource: src, virtualKey: 0x00, keyDown: false)!
keyAUp.flags = .maskCommand; keyAUp.post(tap: .cghidEventTap)
usleep(200000)
let keyC = CGEvent(keyboardEventSource: src, virtualKey: 0x08, keyDown: true)!
keyC.flags = .maskCommand; keyC.post(tap: .cghidEventTap)
usleep(100000)
let keyCUp = CGEvent(keyboardEventSource: src, virtualKey: 0x08, keyDown: false)!
keyCUp.flags = .maskCommand; keyCUp.post(tap: .cghidEventTap)
print("Extracted")
' 2>&1

sleep 1
osascript -e 'tell application "Terminal" to activate'
sleep 0.5
pbpaste > /tmp/team-collab/claude-response-full.md
echo "响应已保存: $(wc -l < /tmp/team-collab/claude-response-full.md) 行"
```

## ⚠️ GUI自动化的可靠性边界

**核心原则：GUI自动化是脆弱的，回退方案不是失败，是正确选择。**

以下情况应**立即**跳过GUI自动化，直接使用回退方案（让用户手动粘贴）：
1. **osascript activate 命令超时（>10秒）** — 说明系统事件链卡住了，继续尝试只会浪费时间
2. **有其他窗口覆盖Claude Desktop** — 尤其是HelpViewer、System Settings等系统窗口，无法可靠关闭
3. **computer_use capture返回0x0或"No on-screen window"** — 窗口不在当前Space
4. **连续2次操作无响应** — 不要尝试第3次

**不要在GUI问题上花超过2分钟。** 2分钟内搞不定，立刻回退。

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Enter后消息未发送 | Enter键被Electron当文字输入（"return"） | 回退方案1: osascript keystroke逐段输入文字，让用户手动按Enter |
| paste后输入框无文字 | 剪贴板竞争 | pbcopy后立即运行swift paste脚本，不要间隔 |
| OCR识别乱码 | 截图未缩放 | 必须sips -z 900 1440缩放后OCR |
| Cmd+A选中了整个窗口 | Claude界面特性 | 正常现象，pbpaste后程序化清理 |
| 滚动无效 | Electron渲染层拦截scroll事件 | 改用Cmd+A+C提取全文，不要滚动 |
| osascript keystroke无响应 | Electron不支持 | 改用Swift CGEvent |
| 辅助功能权限报错 | Terminal未授权 | System Settings → Privacy → Accessibility → 勾选Terminal |
| Python PIL分析截图坐标错位 | screencapture是Retina物理分辨率(2880x1800)，cliclick是逻辑分辨率(1440x900) | Python中坐标除以2：`logical_x = physical_x // 2`，`logical_y = physical_y // 2` |
| **HelpViewer窗口遮挡Claude** | macOS帮助文档窗口（HelpViewer进程）覆盖Claude窗口，osascript关闭和killall都可能失败。screencapture抓到的是帮助窗口而非Claude。 | 直接用回退方案（手动粘贴），不要反复尝试GUI操作。cliclick点击关闭按钮（约36,22）成功率不高。 |
| **"No on-screen window found"** | Claude Desktop窗口被最小化、在其他Space、或完全不可见。`list_apps`能看到进程但`focus_app`和`capture`都找不到窗口。 | **必须先让用户把Claude窗口切到当前屏幕**。osascript activate命令可能不够（尤其窗口在其他Space时）。无法自动解决——这是多Space macOS的根本限制。如果用户不在旁边，此流程阻塞。 |
| **Help窗口/其他窗口遮挡Claude** | macOS帮助文档或其他窗口覆盖了Claude Desktop窗口。`osascript activate`激活了Claude但窗口仍被遮挡。`killall HelpViewer`可能失败（进程名不匹配）。`cliclick`点击关闭按钮坐标不准。 | **直接使用回退方案**：不要反复尝试关闭遮挡窗口，改为手动粘贴。成功率远高于GUI自动化。 |
| **窗口被其他窗口遮挡** | macOS Help Viewer或其他系统窗口覆盖了Claude Desktop。osascript activate成功但screenshot抓到的是遮挡窗口。 | `killall HelpViewer`关闭帮助窗口，然后重新activate Claude。如果遮挡窗口不是HelpViewer，用`screencapture -x`全屏截图+vision_analyze确认哪个窗口在前面，然后针对性关闭。确认Claude可见后再执行paste流程。 |
| **其他窗口覆盖Claude** | HelpViewer、System Settings等窗口挡住了Claude Desktop。`killall HelpViewer`可能无效（进程名不同），osascript activate可能卡住。 | **不要反复尝试关闭。** 立刻使用回退方案：内容已在剪贴板中，告诉用户手动Cmd+Tab切到Claude并粘贴。 |
| **osascript activate 卡死/超时** | macOS System Events在某些状态下会hang，尤其是多个Electron应用同时运行时。 | 设置10秒超时。超时后直接回退，不要重试。 |
| **clear-input.swift 不存在** | 脚本可能未部署到 /tmp/team-collab/ | 不影响核心流程——paste.swift内部已经做了Cmd+A全选。如果需要清空输入框，直接用Swift CGEvent发送Cmd+A+Delete。 |

## 快速回退方案：用户手动粘贴

> 📎 详细案例：`references/blocking-window-case-study.md`（HelpViewer遮挡Claude的完整排查过程）

当GUI自动化失败（窗口不可见、Terminal被blocked、脚本未部署等）时，**不要反复尝试GUI操作**。改为：

1. 把要发给小黄的内容写成简洁的文本块
2. 直接发给用户，说"请复制粘贴给小黄"
3. 用户粘贴后等回复，再告诉你内容
4. 你分析整合小黄的建议

**这个方案的优先级不低** — 对于非实时协作场景（不需要自动提取回复），手动粘贴比GUI自动化更可靠。

**2次失败规则**：如果GUI操作连续失败2次（窗口遮挡、capture失败、activate无效等），立即切换到手动粘贴方案，不要继续尝试GUI hack。详见 `references/helpviewer-blocking-case-20260607.md`。
