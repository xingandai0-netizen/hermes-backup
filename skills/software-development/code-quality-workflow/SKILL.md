---
name: code-quality-workflow
description: "Code quality gates and cleanup: pre-commit verification (security scan, tests, independent reviewer) and post-change simplification (parallel 3-agent review for reuse, quality, efficiency)."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [code-review, security, verification, quality, pre-commit, cleanup, simplify, refactor]
    related_skills: [test-driven-development, plan, subagent-driven-development, systematic-debugging]
---

# Code Quality Workflow

Two complementary quality processes — one runs **before commit** (verification gate), the other **after changes** (cleanup pass).

---

## Part 1: Pre-Commit Verification

> Merged from `requesting-code-review` (archived 2026-06-21).

Automated verification pipeline before code lands. Static scans, baseline-aware quality gates, an independent reviewer subagent, and an auto-fix loop.

**Core principle:** No agent should verify its own work. Fresh context finds what you miss.

### When to Use
- After implementing a feature or bug fix, before `git commit` or `git push`
- When user says "commit", "push", "ship", "done", "verify", or "review before merge"
- After completing a task with 2+ file edits in a git repo

**Skip for:** documentation-only changes, pure config tweaks, or when user says "skip verification".

### Step 1 — Get the diff
```bash
git diff --cached   # or git diff / git diff HEAD~1 HEAD
```

### Step 2 — Static security scan (added lines only)
```bash
# Hardcoded secrets
git diff --cached | grep "^+" | grep -iE "(api_key|secret|password|token|passwd)\s*=\s*['\"][^'\"]{6,}['\"]"
# Shell injection
git diff --cached | grep "^+" | grep -E "os\.system\(|subprocess.*shell=True"
# SQL injection
git diff --cached | grep "^+" | grep -E "execute\(f\"|\.format\(.*SELECT"
```

### Step 3 — Baseline tests and linting
Detect project language, run appropriate tools. Capture baseline failures BEFORE changes. Only NEW failures block commit.

### Step 4 — Self-review checklist
- No hardcoded secrets
- Input validation on user data
- SQL queries parameterized
- File operations validate paths
- External calls have error handling
- No debug prints left behind

### Step 5 — Independent reviewer subagent
```python
delegate_task(
    goal="Independent code review. Return ONLY valid JSON with passed/security_concerns/logic_errors/suggestions/summary.",
    context="Review git diff. security_concerns non-empty → passed=false. logic_errors non-empty → passed=false.",
    toolsets=["terminal"]
)
```

### Step 6 — Evaluate & Step 7 — Auto-fix loop (max 2 cycles)
Spawn a third agent to fix reported issues, then re-verify.

### Step 8 — Commit
```bash
git add -A && git commit -m "[verified] <description>"
```

---

## Part 2: Post-Change Simplification

> Merged from `simplify-code` (archived 2026-06-21).

Review recent code changes with three focused reviewers running in parallel, aggregate findings, and apply fixes.

**Core principle:** Three narrow reviewers beat one broad reviewer.

### When to Use
- User says "simplify" / "simplify my changes" / "clean up my changes"
- Optional modifiers: focus on `reuse`/`quality`/`efficiency`, dry run, scope to specific files

### Phase 1 — Identify changes
```bash
git diff              # default: working-tree changes
git diff HEAD         # include staged
git diff HEAD~1       # last commit
git diff main...HEAD  # this branch
```

### Phase 2 — Launch three reviewers in parallel
Use `delegate_task` batch mode with `terminal`, `file`, `search` toolsets.

**Reviewer 1 — Code Reuse:** Find duplicate functionality, existing utilities the new code could call instead.

**Reviewer 2 — Code Quality:** Redundant state, parameter sprawl, copy-paste-with-variation, leaky abstractions.

**Reviewer 3 — Efficiency:** Unnecessary work, missed concurrency, hot-path bloat, TOCTOU anti-patterns, memory issues.

### Phase 3 — Aggregate and apply
1. Merge findings, dedup
2. Discard false positives
3. Resolve conflicts: correctness > user's stated focus > readability > micro-perf
4. Apply surviving fixes
5. Verify tests still pass
6. Summarize changes

---

## Integration

- **With TDD:** Run verification after each TDD cycle. The pipeline verifies TDD discipline was followed.
- **With subagent-driven-development:** Run verification after each task as the quality gate.
- **With plan:** Validates implementation matches plan requirements.

## Pitfalls
- **Empty diff** — check `git status`, tell user nothing to verify
- **Large diff (>15k chars)** — split by file, review each separately
- **delegate_task returns non-JSON** — retry once with stricter prompt, then treat as FAIL
- **Don't fan out wider than ~3 reviewers** — more means more cost and conflicting suggestions
- **Give the WHOLE diff to each reviewer** — splitting defeats the design
- **Apply ≠ rewrite** — keep edits scoped to what the diff touched
