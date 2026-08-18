# 快速入门模板

## 5分钟快速开始

### 1. 检查系统状态
```bash
cd ~/.hermes/skills/integrated-skills-system
python3 hermes_integrated_system.py status
```

### 2. 保存第一个用户偏好
```bash
python3 hermes_integrated_system.py save-preference \
  --key "language" --value "zh-CN" \
  --description "用户首选语言"
```

### 3. 创建你的第一个技能
```bash
python3 hermes_integrated_system.py create-skill \
  --description "每天检查邮件，提取重要信息，生成摘要" \
  --name "email-digest"
```

### 4. 执行一个代理任务
```bash
python3 hermes_integrated_system.py execute-agent \
  --description "审查email-digest技能的代码质量" \
  --agent code-reviewer
```

### 5. 搜索技能市场
```bash
python3 hermes_integrated_system.py search-skills --query "data"
```

## 常用命令速查

| 命令 | 描述 |
|------|------|
| `status` | 查看系统状态 |
| `create-skill -d "描述"` | 创建新技能 |
| `save-preference -k key -v value` | 保存偏好 |
| `search-memories -q "查询"` | 搜索记忆 |
| `execute-agent -d "任务" -a 代理类型` | 执行代理任务 |
| `search-skills -q "查询"` | 搜索技能 |
| `install-skill -n 名称` | 安装技能 |

## Python API 示例

```python
# 导入系统
import sys
sys.path.insert(0, '/Users/macpro/.hermes/skills/integrated-skills-system')
from hermes_integrated_system import HermesIntegratedSystem

# 初始化系统
system = HermesIntegratedSystem()

# 保存用户偏好
system.save_user_preference("timezone", "Asia/Shanghai")

# 创建技能
result = system.create_skill("每周生成财务报告", "weekly-finance")
print(result)

# 搜索记忆
results = system.search_memories("财务")
print(results)

# 执行代理任务
result = system.execute_agent_task("优化数据库查询性能", "performance")
print(result)

# 搜索技能
results = system.search_skills("data processing")
print(results)

# 获取系统状态
status = system.get_system_status()
print(status)
```

## 支持的代理类型

- `planner` - 规划代理
- `architect` - 架构代理  
- `tdd-guide` - TDD代理
- `code-reviewer` - 代码审查代理
- `security-reviewer` - 安全审查代理
- `performance` - 性能优化代理
- `database` - 数据库代理
- `api-designer` - API设计代理
- `devops` - DevOps代理
- `general` - 通用代理

## 记忆类别

- `user_preferences` - 用户偏好
- `environment_facts` - 环境事实
- `skill_knowledge` - 技能知识
- `project_context` - 项目上下文
- `conversation_history` - 对话历史
- `learned_patterns` - 学习模式
- `error_patterns` - 错误模式
- `performance_metrics` - 性能指标

## 故障排除

### 模块导入错误
```bash
# 确保在正确的目录
cd ~/.hermes/skills/integrated-skills-system

# 检查Python路径
python3 -c "import sys; print(sys.path)"
```

### 数据库错误
```bash
# 检查内存目录权限
ls -la ~/.hermes/memory/

# 重新初始化数据库
rm ~/.hermes/memory/memories.db
python3 scripts/memory_system.py init
```

### 代理执行失败
```bash
# 查看详细错误
python3 hermes_integrated_system.py execute-agent \
  --description "测试任务" \
  --agent general \
  --verbose
```