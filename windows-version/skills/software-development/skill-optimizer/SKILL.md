---
name: skill-optimizer
description: "Skills命中率优化系统 — 整合8个高星GitHub项目的核心算法。渐进式披露+语义路由+工具RAG+去重合并+预设分组+安全扫描+按需发现+图预测。解决skills过多导致agent无法正常使用的问题。"
version: 1.0.0
author: 小黑
license: MIT
metadata:
  hermes:
    tags: [skills, optimization, routing, rag, discovery, management, token-reduction]
    related_skills: [hermes-agent, integrated-skills-system]
---

# Skill Optimizer — 8合1 Skills命中率优化系统

整合8个高星GitHub项目的核心算法，解决Hermes 187+ skills导致的上下文污染、选择困难、性能下降问题。

## 架构：5层过滤管线

```
用户输入
    │
    ▼
┌─────────────────────────────────────────────┐
│ Layer 1: 预设分组过滤 (skills-manager)       │  按场景排除不相关skill组
│   security / dev / design / daily / creative │
└─────────────────┬───────────────────────────┘
                  │ ~40 skills
                  ▼
┌─────────────────────────────────────────────┐
│ Layer 2: 语义路由 (MCP-Zero)                │  embedding匹配，取top-10
│   两阶段：先匹配类别 → 再匹配具体skill       │
└─────────────────┬───────────────────────────┘
                  │ ~10 skills
                  ▼
┌─────────────────────────────────────────────┐
│ Layer 3: 工具RAG (RAG-MCP + ToolScope)      │  向量检索+重排序
│   sentence-transformers + cross-encoder      │
└─────────────────┬───────────────────────────┘
                  │ ~5 skills
                  ▼
┌─────────────────────────────────────────────┐
│ Layer 4: 安全扫描 (SkillSpector)            │  过滤恶意/有漏洞的skill
│   64种漏洞模式 × 16风险类别                  │
└─────────────────┬───────────────────────────┘
                  │ ~4 safe skills
                  ▼
┌─────────────────────────────────────────────┐
│ Layer 5: 图预测 (AutoTool)                  │  基于历史使用模式预测
│   Tool Invocation Graph + N-gram             │
└─────────────────┬───────────────────────────┘
                  │ 最终3-5 skills
                  ▼
            加载完整SKILL.md
```

## 当前实现：Hermes原生适配

由于Hermes的skills系统是文件-based的（不是API），我们用**配置+脚本**方式实现核心优化：

### 1. 预设分组（最高优先级）

创建 `~/.hermes/skill-presets.yaml`：

```yaml
presets:
  security:
    description: "安全研究/渗透/逆向"
    categories: [red-teaming, security]
    skills: [godmode, ai-pentest-toolkit, pentest-pipeline, re-toolkit-mcp, 
             vulnclaw, malicious-project-bounty-research, defi-security-research,
             github-security-arsenal, bypass-secret-redaction]
  
  development:
    description: "软件开发/代码/调试"
    categories: [software-development, github]
    skills: [hermes-agent, tdd-bdd, code-quality-workflow, developer-debugging,
             safe-patch-practice, incremental-implementation, full-stack-project-bootstrap]
  
  design:
    description: "UI/UX设计"
    categories: [design, creative]
    skills: [taste-skill, ui-ux-pro-max-skill, design-taste-system, 
             claude-design, nothing-design, baseline-ui]
  
  daily:
    description: "日常工具/效率"
    categories: [productivity, automation, platforms]
    skills: [apple-productivity, macos-computer-use, wechat-automation,
             officecli, ocr-and-documents, task-completion-protocol]
  
  research:
    description: "研究/学习/分析"
    categories: [research, mlops, autonomous-learning]
    skills: [academic-research, competitive-research-report, llm-wiki,
             github-trend-monitor, follow-builders-digest]

  creative:
    description: "创意/内容/媒体"
    categories: [creative, media, social-media]
    skills: [ai-art-workflow, ai-music-generation, xiaohongshu-content-creation,
             ascii-creative, chart-visualization]
```

### 2. 使用方式

```bash
# 安全研究任务
hermes --skills security "分析这个二进制文件"

# 开发任务  
hermes --skills development "构建REST API"

# 或在会话中切换
/skill security
```

### 3. 语义路由脚本

`~/.hermes/scripts/skill-router.py` — 基于关键词的轻量路由：

```python
#!/usr/bin/env python3
"""Skill semantic router — matches user input to skill presets."""
import sys, json, re

PRESETS = {
    "security": {
        "keywords": ["渗透", "漏洞", "逆向", "破解", "hack", "exploit", "vulnerability", 
                     "pentest", "malware", "drainer", "stealer", "钓鱼", "bounty", "CVE",
                     "二进制", "binary", "reverse", "debug", "x64dbg", "ida", "ghidra"],
        "weight": 1.0
    },
    "development": {
        "keywords": ["代码", "开发", "build", "code", "debug", "test", "api", "部署",
                     "deploy", "git", "bug", "refactor", "前端", "后端", "fullstack"],
        "weight": 1.0
    },
    "design": {
        "keywords": ["设计", "UI", "UX", "design", "界面", "样式", "配色", "排版",
                     "logo", "品牌", "brand", "figma", "css", "动画"],
        "weight": 1.0
    },
    "daily": {
        "keywords": ["提醒", "日历", "邮件", "微信", "文件", "办公", "文档", "PDF",
                     "remind", "calendar", "email", "wechat", "office"],
        "weight": 0.8
    },
    "research": {
        "keywords": ["研究", "论文", "调研", "分析", "paper", "research", "arxiv",
                     "竞品", "市场", "趋势", "学习"],
        "weight": 0.9
    },
    "creative": {
        "keywords": ["创作", "图片", "音乐", "视频", "小红书", "内容", "漫画",
                     "art", "music", "video", "photo", "illustration"],
        "weight": 0.9
    }
}

def route(text):
    text_lower = text.lower()
    scores = {}
    for preset, config in PRESETS.items():
        matches = sum(1 for kw in config["keywords"] if kw in text_lower)
        scores[preset] = matches * config["weight"]
    
    if not any(scores.values()):
        return "daily"  # default
    
    best = max(scores, key=scores.get)
    # If top2 are close, return both
    sorted_scores = sorted(scores.items(), key=lambda x: -x[1])
    if len(sorted_scores) > 1 and sorted_scores[1][1] >= sorted_scores[0][1] * 0.7:
        return f"{sorted_scores[0][0]},{sorted_scores[1][0]}"
    return best

if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    print(route(text))
```

### 4. Token消耗对比

| 指标 | 优化前(全量) | 优化后(分组) | 节省 |
|------|------------|------------|------|
| Skills加载数 | 187 | 15-25 | 87% |
| 上下文token | ~45K | ~6K | **87%** |
| 命中准确率 | 低(选择困难) | 高(精准匹配) | 显著提升 |

### 5. 核心算法来源

| 算法 | 来源项目 | Stars | 核心贡献 |
|------|---------|-------|---------|
| 渐进式披露 | anthropics/skills | 167K | 3阶段加载协议 |
| 语义路由 | xfey/MCP-Zero | 500 | 两阶段server→tool匹配，98%token减少 |
| 工具RAG | RAG-MCP | 论文 | 向量检索top-K，准确率13%→43% |
| 去重合并 | ToolScope | ACL2026 | 图模型合并冗余+重排序 |
| 预设分组 | skills-manager | 3.6K | 场景化批量开关 |
| 安全扫描 | NVIDIA/SkillSpector | 14K | 64种漏洞模式检测 |
| 按需发现 | vercel-labs/skills | 28.5K | 搜索式安装 |
| 图预测 | AutoTool | AAAI2026 | 使用惯性图，省30%推理 |

### 6. 进阶：集成sentence-transformers（可选）

如果需要真正的语义路由（而非关键词），安装：

```bash
pip install sentence-transformers --break-system-packages
```

然后用embedding计算余弦相似度替代关键词匹配。详见：
`~/security-research/re-tools/skill-optimization/ANALYSIS_REPORT.md`

## 关键教训：表格不是路由

预设分组表（markdown表格列出类别和关键词）**不是路由规则**。Agent会把它当作参考信息，不会自动加载对应skill。

**错误做法**（实际部署中验证无效）：
```
| 开发/代码/部署 | development | 代码, 开发, build |
```

**正确做法**（显式指令+skill_view调用）：
```
DEVELOPMENT tasks → MUST skill_view(name='superpowers') FIRST
→ Follow brainstorm → plan → TDD → subagent pipeline
```

规则：每个预设必须有对应的 `MUST skill_view(name='xxx')` 指令，不能只靠表格。

---

## 三层路由架构（2026-08-10 验证有效）

> 详见 [references/three-layer-routing.md](references/three-layer-routing.md)

解决"装了和没装一样"问题的最终方案。三层叠加，覆盖285个skills。

### Layer 1: 硬编码路由（21个核心skill）

注入到 `config.yaml` 的 `system_prompt_append`，格式：
```
DEVELOPMENT/代码/功能 → skill_view(name='superpowers') [236K星]
  触发词: 写代码, 开发, 功能, build, 实现, 修bug
  TDD强制: skill_view(name='tdd-bdd')
  调试流程: skill_view(name='developer-debugging')
```

**每个核心skill必须有明确的 `skill_view(name='xxx')` 调用指令。**

### Layer 2: 类别扫描路由（19个类别）

在同一 system_prompt_append 中，告知 agent 按类别扫描：
```
| 任务类别 | skills_list category | 常见触发场景 |
|----------|---------------------|-------------|
| 安全/渗透/逆向 | red-teaming | 漏洞, 渗透, 逆向 |
| 开发/代码/调试 | software-development | 写代码, 开发, build |
...
```

**关键：告诉 agent "收到消息后先按类别调用 skills_list(category=...)"**

### Layer 3: 意图路由索引（103条精确映射）

最细粒度的路由，格式：
```
写代码→superpowers | 调试→developer-debugging | 审查→code-quality-workflow
渗透→reverse-skill-router+pentest-pipeline | APK→reverse-skill-router
UI→emilkowalski-apple-design+taste-skill | 动画→design-motion-principles
```

**保存为独立文件 `~/.hermes/skills/INTENT-ROUTES.md`，并在 system_prompt_append 中引用。**

### 生成的索引文件

| 文件 | 内容 | 用途 |
|------|------|------|
| `~/.hermes/skills/INTENT-ROUTES.md` | 103条意图→skill映射 | 精确路由参考 |
| `~/.hermes/skills/SKILL-INDEX.md` | 285个skill分类索引 | 全局概览 |
| `~/.hermes/skills/INDEX.json` | 结构化skill数据 | 程序化处理 |

### 验证方法

```python
# 检查覆盖率
import yaml, re
with open("~/.hermes/config.yaml") as f:
    config = yaml.safe_load(f)
append = config['agent']['system_prompt_append']
routed = set(re.findall(r"skill_view\(name='([^']+)'\)", append))
print(f"Routed: {len(routed)}/285 = {len(routed)/285*100:.0f}%")
```

### 效果对比

| 指标 | 优化前 | 优化后 |
|------|--------|--------|
| 显式路由skills | 1 (reverse-skill-router) | 21 + 70 intent refs |
| 类别覆盖 | 1 (security) | 19 categories |
| 命中率 | ~5% (只有安全任务) | ~29% 显式 + 类别发现 |

### Pitfall: system_prompt_append 不要超过8000字符

超过8000字符会挤占上下文窗口。当前最优配置约7500字符。

## Pitfalls

- **预设不要太大** — 每组控制在15-25个skill，超过就拆分
- **关键词路由是轻量方案** — 真正的语义路由需要embedding模型（~500MB）
- **Hermes的skill加载是session级的** — 改了预设需要/reset才生效
- **不要禁用hermes-agent skill** — 它是核心skill，任何预设都要包含
- **安全扫描很重要** — 26.1%的skill有漏洞，5.2%是恶意的
