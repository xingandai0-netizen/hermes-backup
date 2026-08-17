---
name: desktop-control-advanced
description: >-
  桌面自动化控制高级技能，支持通过CLI完全控制macOS/Windows/Linux桌面。
  包括：截图、鼠标控制、键盘输入、Accessibility树控制、窗口管理等。
  基于agent-desktop (Rust)和usecomputer (Zig)两个高性能CLI工具。
version: 1.0.0
author: Hermes Agent
activation: /desktop
license: MIT
metadata:
  created: 2026-04-17
  sources:
    - https://github.com/lahfir/agent-desktop
    - https://github.com/remorses/usecomputer
---

# /desktop

桌面自动化控制：通过CLI完全控制电脑桌面，支持截图、鼠标、键盘、窗口管理。

## 触发条件

当用户提到以下内容时激活：
- "控制桌面"
- "自动化操作"
- "模拟鼠标点击"
- "模拟键盘输入"
- "截图"
- "操作应用"
- "控制窗口"

## 核心工具对比

| 特性 | agent-desktop | usecomputer |
|------|---------------|-------------|
| 语言 | Rust | Zig |
| 控制方式 | Accessibility树 | 像素坐标 |
| 命令数量 | 53个 | 10+个 |
| 输出格式 | 结构化JSON | JSON + 图片 |
| Token效率 | 减少78-96% | 标准 |
| 跨平台 | macOS/Windows/Linux | macOS/Linux/Windows |
| 安装 | npm install -g agent-desktop | npm install -g usecomputer |

## agent-desktop 详解

### 核心优势
- **通过Accessibility树控制** - 不依赖截图和像素匹配
- **确定性元素引用** - 使用`@e1`, `@e2`等引用元素
- **渐进式遍历** - 先获取骨架，再深入细节，减少78-96% token
- **53个命令** - 覆盖观察、交互、键盘、鼠标、通知、剪贴板、窗口管理

### 安装
```bash
npm install -g agent-desktop
# 或
brew install agent-desktop
```

### 权限配置
```bash
# 请求macOS辅助功能权限
agent-desktop permissions --request
```

### 观察命令 (Observation)

#### 获取Accessibility树快照
```bash
# 获取当前应用的交互元素
agent-desktop snapshot --app Safari -i

# 获取骨架视图（减少token）
agent-desktop snapshot --skeleton --app Slack -i --compact

# 获取特定元素的子树
agent-desktop snapshot --root @e3 -i --compact

# 获取菜单
agent-desktop snapshot --surface menu
```

#### 截图
```bash
# 获取应用截图
agent-desktop screenshot --app Finder
```

#### 查找元素
```bash
# 按角色查找
agent-desktop find --role button --app TextEdit

# 按名称查找
agent-desktop find --name "Save" --app TextEdit

# 按值查找
agent-desktop find --value "search text" --app Safari
```

#### 读取元素属性
```bash
# 读取值
agent-desktop get @e3 value

# 检查状态
agent-desktop is @e7 checked

# 列出表面（菜单、弹窗等）
agent-desktop list-surfaces --app Notes
```

### 交互命令 (Interaction)

#### 点击
```bash
# 智能点击（AX优先，15步回退链）
agent-desktop click @e3

# 双击（打开文件、选择单词）
agent-desktop double-click @e3

# 三击（选择行/段落）
agent-desktop triple-click @e3

# 右键点击（返回内联菜单树）
agent-desktop right-click @e3
```

#### 输入
```bash
# 在元素中输入文本
agent-desktop type @e5 "hello world"

# 直接设置值
agent-desktop set-value @e5 "new value"

# 清空元素
agent-desktop clear @e5

# 设置焦点
agent-desktop focus @e5
```

#### 选择
```bash
# 在下拉框/列表中选择
agent-desktop select @e9 "Option B"

# 切换复选框
agent-desktop toggle @e12

# 勾选/取消勾选
agent-desktop check @e12
agent-desktop uncheck @e12
```

#### 展开/折叠
```bash
# 展开树项目
agent-desktop expand @e15

# 折叠树项目
agent-desktop collapse @e15
```

### 键盘命令 (Keyboard)

```bash
# 按键
agent-desktop press enter
agent-desktop press escape
agent-desktop press "cmd+s"
agent-desktop press "ctrl+shift+n"

# 组合键
agent-desktop press "cmd+tab"
agent-desktop press "alt+F4"
```

### 鼠标命令 (Mouse)

```bash
# 移动鼠标
agent-desktop mouse move -x 500 -y 500

# 点击
agent-desktop mouse click -x 500 -y 500 --button left

# 拖拽
agent-desktop mouse drag -x1 100 -y1 100 -x2 500 -y2 500

# 滚动
agent-desktop mouse scroll -x 500 -y 500 --delta-y -100
```

### 窗口管理

```bash
# 列出窗口
agent-desktop list-windows

# 激活窗口
agent-desktop activate-window --app Finder

# 调整窗口大小
agent-desktop resize-window --app Finder --width 800 --height 600

# 移动窗口
agent-desktop move-window --app Finder --x 100 --y 100

# 最小化/最大化
agent-desktop minimize-window --app Finder
agent-desktop maximize-window --app Finder
```

### 通知和剪贴板

```bash
# 获取通知
agent-desktop notifications

# 设置剪贴板
agent-desktop clipboard set "text"

# 获取剪贴板
agent-desktop clipboard get
```

## usecomputer 详解

### 核心优势
- **截图 + 坐标控制** - 直观的视觉反馈循环
- **坐标映射** - 智能坐标转换
- **原生性能** - Zig编写，无Node.js运行时依赖
- **跨平台** - macOS/Linux/Windows

### 安装
```bash
npm install -g usecomputer
```

### 权限配置
- **macOS** - 需要为终端应用启用辅助功能权限
- **Linux** - 需要X11会话，设置`DISPLAY`
- **Windows** - 需要在交互式桌面会话中运行

### 快速开始
```bash
# 获取鼠标位置
usecomputer mouse position --json

# 移动鼠标
usecomputer mouse move -x 500 -y 500

# 点击
usecomputer click -x 500 -y 500 --button left --count 1

# 输入文本
usecomputer type "hello"

# 按键
usecomputer press "cmd+s"
```

### 工作流程：截图→操作→截图反馈
```bash
# 1. 截图
usecomputer screenshot --path ./screen.png

# 2. 分析截图，确定目标坐标

# 3. 移动并点击
usecomputer mouse move -x 400 -y 220
usecomputer click -x 400 -y 220 --button left --count 1

# 4. 再次截图验证
usecomputer screenshot --path ./after_click.png
```

### 坐标映射使用
```typescript
// TypeScript API
import * as usecomputer from 'usecomputer'

const screenshot = await usecomputer.screenshot({
  path: './tmp/shot.png',
  display: null,
  window: null,
  region: null,
  annotate: null,
})

const coordMap = usecomputer.parseCoordMapOrThrow(screenshot.coordMap)
const point = usecomputer.mapPointFromCoordMap({
  point: { x: 400, y: 220 },
  coordMap,
})

await usecomputer.click({
  point,
  button: 'left',
  count: 1,
})
```

## Agent工作模式

### 模式1：Accessibility优先（agent-desktop）
```
1. snapshot --app AppName -i  获取元素树
2. 找到目标元素 @eX
3. click/type/select @eX    执行操作
4. snapshot -i              验证结果
```

### 模式2：视觉反馈（usecomputer）
```
1. screenshot               获取屏幕截图
2. AI分析截图确定坐标
3. mouse move/click         执行操作
4. screenshot               验证结果
```

## 实战示例

### 示例1：打开Safari并搜索
```bash
# 1. 激活Safari
agent-desktop snapshot --app Safari -i

# 2. 找到地址栏并输入
agent-desktop type @e5 "https://google.com"
agent-desktop press enter

# 3. 等待页面加载后搜索
sleep 2
agent-desktop snapshot --app Safari -i
agent-desktop type @e10 "Python tutorial"
agent-desktop press enter
```

### 示例2：在Finder中创建文件夹
```bash
# 1. 激活Finder
agent-desktop snapshot --app Finder -i

# 2. 右键点击创建新文件夹
agent-desktop right-click @e50

# 3. 选择"新建文件夹"
agent-desktop snapshot --surface menu
agent-desktop click @e3

# 4. 重命名
agent-desktop type "New Folder"
agent-desktop press enter
```

### 示例3：使用usecomputer操作
```bash
# 1. 截图
usecomputer screenshot --path ./screen.png

# 2. 移动到"访达"图标并点击
usecomputer mouse move -x 100 -y 700
usecomputer click -x 100 -y 700 --button left --count 1

# 3. 截图验证
usecomputer screenshot --path ./after.png
```

## 最佳实践

### 1. 选择合适的工具
- **精确控制** → agent-desktop（Accessibility树）
- **直观操作** → usecomputer（截图+坐标）
- **复杂UI** → agent-desktop（减少token）
- **简单点击** → usecomputer（快速直接）

### 2. 权限管理
```bash
# macOS辅助功能权限
# 系统偏好设置 → 安全性与隐私 → 辅助功能
# 添加终端或应用到允许列表
```

### 3. 错误处理
```bash
# agent-desktop有内置重试机制
# 15步回退链确保点击成功

# usecomputer需要手动重试
usecomputer click -x 500 -y 500 --button left --count 3
```

### 4. Token优化
```bash
# 使用骨架视图减少token
agent-desktop snapshot --skeleton --app AppName -i --compact

# 只获取特定元素
agent-desktop snapshot --root @e3 -i --compact
```

## 与其他工具对比

| 工具 | 控制方式 | Token效率 | 性能 | 难度 |
|------|----------|-----------|------|------|
| agent-desktop | Accessibility树 | 极高 | 高 | 中 |
| usecomputer | 像素坐标 | 中 | 高 | 低 |
| AppleScript | UI脚本 | 低 | 中 | 高 |
| Playwright | 浏览器DOM | 高 | 中 | 中 |
| PyAutoGUI | 像素坐标 | 低 | 低 | 低 |

## 故障排除

### 权限问题
```bash
# macOS提示"辅助功能"权限
# 解决：系统偏好设置 → 安全性与隐私 → 辅助功能 → 添加应用

# 检查权限状态
agent-desktop permissions --check
```

### 找不到元素
```bash
# 使用find命令搜索
agent-desktop find --role button --app AppName

# 或使用更宽松的快照
agent-desktop snapshot --app AppName
```

### 坐标不准确
```bash
# 使用usecomputer的坐标映射
usecomputer screenshot --annotate

# 或使用agent-desktop的Accessibility定位
agent-desktop snapshot --app AppName -i
```

## 实战案例：微信自动化

### 案例：给联系人发送消息
```bash
# 1. 激活微信
osascript -e 'tell application "WeChat" to activate'
sleep 1.5

# 2. 搜索联系人并发送消息
osascript -e '
tell application "System Events"
    tell process "WeChat"
        set frontmost to true
        delay 0.5
        keystroke "f" using command down
        delay 1.0
        keystroke "老婆"
        delay 2.0
        key code 36
        delay 1.5
        keystroke "hi"
        delay 0.5
        key code 36
        delay 0.5
        key code 53
    end tell
end tell'
```

### Python调用示例
```python
from hermes_tools import terminal
import time

# 激活微信
terminal("osascript -e 'tell application \"WeChat\" to activate'")
time.sleep(1.5)

# 构建AppleScript
script = '''tell application "System Events"
    tell process "WeChat"
        set frontmost to true
        delay 0.5
        keystroke "f" using command down
        delay 1.0
        keystroke "联系人"
        delay 2.0
        key code 36
        delay 1.5
        keystroke "消息"
        delay 0.5
        key code 36
    end tell
end tell'''

terminal(f"osascript -e '{script}'")
```

### ⚠️ 微信自动化注意事项
- **搜索延迟**: 输入联系人后必须等待2秒让搜索结果加载
- **前置窗口**: 必须设置 `set frontmost to true`
- **字符串转义**: Python中使用单引号包裹，内部用双引号
- **terminal()返回值**: 是字典 `{output, exit_code}`，不是对象

---
*基于 agent-desktop 和 usecomputer 两个开源仓库*
*实战测试时间：2026-04-17*
