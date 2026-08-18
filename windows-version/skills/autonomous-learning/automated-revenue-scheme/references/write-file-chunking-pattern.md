# Write-File Chunking Pattern (Verified 2026-06-30)

## Problem
`write_file` with large content (~6K+ tokens) causes stream timeout in cron/unattended mode.
The tool call appears to execute but the stream stalls before delivery.

## Solution: Multi-pass construction
Build large files incrementally using write_file + patch:

### Step 1: Write skeleton with write_file
Write just the header/CSS/structure (under 3K tokens):
```python
write_file(path="/abs/path/report.html", content="<html><head>...<style>...</style></head><body><header/></body></html>")
```

### Step 2-N: Append sections with patch
Use `mode='replace'` to find the closing tags and insert content before them:
```python
patch(mode='replace', path="/abs/path/report.html",
      old_string="</body>\n</html>",
      new_string="<div class='section'>...</div>\n</body>\n</html>")
```

### Final: Close the document
The last patch replaces the placeholder closing with real closing + footer content.

## Verified working (2026-06-30 cron run)
- HTML report: 3 write_file + 3 patch calls = complete 166-line report
- JSON report: single write_file (small enough)
- CSV logs: single write_file (small enough)
- Each tool call: under 3K tokens content

## When to use
- Any file generation in cron/unattended mode
- Reports with 10+ items to render
- Files exceeding ~150 lines of content
- HTML templates with CSS + dynamic data

## Anti-patterns
- ❌ Single write_file with 200+ lines of HTML → stream timeout
- ❌ Building entire file in execute_code then writing → execute_code blocked in cron
- ✅ Incremental write_file + patch → reliable delivery
