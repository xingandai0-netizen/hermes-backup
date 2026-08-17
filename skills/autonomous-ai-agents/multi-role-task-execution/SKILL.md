---
name: multi-role-task-execution
description: |
  强制多角色工作流执行协议。当任务涉及代码开发、功能实现、UI修改等工程类任务时，
  必须使用kanban-orchestrator拆解任务，分配给不同角色(产品经理、代码工程师、测试工程师等)的子agent并行执行。
  禁止单agent从头做到尾——这是强制规则。
tags: [workflow, kanban, multi-agent, team, orchestration]
version: 1.0
created: 2026-05-13
updated: "2026-05-13"
---

# 多角色任务执行协议（强制）

## 触发条件
**当任务涉及以下任何一种情况时，强制执行本协议：**
- 代码修改/开发（前端、后端、全栈）
- UI/UX设计和实现
- 网站功能修改
- 系统架构变更
- 功能测试和验证
- 任何需要 3+ 步骤的工程类任务

**不触发的情况：**
- 纯信息查询/研究
- 简单的配置文件单行修改
- 紧急hotfix（一行代码修复）

## 角色定义

### 1. 产品经理 (Product Manager)
**职责**：需求分析、方案设计、优先级排序
**输出**：需求文档、验收标准、用户故事
**工具集**：file, web, search, vision

### 2. 代码工程师 (Code Engineer)
**职责**：具体代码实现、API对接、功能开发
**输出**：代码文件、部署结果、技术文档
**工具集**：terminal, file, web, browser

### 3. 测试工程师 (QA Engineer)
**职责**：功能验证、回归测试、Playwright自动化测试
**输出**：测试报告、截图证据、bug列表
**工具集**：terminal, browser, vision, file

### 4. 架构师 (Architect)（按需）
**职责**：技术方案设计、Nginx配置、系统架构
**输出**：架构文档、配置文件、迁移方案
**工具集**：terminal, file, web

## 执行流程

### Phase 1: 任务拆解（主agent完成）
1. 收到任务后，先用skills_list扫描相关skill
2. 用skill_view加载所有相关skill
3. 分析任务，拆解为子任务
4. 确定需要哪些角色

### Phase 2: 并行执行（delegate_task）
使用delegate_task的batch模式，将子任务分配给不同角色：

```
delegate_task(tasks=[
  {
    "goal": "产品经理任务：需求分析+方案设计",
    "context": "...",
    "toolsets": ["file", "web", "vision"],
    "role": "leaf"
  },
  {
    "goal": "代码工程师任务：具体实现",
    "context": "...",
    "toolsets": ["terminal", "file"],
    "role": "leaf"
  },
  {
    "goal": "测试工程师任务：验证测试",
    "context": "...",
    "toolsets": ["terminal", "browser", "vision"],
    "role": "leaf"
  }
])
```

### Phase 3: 整合验证
1. 收集所有子agent的输出
2. 主agent进行整合和最终验证
3. 更新skill记录

## 拆解模板

### 典型Web功能修改任务
| 角色 | 子任务 | 输出 |
|------|--------|------|
| 产品经理 | 分析现有UI + 设计新方案 | 方案文档 + 验收标准 |
| 代码工程师 | 实现代码修改 | 代码diff + 部署结果 |
| 测试工程师 | Playwright验证 | 测试截图 + 状态报告 |

### 典型API对接任务
| 角色 | 子任务 | 输出 |
|------|--------|------|
| 架构师 | 分析API文档 + 设计对接方案 | API接口文档 + 数据流图 |
| 代码工程师 | 实现API调用 + 错误处理 | 代码 + 部署 |
| 测试工程师 | API测试 + 端到端验证 | 测试结果 |

## 注意事项

1. **context必须完整**：每个子agent没有上下文记忆，必须在context中提供所有必要信息
2. **最多3个并行任务**：delegate_task的batch模式限制3个
3. **角色不要重叠**：每个子任务职责明确，避免重复工作
4. **先做再验证**：代码工程师先实现，测试工程师再验证
5. **skill优先**：每个子agent的context中应包含相关skill的名称，让它自己去skill_view加载
6. **从现有任务续接**：如果任务已在进行中，把当前状态、已完成步骤、已知问题都写入context

## 禁止事项
- **禁止单agent连续执行代码+测试** — 必须分角色
- **禁止跳过产品经理角色** — 即使是"显而易见"的需求也要先分析
- **禁止在子agent中再用delegate_task** — max_spawn_depth=1

## 踩坑记录

1. **Studio Babel编译需要20秒+** — 测试工程师的Playwright任务中必须`waitForTimeout(22000)`。如果测试任务太复杂（涉及多个页面+登录+截图），可能会因delegate_task的默认timeout(300s)而中断。解决方案：将测试拆分为多个简单子任务，或确保每个测试脚本内做好超时控制。
2. **delegate_task中断后无输出** — 如果子agent被interrupted，其summary可能为null。主agent必须检查每个子任务的status字段，对interrupted的任务直接自己执行（不要再次delegate，可能再次超时）。
3. **context中的shell转义** — 如果context包含特殊字符（单引号、美元符号、反引号），在heredoc或node -e中可能出错。复杂测试脚本建议用write_file写入文件再执行。
4. **delegate_task不适合所有场景** — 当任务依赖链明确（B依赖A的结果）且A较简单时，直接在主agent执行A再delegate B更高效。只有真正可并行的独立子任务才值得delegate。
5. **Playwright登录+页面测试的timeout** — delegate_task的子agent执行登录(new-api)→跳转Studio→等待Babel编译→测试的完整流程，很容易超过默认timeout。解决方案：(a)用`p.request.post`登录（快）而不是页面表单登录 (b)把验证脚本写成独立JS文件 (c)每个子任务只做一个验证点。
6. **⭐ 测试工程师必须实际点击验证** — 阿戴明确批评："当初让你完成任务的时候你不验收吗"。测试不能只验证HTML结构正确（curl grep），必须验证：(a)元素可点击 (b)点击后跳转正确 (c)目标页面加载正常 (d)功能可使用。纯curl验证通过但浏览器点击失败是**不可接受的**。测试工程师的输出必须包含"实际操作截图"而非"结构分析报告"。
7. **⭐ 交付前自检清单** — 每次交付前必须回答：(1)用户能直接使用吗？(2)需要用户额外操作吗？(3)我实际测试过点击/使用吗？如果任何答案是"否"，不要交付。

## NEXUS管线集成（阿戴强制 2026-08-11）
用户明确要求：所有工程任务强制使用agency-agents的NEXUS管线。
**优先使用agency-agents角色而非本skill的PM/Dev/QA角色。**

角色映射：
- 产品经理 → 不需要（需求分析由主agent完成）
- 代码工程师 → Frontend Developer / Backend Architect
- 测试工程师 → Reality Checker + Evidence Collector
- 架构师 → Backend Architect / Security Engineer

执行时先skill_view加载agency-agents，选择NEXUS-Sprint或NEXUS-Full模式。
详见 skill:agency-agents

## 与现有skill的关系
- 本skill是**执行协议**，决定怎么工作
- agency-agents是**角色库**，提供NEXUS管线和147个专业Agent人格
- antokex-website-modification等skill是**领域知识**，决定做什么
- 三者配合：先加载agency-agents选角色→本skill确定工作流→领域skill获取知识
