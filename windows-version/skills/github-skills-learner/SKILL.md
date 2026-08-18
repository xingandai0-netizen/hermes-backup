---
name: github-skills-learner
description: 系统化搜索、分析和学习GitHub技能仓库的方法。适用于当用户要求搜索特定GitHub仓库、学习其架构、或从多个仓库中提取最佳实践时。
version: 1.0.0
author: 小黑
license: MIT
metadata:
  hermes:
    tags: [github, learning, analysis, skills, automation]
prerequisites:
  commands: [git, curl, python3]
  python_packages: [requests, json]
---

# GitHub技能仓库学习器
## GitHub Skills Repository Learner

系统化搜索、克隆、分析GitHub技能仓库并提取可应用于Hermes Agent的知识。

### 核心能力 (Core Capabilities)

#### 1. 仓库搜索 (Repository Search)
- **批量搜索**: 同时搜索多个GitHub仓库
- **智能匹配**: 自动匹配仓库名称，处理名称不完全匹配的情况
- **API优化**: 使用GitHub API进行高效搜索，处理速率限制

#### 2. 仓库分析 (Repository Analysis)
- **结构分析**: 分析仓库目录结构、配置文件、依赖项
- **内容学习**: 读取README、SKILL.md等关键文件，提取核心概念
- **功能评估**: 评估仓库的功能、使用场景、技术特点

#### 3. 学习总结 (Learning Synthesis)
- **关键发现**: 提取每个仓库的关键功能和学习点
- **应用建议**: 提出如何将学习内容应用到Hermes Agent
- **优先级排序**: 建议集成优先级

### 使用场景 (Use Cases)

```bash
# 场景1: 搜索特定技能仓库
"搜索并学习everything-claude-code, find-skills, skill-creator等仓库"

# 场景2: 学习GitHub趋势工具
"学习GitHub上最新的AI代理工具"

# 场景3: 分析特定技术栈
"分析React性能优化相关的仓库"

# 场景4: 提取最佳实践
"从多个设计模式仓库中提取最佳实践"
```

### 执行流程 (Execution Flow)

#### Phase 1: 搜索阶段
```python
# 1. 定义搜索关键词
search_terms = ["everything-claude-code", "find-skills", "skill-creator"]

# 2. 批量搜索GitHub API
for term in search_terms:
    search_github_api(term)
    
# 3. 智能匹配最佳结果
find_best_matches(search_results)
```

#### Phase 2: 克隆阶段
```bash
# 1. 创建学习目录
mkdir -p ~/github-skills

# 2. 克隆相关仓库
for repo in best_repos:
    git clone https://github.com/{repo}.git ~/github-skills/{name}
```

#### Phase 3: 分析阶段
```python
# 1. 分析仓库结构
analyze_repository_structure(repo_path)

# 2. 读取关键文件
read_key_files(["README.md", "SKILL.md", "package.json"])

# 3. 提取核心概念
extract_core_concepts(content)
```

#### Phase 4: 总结阶段
```python
# 1. 生成学习总结
generate_learning_summary(repos_analysis)

# 2. 提出应用建议
suggest_applications(learnings)

# 3. 保存结果
save_learning_results(summary)
```

### 技术实现 (Technical Implementation)

#### GitHub搜索函数
```python
import requests
import time

def search_github_repositories(search_terms):
    """批量搜索GitHub仓库"""
    results = {}
    
    for term in search_terms:
        print(f"搜索仓库: {term}")
        
        url = f"https://api.github.com/search/repositories?q={term}&sort=stars&per_page=5"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                
                if items:
                    # 寻找最佳匹配
                    best_match = find_best_match(term, items)
                    results[term] = best_match
                    print(f"  ✅ 找到: {best_match['full_name']}")
                else:
                    print(f"  ❌ 无搜索结果")
            else:
                print(f"  ⚠️ API错误: {response.status_code}")
                
        except Exception as e:
            print(f"  ⚠️ 请求失败: {e}")
        
        time.sleep(1)  # 避免速率限制
    
    return results

def find_best_match(search_term, items):
    """寻找最佳匹配的仓库"""
    # 首先尝试精确匹配
    for item in items:
        repo_name = item['name'].lower()
        if search_term.lower() in repo_name or repo_name in search_term.lower():
            return item
    
    # 如果没有精确匹配，返回第一个结果
    return items[0] if items else None
```

#### 仓库分析函数
```python
import os
import json

def analyze_repository(repo_path, repo_info):
    """分析单个仓库"""
    analysis = {
        "name": repo_info.get('full_name'),
        "description": repo_info.get('description'),
        "stars": repo_info.get('stargazers_count'),
        "url": repo_info.get('html_url'),
        "language": repo_info.get('language'),
        "topics": repo_info.get('topics', []),
        "structure": analyze_structure(repo_path),
        "key_files": extract_key_files(repo_path),
        "learnings": []
    }
    
    return analysis

def analyze_structure(repo_path):
    """分析仓库目录结构"""
    structure = {
        "has_skills_dir": os.path.exists(os.path.join(repo_path, "skills")),
        "has_agents_dir": os.path.exists(os.path.join(repo_path, "agents")),
        "has_commands_dir": os.path.exists(os.path.join(repo_path, "commands")),
        "has_hooks_dir": os.path.exists(os.path.join(repo_path, "hooks")),
        "has_plugin_json": os.path.exists(os.path.join(repo_path, "plugin.json")),
        "has_skill_md": os.path.exists(os.path.join(repo_path, "SKILL.md")),
    }
    
    # 统计目录数量
    try:
        items = os.listdir(repo_path)
        structure["total_items"] = len(items)
        structure["key_items"] = items[:10]  # 前10个重要项目
    except:
        structure["total_items"] = 0
        structure["key_items"] = []
    
    return structure

def extract_key_files(repo_path):
    """提取关键文件内容"""
    key_files = {}
    
    files_to_check = ["README.md", "SKILL.md", "package.json", "requirements.txt"]
    
    for file in files_to_check:
        file_path = os.path.join(repo_path, file)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(1000)  # 读取前1000字符
                    key_files[file] = {
                        "size": os.path.getsize(file_path),
                        "preview": content[:200]
                    }
            except:
                key_files[file] = {"error": "无法读取"}
    
    return key_files
```

#### 学习总结生成
```python
def generate_learning_summary(repos_analysis, original_search_terms):
    """生成学习总结"""
    summary = {
        "generated_at": datetime.now().isoformat(),
        "search_terms": original_search_terms,
        "repositories_found": len(repos_analysis),
        "repositories": [],
        "key_learnings": [],
        "integration_suggestions": []
    }
    
    for repo in repos_analysis:
        repo_summary = {
            "name": repo["name"],
            "stars": repo["stars"],
            "description": repo["description"],
            "key_features": extract_key_features(repo),
            "learnings": extract_learnings(repo),
            "application_to_hermes": suggest_hermes_application(repo)
        }
        summary["repositories"].append(repo_summary)
    
    # 生成集成建议
    summary["integration_suggestions"] = generate_integration_suggestions(repos_analysis)
    
    return summary
```

### 输出格式 (Output Format)

#### 学习报告模板
```
# GitHub技能学习报告

## 搜索概览
- 搜索关键词: {search_terms}
- 找到仓库: {repositories_found}
- 学习日期: {generated_at}

## 仓库分析

### 1. {repo_name} (⭐ {stars})
**描述**: {description}
**关键功能**: {key_features}
**学习点**: {learnings}
**Hermes应用**: {application_to_hermes}

## 集成建议
1. {suggestion_1}
2. {suggestion_2}
3. {suggestion_3}
```

### 高级功能 (Advanced Features)

#### 1. 分类搜索策略 (Categorized Search Strategy)
```python
def search_by_category(categories):
    """按分类搜索GitHub仓库"""
    search_categories = {
        "cli_tools": "cli+tool+language:python+language:go",
        "ai_agents": "ai+agent+framework",
        "automation": "automation+tool+language:python",
        "developer_tools": "developer+tool+language:python",
        "data_processing": "data+processing+tool+language:python",
        "web_automation": "browser+automation+tool+language:python",
        "academic_formatting": "academic+paper+formatting+word+python-docx",
        "thesis_template": "thesis+template+docx+automation"
    }
    
    results = {}
    for category, query in search_categories.items():
        print(f"搜索分类: {category}")
        results[category] = search_github_api(query)
    
    return results
```

#### 实战案例：学术论文排版仓库搜索（2026-06-03）

搜索关键词组合：
```python
search_queries = [
    "academic paper formatting word python-docx",
    "thesis formatting docx automation",
    "academic writing word document template",
    "python-docx academic report formatting",
    "docx formatter",
    "python-docx style helper"
]
```

找到的最佳仓库：
1. **format-thesis-docx** ⭐0 - 三步法：模板提取→审计→修复，200+检查点
2. **docx-format-skill** ⭐1 - python-docx模板库，中英文字体处理
3. **LogicPaper** ⭐123 - Jinja2模板批量文档生成引擎

关键发现：
- 大多数学术格式化仓库星数很低（<5），但代码质量不错
- 搜索时用多个关键词组合效果更好
- 优先分析SKILL.md和README.md获取核心概念
# 实战案例：学习10个不同领域仓库
# 1. natural-language-optimizer (文本处理)
# 2. ai-art-workflow (艺术创作)
# 3. wechat-automation-reference (社交媒体)
# 4. social-media-automation (社交媒体)
# 5. langchain-agent-fundamentals (AI Agent)
# 6. drission-page-automation (网页自动化)
# 7. lazygit-advanced (开发者工具)
# 8. ripgrep-search (搜索工具)
# 9. chinese-nlp-toolkit (中文NLP)
# 10. certbot-ssl-management (DevOps)
```

#### 2. 智能推荐
```python
def recommend_similar_repositories(repo_name, repo_topics):
    """推荐相似仓库"""
    # 基于话题推荐
    topics_query = "+".join(repo_topics)
    url = f"https://api.github.com/search/repositories?q=topic:{topics_query}&sort=stars"
    
    # 分析并推荐
    return recommendations
```

#### 2. 趋势分析
```python
def analyze_github_trends(category="ai-agents", timeframe="weekly"):
    """分析GitHub趋势"""
    # 获取趋势仓库
    # 分析技术栈
    # 生成趋势报告
    pass
```

#### 3. 知识提取
```python
def extract_architectural_patterns(repos):
    """从多个仓库提取架构模式"""
    patterns = {
        "skill_organization": [],
        "agent_architecture": [],
        "memory_systems": [],
        "plugin_systems": []
    }
    
    for repo in repos:
        patterns = analyze_patterns(repo, patterns)
    
    return patterns
```

### 集成Hermes Agent (Integration with Hermes Agent)

#### 技能触发条件
- 用户提到"搜索GitHub"
- 用户要求"学习仓库"
- 用户提到"分析项目"
- 用户要求"提取最佳实践"

#### 使用示例
```bash
# 作为技能使用
skill github-skills-learner search ["repo1", "repo2", "repo3"]

# 分析特定技术
skill github-skills-learner analyze "react-performance"

# 提取模式
skill github-skills-learner extract-patterns ["memory-systems", "agent-architecture"]
```

### 最佳实践 (Best Practices)

#### 1. 搜索优化
- 使用多个关键词搜索同一概念
- 考虑名称变体和拼写错误
- 设置合理的per_page参数

#### 2. 分析深度
- 优先分析README和SKILL.md
- 检查依赖文件了解技术栈
- 分析目录结构了解架构

#### 3. 学习提取
- 关注可重用的模式
- 记录具体的应用场景
- 提出具体的集成建议

### 限制与注意事项 (Limitations & Notes)

#### 1. API限制
- GitHub API有速率限制（未认证60次/小时）
- 建议使用GITHUB_TOKEN提高限制
- 批量搜索时添加延迟

#### 2. 分析范围
- 只分析主要文件（README, SKILL.md）
- 代码分析仅限于关键文件
- 依赖分析基于配置文件

#### 3. 学习质量
- 需要人工验证提取的关键概念
- 集成建议需要结合实际需求
- 架构模式需要考虑技术兼容性

### 深度架构分析方法 (Deep Architecture Analysis)

#### 1. Channel架构模式分析
当学习具有多平台/多渠道支持的工具时，分析其Channel架构：

```python
# Channel架构分析流程
channel_analysis = {
    "base_class": "查找Channel基类定义",
    "registry": "查看Channel注册机制 (__init__.py)",
    "implementations": "分析各平台Channel实现",
    "config_system": "理解配置管理方式",
    "health_check": "学习Doctor检测机制"
}

# 实战案例：Agent-Reach的Channel架构
# - base.py: 定义Channel抽象基类，包含name, description, backends, tier
# - __init__.py: 注册所有Channel到ALL_CHANNELS列表
# - 每个平台实现: twitter.py, youtube.py, xiaohongshu.py等
# - doctor.py: 遍历所有Channel检查状态
# - config.py: 统一配置管理 (~/.agent-reach/config.yaml)
```

#### 2. 配置系统分析模式
```python
# 配置系统分析要点
config_analysis = {
    "config_location": "配置文件存储位置",
    "config_format": "配置格式 (YAML/JSON/TOML)",
    "config_keys": "必需的配置项",
    "config_validation": "配置验证机制",
    "config_auto_create": "是否自动创建配置目录"
}

# Agent-Reach配置系统特点:
# - 存储位置: ~/.agent-reach/config.yaml
# - 配置等级: tier 0=零配置, 1=免费key, 2=复杂配置
# - FEATURE_REQUIREMENTS: 定义各功能所需配置项
# - 自动创建: 首次使用时创建目录
```

#### 3. 健康检测机制分析
```python
# Doctor/Health Check分析
health_check_analysis = {
    "detection_method": "如何检测工具可用性",
    "status_levels": "状态等级 (ok/warn/off/error)",
    "remediation": "提供修复建议",
    "report_format": "报告输出格式"
}

# Agent-Reach Doctor机制:
# - 遍历ALL_CHANNELS调用每个Channel的check()方法
# - 返回(status, message)元组
# - format_report()生成可读报告
# - 支持emoji标识状态 (✅/⚠️/❌)
```

### 扩展分类搜索策略 (Extended Categorized Search)

```python
# 扩展的搜索分类
extended_search_categories = {
    # 原有分类
    "cli_tools": "cli+tool+language:python+language:go",
    "ai_agents": "ai+agent+framework",
    "automation": "automation+tool+language:python",
    "developer_tools": "developer+tool+language:python",
    "data_processing": "data+processing+tool+language:python",
    "web_automation": "browser+automation+tool+language:python",
    
    # 新增分类 (基于实战学习)
    "networking": "http+client+api+tool+language:python",
    "system_admin": "system+administration+tool",
    "nlp_tools": "nlp+text+processing+chinese",
    "ssl_security": "ssl+https+certificate+tool",
    "git_tools": "git+ui+terminal+tool",
    "search_tools": "search+grep+fast+tool",
    "video_tools": "video+subtitle+transcript",
    "social_media": "social+media+automation",
    "rss_feeds": "rss+feed+reader+parser"
}
```

### 技能创建最佳实践 (Skill Creation Best Practices)

#### 从仓库到技能的转换流程
```python
# 技能创建流程
skill_creation_workflow = {
    "step1_explain": "理解仓库核心价值和解决的问题",
    "step2_structure": "分析代码架构和关键模块",
    "step3_patterns": "提取可复用的设计模式",
    "step4_document": "编写SKILL.md文档",
    "step5_test": "验证技能可用性"
}

# Agent-Reach案例:
# 1. 核心价值: 给AI Agent提供互联网访问能力，零API费用
# 2. 代码架构: Channel系统 + CLI工具 + 配置管理
# 3. 设计模式: Channel抽象、Doctor检测、Tier分级
# 4. 文档: 包含15+平台、安装方法、使用示例、配置说明
# 5. 验证: 通过doctor命令验证环境
```

#### SKILL.md文档结构模板
```markdown
---
name: skill-name
description: 一句话描述
version: 1.0.0
author: Hermes Agent
---

# 技能名称

## 触发条件 (什么情况下激活)

## 核心功能 (主要能力列表)

## 使用方法 (命令和代码示例)

## 架构说明 (核心设计模式)

## 配置说明 (如何配置)

## 实战场景 (具体使用案例)

## 故障排除 (常见问题)
```

### 学习质量检查清单 (Learning Quality Checklist)

```python
# 确保学习质量的检查项
quality_checklist = {
    "architecture_understood": "是否理解核心架构",
    "key_modules_identified": "是否识别关键模块",
    "config_system_mapped": "是否理解配置系统",
    "usage_examples_collected": "是否收集使用示例",
    "limitations_noted": "是否记录限制和注意事项",
    "integration_path": "是否明确集成路径"
}
```

---

*技能创建时间: 2026年4月17日*
*最后更新: 2026-04-17 (添加深度架构分析、Channel模式、配置系统分析)*
*基于everything-claude-code, buildwithclaude, agent-skill-creator, agent-reach等仓库学习*
*适用于Hermes Agent的GitHub技能学习需求*