# Hermes Integration Opportunity Analysis

## Technique (Verified 2026-08-16)

When analyzing trending repos for Hermes integration potential, use this classification framework.

## Integration Categories

| Category | Description | Example |
|----------|-------------|---------|
| **MCP Server** | Expose repo's functionality as Hermes MCP tool | SpiderFoot for OSINT |
| **Skill Candidate** | Repo's core pattern becomes a Hermes skill | Unsloth for fine-tuning |
| **CLI Wrapper** | Wrap CLI tool as Hermes terminal tool | CLI-Anything pattern |
| **Subagent Target** | Use as delegate_task target for specialized work | FreeBuff for coding |
| **Architecture Reference** | Pattern informs Hermes architecture decisions | ai-memory for cross-agent handoff |
| **Content Pipeline** | Automate content creation workflows | MoneyPrinterTurbo for video |

## Priority Classification

- **HIGH PRIORITY**: Direct integration with Hermes core (memory, agent loop, architecture)
- **MEDIUM PRIORITY**: Skill creation or MCP server opportunity
- **LOW PRIORITY**: Monitoring only, niche use case

## Keyword Signals for Integration Potential

High-signal keywords in descriptions:
- `agent`, `mcp`, `api`, `cli`, `tool`, `automation`, `workflow` → integration candidate
- `llm`, `model`, `fine-tune`, `inference` → MLOps skill candidate
- `memory`, `handoff`, `cross-vendor` → core Hermes improvement
- `security`, `osint`, `pentest` → red team skill suite
- `video`, `content`, `social` → content creation pipeline

## Output Format

Each analyzed repo should include:
```json
{
  "hermes_integration": true/false,
  "hermes_opportunity": "Brief description of integration value",
  "integration_category": "mcp|skill|cli|subagent|reference|pipeline",
  "priority": "high|medium|low"
}
```

## Deduplication

When fetching multiple trending pages, dedup by `owner/repo` name. Keep the entry with the most detailed metadata (prefer main trending page over language-specific pages).
