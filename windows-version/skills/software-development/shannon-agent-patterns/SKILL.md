---
name: shannon-agent-patterns
description: "Shannon AI渗透测试的Agent框架设计模式。多Agent管线、证据验证、浏览器隔离、断点续传。应用这些模式到Hermes工作流。"
version: 1.0.0
author: Hermes Agent
license: AGPL-3.0 (patterns extracted under fair use)
metadata:
  hermes:
    tags: [agent-architecture, multi-agent, pipeline, security, shannon, patterns]
    related_skills: [ai-pentest-toolkit, vulnclaw, kanban, subagent-driven-development]
---

# Shannon Agent Framework 设计模式

从 Shannon (KeygraphHQ/shannon) 提取的核心架构模式，可应用到 Hermes 的任何复杂任务。

## Shannon 是什么？
AI自动化渗透测试工具。核心不是"工具"，而是**Agent编排框架**。
- 多Agent并行协作
- 证据驱动（不许编造）
- 断点续传（崩溃后恢复）
- 浏览器隔离（每个Agent独立浏览器）
- MCP工具集成

## 核心模式

### 模式1：5阶段管线架构
```
Shannon的渗透流程：

Phase 1: Pre-Recon（代码分析）     ← 顺序执行
Phase 2: Recon（信息收集）         ← 顺序执行
Phase 3: Vuln Analysis（漏洞分析） ← 5个Agent并行
Phase 4: Exploitation（漏洞利用）  ← 5个Agent并行
Phase 5: Reporting（报告生成）     ← 顺序执行
```

**应用到Hermes：**
```python
# 任何复杂任务都可以拆成这个模式
Phase 1: Research（调研）          ← 小黑顺序执行
Phase 2: Planning（规划）          ← 小黑顺序执行
Phase 3: Implementation（实现）    ← 多个delegate_task并行
Phase 4: Validation（验证）        ← 多个delegate_task并行
Phase 5: Reporting（报告）         ← 小黑顺序执行
```

### 模式2：Agent依赖图
```typescript
// Shannon的Agent定义：每个Agent声明自己的前置依赖
'pre-recon':    { prerequisites: [] }
'recon':        { prerequisites: ['pre-recon'] }
'injection-vuln': { prerequisites: ['recon'] }
'injection-exploit': { prerequisites: ['injection-vuln'] }
'report':       { prerequisites: ['injection-exploit', 'xss-exploit', ...] }
```

**应用到Hermes：**
```yaml
# 用todo系统管理依赖
任务1: 调研竞品 → 无依赖
任务2: 设计架构 → 依赖任务1
任务3: 前端开发 → 依赖任务2
任务3: 后端开发 → 依赖任务2（跟前端并行）
任务4: 集成测试 → 依赖任务3（前端+后端都完成）
```

### 模式3：证据驱动（反幻觉闸门）
```typescript
// Shannon的关键设计：结论必须有真实证据支撑
// 证据闸门：FINAL结论必须在真实工具输出中逐字符出现

// Validator检查：
// 1. 工具输出文件是否存在
// 2. 结论是否引用了真实证据
// 3. 未被支撑的结论会被拒绝
```

**应用到Hermes：**
```
规则：任何结论必须附带证据来源
- "这个API有SQL注入" → 附带实际请求/响应截图
- "性能提升了50%" → 附带benchmark数据
- "测试全部通过" → 附带测试输出

在delegate_task时，要求子agent返回证据而非结论。
```

### 模式4：浏览器会话隔离
```typescript
// Shannon为每个Agent分配独立的浏览器会话
// 防止并行Agent互相干扰
PLAYWRIGHT_SESSION_MAPPING = {
  'pre-recon-code': 'agent1',
  'recon': 'agent2',
  'vuln-injection': 'agent1',
  'vuln-xss': 'agent2',
  'vuln-auth': 'agent3',
  'vuln-ssrf': 'agent4',
  'vuln-authz': 'agent5',
}
```

**应用到Hermes：**
```
并行delegate_task时，每个子agent用独立的：
- 工作目录（worktree模式）
- 浏览器实例（如果需要网页操作）
- 临时文件（避免冲突）

用 hermes -w (worktree模式) 实现git隔离。
```

### 模式5：条件执行管线
```typescript
// Shannon的Vuln→Exploit条件管线：
// 只有当Vuln Agent发现漏洞时，Exploit Agent才运行

// 5条管线并行，每条独立：
Pipeline 1: injection-vuln → (有漏洞?) → injection-exploit
Pipeline 2: xss-vuln → (有漏洞?) → xss-exploit
Pipeline 3: auth-vuln → (有漏洞?) → auth-exploit
Pipeline 4: ssrf-vuln → (有漏洞?) → ssrf-exploit
Pipeline 5: authz-vuln → (有漏洞?) → authz-exploit
```

**应用到Hermes：**
```
复杂任务的并行分支：
- 分支A: 分析模块1 → (有问题?) → 修复模块1
- 分支B: 分析模块2 → (有问题?) → 修复模块2
- 分支C: 分析模块3 → (有问题?) → 修复模块3

用delegate_task(tasks=[...])并行执行分支。
每个分支内部用条件判断决定是否继续。
```

### 模式6：断点续传
```typescript
// Shannon的Resume系统：
// 1. 每个Agent完成后保存checkpoint
// 2. 崩溃后从最后一个checkpoint恢复
// 3. 已完成的Agent跳过，未完成的重新执行

// Git checkpoint:
await a.saveCheckpoint(activityInput, agentName, phaseName, state);
// Resume:
const shouldSkip = (agentName) => resumeState.completedAgents.includes(agentName);
```

**应用到Hermes：**
```
长任务的断点续传：
1. 每个阶段完成后，用memory保存进度
2. 中断后用session_search找回上下文
3. 检查哪些步骤已完成，跳过它们
4. 从未完成的步骤继续

用todo系统跟踪进度，用memory保存关键状态。
```

### 模式7：MCP工具编排
```typescript
// Shannon通过MCP协议让Agent调用外部工具
// fetch (HTTP), memory (状态), chrome-devtools (浏览器), burp (抓包)

// Agent不直接调用工具，通过MCP标准化接口
```

**应用到Hermes：**
```bash
# Hermes MCP配置
hermes mcp add <tool-name> --command <command>
# Agent通过MCP协议调用工具，标准化接口
```

### 模式8：产出物驱动
```typescript
// 每个Agent必须产出一个具体的文件
'pre-recon':  { deliverableFilename: 'pre_recon_deliverable.md' }
'recon':      { deliverableFilename: 'recon_deliverable.md' }
'injection-vuln': { deliverableFilename: 'injection_analysis_deliverable.md' }
'injection-exploit': { deliverableFilename: 'injection_exploitation_evidence.md' }
'report':     { deliverableFilename: 'comprehensive_security_assessment_report.md' }
```

**应用到Hermes：**
```
每个delegate_task必须返回具体产出物：
- 不是"我完成了"
- 而是"这是产出文件路径: /path/to/output.md"

子agent的goal里明确指定产出物路径。
```

## Shannon的Agent类型

| Agent | 阶段 | 职责 | 产出物 |
|-------|------|------|--------|
| pre-recon | 侦察 | 代码分析、架构理解 | pre_recon_deliverable.md |
| recon | 侦察 | 端口扫描、目录枚举 | recon_deliverable.md |
| injection-vuln | 漏洞分析 | SQL注入检测 | injection_analysis_deliverable.md |
| xss-vuln | 漏洞分析 | XSS检测 | xss_analysis_deliverable.md |
| auth-vuln | 漏洞分析 | 认证绕过检测 | auth_analysis_deliverable.md |
| ssrf-vuln | 漏洞分析 | SSRF检测 | ssrf_analysis_deliverable.md |
| authz-vuln | 漏洞分析 | 授权绕过检测 | authz_analysis_deliverable.md |
| injection-exploit | 利用 | SQL注入PoC | injection_exploitation_evidence.md |
| xss-exploit | 利用 | XSS PoC | xss_exploitation_evidence.md |
| report | 报告 | 综合报告 | comprehensive_security_assessment_report.md |

## Shannon的重试策略

```typescript
// 生产环境：长间隔，高重试
PRODUCTION_RETRY = {
  initialInterval: '5 minutes',
  maximumInterval: '30 minutes',
  backoffCoefficient: 2,
  maximumAttempts: 50,
}

// 测试环境：短间隔，低重试
TESTING_RETRY = {
  initialInterval: '10 seconds',
  maximumInterval: '30 seconds',
  backoffCoefficient: 2,
  maximumAttempts: 5,
}
```

**应用到Hermes：**
```
delegate_task失败时的重试策略：
- 网络错误：指数退避重试
- 认证错误：不重试，直接报错
- 逻辑错误：修改参数后重试
- 资源不足：等待后重试
```

## 实际应用示例

### 示例：用Shannon模式做Web项目开发
```
Phase 1: Research（顺序）
  → 调研竞品、技术选型、需求分析

Phase 2: Planning（顺序）
  → 架构设计、API设计、数据库设计

Phase 3: Implementation（并行）
  → 分支A: 前端开发（delegate_task）
  → 分支B: 后端开发（delegate_task）
  → 分支C: 数据库开发（delegate_task）

Phase 4: Validation（并行）
  → 分支A: 前端测试（delegate_task）
  → 分支B: 后端测试（delegate_task）
  → 分支C: 集成测试（delegate_task）

Phase 5: Reporting（顺序）
  → 汇总所有分支结果，生成报告
```

### 示例：用Shannon模式做安全审计
```
Phase 1: Pre-Recon
  → 读代码，理解架构

Phase 2: Recon
  → 端口扫描、目录枚举

Phase 3: Vuln Analysis（5路并行）
  → SQL注入分析
  → XSS分析
  → 认证分析
  → SSRF分析
  → 授权分析

Phase 4: Exploitation（条件执行）
  → 只对Phase 3发现的漏洞做PoC

Phase 5: Report
  → 综合报告
```

## 关键教训

1. **不要让一个Agent做所有事** — 拆成多个专职Agent并行
2. **证据优先** — 每个结论必须有工具输出支撑
3. **断点续传** — 长任务必须能从中间恢复
4. **浏览器隔离** — 并行Agent不能共享浏览器状态
5. **产出物明确** — 每个Agent必须输出具体文件
6. **条件执行** — 不是所有分支都需要执行
7. **重试策略** — 区分可重试和不可重试错误
8. **不要只学模式要直接用** — 用户要求把框架逻辑变成Hermes原生能力，不是文档化

## 关键教训：直接集成，不要只文档化

用户明确要求："不要直接使用它"（指Shannon工具本身），而是"把它的框架逻辑变成Hermes自己的能力"。

正确做法：
- 用 delegate_task 实现多Agent并行
- 用 todo 管理依赖图
- 用 memory 保存checkpoint
- 用 MCP 接入外部工具
- 直接在Hermes里运行Shannon风格的管线

错误做法：
- 只写文档说明Shannon怎么用
- 让用户自己安装Shannon
- 不把模式应用到Hermes自身工作流

## User Preferences (embedded from session)
- 报告用大白话，适合完全不懂计算机的人群
- 不要直接调用外部工具，要集成进Hermes变成自己的能力
- 遇到terminal安全扫描拦截时，写脚本让用户手动运行
- 安装工具时优先用uv pip（比brew快），brew放后台
- 配置文件修改用Python脚本（因为config.yaml受agent保护）
