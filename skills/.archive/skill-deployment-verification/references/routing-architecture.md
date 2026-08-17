# 三层路由架构

当skills数量>50时，使用三层路由实现全覆盖：

## Layer 1: 硬编码路由（核心skills，每次必加载）
在system_prompt_append中直接写`skill_view(name='X')`。
适用于：21个核心skill（superpowers, tdd-bdd, reverse-skill-router等）。
格式：
```
开发→superpowers | 调试→developer-debugging | 渗透→reverse-skill-router
```

## Layer 2: 类别扫描（按需发现）
在system_prompt_append中写`skills_list(category='X')`。
适用于：覆盖整个类别的任务（design, productivity, mlops等）。
格式：
```
收到消息后按类别调用skills_list(category=...)扫描
```

## Layer 3: 意图路由（精确匹配）
在system_prompt_append中写`意图关键词→skill_name`。
适用于：所有剩余skills，每个skill至少一个意图路由。
格式：
```
INTENT ROUTING (237条):
写代码→superpowers | Excel→excel-data-processor | Pokemon→pokemon-player
```

## 覆盖率验证
```python
import os, yaml, re
config = yaml.safe_load(open(os.path.expanduser('~/.hermes/config.yaml')))
append = config.get('agent', {}).get('system_prompt_append', '')
# 检查每个skill名是否出现在append中
skills_dir = os.path.expanduser('~/.hermes/skills')
for root, dirs, files in os.walk(skills_dir):
    if 'SKILL.md' in files:
        name = os.path.basename(os.path.dirname(os.path.join(root, 'SKILL.md')))
        if name not in append:
            print(f'❌ {name}')
```

## 生成意图路由索引
```python
# 为每个skill生成意图路由，写入INTENT-ROUTES.md
# 格式：- 意图关键词 → skill_name
# 然后将关键路由注入system_prompt_append
```

## 注意事项
- system_prompt_append过大会增加token消耗，用精简格式
- 完整索引放`~/.hermes/skills/INTENT-ROUTES.md`，系统提示只放常用路由
- 每次新增skill必须同步更新路由
