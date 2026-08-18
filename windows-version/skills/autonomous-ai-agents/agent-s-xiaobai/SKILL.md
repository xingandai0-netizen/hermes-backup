---
name: agent-s-xiaobai
description: "小白(Xiao Bai) - 基于Simular Agent-S的GUI桌面自动化子agent。与小黑组成'黑白双煞'团队，强制共同完成所有任务。"
version: 1.0.0
tags: [agent-s, gui-automation, desktop, computer-use, xiaobai, team]
created: 2026-05-13
---

# 小白 (Xiao Bai) — Agent-S GUI Automation Agent

## 概述
小白是基于Simular Agent-S (gui-agents v0.3.2) 的GUI桌面自动化agent。
仓库: https://github.com/simular-ai/agent-s
本地路径: ~/github-skills/agent-s

## Agent-S 核心架构
- **S1**: ICLR 2025, Manager-Worker层级架构, ProceduralMemory
- **S2**: COLM 2025, 知识增强, 搜索集成(Perplexica)
- **S3**: 最新, 超越人类OSWorld性能(72.60%), 无层级扁平架构, BBON行为评判
- **CLI入口**: `agent_s` → `gui_agents.s3.cli_app:main`
- **LLM引擎**: 支持OpenAI/Anthropic/Google/Azure, 通过base_url可接入antokex中转站

## 踩坑记录

### Pitfall 1: osascript开新终端丢失环境变量
通过`osascript -e 'tell application "Terminal" to do script "..."'`开新终端时，当前shell的环境变量**不会继承**到新窗口。
- 错误表现: `OPENAI_API_KEY not provided` 错误反复出现
- 解决: API key必须写死在启动脚本文件里，不能依赖环境变量传递
- 启动脚本里必须包含: `export XIAOBAI_API_KEY="..."` 和 `export OPENAI_API_KEY="$XIAOBAI_API_KEY"`

### Pitfall 2: Python版本兼容性
Agent-S setup.py限制`python_requires=">=3.9, <=3.12"`，macOS默认Python 3.14会拒绝安装。
- 解决: 创建专用venv用Python 3.12 (`/usr/local/bin/python3.12`)
- `<=3.12` 实际意思是 `<=3.12.0`，所以3.12.9也会被拒 → 需要修改setup.py去掉上限
- venv路径: ~/agent-s-venv

### Pitfall 3: 小白是交互式CLI，无法通过Hermes的terminal工具直接运行
小白需要交互式终端(PTY)等待用户输入`Query:`。Hermes的terminal/execute_code没有stdin。
- 解决: 通过osascript开新Terminal窗口执行启动脚本
- 无法从Hermes内部直接与小白交互，只能帮用户开窗口

### Pitfall 4: Agent-S需要两个模型
Agent-S3 CLI需要两组模型配置:
- `--model` + `--model_url` + `--model_api_key`: 推理/对话模型(主引擎)
- `--ground_model` + `--ground_url` + `--ground_api_key`: 视觉定位模型(屏幕理解)
两者可以用同一个模型(如mimo-v2-omni)，但API key需要分别传入。

## 部署踩坑记录 (MUST READ)

### 踩坑1: Agent-S不是对话式agent
Agent-S是GUI自动化工具，`Query:`接受的是操作指令(如"打开Safari")，不是聊天。
**解法**: 写wrapper(xiaobai.py)包装Agent-S，用MiMo-V2-Omni直接做对话，
只有检测到GUI关键词时才调用Agent-S的截图+执行流程。

### 踋坑2: 从Hermes terminal启动交互式程序无stdin
Hermes的terminal环境是非交互式的(无PTY/EOFError)。
**解法**: 用`osascript`开新Terminal窗口执行脚本:
```python
osascript -e 'tell application "Terminal" to activate; do script "~/agent-s-xiaobai.sh"'
```

### 踋坑3: osascript新窗口丢失环境变量
**解法**: key直接写在启动脚本里，不依赖环境变量传递。

### 踋坑4: Python版本限制
Agent-S setup.py限制`<=3.12`，但系统Python是3.14。
**解法**: 1) 用系统自带的python3.12 2) 创建venv 3) 修改setup.py去掉版本上限
```bash
/usr/local/bin/python3.12 -m venv ~/agent-s-venv
```

## 部署架构
```
~/agent-s-xiaobai.sh        # 启动脚本(入口，含API key)
~/xiaobai/xiaobai.py        # Wrapper: 对话+GUI双模式
~/agent-s-venv/             # Python 3.12 venv
~/github-skills/agent-s/    # Agent-S源码(git clone)
~/xiaobai/memory/           # 共享记忆目录
~/xiaobai/skills/           # 从Hermes同步的skills
```

## Scripts & Templates
- `scripts/xiaobai.py` — 对话wrapper(参考实现)
- `templates/xiaobai-launch.sh` — 启动脚本模板(含环境变量)

## 黑白双煞协作流程
当阿戴提到"黑白双煞"时：
1. 小黑(主agent)负责：诊断/编码/部署/DB操作
2. 小白负责：GUI验证(截图+操作)、浏览器自动化任务
3. 协作点：小黑修完代码 → 小白操作验证 → 小黑根据反馈修正

### HTML下载文件验收流程（2026-05-14验证）
验收可下载HTML文件的标准流程：
1. **文件大小验证** — 下载文件大小应与服务器文件一致（误差<1%）
2. **自包含验证** — `grep -c 'src="' file.html`应为0（无外部JS引用）
3. **本地HTTP服务器** — `python3 -m http.server PORT --directory /tmp`启动测试
4. **浏览器打开** — 用Playwright或Safari打开localhost:PORT/file.html
5. **内容验证** — 检查标题、功能卡片、设置面板等关键元素
6. **截图保存** — 保存验证截图到/tmp/

### 常见验收失败原因
- **SPA入口文件** — 下载的是React SPA入口（2-3KB），不是自包含HTML（30KB+）
- **Nginx catch-all拦截** — /downloads/路径被SPA路由拦截，返回主站index.html
- **外部依赖** — HTML引用了外部JS/CSS，本地打开时404导致白屏
- **设置面板缺失** — JS引用了getElementById但HTML中没有对应元素

### 网页应用验收流程（2026-05-14验证）
验收部署在服务器上的网页应用（如antokex.com/studio/）：
1. **外部域名访问** — `curl -sk https://antokex.com/path`（不能只测localhost，CF路由可能不同）
2. **HTTP状态码** — 200 OK
3. **页面标题** — grep `<title>`确认正确（非SPA默认标题）
4. **关键元素** — grep验证功能卡片/按钮/输入框等关键DOM元素存在
5. **Nginx路由验证** — response headers不含`x-new-api-version`（否则走了catch-all）
6. **双路径测试** — 带尾斜斜(/studio/)和不带(/studio)都要测试
7. **截图保存** — Playwright截图保存到/tmp/

### 常见验收失败原因（网页应用）
- **Cloudflare HTTP路由** — CF Flexible SSL走HTTP(8088)，HTTP block缺location(pitfall#109)
- **SPA catch-all拦截** — specific location在catch-all之后定义(pitfall#106)
- **设置面板HTML缺失** — JS引用getElementById但HTML中无对应元素(pitfall#108)
- **功能卡片残留** — 用户要求删除但替换不完整

### 验收报告格式
```
== 验收报告 ==
HTTP状态码: XXX
页面大小: XXX字节
页面标题: "XXX"
关键元素: ✅/❌ (功能卡片X个, 按钮X个, 输入框X个)
设置面板: ✅/❌
Nginx路由: ✅/❌ (是否走了catch-all)
双路径测试: /path ✅/❌, /path/ ✅/❌
截图: /tmp/xxx.png
结论: ✅通过 / ❌失败
```
## 部署状态 (2026-05-13 已完成)
- venv: ~/agent-s-venv (Python 3.12.9)
- 启动脚本: ~/agent-s-xiaobai.sh (一键启动)
- 主程序: ~/xiaobai/xiaobai.py (对话+GUI双模式)
- 视觉引擎: mimo-v2-omni via antokex.com/v1
- API Key: sk-HwIi53zWV9doQayy8FwUhHYJiCrguvA16eOHHt4K8anDdrjY
- 屏幕分辨率: 2560x1600 (Retina)
## 部署状态 (2026-05-13 已验证)
- venv: ~/agent-s-venv (Python 3.12.9)
- 启动脚本: ~/agent-s-xiaobai.sh (一键启动，内含API key)
- 主程序: ~/xiaobai/xiaobai.py (对话+GUI双模式wrapper)
- 视觉引擎: mimo-v2-omni via antokex.com/v1
- 屏幕分辨率: 2560x1600 (Retina)
- 共享记忆: ~/xiaobai/memory/shared-memory.md (小黑小白共用)
- Skills目录: ~/xiaobai/skills/ (启动时自动加载)

## 关键认知 (MUST READ)
**Agent-S不是对话agent，是GUI自动化工具。** 它的`Query:`输入是GUI操作指令（如"打开Safari"），不是聊天。直接部署给用户=无法对话。
**正确方案**: 写wrapper(xiaobai.py)实现双模式：
1. 普通问题→MiMo直接chat回复
2. GUI操作→截图+MiMo视觉分析→pyautogui执行
启动脚本把API key硬编码在脚本文件内(osascript新开Terminal环境变量丢失)。

## 共享记忆协议
- 小黑改记忆时需同步更新shared-memory.md
- 小白启动时自动加载shared-memory.md + ~/xiaobai/skills/*.md
- 记忆文件路径: ~/xiaobai/memory/shared-memory.md
