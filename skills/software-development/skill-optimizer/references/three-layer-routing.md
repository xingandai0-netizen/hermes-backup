# Three-Layer Routing Architecture

**Status**: Deployed 2026-08-10, verified 280/282 coverage (99.3%)

## Layer 1: Hardcoded Routing (21 core skills)

In `~/.hermes/config.yaml` → `agent.system_prompt_append`:

```
开发: 写代码→superpowers | 调试→developer-debugging | 审查→code-quality-workflow | 测试→tdd-bdd
安全: 渗透→reverse-skill-router+pentest-pipeline | 逆向→re-toolkit-mcp | 赏金→malicious-project-bounty-research
设计: UI→emilkowalski-apple-design+taste-skill | 动画→design-motion-principles
产品: PRD→pm-skills-77 | 竞品→competitive-analysis-process
```

Each has explicit `skill_view(name='X')` call. Loaded every time.

## Layer 2: Category Scanning (19 categories)

Same system_prompt_append, tells agent to call `skills_list(category=...)`:

| Category | Trigger |
|----------|---------|
| red-teaming | 渗透, 漏洞, 逆向 |
| software-development | 代码, 开发, build |
| design | 设计, UI, UX |
| productivity | 产品, PRD, 办公 |
| creative | 创作, 图片, 音乐 |
| security | 恶意项目, 赏金 |
| + 13 more | ... |

## Layer 3: Intent Routing (237 intents → 280 skills)

Condensed in system_prompt_append, full index in `~/.hermes/skills/INTENT-ROUTES.md`.

Format: `中文意图→skill-name` or `中文意图→skill1+skill2`

## Verification Script

```python
import yaml, os
config = yaml.safe_load(open(os.path.expanduser('~/.hermes/config.yaml')))
append = config['agent']['system_prompt_append']
skills_dir = os.path.expanduser('~/.hermes/skills')
local = set()
for r, d, f in os.walk(skills_dir):
    if 'SKILL.md' in f:
        local.add(os.path.basename(os.path.dirname(os.path.join(r, 'SKILL.md'))))
sub = {'brainstorming','writing-plans','subagent-development','tdd','systematic-debugging','finishing-branch','skill-card'}
target = local - sub
hit = sum(1 for s in target if s in append)
print(f"Coverage: {hit}/{len(target)} = {hit/len(target)*100:.1f}%")
```

## Pitfalls

- **Tables are NOT routing** — agent ignores markdown tables, only follows MUST instructions
- **system_prompt_append limit** — keep under 8000 chars to avoid context window pressure
- **100% or bust** — user explicitly requires complete coverage before reporting done
- **grep to verify** — always confirm skill name appears in config.yaml after editing
