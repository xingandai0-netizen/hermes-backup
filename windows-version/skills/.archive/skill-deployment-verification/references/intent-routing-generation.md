# Intent Routing Index Generation

## When to Generate
When skill count > 50 and hardcoded routing can't cover everything.

## Methodology

### Step 1: Build skill index
```python
import os, json
skills_dir = "/Users/macpro/.hermes/skills"
all_skills = []
for root, dirs, files in os.walk(skills_dir):
    if 'SKILL.md' in files:
        name = os.path.basename(os.path.dirname(os.path.join(root, 'SKILL.md')))
        with open(os.path.join(root, 'SKILL.md'), 'r') as f:
            content = f.read()
        # Extract description from YAML frontmatter
        desc = ""
        for line in content.split('\n'):
            if line.strip().startswith('description:'):
                desc = line.split('description:', 1)[1].strip().strip('"')[:120]
                break
        all_skills.append({'name': name, 'desc': desc})
# Save
with open(os.path.join(skills_dir, 'INDEX.json'), 'w') as f:
    json.dump(all_skills, f, ensure_ascii=False, indent=2)
```

### Step 2: Generate intent routes
Group skills by domain/use-case, create intent→skill mappings:
```
写代码→superpowers | 调试→developer-debugging | 渗透→reverse-skill-router
```

### Step 3: Write INTENT-ROUTES.md
```python
with open(os.path.join(skills_dir, 'INTENT-ROUTES.md'), 'w') as f:
    f.write(f"# Skills Intent Routing Index\n# {len(routes)} intent patterns\n\n")
    for intent, skills in routes.items():
        f.write(f"- {intent} → {', '.join(skills)}\n")
```

### Step 4: Inject condensed version into system_prompt_append
- Max ~150 lines grouped by domain
- Format: `领域: 意图→skill | 意图→skill`
- Reference full file: `完整索引: ~/.hermes/skills/INTENT-ROUTES.md`

## Coverage Verification Pitfall
**Don't use regex to verify skill name presence in YAML strings.**
YAML escaping (`\\n`, `\\`, quotes) causes false negatives.

**Correct approach:**
```python
# Simple string-in-string check, NOT regex
for skill_name in all_skills:
    if skill_name in config_yaml_string:
        covered += 1
```

This gives accurate coverage because skill names are unique enough to not false-match.

## YAML Quoting Pitfall
When injecting text into `system_prompt_append` (a YAML quoted string):
- **Don't** use raw Python string manipulation + yaml.dump (reformats entire file)
- **Don't** insert literal newlines into a single-quoted YAML value
- **Do** use `\\n` for newlines within the quoted string
- **Do** use `hermes config set` for simple values
- **Do** test with `yaml.safe_load()` after ANY edit
