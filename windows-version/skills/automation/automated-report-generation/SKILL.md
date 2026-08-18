---
name: automated-report-generation
description: Generate automated reports (JSON + HTML) via web scraping when terminal/execute_code are blocked. Covers cron-mode fallback, large-file chunking, multi-format output, pointer management, and run logging.
triggers:
  - automated report generation
  - cron job report
  - tech trend report
  - GitHub trending report
  - scheduled report
  - web scrape and generate report
  - terminal blocked fallback
---

# Automated Report Generation

Generate structured reports by scraping web data when Python scripts or terminal commands are unavailable (e.g. cron mode security policy blocking `terminal` and `execute_code`).

## When to Use

- Scheduled cron jobs that need to generate daily/weekly reports
- Python scripts exist but can't execute (security policy, missing deps, etc.)
- Need to produce JSON data + HTML report + logs from web sources
- Large output files that risk stream timeouts

## Workflow

### Step 1: Collect Data via Web Tools

**Preferred: GitHub Trending Page** (see `references/github-trending-page-extraction.md`):
```
web_extract(urls=["https://github.com/trending"])  # Ranks + daily star growth ⭐
```
Returns repo name, description, language, total stars, AND daily growth — richer than the API endpoint.

**Multi-page enrichment (recommended)**: Fetch language-specific pages in one call for broader coverage:
```python
# execute_code approach (non-cron contexts):
from hermes_tools import web_extract
result = web_extract(urls=[
    "https://github.com/trending",
    "https://github.com/trending/python",
    "https://github.com/trending/typescript"
])
```
This yields 15-20 unique repos vs ~8 from the main page alone. Dedup by repo name in post-processing.

**Fallback: GitHub Search API**:
```
web_extract(urls=["https://api.github.com/search/repositories?q=stars:>500&sort=updated&order=desc"])
```

**Discovery: web_search**:
```
web_search(query="GitHub trending repositories today", limit=5)
```
Use to find third-party aggregators (trendshift.io, attentionvc.ai, etc.) for cross-referencing.

**⚠️ execute_code availability**: `execute_code` is NOT blocked in all cron jobs — only in jobs running under Tirith security scan. Many cron jobs run with full tool access. Try `execute_code` first; fall back to `web_extract` + `write_file` only if blocked. (Confirmed 2026-08-16: cron job successfully used `execute_code` with `hermes_tools` for full data pipeline.)

- Use `web_search` first to find data sources
- Use `web_extract` on structured pages (GitHub trending page, APIs, dashboards)
- Extract into structured Python dicts/lists in your head

### Step 2: Generate JSON Data File

Write structured data as JSON. Keep the file **under 5KB** — if larger, split into a main file + supplementary files.

```
write_file(path="reports/trend_data_YYYYMMDD_HHMMSS.json", content=...)
```

### Step 3: Generate HTML Report (CHUNKED)

**⚠️ CRITICAL: HTML reports must be written in chunks to avoid stream timeouts.**

1. **Write the HTML shell** (head, styles, first section) via `write_file`. Keep under ~5KB.
2. **Patch in remaining sections** via `patch(mode='replace')` — replace placeholder comments like `<!-- PART 2 CONTINUES -->` with actual content.
3. Each patch call should add **one section** (e.g., Top 10 repos, language distribution, insights).

Example:
```python
# Step 3a: Write shell with first 5 repos
write_file(path="report.html", content=html_shell_with_placeholder)

# Step 3b: Patch in remaining repos + sections
patch(mode='replace', path="report.html",
      old_string="<!-- PART 2 CONTINUES -->",
      new_string=remaining_repos_html + insights_html + footer_html)
```

### Step 4: Update Pointer Files

Update "latest" pointer files so they always point to today's report:

```
write_file(path="reports/latest_data.json", content=minimal_json_summary)
write_file(path="reports/latest_report.html", content=redirect_html)
```

The redirect HTML:
```html
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Latest</title></head>
<body>
<script>window.location.href='report_YYYYMMDD.html';</script>
<p>Redirecting to <a href="report_YYYYMMDD.html">today's report</a></p>
</body></html>
```

### Step 5: Update Logs

Update **all** of these:

| Log File | Format | Update Method |
|----------|--------|---------------|
| `data/email_log.csv` | CSV rows | **⚠️ MUST read_file first, then patch append. NEVER write_file without reading — loses all history (confirmed 2026-08-05).** |
| `data/system_run.log` | Markdown entries | `patch` append after last entry |
| `data/daily_status_report.md` | Full status report | `write_file` overwrite |
| `logs/daily_run.jsonl` | JSONL entries | `patch` append after last entry |

**⚠️ For `system_run.log`**: The string `- Status: ✅ SUCCESS` appears multiple times. Use a longer unique context string (include the preceding `Method:` line) to avoid ambiguity in patch.

### Step 6: Simulate Email Delivery

If no real SMTP is configured, log emails as "simulated":

```csv
2026-07-24T09:00:00,user@example.com,Report Subject,sent,simulated
```

## Pitfalls

1. **Stream timeout on large files**: HTML reports >~8KB in a single `write_file` risk stream timeouts. The system will reject with "too large and the stream timed out." Safe limit is ~5KB per write. If you must write larger, split: `write_file` for shell+first section, then `patch` for each additional section. Writing 7-8KB *can* work but is unreliable — chunk at 5KB to be safe. (Confirmed 2026-08-07: a ~12KB write timed out, but two 7.8KB writes succeeded.)
2. **Patch ambiguity**: When appending to logs, use enough unique context to avoid matching multiple locations.
3. **Pointer file format**: `latest_report.html` should be a simple redirect, not the full report.
4. **Cron mode**: `terminal` and `execute_code` are blocked in cron jobs (tirith security). Always use `web_search` + `web_extract` + `write_file` + `patch`.
5. **JSON data size**: Keep `latest_data.json` minimal (~1KB). Full data goes in the timestamped file.
6. **⚠️ CRITICAL: email_log.csv is append-style** — NEVER use `write_file` on email_log.csv without reading the existing content first. `write_file` overwrites everything. Correct pattern: `read_file` the full CSV → build new lines → `patch` to append after last line. OR: `read_file` → `write_file` with combined old+new content. Violating this loses ALL historical email send records (confirmed 2026-08-05 — all prior entries lost).
7. **Pointer files should be minimal** — `latest_report.html` should be a simple redirect HTML (~200 bytes), NOT a full copy of the report. `latest_data.json` should be a summary (~1KB), NOT the full dataset. Writing full copies wastes tokens and risks stream timeouts.
8. **Patch context uniqueness** — When appending to log files via `patch`, the `old_string` must be unique in the file. If the last line appears multiple times (e.g., same status string repeated), include more surrounding context (2-3 lines) to make it unique. `patch` fails with "Found N matches" if ambiguous. (Confirmed 2026-08-07: patch on "stats-grid" class failed due to 2 matches, had to use longer context.)
9. **⚠️ CRITICAL: `read_file` returns `N|content` format** — Every line is prefixed with its line number and a pipe (`1|<!DOCTYPE html>`). When reconstructing/copying a file by reading it and writing elsewhere, you MUST strip these prefixes. Naive `read_file` → `write_file` copies will produce corrupt files with line numbers embedded in the content. Safe pattern: read the file, manually reconstruct the content from memory/template, then `write_file`. Or use `execute_code` with `read_file()` from hermes_tools to programmatically strip prefixes — but note `execute_code` is also blocked in cron mode. (Confirmed 2026-08-11: attempted file copy via read_file → write_file, realized line numbers would contaminate output.)
10. **Token cost of full-file "copies"** — When terminal is blocked, the only way to "copy" a file is `read_file` + `write_file`, which doubles token usage. For large HTML reports (~14KB), this is expensive. **Always use the redirect-HTML pattern for `latest_report.html`** (see Step 4). Don't write the full report twice. (Confirmed 2026-08-11: wrote 14KB HTML to both `trend_report_20260811.html` AND `latest_report.html` — wasteful.)

## File Structure

```
reports/
  trend_data_YYYYMMDD_HHMMSS.json    # Full data
  trend_report_YYYYMMDD_HHMMSS.html  # Full HTML report
  latest_data.json                    # Pointer (minimal)
  latest_report.html                  # Redirect pointer
data/
  daily_status_report.md             # Overwritten each run
  email_log.csv                      # Appended each run
  system_run.log                     # Appended each run
logs/
  daily_run.jsonl                    # Appended each run
```
