---
name: team-collaboration-protocol
description: |
  三方团队协作强制协议。小黑(Hermes统筹) + Claude.app(方案规划) + VS Code Roo Code(编码优化)。
  收到任何任务必须自动开启，优先级最高。小黑作为唯一中转，真实传输指令到Claude.app和VS Code，禁止任何伪造行为。
tags: [team, collaboration, mandatory, startup, xiaohei, claude-app, vscode, roo-code]
version: 3.1
created: 2026-05-08
updated: 2026-05-09
---

# 三方团队协作协议 Team Collaboration Protocol v3.0

## ⚡ 强制执行规则

**此skill在收到任何任务时必须自动加载、自动执行，优先级最高。**
**小黑不得跳过任何阶段，不得伪造任何一方软件的输出。**
**所有三个软件必须真实参与，缺一不可。**

## 团队成员 Team Members

| 成员 | 软件 | 角色 | 交互方式 |
|------|------|------|----------|
| **小黑 (Xiao Hei)** | Hermes Agent | 统筹者、中转者、验收者 | 本体 |
| **小黄（残疾版）** | 小黄（残疾版）.app (原Claude.app) | 方案规划者、目标制定者 | GUI自动化(AppleScript+OCR) |
| **小白猪 (Xiao Bai Zhu)** | VS Code + Roo Code | 编码执行者、优化者 | VS Code自动化(AppleScript) |

## 工具路径

- 小黄（残疾版）: `/Applications/小黄（残疾版）.app`
- 小黄进程名 (System Events): `Claude` (不是"小黄")
- VS Code: `/Applications/Visual Studio Code.app`
- VS Code CLI: `/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code`
- Roo Code扩展: `rooveterinaryinc.roo-cline`

### ⚠️ 已知坑点 (2026-05-09验证)

1. **App激活必须用完整路径**: `tell application "Claude"` 返回 -43 找不到文件。必须用:
   ```bash
   osascript -e 'tell application "/Applications/小黄（残疾版）.app" to activate'
   ```
2. **TCC辅助功能权限**: osascript可能返回 -25211 "不允许辅助访问"。必须先检测:
   ```bash
   osascript -e 'tell app "System Events" to tell process "Claude" to return 1' 2>&1
   # 如果输出含 "-25211" → 权限不足，走降级路径
   ```
3. **长文本不能用keystroke**: 超过100字符的任务描述必须用pbcopy+Cmd+V:
   ```bash
   cat /tmp/task.md | pbcopy
   osascript -e 'tell app "System Events" to keystroke "v" using {command down}'
   ```
4. **OCR降级**: MiMo模型不支持vision(404)，必须用Swift Vision框架做OCR:
   ```bash
   swift - <<'SWIFT'
   import Vision, Cocoa
   let image = NSImage(contentsOfFile: "/tmp/screenshot.png")!
   let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil)!
   let request = VNRecognizeTextRequest()
   request.recognitionLevel = .accurate
   request.recognitionLanguages = ["zh-Hans", "en"]
   try VNImageRequestHandler(cgImage: cgImage, options: [:]).perform([request])
   for obs in request.results ?? [] {
       if let t = obs.topCandidates(1).first?.string { print(t) }
   }
   SWIFT
   ```

## ⚡ 核心流程（5阶段，必须全部执行）

```
阿戴下达任务
    ↓
小黑收到任务，自动启动团队协作流程
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: 方案规划 (Claude.app)                                │
│ 小黑 → 将任务描述发送到 Claude.app                            │
│ Claude.app → 输出技术方案、目标确认、实施计划                  │
│ 小黑 → 读取方案，确认完整性                                   │
├─────────────────────────────────────────────────────────────┤
│ Phase 2: 编码实现 (VS Code + Roo Code)                       │
│ 小黑 → 将方案发送到 VS Code 的 Roo Code                      │
│ 小白猪 → 按方案编写代码                                      │
│ 小白猪 → 完成编码，输出代码文件                               │
├─────────────────────────────────────────────────────────────┤
│ Phase 3: 第一轮检查润色 (小黑)                                │
│ 小黑 → 读取代码文件                                          │
│ 小黑 → 检查代码质量、逻辑正确性、错误处理                     │
│ 小黑 → 润色优化代码                                          │
│ 小黑 → 记录问题和改进点                                      │
├─────────────────────────────────────────────────────────────┤
│ Phase 4: 第二轮优化 (VS Code + Roo Code)                     │
│ 小黑 → 将检查结果和优化建议发送到 VS Code 的 Roo Code        │
│ 小白猪 → 根据反馈优化代码结构、性能、可读性                   │
│ 小白猪 → 完成优化，输出最终代码                               │
├─────────────────────────────────────────────────────────────┤
│ Phase 5: 三重验收 (小黑)                                      │
│ 第1次验收: 代码正确性 — 语法、逻辑、依赖                      │
│ 第2次验收: 功能验证 — 运行测试、浏览器验证                    │
│ 第3次验收: 最终确认 — 完整性、质量、交付标准                  │
└─────────────────────────────────────────────────────────────┘
    ↓
小黑汇总结果，交付阿戴
```

## Phase 1 详细步骤：Claude.app 方案规划

### 1.1 准备任务描述
小黑整理任务描述，包含：
- 任务目标
- 技术要求
- 约束条件
- 期望输出格式

### 1.2 发送到 Claude.app
使用 AppleScript 自动化 Claude.app：

```bash
# 激活小黄app — 必须用完整路径
osascript -e 'tell application "/Applications/小黄（残疾版）.app" to activate'
sleep 2

# 先检测TCC权限
PERM=$(osascript -e 'tell app "System Events" to tell process "Claude" to return 1' 2>&1)
if echo "$PERM" | grep -q "25211"; then
    echo "TCC权限不足，走降级路径"
    # 见下方"降级路径"章节
    exit 1
fi

# 长文本用 pbcopy + Cmd+V (不要用keystroke，会截断)
cat /tmp/team-collab/phase1-task-description.md | pbcopy
sleep 0.5

osascript <<'EOF'
tell application "System Events"
    tell process "Claude"
        set frontmost to true
        keystroke "v" using {command down}
        delay 0.5
        keystroke return
    end tell
end tell
EOF
```

### 1.3 等待 Claude.app 响应
```bash
# 等待 Claude 完成响应（监控停止按钮消失）
# Claude.app 在生成响应时会显示停止按钮
# 可通过 Accessibility API 检测
```

### 1.4 读取 Claude.app 响应
使用 macOS Vision OCR 读取屏幕内容：
```bash
# 截取 Claude.app 窗口 (用进程名"Claude")
screencapture -l$(osascript -e 'tell app "System Events" to tell process "Claude" to get id of window 1' 2>/dev/null) /tmp/team-collab/phase1-claude-response.png

# 使用 Swift Vision 框架做OCR (MiMo模型不支持vision API)
swift - <<'SWIFT'
import Vision, Cocoa
let image = NSImage(contentsOfFile: "/tmp/team-collab/phase1-claude-response.png")!
let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil)!
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["zh-Hans", "en"]
try VNImageRequestHandler(cgImage: cgImage, options: [:]).perform([request])
for obs in request.results ?? [] {
    if let t = obs.topCandidates(1).first?.string { print(t) }
}
SWIFT
```

### 1.5 保存方案
将 Claude.app 输出的方案保存到临时文件：
```bash
echo "$CLAUDE_RESPONSE" > /tmp/team-plan-phase1.md
```

## Phase 2 详细步骤：VS Code + Roo Code 编码

### 2.1 打开 VS Code
```bash
open -a "Visual Studio Code" /path/to/project
sleep 3
```

### 2.2 打开 Roo Code 面板
```bash
# 通过 VS Code 命令面板打开 Roo Code
osascript <<'EOF'
tell application "System Events"
    tell process "Code"
        set frontmost to true
        keystroke "p" using {command down, shift down}
        delay 1
        keystroke "Roo Code: Open in Editor"
        delay 0.5
        keystroke return
    end tell
end tell
EOF
```

### 2.3 发送方案到 Roo Code
```bash
# 在 Roo Code 输入框中输入方案
osascript <<'EOF'
tell application "System Events"
    tell process "Code"
        -- 找到 Roo Code 输入框
        -- 输入 Phase 1 的方案内容
        keystroke "PLAN_CONTENT_HERE"
        delay 0.5
        keystroke return
    end tell
end tell
EOF
```

### 2.4 等待编码完成
监控 Roo Code 的响应状态，等待编码完成。

### 2.5 读取代码输出
```bash
# 读取 Roo Code 生成的代码文件
cat /path/to/generated/code/file
```

## Phase 3 详细步骤：小黑第一轮检查润色

### 3.1 读取代码
小黑使用 read_file 或 terminal 读取 Phase 2 生成的代码文件。

### 3.2 代码质量检查
检查项目：
- [ ] 语法正确性
- [ ] 逻辑完整性
- [ ] 错误处理
- [ ] 命名规范
- [ ] 注释完整性
- [ ] 代码风格一致性
- [ ] 安全性检查
- [ ] 性能考虑

### 3.2.1 ⚠️ 配置文件额外检查 (Subagent生成配置时必须执行)

当Phase 2产出涉及服务器配置(Docker/Nginx/数据库)时，subagent没有SSH访问能力，
基于假设生成的配置往往与实际环境不符。Phase 3必须额外执行:

**必做对比流程:**
1. SSH读取服务器当前运行配置作为baseline
   ```bash
   ssh root@SERVER 'docker network ls'
   ssh root@SERVER 'docker inspect CONTAINER | jq'
   ssh root@SERVER 'nginx -T'
   ssh root@SERVER 'cat /etc/nginx/sites-available/antokex'
   ```
2. 逐项对比subagent生成的配置 vs 实际配置
3. 重点检查(已踩过的坑):
   - Docker网络名: 不要用假设名(如pgnet)，必须查`docker network ls`
   - 端口映射: 不要假设默认端口，查`docker ps`确认
   - 数据库/Redis连接串: host.docker.internal vs bridge IP，查网络gateway
   - Nginx location块结构: 必须与现有配置完全一致(除非明确要改)
   - 特殊端口用途: 如8088是Cloudflare Tunnel入口，不能改为redirect
   - API模型名称: 从当前运行配置读取，不从记忆/文档猜测

**教训**: 不确定的参数宁可从现有配置复制，不要猜。subagent生成配置≈草稿，Phase 3审查才出最终版。

### 3.3 润色优化
小黑直接修改代码：
- 修复发现的问题
- 优化代码结构
- 改善可读性
- 添加必要的注释
- 完善错误处理

### 3.4 记录改进点
将检查结果和改进点保存：
```bash
echo "改进点记录" > /tmp/team-review-phase3.md
```

## Phase 4 详细步骤：VS Code + Roo Code 优化

### 4.1 发送优化建议到 Roo Code
```bash
# 将 Phase 3 的检查结果发送到 Roo Code
osascript <<'EOF'
tell application "System Events"
    tell process "Code"
        keystroke "OPTIMIZATION_SUGGESTIONS_HERE"
        delay 0.5
        keystroke return
    end tell
end tell
EOF
```

### 4.2 等待优化完成
监控 Roo Code 的响应状态。

### 4.3 读取优化后的代码
```bash
cat /path/to/optimized/code/file
```

## Phase 5 详细步骤：小黑三重验收

### 第1次验收：代码正确性
```bash
# 检查语法
python3 -m py_compile /path/to/code.py
node --check /path/to/code.js

# 检查依赖
pip check
npm audit
```

检查清单：
- [ ] 语法无误
- [ ] 逻辑正确
- [ ] 依赖完整
- [ ] 无未定义变量
- [ ] 无类型错误

### 第2次验收：功能验证
```bash
# 运行代码
python3 /path/to/code.py
node /path/to/code.js

# 浏览器验证（如果是Web项目）
open http://localhost:PORT
```

检查清单：
- [ ] 程序正常运行
- [ ] 功能符合需求
- [ ] 无运行时错误
- [ ] 输出结果正确
- [ ] 浏览器显示正常

### 第3次验收：最终确认
```bash
# 完整性检查
ls -la /path/to/project/

# 代码行数统计
wc -l /path/to/code/*
```

检查清单：
- [ ] 所有文件完整
- [ ] 代码质量达标
- [ ] 文档注释齐全
- [ ] 符合交付标准
- [ ] 无遗留问题

## 反欺骗规则 Anti-Cheating Rules

### ⚠️ 绝对禁止行为

1. **禁止伪造 Claude.app 输出**
   - 不得自己编写方案然后声称是 Claude.app 生成的
   - 不得跳过 Claude.app 直接进入编码阶段
   - 必须真实通过 AppleScript 与 Claude.app 交互

2. **禁止伪造 VS Code 输出**
   - 不得自己编写代码然后声称是 Roo Code 生成的
   - 不得跳过 VS Code 直接进入检查阶段
   - 必须真实通过 AppleScript 与 VS Code 交互

3. **禁止跳过阶段**
   - 不得跳过任何 Phase
   - 不得合并 Phase
   - 不得简化 Phase

4. **禁止伪造交互记录**
   - 所有 AppleScript 调用必须真实执行
   - 所有 OCR 读取必须真实执行
   - 所有文件读写必须真实执行

### ✅ 验证方法

1. **Claude.app 交互验证**
   - 每次调用 Claude.app 必须截图保存
   - 截图路径: `/tmp/team-collab/phase1-claude-screenshot.png`
   - 小黑验收时检查截图是否存在

2. **VS Code 交互验证**
   - 每次调用 VS Code 必须截图保存
   - 截图路径: `/tmp/team-collab/phase2-vscode-screenshot.png`
   - 小黑验收时检查截图是否存在

3. **代码来源验证**
   - Phase 2 的代码必须来自 VS Code 的 Roo Code
   - Phase 4 的优化必须来自 VS Code 的 Roo Code
   - 小黑只做检查和润色，不替代编码

## 小黑职责清单

### 作为统筹者
- 接收阿戴任务
- 自动启动团队协作流程
- 协调三方软件的工作

### 作为中转者
- 将任务描述发送到 Claude.app
- 将方案发送到 VS Code
- 将检查结果发送到 VS Code
- 在三方之间传递信息

### 作为验收者
- 检查 Claude.app 的方案质量
- 检查 VS Code 的代码质量
- 执行三重验收
- 最终交付给阿戴

## 文件管理

### 临时文件目录
```
/tmp/team-collab/
├── phase1-task-description.md    # 任务描述
├── phase1-claude-response.md     # Claude.app 方案
├── phase1-claude-screenshot.png  # Claude.app 截图
├── phase2-vscode-code/           # VS Code 生成的代码
├── phase2-vscode-screenshot.png  # VS Code 截图
├── phase3-review-notes.md        # 小黑检查记录
├── phase4-optimized-code/        # 优化后的代码
├── phase4-vscode-screenshot.png  # VS Code 截图
└── phase5-verification-report.md # 验收报告
```

## 错误处理

### Claude.app 交互失败
1. 检查 Claude.app 是否正在运行: `pgrep -f "小黄" || pgrep -f "Claude"`
2. **检测TCC权限**: `osascript -e 'tell app "System Events" to tell process "Claude" to return 1' 2>&1`
3. 如果返回 -25211 → **走降级路径** (见下方)
4. 重试最多 3 次
5. 如果仍然失败，通知阿戴并等待手动干预

### ⚡ 降级路径：TCC权限不足时
当辅助功能权限未授予时，小黑无法通过AppleScript控制GUI。降级方案：

**方案A (推荐): delegate_task + Claude Code CLI**
- 使用 `delegate_task(acp_command="claude")` 启动Claude Code子进程
- 将任务描述作为goal传入，Claude Code输出方案
- 这是真正的"小黄参与"——Claude Code底层就是Claude
- 无需GUI权限，纯CLI自动化

**方案B: cliclick + Vision OCR 手动半自动**
- `brew install cliclick` — 可在无辅助权限下模拟鼠标点击（需TCC for keyboard）
- macOS Vision OCR (Swift脚本) 可读取屏幕文字 — 替代 vision_analyze
- ⚠️ Retina截图分辨率2880x1800，OCR前必须 `sips -z 900 1440` 缩小
- 流程: open app → cliclick点击输入框 → pbcopy粘贴 → OCR读回复
- ⚠️ cliclick的 `kd:/ku:` 键盘模拟需要辅助权限，仅 `c:` 鼠标点击可用

**方案C: 小黑独立完成方案规划**
- 小黑已经具备完整的上下文和调研能力
- 直接输出方案到文件 `/tmp/team-collab/phase1-plan.md`
- 向阿戴明确说明：因GUI权限限制，方案由小黑独立制定，非小黄输出
- 阿戴确认后继续Phase 2

**方案D: 阿戴手动中转**
- 小黑将任务描述写入 `/tmp/team-collab/phase1-task-description.md`
- 阿戴手动粘贴到小黄app，手动复制回复给小黑
- 小黑继续后续流程

**macOS Vision OCR脚本模板** (替代vision_analyze):
```swift
import Vision
import Cocoa
let image = NSImage(contentsOfFile: "/path/to/screenshot.png")!
let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil)!
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["zh-Hans", "en"]
request.usesLanguageCorrection = true
let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
try handler.perform([request])
for obs in request.results ?? [] {
    if let text = obs.topCandidates(1).first?.string {
        let bb = obs.boundingBox
        let x = Int(bb.origin.x * Double(cgImage.width))
        let y = Int((1.0 - bb.origin.y - bb.height) * Double(cgImage.height))
        print("(\(x),\(y)) \(text)")
    }
}
```

**Claude.app 关键路径信息**:
- 进程名: `Claude`
- App路径: `/Applications/小黄（残疾版）.app`
- Bundle ID: `com.anthropic.claudefordesktop`
- URL Scheme: `claude://new` (创建新对话)
- 激活命令: `open -a "/Applications/小黄（残疾版）.app"`
- ⚠️ 不要用 `tell application "小黄（残疾版）" to activate`，会timeout

**禁止**: 因TCC失败就卡死不动或无限重试。必须立即提供降级选项给阿戴。

### VS Code 交互失败
1. 检查 VS Code 是否正在运行
2. 检查 Roo Code 扩展是否已加载
3. 重试最多 3 次
4. 如果仍然失败，通知阿戴并等待手动干预

### 代码质量不达标
1. 返回 Phase 4 重新优化
2. 最多重试 2 次
3. 如果仍然不达标，通知阿戴并说明问题

## 成功标准

任务完成必须满足：
1. ✅ Claude.app 真实参与并输出方案
2. ✅ VS Code + Roo Code 真实参与并输出代码
3. ✅ 小黑完成三重验收
4. ✅ 所有截图和记录完整
5. ✅ 代码质量达标
6. ✅ 功能符合需求

## 示例工作流

### 阿戴任务: "创建一个Python脚本，统计文件夹中的文件数量"

**Phase 1: Claude.app 方案**
```
小黑 → Claude.app: "请为以下任务制定技术方案：创建一个Python脚本，统计文件夹中的文件数量。要求：支持递归统计、输出总文件数和各类型文件数。"
Claude.app → 小黑: "方案：使用os.walk递归遍历目录，使用collections.Counter统计文件类型，输出总文件数和各类型文件数。"
```

**Phase 2: VS Code 编码**
```
小黑 → Roo Code: "请根据以下方案编写Python脚本：使用os.walk递归遍历目录，使用collections.Counter统计文件类型，输出总文件数和各类型文件数。"
Roo Code → 小黑: (生成代码文件)
```

**Phase 3: 小黑检查润色**
```
小黑读取代码，检查质量，润色优化。
```

**Phase 4: VS Code 优化**
```
小黑 → Roo Code: "请根据以下反馈优化代码：添加错误处理、改善输出格式、添加命令行参数支持。"
Roo Code → 小黑: (生成优化后的代码)
```

**Phase 5: 三重验收**
```
第1次验收: 检查语法、逻辑、依赖
第2次验收: 运行脚本，验证功能
第3次验收: 确认代码质量，准备交付
```

## ⚠️ 最高原则

1. **真实性** — 所有交互必须真实发生，禁止伪造
2. **完整性** — 所有阶段必须执行，禁止跳过
3. **质量** — 代码质量必须达标，禁止敷衍
4. **透明** — 所有过程必须可追溯，有截图和记录
