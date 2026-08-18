---
name: integrated-skills-system
description: >-
  综合技能集成系统，整合了everything-claude-code的代理编排、agent-skill-creator的技能创建、MemOS的记忆系统、buildwithclaude的技能市场、以及awesome-design-patterns的设计模式。为Hermes Agent提供完整的技能管理、记忆系统和代理编排能力。
version: 1.0.0
author: 小黑
license: MIT
metadata:
  hermes:
    tags: [skills-system, memory, agents, orchestration, marketplace]
    integrated-learning: true
    source-repos:
      - everything-claude-code
      - agent-skill-creator
      - MemOS
      - buildwithclaude
      - awesome-design-patterns
      - vercel-react-best-practices
      - ai-notes
---

# Hermes综合技能集成系统
## Integrated Skills System for Hermes Agent

本技能整合了GitHub上7个重要仓库的学习成果，为Hermes Agent提供完整的技能管理、记忆系统和代理编排能力。

## 系统架构

### 1. 核心组件 (Core Components)

#### 1.1 技能管理系统 (Skills Management)
- **技能目录**：`~/.hermes/skills/` - 技能存储位置
- **技能注册**：自动发现和注册新技能
- **技能分类**：按功能分类的技能组织
- **技能版本**：版本控制和更新管理

#### 1.2 记忆系统 (Memory System) - 基于MemOS
- **持久记忆**：跨会话的持久化记忆
- **记忆类型**：用户偏好、环境事实、技能知识
- **记忆检索**：基于关键词的记忆搜索
- **记忆更新**：自动更新和修正记忆

#### 1.3 代理编排 (Agent Orchestration) - 基于everything-claude-code
- **专业代理**：48个专业代理的调度系统
- **代理选择**：基于任务类型的自动选择
- **并行执行**：独立任务的并行处理
- **错误处理**：代理失败时的降级策略

#### 1.4 技能市场 (Skills Marketplace) - 基于buildwithclaude
- **技能发现**：自动发现新技能
- **技能安装**：一键安装技能
- **技能更新**：自动更新已安装技能
- **技能分享**：分享自定义技能

#### 1.5 设计模式库 (Design Patterns) - 基于awesome-design-patterns
- **架构模式**：常见架构模式参考
- **代码模式**：代码组织最佳实践
- **安全模式**：安全实现模式
- **性能模式**：性能优化模式

### 2. 专业代理系统 (Specialized Agents)

基于everything-claude-code的代理系统，Hermes支持以下专业代理：

| 代理类型 | 功能 | 触发条件 |
|---------|------|----------|
| **规划代理** | 实现规划和任务分解 | 复杂功能请求 |
| **架构代理** | 系统设计和可扩展性 | 架构决策 |
| **TDD代理** | 测试驱动开发 | 新功能、bug修复 |
| **代码审查代理** | 代码质量和可维护性 | 代码编写/修改后 |
| **安全审查代理** | 漏洞检测 | 提交前、敏感代码 |
| **构建错误解决代理** | 修复构建/类型错误 | 构建失败时 |
| **重构清理代理** | 死代码清理 | 代码维护 |
| **文档更新代理** | 文档和代码映射 | 更新文档时 |

### 3. 技能创建系统 (Skill Creation) - 基于agent-skill-creator

#### 3.1 五阶段创建流程
1. **发现阶段**：读取所有材料，研究API、数据源、工具
2. **设计阶段**：生成内部规范（用例、方法、输出）
3. **架构阶段**：构建技能目录结构（简单vs复杂套件）
4. **检测阶段**：制定激活描述+关键词，确保可靠触发
5. **实现阶段**：创建所有文件，验证，安全扫描，交付

#### 3.2 技能创建触发条件
- 用户要求创建代理
- 自动化重复工作流
- 创建自定义技能
- 高级代理创建需求

#### 3.3 技能创建命令
```bash
# 自动创建技能
/hermes-skill-create "每周我拉取销售数据，清理，生成报告"

# 从现有脚本创建
/hermes-skill-create "见 scripts/invoice_processor.py - 转换为可重用技能"

# 从API文档创建
/hermes-skill-create "基于API文档创建库存查询技能"
```

### 4. 记忆系统架构 (Memory Architecture) - 基于MemOS

#### 4.1 记忆类型
- **用户偏好**：称呼、交流风格、任务偏好
- **环境事实**：操作系统、工具配置、项目结构
- **技能知识**：API端点、工具特定命令、已验证工作流
- **项目上下文**：任务状态、完成结果、临时TODO

#### 4.2 记忆管理规则
1. **优先级**：用户偏好和纠正 > 环境事实 > 程序知识
2. **价值**：最有价值的记忆是防止用户再次纠正的记忆
3. **更新**：当技能过时、不完整或错误时立即修补
4. **清理**：不保存任务进度、会话结果、临时状态

#### 4.3 记忆搜索和检索
```python
# 记忆搜索语法
关键词 OR 关键词  # OR搜索获得最佳召回
"精确短语"        # 精确短语搜索
布尔 NOT 排除词   # 布尔搜索
前缀*            # 前缀搜索
```

### 5. 性能优化模式 (Performance Patterns) - 基于vercel-react-best-practices

#### 5.1 关键优化原则
1. **消除瀑布流**：避免连续await，最大化并行
2. **包大小优化**：避免桶文件导入，使用动态导入
3. **服务器性能**：使用React.cache()，LRU缓存
4. **客户端数据获取**：SWR自动去重，事件监听器去重
5. **重新渲染优化**：延迟状态读取，提取到记忆化组件

#### 5.2 JavaScript性能模式
- **缓存模式**：缓存属性访问、函数结果、存储API调用
- **循环优化**：构建索引映射、组合迭代、早期长度检查
- **函数优化**：早期返回、提升正则表达式创建、使用Set/Map

### 6. 设计模式库 (Design Patterns Library)

#### 6.1 架构模式
- **微服务架构**：服务拆分、API网关、服务发现
- **事件驱动架构**：事件发布/订阅、事件溯源
- **CQRS模式**：命令查询职责分离
- **仓库模式**：数据访问抽象，业务逻辑依赖抽象接口

#### 6.2 代码组织模式
- **小文件组织**：200-400行，800行最大
- **功能域组织**：按功能/域组织，而非按类型
- **高内聚低耦合**：相关功能集中，减少依赖
- **不可变性**：始终创建新对象，永不改变现有对象

### 7. 技能市场架构 (Skills Marketplace) - 基于buildwithclaude

#### 7.1 技能分类
| 类别 | 描述 | 示例 |
|------|------|------|
| **代理** | 专业AI专家 | Python专家、Go专家、安全专家 |
| **命令** | 斜杠命令自动化 | /commit、/docs、/tdd |
| **钩子** | 事件驱动自动化 | Slack通知、Git自动暂存 |
| **技能** | 可重用能力 | 数据转换、文件处理 |
| **插件** | 捆绑包 | 开发工具包、部署工具包 |

#### 7.2 技能发现和安装
```bash
# 搜索技能
/hermes-skill-search "数据转换"

# 安装技能
/hermes-skill-install data-converter

# 更新技能
/hermes-skill-update data-converter

# 列出已安装技能
/hermes-skill-list
```

### 8. AI学习笔记 (AI Notes) - 基于ai-notes

#### 8.1 AI技术栈
- **文本生成**：GPT-4、Claude、开源模型
- **图像生成**：Stable Diffusion、Midjourney、DALL-E
- **音频生成**：语音合成、音乐生成、语音转录
- **代码生成**：Copilot、CodeLlama、StarCoder

#### 8.2 AI基础设施
- **模型服务**：vLLM、TGI、Ollama
- **向量数据库**：Pinecone、Weaviate、Chroma
- **监控工具**：Weights & Biases、MLflow
- **部署平台**：Modal、Replicate、Hugging Face

## 使用指南

### 1. 技能管理
```bash
# 创建新技能
/hermes-skill-create "描述你的技能"

# 搜索技能
/hermes-skill-search "关键词"

# 安装技能
/hermes-skill-install skill-name

# 查看技能详情
/hermes-skill-view skill-name
```

### 2. 代理编排
```python
# 自动代理选择
agent = select_agent_for_task(task_type)
result = agent.execute(task)

# 并行代理执行
results = run_agents_parallel([agent1, agent2, agent3])

# 代理错误处理
try:
    result = agent.execute(task)
except AgentError:
    result = fallback_agent.execute(task)
```

### 3. 记忆管理
```python
# 保存记忆
memory.save(key, value, category)

# 搜索记忆
results = memory.search(query)

# 获取记忆
value = memory.get(key)

# 更新记忆
memory.update(key, new_value)
```

## 实现经验（2026-04-17）

### 已验证的工作流
1. **仓库搜索** - 成功搜索10个GitHub仓库，找到9个相关项目
2. **批量克隆** - 克隆7个核心仓库到 `~/github-skills/`
3. **深度分析** - 分析每个仓库的README、结构、SKILL.md文件
4. **知识提取** - 提取代理编排、技能创建、记忆系统等模式
5. **系统设计** - 设计4个核心组件：技能创建器、记忆系统、代理编排器、技能市场
6. **代码实现** - 实现4个Python脚本，总计约100KB代码
7. **配置管理** - 创建config.yaml配置文件
8. **文档生成** - 生成README.md和SKILL.md文档
9. **问题修复** - 修复Python导入路径问题
10. **系统验证** - 验证所有组件正常初始化

### 遇到的问题与解决方案
- **导入路径错误** - 使用try/except回退机制，先尝试相对导入，失败后添加脚本目录到sys.path
- **模块依赖** - 创建requirements.txt，明确Python依赖
- **配置复杂性** - 使用YAML配置文件，支持层级配置

### 成功指标
1. **技能创建成功率**：>90%
2. **代理选择准确率**：>95%
3. **记忆检索相关性**：>85%
4. **系统响应时间**：<2秒
5. **用户满意度**：>4.5/5

### 实际部署信息
- **系统位置**：`~/.hermes/skills/integrated-skills-system/`
- **主入口脚本**：`hermes_integrated_system.py`
- **脚本目录**：`scripts/` (4个核心脚本)
- **配置文件**：`config.yaml`
- **文档**：`README.md`, `SKILL.md`
- **依赖**：`requirements.txt`

## 技术规格

- **Python版本**：3.8+
- **依赖包**：requests, json, pathlib, typing, sqlite3, asyncio, yaml
- **配置文件**：`~/.hermes/skills/integrated-skills-system/config.yaml`
- **技能目录**：`~/.hermes/skills/`
- **记忆存储**：`~/.hermes/memory/memories.db`
- **缓存目录**：`~/.hermes/cache/skills/`

## 成功指标

1. **技能创建成功率**：>90%
2. **代理选择准确率**：>95%
3. **记忆检索相关性**：>85%
4. **系统响应时间**：<2秒
5. **用户满意度**：>4.5/5

---

*系统整合完成时间：2026年4月17日*
*基于7个GitHub仓库的学习成果*
*支持Python 3.8+和现代AI代理架构*