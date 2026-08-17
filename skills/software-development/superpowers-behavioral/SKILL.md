---
name: superpowers-behavioral
description: "Superpowers行为模式补丁 (236K⭐) — 6个Hermes缺失的铁律模式：反合理化表、铁律门控、红线停止器、修复循环上限、账本追踪、模型选择指导。"
version: 1.0.0
author: obra + 小黑
license: MIT
metadata:
  hermes:
    tags: [superpowers, behavioral, anti-rationalization, verification, debugging]
    related_skills: [superpowers, tdd-bdd, doubt-driven-development, anti-sycophancy]
---

# Superpowers行为模式补丁

**来源:** https://github.com/obra/superpowers (236K⭐)
**目的:** 把superpowers的6个独特行为模式注入Hermes

## 模式1: 铁律门控 (Iron Law Gate)

**调试铁律：**
```
没有根因调查，禁止提出修复方案
```
Phase 1(根因调查) → Phase 2(模式分析) → Phase 3(假设验证) → Phase 4(实现)

**验证铁律：**
```
没有新鲜验证证据，禁止声称完成
```
在说"完成"/"通过"/"修好了"之前，必须先运行验证命令并读取输出。

## 模式2: 反合理化表 (Anti-Rationalization)

每次想走捷径时，对照检查：

| 借口 | 现实 |
|------|------|
| "应该能用" | 去跑验证 |
| "我很自信" | 自信≠证据 |
| "就这一次" | 没有例外 |
| "检查器过了" | 检查器≠编译器 |
| "Agent说成功了" | 独立验证 |
| "我累了" | 疲惫≠借口 |
| "简单问题不需要流程" | 简单问题也有根因 |
| "紧急，没时间走流程" | 系统化调试比乱试更快 |
| "先试这个，再调查" | 第一次修复决定模式 |
| "差不多符合规格" | 差距=没完成 |
| "我自己修，调度是开销" | 控制器修复污染上下文并跳过审查 |
| "再来一轮就会收敛" | 超过上限后轮次不会收敛 |
| "审查员总会找到新问题" | 范围审查只验证修复 |
| "这个发现明显错了，跳过" | 只在上限时裁决，每个裁决必须记录 |

## 模式3: 红线停止器 (Red Flags)

发现以下想法时，**立即停止，回到Phase 1**：
- "先快速修一下，以后再调查"
- "试试改X看看行不行"
- "加多个改动，跑测试"
- "跳过测试，我手动验证"
- "可能是X，修修看"
- "我不完全理解但这可能行"
- "模式说X但我换个方式"
- "主要问题是：[列修复方案但没调查]"
- 在追踪数据流之前提出解决方案
- "再来一次修复尝试"（已经试了2+次）
- 每次修复暴露不同位置的新问题

## 模式4: 修复循环上限 (Fix Loop Cap)

```
修复轮次上限 = 5次

Round 1-3: 恢复原始实现者（上下文完整）
Round 4-5: 新实现者+更强模型（新视角+能力提升）

5轮后仍有问题 → 裁决：
  - 审查员错了 → 记录搁置
  - 真实但不影响下游 → 记录搁置
  - 真实且影响下游 → BLOCKED，报告给人类
```

**禁止：**
- 超过5轮继续尝试
- 跳过审查直接修
- 自己修（控制器修复跳过审查）
- 静默丢弃发现

## 模式5: 账本追踪 (Ledger Tracking)

上下文压缩会丢失记忆。用账本文件持久化：

```markdown
# SDD ledger — plan: <plan文件路径>

Task 1: complete (commits a1b2c3d..d4e5f6a, review clean)
Task 2: fix round 1/5 (2 addressed, 0 open; commits d4e5f6a..b7c8d9e)
Task 2: complete (commits d4e5f6a..b7c8d9e, review clean)
Task 3: minor (deferred): 魔法数字100
Task 4: parked — 未处理异常 — 裁决: 下游不依赖，延迟处理
Task 5: BLOCKED — 数据库schema冲突
```

**规则：**
- 账本是恢复地图，不是装饰
- 压缩后信任账本和git log，不信任记忆
- 每个裁决必须是账本条目
- 禁止静默丢弃

## 模式6: 模型选择指导 (Model Selection)

| 任务类型 | 模型级别 | 原因 |
|---------|---------|------|
| 机械实现（1-2文件，明确规格） | 最便宜 | 转录+测试 |
| 集成任务（多文件协调） | 中等 | 需要判断力 |
| 架构设计 | 最强 | 需要全局视野 |
| 最终全分支审查 | 最强 | 质量门控 |
| 修复循环Round 4-5 | 比实现者高一级 | 新视角+能力提升 |
| 范围审查小diff | 便宜到中等 | 不需要最强模型 |

**关键：调度子agent时必须明确指定模型。省略=继承当前session的模型（通常最贵）。**

## 在Hermes中的应用

当小黑执行以下任务时，自动激活这些模式：

1. **调试** → 激活铁律门控+反合理化+红线停止器
2. **开发** → 激活验证铁律+修复循环上限
3. **子agent调度** → 激活模型选择指导+账本追踪
4. **代码审查** → 激活反合理化表

## 与现有skill的关系

| 已有skill | 本skill补充 |
|-----------|-----------|
| superpowers | 完整方法论，本skill提取行为模式 |
| tdd-bdd | TDD流程，本skill加反合理化 |
| doubt-driven-development | 质疑决策，本skill加铁律门控 |
| anti-sycophancy | 不顺从，本skill加红线停止器 |
| developer-debugging | 调试方法，本skill加4阶段铁律 |
| code-quality-workflow | 质量门控，本skill加验证铁律 |
