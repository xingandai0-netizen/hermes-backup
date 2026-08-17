# NEXUS Enforcement Rules (2026-08-11)

## Mandatory for ALL Engineering Tasks

When receiving any engineering task (code, UI, system changes, feature implementation):

1. **Load agency-agents**: `skill_view(name='agency-agents')` — get role definitions
2. **Classify task**: Determine which roles needed
3. **Delegate**: `delegate_task(tasks=[...])` with batch mode (max 3 parallel)
4. **Verify**: Reality Checker + Evidence Collector must approve

## Role Selection Quick Reference

| Task Type | Required Roles |
|-----------|---------------|
| Frontend work | Frontend Developer + Evidence Collector |
| Backend/API | Backend Architect + Security Engineer |
| Full stack | Frontend + Backend + Reality Checker |
| Security review | Security Engineer + Evidence Collector |
| Deployment | DevOps Automator + Reality Checker |
| Any feature | PM analysis + Dev + QA (minimum 3 roles) |

## Execution Template

```python
delegate_task(tasks=[
    {
        "goal": "[Role] task: [specific goal]",
        "context": "[full task details, files, constraints]",
        "toolsets": ["terminal", "file"],
        "role": "leaf"
    },
    {
        "goal": "[Role] task: [specific goal]",
        "context": "[full task details]",
        "toolsets": ["terminal", "browser", "vision"],
        "role": "leaf"
    }
])
```

## Forbidden Patterns
- Single agent doing code + test (must split roles)
- Skipping PM analysis even for "obvious" tasks
- Using delegate_task inside a sub-agent (max_spawn_depth=1)
- Reporting done without Reality Checker PASS
- Evidence without actual screenshots (HTML analysis is NOT evidence)

## Reality Checker Protocol
- Default verdict: NEEDS WORK
- PASS requires: overwhelming evidence (screenshots, test results, build output)
- First implementation usually needs 2-3 rounds of fixes
- C+/B- is normal; A+ is fantasy
