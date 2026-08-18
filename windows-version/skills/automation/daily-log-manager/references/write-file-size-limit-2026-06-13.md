# write_file Size Limit in Cron Mode — 2026-06-13

## Problem
When writing daily logs via `write_file`, the content can exceed the cron stream delivery limit (~8K tokens). This causes the tool call to hang until timeout, and the system intervenes with:

> "Your previous tool call (write_file) was too large and the stream timed out before it could be delivered. Do NOT retry the same tool call with the same large content. Instead, break the content into multiple smaller tool calls."

## Triggering Condition
- Daily log with 10+ table rows, detailed task descriptions, and multiple sections
- Content > ~3000 characters (rough threshold, varies with token encoding)
- First attempt wrote 2.5KB successfully; a larger earlier attempt (~6KB+) failed

## Solution: Write Concise, Not Exhaustive

### ❌ What NOT to do
- Copy full session summaries into the log (session_search already stores these)
- Include complete trend data tables with all columns
- Write verbose task descriptions with every step documented
- Repeat the same data in multiple formats (table + bullets + prose)

### ✅ What TO do
- **Summarize in bullets** — 3-5 key points per task, not paragraphs
- **Tables: top 3-5 rows max** — full data stays in session_search or dedicated output files
- **One-line task entries** — `时间 | 任务名 | 结果 | 输出文件路径`
- **Pointer pattern** — reference output files by path, don't inline their content
- **Compress the day** — a light day (1-2 cron sessions) should be < 2KB

### Size Budget (approximate)
| Section | Target Size |
|---------|-------------|
| Header + metadata | 100 chars |
| Task entries (per task) | 200-400 chars |
| Communication summary | 100-200 chars |
| Next steps | 100-200 chars |
| Notes | 100-200 chars |
| **Total target** | **< 2500 chars** |

## Verification
After `write_file`, check `dirs_created` or `files_modified` in the response. If absent, the write likely timed out.
