# Config Verification Commands

## Critical Discovery (2026-08-11)

**Problem:** `system_prompt_append` was EMPTY (0 chars) despite previous sessions claiming successful writes. The "99.3% coverage" claim was incorrect.

**Root Cause:** Either:
1. Write was blocked by security scanning but session reported success
2. Config was overwritten/cleared at some point
3. Write succeeded but config was later reset

**Lesson:** NEVER trust a previous session's "completed" report. ALWAYS verify actual config content at the start of each session.

## Quick Verification Commands

### Check system_prompt_append status
```bash
python3 -c "
import yaml
config = yaml.safe_load(open('$HOME/.hermes/config.yaml'))
append = config.get('agent', {}).get('system_prompt_append', '')
print(f'System prompt: {len(append)} chars')
for marker in ['skill_view', 'skills_list', 'SKILL ROUTING', 'CATEGORY ROUTING', 'NEXUS']:
    count = append.count(marker)
    print(f'  {marker}: {count} occurrences')
"
```

### Check specific skill routing
```bash
python3 -c "
import yaml
config = yaml.safe_load(open('$HOME/.hermes/config.yaml'))
append = config.get('agent', {}).get('system_prompt_append', '')
skills_to_check = ['superpowers', 'tdd-bdd', 'reverse-skill-router', 'agency-agents']
for skill in skills_to_check:
    found = skill in append
    print(f'  {\"✅\" if found else \"❌\"} {skill}')
"
```

### Full deployment audit
```bash
python3 -c "
import yaml, os
config = yaml.safe_load(open(os.path.expanduser('~/.hermes/config.yaml')))
append = config.get('agent', {}).get('system_prompt_append', '')
print(f'Config size: {len(append)} chars')
print(f'Contains skill_view: {\"skill_view\" in append}')
print(f'Contains skills_list: {\"skills_list\" in append}')
if len(append) == 0:
    print('⚠️ WARNING: system_prompt_append is EMPTY - all routing is missing!')
    print('Action: Must re-write skills routing config')
"
```

## If system_prompt_append is Empty

1. **Do NOT trust previous session reports** - they may be stale
2. **Re-write the routing config** using `skill_manage(action='patch')` or `terminal` with python3
3. **Verify after write** using the commands above
4. **Inform user** that a new conversation is needed for changes to take effect

## Hermes Config Behavior

- `system_prompt_append` is read ONCE at conversation start
- Changes require a NEW conversation to take effect
- This is NOT a feature we built - it's Hermes's inherent mechanism
- `grep` on config.yaml may match comments or empty lines - use python3 to verify actual content
