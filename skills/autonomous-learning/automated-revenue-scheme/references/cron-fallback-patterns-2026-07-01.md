# Cron Fallback Execution Patterns — 2026-07-01 Session

## Context
Cron job running daily automated tech trend report generation. Terminal and execute_code blocked by `approvals.cron_mode: deny`. All tasks completed successfully using web_search + web_extract + write_file fallback.

## Tools Verified Working in Cron (2026-07-01)

| Tool | Status | Use Case |
|------|--------|----------|
| web_search | ✅ | Search engine queries for trending data |
| web_extract | ✅ | Structured content extraction from URLs (up to 5 per call) |
| read_file | ✅ | Reading existing reports, logs, subscriber lists |
| write_file | ✅ | Writing JSON, HTML, MD report files |
| patch | ✅ | Appending to CSV log files |
| terminal | ❌ | Blocked by approvals.cron_mode: deny |
| execute_code | ❌ | Blocked by approvals.cron_mode: deny |

## Multi-Source Data Aggregation Pattern

### Data Sources Used
1. **github.com/trending** (via web_extract) — daily trending repos with stars-today counts
2. **wangchujiang.com/github-rank/trending-monthly** (via web_extract) — monthly growth data, total stars
3. **repositorystats.com/trending** (via web_search snippets) — growth percentages
4. **ossinsight.io/trending/ai** (via web_search snippets) — AI-specific category trends

### Execution Flow
```
Step 1: web_search × 2 queries (different angles)
  → "GitHub trending repositories today 2026 July"
  → "top GitHub repos stars trending AI machine learning 2026"
  → Returns: URLs + snippets with partial data

Step 2: web_extract × 1 call (2 URLs)
  → github.com/trending (daily data)
  → wangchujiang.com/github-rank/trending-monthly (monthly data)
  → Returns: structured markdown with tables

Step 3: Cross-reference and deduplicate
  → Combine daily stars-today with monthly growth
  → Deduplicate repos across sources
  → Rank by composite signal (daily + monthly + growth %)

Step 4: Generate outputs via write_file
  → trend_data_YYYYMMDD_HHMMSS.json (structured data)
  → trend_report_YYYYMMDD_HHMMSS.html (styled report)
  → system_status_YYYYMMDD.md + .json (operational report)

Step 5: Update logs via patch
  → system_run_log.csv (append new line)
  → run_log.csv (append new line)
  → email_log.csv (append subscriber entries)
```

## Dual-Format Report Generation

### JSON Data Structure
```json
{
  "timestamp": "ISO-8601",
  "report_date": "human-readable",
  "data_sources": ["url1", "url2", ...],
  "summary": { "total_repos": N, "avg_stars": N, "languages": {...}, "investment_opportunities": N },
  "trending_repos": [
    { "rank": N, "name": "owner/repo", "stars": N, "stars_month": N, "language": "...", "description": "...", "category": "...", "investment_signal": "HIGH|MEDIUM|LOW" }
  ],
  "analysis": {
    "top_themes": [{ "theme": "...", "repos": N, "trend": "...", "note": "..." }],
    "investment_opportunities": [{ "name": "...", "reason": "..." }]
  }
}
```

### HTML Report Style
- Dark theme (#0d1117 background, #c9d1d9 text)
- GitHub-inspired color palette (#58a6ff links, #3fb950 success, #f0883e warnings)
- Stats grid, repo list with rank badges, theme cards, investment opportunity cards
- Mobile-responsive with max-width container

## CSV Log Update Pattern

Always read existing CSV before appending to avoid overwriting:
```python
# 1. Read current content
read_file("data/system_run_log.csv")
# 2. Append new entry
patch("data/system_run_log.csv", old_last_line, old_last_line + "\n" + new_entry)
```

## Fix: approvals.cron_mode

The correct config command is:
```bash
hermes config set approvals.cron_mode approve
```
NOT `trust` (incorrect value previously documented in skill).

## Session Stats
- 20 repos analyzed
- 4 data sources aggregated
- 6 investment opportunities identified
- 5 subscribers notified (simulated)
- 6 output files generated
- Execution time: ~2 minutes (within cron window)
