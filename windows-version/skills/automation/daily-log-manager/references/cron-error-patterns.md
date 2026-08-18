# Cron Environment Error Patterns

## execute_code BLOCKED (2026-06-17)

```
BLOCKED: execute_code runs arbitrary local Python (including subprocess calls that bypass shell-string approval checks). Cron jobs run without a user present to approve it. Use normal tools instead, or set approvals.cron_mode: approve only if this cron profile is intentionally trusted.
```

**Trigger**: Any `execute_code` call in cron mode when `approvals.cron_mode` is not set to trust the cron profile.
**Impact**: Cannot use Python sandbox for file operations or data processing.
**Workaround**: Use `write_file`, `read_file`, `search_files` directly. These file tools are NOT blocked by the approval system.

## session_search FTS5 Date Query Failures (2026-06-17)

**Symptom**: `session_search(query="2026-06-17")` returns 0 results even when sessions from that date exist.
**Root cause**: FTS5 tokenizer may not index date strings reliably. Session titles and content may not contain the date string in searchable form.
**Workaround**: Use `session_search(sort="newest", limit=10)` (no query) to browse recent sessions, then check `started_at`/`last_active` timestamps programmatically.

## Cron Tool Availability Matrix (updated 2026-06-17)

| Tool | Status | Notes |
|------|--------|-------|
| write_file | ✅ | Preferred for file creation/updates |
| read_file | ✅ | Reliable file reading |
| search_files | ✅ | File search and listing |
| session_search | ✅ | Primary data source |
| execute_code | ❌ | BLOCKED by approvals system |
| terminal | ❌ | Tirith security scanner blocks |
| memory | ❌ | Disabled in cron config |
| browser_* | ✅ | Available but cannot write local files |
