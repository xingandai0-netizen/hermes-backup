# 技能市场使用示例
# Skill Marketplace Usage Examples

## 基本搜索

```python
from skill_marketplace import SkillMarketplace

marketplace = SkillMarketplace()

# 搜索数据相关技能
results = marketplace.search_skills("data processing")
for skill in results:
    print(f"{skill['name']}: {skill['description']}")
```

## 安装技能

```bash
# 从本地源安装
python scripts/skill_marketplace.py install --skill data-converter --source local

# 从GitHub安装
python scripts/skill_marketplace.py install --skill api-tester --source github

# 从社区安装
python scripts/skill_marketplace.py install --skill image-optimizer --source community
```

## 管理已安装技能

```bash
# 列出已安装技能
python scripts/skill_marketplace.py list

# 查看技能详情
python scripts/skill_marketplace.py info --skill data-converter

# 更新技能
python scripts/skill_marketplace.py update --skill data-converter

# 卸载技能
python scripts/skill_marketplace.py uninstall --skill data-converter
```

## 备份和恢复

```bash
# 备份所有技能
python scripts/skill_marketplace.py backup --backup-path /path/to/backup.tar.gz

# 从备份恢复
python scripts/skill_marketplace.py restore --backup-path /path/to/backup.tar.gz
```

## 发布技能

```python
from skill_marketplace import SkillPublisher, SkillMarketplace

marketplace = SkillMarketplace()
publisher = SkillPublisher(marketplace)

# 发布技能
result = publisher.publish_skill(
    skill_path="~/.hermes/skills/my-custom-skill",
    metadata={
        "name": "my-custom-skill",
        "version": "1.0.0",
        "description": "我的自定义技能",
        "author": "Your Name",
        "category": "utility",
        "tags": ["custom", "utility"]
    }
)

if result['success']:
    print(f"发布成功: {result['package_path']}")
else:
    print(f"发布失败: {result['message']}")
```

## 统计信息

```bash
# 查看市场统计
python scripts/skill_marketplace.py stats

# 输出示例:
# {
#   "total_skills": 5,
#   "categories": {
#     "data-processing": 2,
#     "testing": 1,
#     "media": 1,
#     "development": 1
#   },
#   "sources": {
#     "local": 3,
#     "github": 2
#   }
# }
```

## 高级用法

### 自定义搜索过滤器

```python
# 只搜索特定类别
skills = marketplace.search_skills("conversion", category="data-processing")

# 搜索并限制结果数量
skills = marketplace.search_skills("image", limit=5)
```

### 批量安装

```python
skills_to_install = [
    ("data-converter", "github"),
    ("api-tester", "community"),
    ("image-optimizer", "github")
]

for skill_name, source in skills_to_install:
    result = marketplace.install_skill(skill_name, source)
    if result['success']:
        print(f"✓ {skill_name} 安装成功")
    else:
        print(f"✗ {skill_name} 安装失败: {result['message']}")
```

### 技能验证

```python
# 验证技能目录
from skill_marketplace import SkillPublisher

publisher = SkillPublisher(marketplace)
validation = publisher._validate_skill(Path("~/.hermes/skills/my-skill"))

if validation['valid']:
    print("技能验证通过")
else:
    print(f"验证失败: {validation['errors']}")
```
