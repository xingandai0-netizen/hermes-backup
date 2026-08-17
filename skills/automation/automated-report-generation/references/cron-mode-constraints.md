# Cron Mode Constraints

## Security Policy

When running as a Hermes scheduled cron job, the following tools are **blocked** by tirith security:
- `terminal` — all shell commands (even `pwd`)
- `execute_code` — Python execution with subprocess

These return `exit_code: -1` with `status: "pending_approval"` that never resolves (no user present).

### Specific Blocked Patterns (Verified 2026-08-06)

| Pattern | Detection Key | Notes |
|---------|---------------|-------|
| `python3 script.py` | `tirith:unknown` | Direct script execution |
| `python3 -c "code"` | `tirith:unknown` | "script execution via -e/-c flag" |
| `python3 -e "code"` | `tirith:unknown` | Same category as -c |
| `ls -la /path` | `tirith:unknown` | Simple file listing |
| `pwd` | `tirith:unknown` | Even basic commands blocked |
| `cd /path && python3 ...` | `tirith:unknown` | Chained commands |

**Key insight**: The security scan triggers on ANY terminal command in cron mode, regardless of complexity. Even `pwd` is blocked. There is no way to run shell commands or Python scripts from cron jobs.

## Working Tools in Cron Mode

These tools work normally:
- `web_search` — search engine queries
- `web_extract` — fetch and parse web pages
- `write_file` — create/overwrite files
- `patch` — find-and-replace edits
- `read_file` — read existing files
- `search_files` — find files by name/pattern

## Email Simulation Pattern

Without SMTP access (blocked terminal), simulate email delivery by:
1. Reading `data/subscribers.csv` for active subscribers
2. Generating email content (subject, HTML, text) from report data
3. Appending rows to `data/email_log.csv` with `mode=simulated`
4. Each row: `timestamp,email,subject,status,mode`

## Log Rotation

Logs are append-only. Files grow over time. Current log sizes after ~2 months of daily runs:
- `email_log.csv`: ~30 rows
- `system_run.log`: ~40 lines  
- `daily_run.jsonl`: ~80 lines

No rotation implemented yet. Consider periodic cleanup if files exceed 100KB.

## Past Run History

Runs have been successful since at least 2026-06-24 using the fallback pattern.
Last verified: 2026-08-09 (web_extract on github.com/trending + web_search for supplementary data, 12 repos with daily star growth data, 6 investment opportunities, HTML+JSON reports + status + logs all generated via write_file/patch). **New technique**: `web_extract` on `https://github.com/trending` returns richer data than API endpoint (includes daily star growth counts). See `references/github-trending-page-extraction.md`.

## GitHub API via web_extract (Verified 2026-08-06)

Using `web_extract` on GitHub API endpoints works well and returns structured data:
- URL: `https://api.github.com/search/repositories?q=stars:>10000&sort=updated&order=desc&per_page=10`
- Returns: Pre-summarized markdown with table of repos, detailed profiles, and analysis
- Data includes: stars, forks, language, license, description, topics, update timestamps
- **Note**: Content is LLM-summarized by web_extract, so some details may be condensed
- For full JSON data, construct manually from the extracted information

## Web Search Fallback (Verified 2026-08-07)

When web_extract on GitHub API is unavailable or returns poor results, use `web_search` with multiple queries:
1. `web_search("GitHub trending repositories today YYYY Month", limit=5)` — finds aggregator sites
2. `web_search("site:github.com/trending stars:>100000 popular repositories YYYY", limit=5)` — finds GitHub trending page
3. Extract data from sites like `trendsmcp.ai`, `trending.magikaru.com`, `attentionvc.ai` which provide structured trending data with star counts

**Pros**: Gets real-time data from multiple sources, not just GitHub API
**Cons**: Star counts may be approximate, data format varies by source, requires manual extraction from search results

## Cron Job Skill Name Mismatch (Day 70+ as of 2026-08-06)

The cron job references "GitHub Trend Monitor" (with spaces) but the actual skill name is "github-trend-monitor" (with hyphens). This causes the skill to NOT load, wasting 3-5 tool calls per run as the agent tries blocked tools.

**Evidence from 2026-08-06 run**:
```
[IMPORTANT: The following skill(s) were listed for this job but could not be found and were skipped: GitHub Trend Monitor]
```

**Fix**: Update cron job config to use `github-trend-monitor` (hyphens, no spaces).

**Impact**: Each run without the skill wastes ~5 calls testing blocked terminal commands before falling back to web_extract + write_file pattern.

## ⚠️ email_log.csv Warning (CRITICAL)

**NEVER use `write_file` on `data/email_log.csv` without reading existing content first.** This was violated on 2026-08-05, losing all historical email send records. Correct pattern:
1. `read_file("data/email_log.csv")` to get existing content
2. Build new lines
3. `patch` to append after last line (preferred) OR `write_file` with combined old+new content

## Cron Job Config Issue

The cron job references a skill named "GitHub Trend Monitor" which does not exist. It gets skipped every run with:
```
[IMPORTANT: The following skill(s) were listed for this job but could not be found and were skipped: GitHub Trend Monitor]
```
This skill (`automated-report-generation`) should be used instead. The cron config should be updated to reference `automated-report-generation` instead of `GitHub Trend Monitor`.
