---
name: vulnclaw
description: "VulnClaw: AI驱动渗透测试工具，集成Chrome DevTools MCP + Burp MCP + 50个专项Skill。中文项目，开箱即用。"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [pentest, ai-pentest, MCP, chrome-mcp, burp-mcp, vulnclaw, chinese-tool, security]
    related_skills: [ai-pentest-toolkit, godmode, browser-use-automation]
---

# VulnClaw — AI驱动渗透测试

来源：教红队的Des 推荐
GitHub：https://github.com/Unclecheng-li/VulnClaw（2674⭐）
安装：`pip install vulnclaw`

## 一句话介绍
自然语言输入 → 自动完成「信息收集 → 漏洞发现 → 漏洞利用 → 报告生成」全流程。

## 核心能力

### 4个MCP服务
| MCP服务 | 模式 | 用途 |
|---------|------|------|
| **fetch** | 本地(httpx) | HTTP/HTTPS请求 |
| **memory** | 本地(JSON) | 上下文记忆、状态持久化 |
| **chrome-devtools** | stdio MCP | **浏览器自动化（替代computer_use）** |
| **burp** | stdio MCP | HTTP抓包与重放 |

### 50个专项Skill
- 核心技能(7)：pentest-flow, recon, vuln-discovery, exploitation, waf-bypass等
- 专项技能(16+)：web-pentest, ctf-web, intranet-pentest-advanced, crypto-toolkit等
- 29种编解码/加解密：Base64, AES, JWT等

### 14个LLM Provider
OpenAI, Anthropic, MiniMax, DeepSeek, 智谱, Kimi, 通义千问, SiliconFlow, 豆包, 百川, 阶跃星辰, 商汤, 零一万物, Ollama

## 安装

```bash
# PyPI安装（推荐）
pip install vulnclaw

# Docker运行
cp .env.example .env  # 填入 VULNCLAW_LLM_API_KEY
docker compose up --build
# 打开 http://127.0.0.1:7788
```

## 四步启动

```bash
# 1. 选择提供商
vulnclaw config provider minimax  # 或 openai/anthropic/deepseek

# 2. 设置API Key
vulnclaw config set llm.api_key sk-your-key

# 3. 启动CLI
vulnclaw

# 4. 可选：TUI工作台
vulnclaw tui
```

## CLI命令速查

```bash
vulnclaw run <target>           # 一键全流程渗透
vulnclaw solve <target>         # 目标驱动求解（模型主导）
vulnclaw persistent <target>    # 持续性渗透（100轮/周期）
vulnclaw recon <target>         # 仅信息收集
vulnclaw scan <target>          # 仅漏洞扫描
vulnclaw exploit <target>       # 仅漏洞利用
vulnclaw report <session>       # 生成报告
vulnclaw repl                   # REPL交互
vulnclaw tui                    # TUI工作台
vulnclaw web                    # Web UI (127.0.0.1:7788)
vulnclaw doctor                 # 环境检查
```

## Chrome DevTools MCP 配置

VulnClaw内置chrome-devtools MCP服务，用于浏览器自动化渗透测试：
- 自动打开目标网页
- 自动点击、填表、截屏
- 自动读取控制台错误
- 自动执行XSS/CSRF等浏览器端攻击

### 跟Hermes集成
```bash
# 添加VulnClaw的chrome-devtools MCP到Hermes
hermes mcp add vulnclaw-chrome --command "npx chrome-devtools-mcp@latest"

# 或直接用VulnClaw的CLI
vulnclaw run http://target.com
```

## 替代Hermes内置computer_use
VulnClaw的chrome-devtools MCP比Hermes内置的computer_use更适合安全测试：
- 支持Chrome DevTools Protocol（更底层）
- 支持Burp Suite集成（HTTP抓包）
- 支持MCP协议（标准化）
- 支持14个LLM Provider

### Hermes MCP配置（已生效）
```yaml
# ~/.hermes/config.yaml
mcp:
  servers:
    chrome-devtools:
      command: npx
      args: ["-y", "chrome-devtools-mcp@latest", "--autoConnect"]
    vulnclaw-chrome:
      command: vulnclaw
      args: ["mcp", "chrome"]
    vulnclaw-burp:
      command: vulnclaw
      args: ["mcp", "burp"]
```

### Chrome MCP使用前准备
1. Chrome打开 `chrome://inspect/`
2. 启用远程调试
3. MCP服务器自动连接

## 实际使用示例

### 示例1：一键渗透测试
```bash
vulnclaw run http://192.168.1.100
# 自动执行：信息收集→漏洞发现→漏洞利用→报告生成
```

### 示例2：仅信息收集
```bash
vulnclaw recon http://target.com
# 端口扫描、指纹识别、目录枚举
```

### 示例3：持续性深度测试
```bash
vulnclaw persistent http://target.com
# 100轮/周期，长时间深度测试
```

### 示例4：TUI工作台（图形化）
```bash
vulnclaw tui
# 终端图形界面，可先确认测试范围
```

### 示例5：Web UI
```bash
vulnclaw web
# 打开 http://127.0.0.1:7788
```

### 示例6：自然语言交互
```bash
vulnclaw
# 进入REPL，直接用中文描述意图
# 例如："帮我对 http://target.com 进行渗透测试"
```

## VulnClaw vs Shannon 对比
| 维度 | VulnClaw | Shannon |
|------|----------|---------|
| 语言 | Python | TypeScript |
| 安装 | pip install（简单） | Docker + Node.js（复杂） |
| LLM支持 | 14个Provider | 仅Anthropic Claude |
| MCP服务 | 4个（fetch/memory/chrome/burp） | 无（用Playwright） |
| Skill数量 | 50个 | 内置Agent |
| 中文支持 | ✅ 原生中文 | ❌ 英文 |
| 适合场景 | 快速测试、中文环境 | 深度白盒审计 |
| 推荐度 | ⭐⭐⭐⭐⭐ 首选 | ⭐⭐⭐⭐ 深度用 |

## 注意事项
- 仅用于已授权的安全测试
- 公开Alpha阶段，可能有bug
- 需要Python 3.10+
- 社区QQ群：954402631
- 安装用uv pip：`uv pip install vulnclaw`（比brew快）

## 跟其他skill的关系
- ai-pentest-toolkit: 综合工具集，包含VulnClaw作为首选工具
- pentest-pipeline: Hermes原生渗透管线，可调用VulnClaw作为工具
- shannon-agent-patterns: Shannon架构模式，VulnClaw是类似工具
