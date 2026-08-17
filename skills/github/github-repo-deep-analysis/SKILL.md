---
name: github-repo-deep-analysis
version: 1.0.0
description: "Deep analysis of a single GitHub repository - architecture extraction, pattern recognition, and integration opportunity identification. Goes beyond surface README reading to understand design principles, implementation patterns, and applicability to existing systems."
keywords: [github, repository-analysis, architecture, code-review, pattern-extraction, deep-dive]
author: Xiao Hei
---

# GitHub Repository Deep Analysis

## When to Use

Use this skill when you need to:
- **Truly understand** a repository (not just read the README)
- Extract **architectural patterns** and **design principles**
- Assess **integration opportunities** with existing systems
- Learn from **implementation details** in source code
- Compare approaches with **alternative solutions**

## Two Research Modes

### Quick Research Mode (no clone needed)
For调研/overview tasks where you need to understand what a project is,
compare it with alternatives, and assess value — but don't need to read
source code line by line:

1. `web_search` for the repo name → find the main GitHub URL + related repos
2. `web_extract` on the GitHub README page → get full description
3. `web_search` for comparisons, alternatives, ecosystem context
4. Compile report with: overview, features, architecture, comparison, recommendation

This covers 80% of research tasks. Only clone when you need to:
- Read actual source code implementation details
- Install/extract files (skills, configs, code)
- Run tests or build the project

### Deep Analysis Mode (clone required)
Use the full workflow below when Quick Research isn't enough.

## The Deep Analysis Workflow

### Phase 1: Repository Discovery & Selection

**Handle Forks and Variants:**
```bash
# Search for all related repositories
curl -s "https://api.github.com/search/repositories?q=<topic>" | \
  jq -r '.items[] | "\(.full_name): \(.description)"'
```

**Selection Criteria:**
1. **Most stars** is NOT always best - check maintenance
2. **Original vs Fork**: Prefer original unless fork has significant improvements
3. **Recent activity**: Last commit within 3 months
4. **Documentation quality**: README is just the start

### Phase 2: Systematic File Reading

**Read in This Order:**

1. **README.md** - Surface understanding
2. **docs/** or **wiki/** - Deep documentation
3. **package.json / Cargo.toml / requirements.txt** - Dependencies reveal architecture
4. **src/** or **lib/** - Core implementation
5. **tests/** - Usage patterns
6. **examples/** - Real-world application

**What to Extract:**
```markdown
## Architecture Notes
- **Core Pattern**: [e.g., Event Sourcing, CQRS, Layered]
- **Key Abstractions**: [List main interfaces/modules]
- **Data Flow**: [How does input become output?]
- **Extension Points**: [Where can users hook in?]

## Design Decisions
- **Trade-offs Made**: [What did they sacrifice for what gain?]
- **Philosophy**: [Unix philosophy? Batteries included?]

## Integration Opportunities
- **Similar to**: [Our existing systems]
- **Can Replace**: [Current solutions]
- **Complements**: [What we should keep]
```

### Phase 3: Architecture Extraction

**Draw the Architecture:**
```
┌─────────────────────────────────────┐
│           [System Name]              │
├─────────────────────────────────────┤
│  Layer 1 │ Layer 2    │ Layer 3     │
│  [Name]  │ [Name]     │ [Name]      │
│          │            │             │
│  ┌───┐   │   ┌───┐    │    ┌───┐    │
│  │ A │───┼──→│ B │────┼───→│ C │    │
│  └───┘   │   └───┘    │    └───┘    │
└──────────┴────────────┴─────────────┘
```

**Identify Patterns:**
- **Creational**: Factory, Builder, Singleton?
- **Structural**: Adapter, Bridge, Composite?
- **Behavioral**: Observer, Strategy, Command?

### Phase 4: Comparison & Integration

**Compare with Existing Systems:**

| Aspect | Current System | New Repository | Winner |
|--------|---------------|----------------|--------|
| Performance | [X] | [Y] | ? |
| Flexibility | [X] | [Y] | ? |
| Complexity | [X] | [Y] | ? |
| Maturity | [X] | [Y] | ? |

**Integration Strategy:**
1. **Direct Replacement**: Drop-in substitute?
2. **Hybrid Approach**: Use both selectively?
3. **Incremental Adoption**: Gradual migration?
4. **Pass**: Not worth the switching cost?

## Output Format

```markdown
# Deep Analysis: [Repository Name]

## Executive Summary
[2-3 sentences on what this is and why it matters]

## Architecture Deep Dive
### Core Components
[Detailed breakdown]

### Data Flow
[How information moves through the system]

### Design Patterns
[What patterns are used and why]

## Key Insights
### What Works Well
[Strengths]

### Limitations
[Weaknesses and trade-offs]

### Surprising Discoveries
[Non-obvious findings from source code]

## Integration Assessment
### Compatibility with Our Systems
[How well it fits]

### Migration Path
[If we were to adopt it, how would we do it?]

### Recommendation
[Adopt / Consider / Pass]

## Resources
- [Links to key files, docs, related projects]
```

## Common Pitfalls

1. **Stopping at README**: The real insights are in the source code
2. **Ignoring tests**: Tests reveal usage patterns and edge cases
3. **Not checking dependencies**: `package.json` reveals architectural choices
4. **Skipping git history**: Recent commits show project health
5. **No comparison**: Without comparing to alternatives, you can't assess value
6. **execute_code sandbox isolation**: `read_file` inside `execute_code` scripts runs in an isolated sandbox — it CANNOT access files on the host filesystem. When you need to process files from a cloned repo, use `terminal` commands (cp, cat, etc.) instead of execute_code's read_file/write_file.
7. **Cloning for research-only tasks**: Don't clone a repo just to read its README. web_extract on the GitHub URL gives you the full content faster and cheaper. Only clone when you need to copy/install files or read source code that web_extract truncates.

## Success Criteria

You've done a deep analysis when you can:
- [ ] Explain the architecture without looking at the code
- [ ] Identify the key design trade-offs
- [ ] Compare it to 2+ alternatives
- [ ] Make a concrete adoption recommendation
- [ ] Anticipate integration challenges

---

*This skill transforms surface-level repository browsing into deep architectural understanding.*