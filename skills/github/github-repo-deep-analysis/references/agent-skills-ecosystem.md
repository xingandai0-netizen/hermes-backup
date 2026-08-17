# Agent Skills Ecosystem Reference

## What Are Agent Skills?
A standardized format (by Anthropic, now open standard at agentskills.io) for
extending AI agents with reusable procedural knowledge.

Core unit: a folder with `SKILL.md` (metadata + instructions) + optional
`scripts/`, `references/`, `assets/`.

## Key Mechanism: Progressive Disclosure
1. Discovery: agent loads only name + description (cheap)
2. Activation: task matches → full SKILL.md loaded
3. Execution: agent follows instructions, loads resources as needed

This is the same pattern Hermes uses natively.

## Major Repositories (by stars)

| Repo | Stars | What It Is |
|------|-------|------------|
| multica-ai/andrej-karpathy-skills | 191K | Single CLAUDE.md with 4 behavioral principles |
| addyosmani/agent-skills | 78K | 24 production-grade engineering lifecycle skills |
| agentskills/agentskills | 23K | Official specification + documentation |
| anthropics/skills | 153K | Anthropic's official skills collection |
| LambdaTest/agent-skills | 272 | Test automation skills (50+ frameworks) |
| ngrok/agent-skills | 11 | ngrok tunnel skill |

## addyosmani/agent-skills (78K) — The 24 Skills

Lifecycle phases: DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP

Skills by phase:
- Define: interview-me, idea-refine, spec-driven-development
- Plan: planning-and-task-breakdown
- Build: incremental-implementation, context-engineering, source-driven-development, doubt-driven-development, frontend-ui-engineering, test-driven-development, api-and-interface-design
- Verify: browser-testing-with-devtools, debugging-and-error-recovery
- Review: code-review-and-quality, code-simplification, security-and-hardening
- Ship: shipping-and-launch
- Cross-cutting: performance-optimization, observability-and-instrumentation, ci-cd-and-automation, git-workflow-and-versioning, documentation-and-adrs, deprecation-and-migration
- Meta: using-agent-skills

## Installation Patterns

### npx skills CLI (universal)
```bash
npx skills add addyosmani/agent-skills           # all skills
npx skills add addyosmani/agent-skills --skill X  # single skill
```

### Claude Code plugin
```
/plugin marketplace add <owner>/<repo>
/plugin install <name>@<marketplace>
```

### Hermes (our approach)
Clone repo → copy SKILL.md files to `~/.hermes/skills/<category>/<name>/SKILL.md`
Hermes auto-discovers them via skills_list.

## Karpathy's 4 Principles (191K stars — already in our CLAUDE.md)
1. Think Before Coding — don't assume, surface tradeoffs
2. Simplicity First — minimum code, nothing speculative
3. Surgical Changes — touch only what you must
4. Goal-Driven Execution — define success criteria, loop until verified

## Our Integration Status (as of 2026-07-14)
- Karpathy 4 principles: already in CLAUDE.md ✓
- 14 addyosmani skills installed to software-development/ ✓
- Principle 11 added to skills-first-execution-protocol ✓
- Skills map: spec-driven, incremental, context-engineering, source-driven, doubt-driven, code-simplification, api-design, shipping, ci-cd, observability, performance, deprecation, interview-me, idea-refine
