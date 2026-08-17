---
name: computer-use-learnings
description: Computer Use技术深度学习成果。包含OpenAI Codex Computer Use、Agent-S、Microsoft Fara-7B、autoMate等核心框架的架构、实现原理和使用方法。需要时用于构建桌面自动化agent或研究CU技术。
---

# Computer Use 技术深度学习

## 技术概览

Computer Use (CU) 让AI能够像人类一样操作电脑：截图、鼠标点击、键盘输入。

### 主要玩家
| 厂商/项目 | 产品 | 发布时间 | 特点 |
|-----------|------|----------|------|
| Anthropic | Claude Computer Use | 2024.10 | 最早发布，API原生支持 |
| OpenAI | Codex Computer Use | 2026.04 | 集成在Codex CLI中 |
| Microsoft | Fara-7B | 2025.11 | 7B小模型，成本低10倍 |
| 开源 | Agent-S (10.8k⭐) | 2024.10 | OSWorld第一(72.6%)，超人类 |
| 开源 | autoMate (3.8k⭐) | 2025.12 | MCP集成，跨平台 |

---

## Agent-S 深度解析 (OSWorld第一)

### 仓库位置
`~/computer-use-agent-s/`

### 架构 (S3版本)
```
┌─────────────────────────────────────────────────────────┐
│                      Agent S3                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   Worker    │───▶│   ACI       │───▶│  执行动作   │ │
│  │  (执行者)   │    │  ( grounding)│    │ (pyautogui) │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│         │                                       ▲      │
│         ▼                                       │      │
│  ┌─────────────┐    ┌─────────────┐              │      │
│  │  Reflection │    │ Procedural  │──────────────┘      │
│  │  (反思agent)│    │  Memory     │                     │
│  └─────────────┘    └─────────────┘                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 核心组件

#### 1. Worker (gui_agents/s3/agents/worker.py)
- 接收任务指令和截图
- 生成下一个动作
- 支持反思机制(Reflection)
- 自动管理上下文长度

#### 2. ACI - Agent-Computer Interface (gui_agents/s3/agents/grounding.py)
- 将自然语言动作转换为具体坐标
- 支持多种动作类型：click, type, key, scroll, drag
- 集成 accessibility tree 解析

#### 3. LMM Engine (gui_agents/s3/core/mllm.py)
- 支持 OpenAI, Anthropic, Gemini
- 支持 Claude thinking mode
- 自动重试和错误处理

#### 4. Procedural Memory (gui_agents/s3/memory/procedural_memory.py)
- 预定义的操作模板
- 平台特定指令 (macOS/Linux/Windows)

### 关键代码示例

```python
from gui_agents.s3.agents.agent_s import AgentS3
from gui_agents.s3.agents.grounding import ACI
from gui_agents.s3.core.mllm import LMMEngineOpenAI

# 初始化
engine_params = {
    "engine_type": "openai",
    "model": "gpt-4o",
    "api_key": "your-key"
}

agent = AgentS3(
    worker_engine_params=engine_params,
    grounding_agent=ACI(platform="darwin"),
    platform="darwin"
)

# 运行
instruction = "打开浏览器搜索Python"
observation = {"screenshot": screenshot_image}
info, actions = agent.predict(instruction, observation)
```

---

## Microsoft Fara-7B 深度解析

### 仓库位置
`~/computer-use-fara/`

### 核心特点
- **7B参数** - 可本地部署，隐私友好
- **视觉驱动** - 直接从截图预测坐标，无需accessibility tree
- **高效** - 平均16步完成任务(同类模型约41步)
- **训练数据** - 145K trajectories

### 安装使用
```bash
# 1. 克隆仓库
git clone https://github.com/microsoft/fara.git
cd fara && pip install -e .

# 2. 启动模型 (需要vLLM)
vllm serve "microsoft/Fara-7B" --port 5000

# 3. 使用CLI测试
fara-cli --task "搜索纽约天气"
```

### 性能对比
| 模型 | 参数量 | OSWorld准确率 | 每任务步数 |
|------|--------|--------------|-----------|
| Fara-7B | 7B | ~45% | 16 |
| GPT-4o | - | ~60% | 35 |
| Claude Sonnet | - | ~65% | 41 |

---

## autoMate 深度解析

### 仓库位置
`~/computer-use-automate/`

### 核心特点
- **MCP Server** - 直接集成Claude/Cursor/OpenClaw
- **跨平台** - Windows/macOS/Linux
- **零配置** - 无需API key
- **脚本库** - 可保存复用工作流

### MCP Tools
| 工具 | 功能 |
|------|------|
| `screenshot` | 截取屏幕 |
| `click` | 点击坐标 |
| `type` | 输入文字 |
| `key` | 按键 |
| `scroll` | 滚动 |
| `run_script` | 运行保存的脚本 |
| `save_script` | 保存工作流为脚本 |

### 安装配置 (Claude Desktop)
```json
{
  "mcpServers": {
    "automate": {
      "command": "uvx",
      "args": ["automate-mcp@latest"]
    }
  }
}
```

---

## 实战应用

### 1. 自动化微信操作
```python
# 使用Agent-S
agent = AgentS3(...)
instruction = "打开微信，发送消息给阿戴说'你好'"
```

### 2. 批量处理表格
```python
# 使用Fara-7B (本地部署，隐私友好)
fara-cli --task "打开Excel，填充A1到D10的数据"
```

### 3. Claude Desktop集成
```json
// 使用autoMate MCP
// Claude会自动使用screenshot/click等工具
```

---

## 实战经验 (2026-04-29 新增)

### 问题：Agent截图抓到终端窗口而非桌面
**原因**: agent在终端运行时截图，抓到的是终端窗口本身
**解决方案**:
- 运行agent前先隐藏终端（Cmd+H）或将终端移到后台
- 或者在agent开头加一步：先Cmd+H隐藏所有窗口，再截图
- 截图前调用 `osascript -e 'tell application "System Events" to key code 50 using {command down, option down}'` 隐藏所有窗口

### 关键教训
- pyautogui.screenshot()抓的是**当前屏幕**，如果终端在前台就抓到终端
- 需要在截图前确保目标应用在前台
- Agent-S等框架处理这个问题的方式：先将agent进程放后台，用独立截图进程

---

## 技术选型建议

| 场景 | 推荐方案 |
|------|----------|
| 需要最高准确率 | Agent-S + GPT-4o/Claude |
| 需要本地部署/隐私 | Fara-7B + vLLM |
| 快速集成Claude | autoMate MCP |
| 研究/学术 | Agent-S (论文完整) |
| 企业生产 | Claude API原生CU |

---

*学习时间: 2026年4月17日*
*仓库已克隆到本地*