---
name: loopx-control-plane
description: "LoopX — 长时间Agent控制平面 (4K⭐)。字节工程师开源，200+小时稳定运行。目标持久化+门控审批+证据链+配额管理+跨Agent交接。适用于多天任务、渗透管线、安全研究。"
version: 1.0.0
author: huangruiteng + 小黑
license: MIT
metadata:
  hermes:
    tags: [loop-engineering, agent-control, long-running, goals, evidence, quota]
    related_skills: [kanban, pentest-pipeline, hermes-agent]
---

# LoopX — 长时间Agent控制平面

**GitHub:** https://github.com/huangruiteng/loopx | 4K⭐ | MIT | v0.4.4
**安装:** `pip install -e ~/security-research/re-tools/loopx/`
**命令:** `loopx --help`

## 核心定位

> "大多数Agent工具优化模型思考的10分钟。LoopX为真实项目需要的200小时而建。"

**不是新Agent运行时**，是Agent之上的**状态控制层**：
- 目标、门控、Todo、证据、配额存在 `.loopx/` 目录
- 跨session、跨工具、跨Agent持久化
- 人工审批点，不自动发布

## Tick循环（核心机制）

```bash
loopx quota should-run    # 该不该跑？
loopx todo claim          # 谁负责？
loopx todo update         # 改了什么？
loopx refresh-state       # 下一轮看什么？
loopx quota spend-slot    # 算力记账
```

## 日常命令

```bash
loopx status                          # 查看当前目标、门控、下一步
loopx start-goal --guided --project . --goal-text "目标描述"
loopx diagnose --goal-id ID           # 构建证据包
loopx evidence-log --goal-id ID --agent-id AGENT --thin
loopx todo --help                     # 添加/认领/完成/更新/归档
loopx task-lease --help               # 硬租约管理
loopx doctor                          # 检查安装状态
loopx ready-score --goal-id ID        # 评估就绪度
```

## 与Hermes集成

| Hermes现有 | LoopX补充 |
|-----------|----------|
| kanban任务板 | 更结构化的目标+门控+证据 |
| cron定时任务 | 配额感知调度，不空跑 |
| delegate_task子agent | 跨Agent所有权+交接协议 |
| memory持久记忆 | 证据链+决策溯源 |

### 使用场景

1. **渗透测试管线** — 多天多目标，每个阶段有门控
2. **安全研究** — 长时间漏洞分析，证据链完整
3. **逆向工程** — 大型二进制分析，分阶段推进
4. **代码审计** — 多模块审查，进度可追溯

### 典型工作流

```bash
# 1. 初始化目标
loopx start-goal --guided --project ~/my-project --goal-text "完成X模块渗透测试"

# 2. 每轮执行前检查
loopx quota should-run

# 3. 认领任务
loopx todo claim --todo-id T-001

# 4. 执行后更新
loopx todo update --todo-id T-001 --status done --evidence "发现SQL注入漏洞"

# 5. 刷新状态
loopx refresh-state

# 6. 消耗配额
loopx quota spend-slot
```

## 设计原则

- **本地优先** — 状态存在 `.loopx/`，不依赖云服务
- **Agent无关** — 支持Codex、Claude Code、Cursor、Hermes
- **人工在环** — 危险操作需人工审批
- **证据驱动** — 每步操作留痕可追溯
- **配额管理** — 防止无限烧算力

## 常见Pitfall

- **不是替代Hermes** — 是Hermes之上的补充层
- **不自动发布** — 生产写入/发布/凭证必须人工
- **v0.4.x早期** — 核心稳定，高级功能可能有变
- **状态文件不提交** — `.loopx/` 在.gitignore中
