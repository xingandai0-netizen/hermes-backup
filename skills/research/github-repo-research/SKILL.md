---
name: github-repo-research
description: 系统化搜索、评估和分析GitHub仓库的研究技能。当用户要求搜索特定类型工具、比较多个仓库、评估可行性、或需要深度技术调研时激活。支持多维度评估框架和可行性报告生成。
version: 1.0.0
author: 小黑
license: MIT
metadata:
  created: 2026-04-17
  last_reviewed: 2026-04-17
  review_interval_days: 30
activation: /github-research
platforms:
  - hermes
  - claude-code
capabilities:
  - GitHub仓库搜索和筛选
  - 多维度质量评估
  - 可行性分析框架
  - 技术栈识别
  - 风险评估
  - 研究报告生成
tags: [github, research, analysis, feasibility, repository]
---

# /github-repo-research

系统化GitHub仓库研究和可行性分析技能。

## 触发条件

当用户提到以下内容时激活：
- "搜索GitHub仓库"
- "查找xxx工具/技能"
- "分析xxx可行性"
- "对比xxx和xxx"
- "评估是否下载学习"
- "研究xxx技术方案"

## 工作流程

### Phase 1: 搜索策略制定 (SEARCH STRATEGY)

```
1. 理解用户需求的核心功能
2. 生成搜索关键词组合
3. 确定搜索维度（功能、技术栈、平台）
4. 执行多轮搜索
```

#### 搜索查询模板
```python
search_queries = {
    "核心功能": [
        "{功能关键词} skill",
        "{功能关键词} agent",
        "{功能关键词} automation"
    ],
    "技术栈": [
        "{功能} python",
        "{功能} API",
        "{功能} open source"
    ],
    "平台特定": [
        "{平台} {功能} bot",
        "{平台} {功能} automation"
    ]
}
```

#### GitHub搜索语法
```
# 基本搜索
gh search repos "{query}" --limit 10 --json name,fullName,description,stargazerCount,url

# 按星数排序
gh search repos "{query}" --sort stars --order desc

# 语言过滤
gh search repos "{query} language:python"

# 浏览器搜索
https://github.com/search?q={query}&type=repositories&s=stars&o=desc
```

### Phase 2: 多维度评估框架 (EVALUATION FRAMEWORK)

#### 2.1 星数和社区认可度
```python
def evaluate_stars(stars):
    if stars >= 10000: return "⭐⭐⭐⭐⭐ 极高"
    elif stars >= 1000: return "⭐⭐⭐⭐ 高"
    elif stars >= 100: return "⭐⭐⭐ 中"
    elif stars >= 10: return "⭐⭐ 低"
    else: return "⭐ 极低"
```

#### 2.2 活跃度评估
```python
def evaluate_activity(updated_at):
    # 检查最后更新时间
    # < 1个月: 活跃
    # < 6个月: 一般
    # > 1年: 不活跃
```

#### 2.3 集成难度评估
```python
difficulty_factors = {
    "有SKILL.md": 低,
    "有完整文档": 低,
    "有示例代码": 低,
    "有Docker支持": 中,
    "需要复杂配置": 高,
    "依赖专有服务": 高
}
```

#### 2.4 风险评估矩阵
```python
risk_levels = {
    "法律风险": ["合规", "灰色地带", "违规", "违法"],
    "维护风险": ["活跃维护", "偶尔更新", "已弃坑"],
    "技术风险": ["成熟稳定", "实验性", "不可用"],
    "账号风险": ["安全", "可能封号", "必封"]
}
```

### Phase 3: 可行性报告生成 (FEASIBILITY REPORT)

#### 报告模板
```markdown
# {项目名称} 可行性分析报告

## 基本信息
- 仓库地址: {url}
- Stars: {stars}
- 最后更新: {date}
- 许可证: {license}

## 核心功能
{功能列表}

## 技术栈
{依赖和框架}

## 评估结果
| 指标 | 评分 | 说明 |
|------|------|------|
| 星数 | ⭐⭐⭐⭐ | {说明} |
| 活跃度 | ⭐⭐⭐ | {说明} |
| 文档 | ⭐⭐⭐⭐ | {说明} |
| 集成难度 | ⭐⭐⭐ | {说明} |
| 风险 | ⭐⭐ | {说明} |

## 推荐结论
{推荐/不推荐/可选推荐}

## 下一步行动
{具体建议}
```

### Phase 4: 决策矩阵 (DECISION MATRIX)

当比较多个仓库时，使用决策矩阵：

```python
decision_matrix = {
    "仓库A": {
        "stars": 4.5,
        "activity": 4.0,
        "docs": 4.5,
        "integration": 4.0,
        "risk": 4.5,
        "total": 4.3
    },
    "仓库B": {
        "stars": 3.0,
        "activity": 3.5,
        "docs": 3.0,
        "integration": 3.5,
        "risk": 3.0,
        "total": 3.2
    }
}
```

## 使用示例

### 示例1: 搜索特定功能
```bash
/github-research 搜索能降低AI语言僵硬感的GitHub技能
```

### 示例2: 多维度分析
```bash
/github-research 分析 humanizer 仓库的可行性
```

### 示例3: 对比多个方案
```bash
/github-research 对比微信自动化方案：weixin-bot vs wechat-automation-api
```

## 工具集成

### 浏览器搜索
```python
# 使用browser_navigate搜索GitHub
browser_navigate("https://github.com/search?q={query}&type=repositories&s=stars&o=desc")
```

### 命令行搜索
```python
# 使用gh CLI（如果可用）
terminal("gh search repos '{query}' --limit 10 --json name,fullName,description,stargazerCount")
```

### 研究报告保存
```python
# 保存到标准位置
~/github-learning/{category}-research-report.md
```

## 报告输出格式

### 快速摘要
```
📊 搜索结果总览
| 类别 | 结果数 | 高星仓库 | 可行性 |
|------|--------|----------|--------|
| 功能A | 50个 | ⭐5k | ✅高 |
```

### 详细分析
```
🎯 仓库名称 (Stars)
核心功能: ...
技术栈: ...
可行性: ...
风险: ...
推荐度: ...
```

### 决策建议
```
✅ 强烈推荐: ...
⚠️ 可选增强: ...
❌ 不推荐: ...
```

## 注意事项

1. **搜索限制**: GitHub API有速率限制，避免短时间内大量请求
2. **星数参考**: 星数不是唯一标准，需综合考虑活跃度和文档
3. **风险评估**: 法律风险和账号风险需要特别关注
4. **定期更新**: 研究结果可能随时间变化，建议定期复查

## 集成建议

### 与Hermes技能系统集成
- 将研究报告保存到 `~/github-learning/`
- 更新记忆系统记录学习成果
- 使用skill_manage创建新技能（如果仓库适合）

### 与研究工作流集成
- 可与DeepGit深度研究结合
- 可与agent-skill-creator技能创建结合
- 可与buildwithclaude技能发现结合

---

**技能创建时间**: 2026年4月17日  
**基于实际项目**: 三类技能搜索和可行性分析  
**版本**: 1.0.0