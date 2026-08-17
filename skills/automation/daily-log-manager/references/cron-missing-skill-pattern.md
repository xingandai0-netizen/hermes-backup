# Cron Missing Skill Reference Pattern

**First observed**: 2026-07-01  
**Frequency**: High — affects multiple recurring cron jobs

## Problem

Cron jobs configured with a skill name (e.g., `skill: "GitHub Trend Monitor"`) that doesn't match any installed skill. Every execution outputs:

```
⚠️ Skill(s) not found and skipped: <skill_name>
```

The agent then falls back to executing the task with its own capabilities, which usually works but is suboptimal (no skill-specific pitfalls, templates, or reference docs loaded).

## Observed Cases (2026-07-01)

| Cron Job Title | Missing Skill Name | Fallback Behavior |
|---|---|---|
| GitHub Trend Monitor (×3 daily) | `GitHub Trend Monitor` | Uses web_extract + write_file directly |
| Auto Tech Trend Revenue System | `GitHub Trend Monitor` | Same fallback |
| AI行业3天热点报道 | (none — skill `follow-builders-digest` loaded correctly) | N/A |

## Detection During Log Review

When scanning session content for daily log compilation, look for:
- `"Skill(s) not found and skipped"` in any session snippet
- `"⚠️ Skill"` in assistant responses

If found, add to the daily log's **下一步待执行** section:
- The cron job name/ID (from session title)
- The missing skill name
- Recommended action: verify correct skill name via `skills_list`, update cron config

## Root Cause

The skill name in the cron config doesn't match the actual skill directory name. Common causes:
- Skill was renamed but cron config wasn't updated
- Skill was deleted/consolidated into another skill
- Typo or casing mismatch in the cron config

## Fix

```bash
# Check available skills
hermes skills list | grep -i "<partial_name>"

# Update cron job's skill reference
hermes cron edit <job_id> --skill "<correct_skill_name>"
```

## Why It Matters

When the skill loads correctly, the agent gets:
- Pitfall documentation (avoiding known failures)
- Reference files (API patterns, templates)
- Correct execution sequence
- Environment-specific workarounds

Without the skill, the agent operates blind — it may repeat documented pitfalls or miss established fallback chains.
