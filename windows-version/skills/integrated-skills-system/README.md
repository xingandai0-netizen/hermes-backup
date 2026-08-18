# Hermes综合技能集成系统
## Integrated Skills System for Hermes Agent

这是一个完整的技能管理、记忆系统、代理编排和技能市场系统，整合了GitHub上7个重要仓库的学习成果。

## 📋 系统概述

### 核心组件

1. **技能创建系统** (基于agent-skill-creator)
   - 自动创建技能的五阶段流程
   - 从工作流描述、现有代码、API文档创建技能
   - 跨平台兼容，支持多种技能格式

2. **记忆系统** (基于MemOS)
   - 持久化、可检索、可编辑的记忆存储
   - 支持用户偏好、环境事实、技能知识等多种记忆类型
   - 全文搜索和语义检索功能

3. **代理编排系统** (基于everything-claude-code)
   - 19种专业代理，覆盖开发、测试、安全、性能等各个领域
   - 智能任务分配和并行执行
   - 错误处理和降级策略

4. **技能市场系统** (基于buildwithclaude)
   - 技能发现、安装、更新和分享
   - 本地、GitHub、社区三来源支持
   - 自动验证和安全扫描

5. **设计模式库** (基于awesome-design-patterns)
   - 架构模式参考
   - 代码组织最佳实践
   - 安全实现模式

## 🚀 快速开始

### 1. 系统初始化

```bash
# 进入技能目录
cd ~/.hermes/skills/integrated-skills-system

# 查看系统状态
python hermes_integrated_system.py status
```

### 2. 创建技能

```bash
# 从描述创建技能
python hermes_integrated_system.py create-skill \
  --description "每周我拉取销售数据，清理，生成报告" \
  --name "sales-report-generator"

# 从现有代码创建技能
python scripts/skill_creator.py create scripts/existing_script.py --type code
```

### 3. 记忆管理

```bash
# 保存用户偏好
python hermes_integrated_system.py save-preference \
  --key "user_name" --value "阿戴" \
  --description "用户姓名"

# 搜索记忆
python hermes_integrated_system.py search-memories --query "销售数据"

# 查看所有偏好
python hermes_integrated_system.py get-preferences
```

### 4. 代理执行

```bash
# 执行规划任务
python hermes_integrated_system.py execute-agent \
  --description "分析项目结构并制定实现计划" \
  --agent planner

# 执行代码审查
python hermes_integrated_system.py execute-agent \
  --description "审查main.py代码质量" \
  --agent code-reviewer
```

### 5. 技能市场

```bash
# 搜索技能
python hermes_integrated_system.py search-skills --query "数据转换"

# 安装技能
python hermes_integrated_system.py install-skill --name data-converter --source github

# 查看已安装技能
python scripts/skill_marketplace.py list
```

## 📁 文件结构

```
integrated-skills-system/
├── SKILL.md                    # 技能描述文件
├── README.md                   # 本文件
├── config.yaml                 # 系统配置
├── hermes_integrated_system.py # 主入口脚本
├── requirements.txt            # Python依赖
├── scripts/                    # 脚本目录
│   ├── skill_creator.py        # 技能创建器
│   ├── memory_system.py        # 记忆系统
│   ├── agent_orchestrator.py   # 代理编排器
│   └── skill_marketplace.py    # 技能市场
├── references/                 # 参考文档
└── templates/                  # 模板文件
```

## 🔧 组件详情

### 1. 技能创建器 (skill_creator.py)

#### 五阶段创建流程

1. **发现阶段** - 读取所有材料，研究API、数据源、工具
2. **设计阶段** - 生成内部规范（用例、方法、输出）
3. **架构阶段** - 构建技能目录结构
4. **检测阶段** - 制定激活描述和关键词
5. **实现阶段** - 创建所有文件，验证，安全扫描

#### 使用示例

```python
from scripts.skill_creator import HermesSkillCreator

creator = HermesSkillCreator()

# 从描述创建
result = creator.create_skill_from_description(
    "每周处理发票数据，生成财务报告",
    "finance-report"
)

# 从代码创建
result = creator.create_skill_from_code("scripts/existing.py")

# 从API文档创建
result = creator.create_skill_from_api_docs(api_documentation)
```

### 2. 记忆系统 (memory_system.py)

#### 记忆类型

- **用户偏好** - 称呼、交流风格、任务偏好
- **环境事实** - 操作系统、工具配置、项目结构
- **技能知识** - API端点、工具特定命令、已验证工作流
- **项目上下文** - 任务状态、完成结果、临时TODO

#### 使用示例

```python
from scripts.memory_system import HermesMemoryManager

memory = HermesMemoryManager()

# 保存用户偏好
memory.save_user_preference("language", "zh-CN")

# 保存技能知识
memory.save_skill_knowledge(
    "data-converter",
    {"api_endpoint": "/api/convert", "methods": ["POST"]}
)

# 搜索记忆
results = memory.search_insights("销售数据")
```

### 3. 代理编排器 (agent_orchestrator.py)

#### 支持的代理类型

| 代理类型 | 功能描述 |
|---------|----------|
| planner | 规划代理 - 任务分解和规划 |
| architect | 架构代理 - 系统设计和架构 |
| tdd-guide | TDD代理 - 测试驱动开发 |
| code-reviewer | 代码审查代理 - 代码质量检查 |
| security-reviewer | 安全审查代理 - 漏洞检测 |
| build-error-resolver | 构建错误解决代理 |
| refactor-cleaner | 重构清理代理 |
| doc-updater | 文档更新代理 |
| debugger | 调试代理 |
| testing | 测试代理 |
| performance | 性能优化代理 |
| database | 数据库代理 |
| api-designer | API设计代理 |
| ui-designer | UI设计代理 |
| devops | DevOps代理 |
| security-scanner | 安全扫描代理 |
| data-engineer | 数据工程代理 |
| ml-engineer | 机器学习代理 |
| general | 通用代理 |

#### 使用示例

```python
from scripts.agent_orchestrator import AgentOrchestrator, AgentType, create_task
import asyncio

orchestrator = AgentOrchestrator()

# 创建任务
task = create_task(
    "分析项目结构并制定实现计划",
    AgentType.PLANNER,
    context={'project_path': '/path/to/project'}
)

# 执行任务
result = asyncio.run(orchestrator.execute_task(task))

# 并行执行多个任务
tasks = [
    create_task("任务1", AgentType.CODE_REVIEWER),
    create_task("任务2", AgentType.SECURITY_REVIEWER)
]
results = asyncio.run(orchestrator.execute_tasks_parallel(tasks))
```

### 4. 技能市场 (skill_marketplace.py)

#### 技能来源

- **local** - 本地技能库
- **github** - GitHub技能库  
- **community** - 社区技能库

#### 使用示例

```python
from scripts.skill_marketplace import SkillMarketplace

marketplace = SkillMarketplace()

# 搜索技能
skills = marketplace.search_skills("数据转换", category="data-processing")

# 安装技能
result = marketplace.install_skill("data-converter", source="github")

# 列出已安装技能
installed = marketplace.list_installed_skills()

# 更新技能
result = marketplace.update_skill("data-converter")

# 备份技能
backup_path = marketplace.backup_skills()
```

## 🎯 使用场景

### 场景1: 创建自定义技能

```bash
# 从工作流描述创建技能
python hermes_integrated_system.py create-skill \
  --description "每天早上9点，检查邮件，提取重要信息，生成日报" \
  --name "daily-email-digest"
```

### 场景2: 智能任务执行

```bash
# 让代理分析并优化代码
python hermes_integrated_system.py execute-agent \
  --description "分析main.py的性能瓶颈并提出优化建议" \
  --agent performance
```

### 场景3: 记忆驱动的工作流

```bash
# 保存用户偏好
python hermes_integrated_system.py save-preference \
  --key "work_hours" --value "9:00-18:00"

# 搜索相关记忆
python hermes_integrated_system.py search-memories --query "工作时间"
```

## 📊 系统监控

### 查看系统状态

```bash
python hermes_integrated_system.py status
```

### 查看统计信息

```bash
# 记忆统计
python scripts/memory_system.py stats

# 代理统计
python scripts/agent_orchestrator.py stats

# 技能市场统计
python scripts/skill_marketplace.py stats
```

## 🔄 维护和备份

### 备份系统

```bash
# 备份记忆
python scripts/memory_system.py backup --backup-path /path/to/backup.db

# 备份技能
python scripts/skill_marketplace.py backup --backup-path /path/to/backup.tar.gz
```

### 恢复系统

```bash
# 恢复记忆
python scripts/memory_system.py restore --backup-path /path/to/backup.db

# 恢复技能
python scripts/skill_marketplace.py restore --backup-path /path/to/backup.tar.gz
```

## 🚨 故障排除

### 常见问题

1. **模块导入失败**
   - 检查Python路径
   - 确保所有依赖已安装

2. **数据库连接失败**
   - 检查内存目录权限
   - 确保SQLite可用

3. **代理执行失败**
   - 检查代理类型是否支持
   - 查看错误日志

### 调试模式

```bash
# 启用详细日志
export PYTHONPATH=/path/to/scripts
python -v hermes_integrated_system.py status
```

## 📈 性能优化

### 缓存配置

系统支持多级缓存：
- 技能注册表缓存
- 记忆查询缓存
- 代理结果缓存

### 并行执行

代理编排器支持：
- 最多4个并行工作线程
- 任务依赖管理
- 超时和重试机制

## 🔐 安全考虑

### 输入验证

- 所有用户输入都经过验证
- 支持SQL注入防护
- 支持XSS防护

### 权限控制

- 技能执行需要验证
- 记忆访问需要授权
- 代理调用需要认证

## 🤝 贡献指南

### 添加新代理类型

1. 在`agent_orchestrator.py`中定义新的代理类
2. 实现`execute`方法
3. 在`AgentOrchestrator`中注册代理

### 添加新的记忆类别

1. 在`config.yaml`中定义新类别
2. 在`memory_system.py`中添加处理逻辑
3. 更新文档

### 扩展技能市场

1. 在`skill_marketplace.py`中添加新的技能源
2. 实现搜索和安装逻辑
3. 更新配置

## 📄 许可证

MIT License

## 🙏 致谢

感谢以下GitHub仓库提供的学习成果：

1. **everything-claude-code** - 代理编排模式
2. **agent-skill-creator** - 技能创建方法
3. **MemOS** - 记忆系统设计
4. **buildwithclaude** - 技能市场架构
5. **awesome-design-patterns** - 设计模式参考
6. **vercel-react-best-practices** - 性能优化模式
7. **ai-notes** - AI技术栈参考

---

*系统创建时间: 2026年4月17日*
*版本: 1.0.0*
*作者: 小黑 (Xiao Hei)*