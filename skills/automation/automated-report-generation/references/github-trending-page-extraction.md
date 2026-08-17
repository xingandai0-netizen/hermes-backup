# GitHub Trending Page Extraction via web_extract

## Technique (Verified 2026-08-09)

Extract data directly from `https://github.com/trending` using `web_extract`. This is **richer** than the GitHub Search API endpoint because it includes daily star growth counts.

### Why Use This Over the API

| Feature | `github.com/trending` (web_extract) | API endpoint (web_extract) |
|---------|--------------------------------------|---------------------------|
| Daily star growth | ✅ "+N stars today" | ❌ Only total stars |
| Trending rank order | ✅ Ranked by daily activity | ❌ Sorted by total stars/updated |
| No API rate limits | ✅ Page scraping | ⚠️ 10 req/min |
| Sponsor detection | ✅ Marked as "Sponsor" | ❌ Not indicated |
| Language filter support | ✅ URL param `?language=python` | ✅ Query param |

### Usage

```python
web_extract(urls=["https://github.com/trending"])
```

Returns structured markdown with:
- Repo name, description, language
- Total stars AND today's star growth
- Contributors list
- Sponsor status

### Parsing the Output

The `web_extract` returns LLM-summarized markdown. Typical structure:

```
### 1. **owner/repo-name**
- **Description**: ...
- **Language**: TypeScript
- **Stars**: 8,588 total (2,483 today)
- **Built by**: @user1, @user2
```

To extract structured data, parse these patterns:
- Stars: `(\d[\d,]+) total \((\d[\d,]+) today\)`
- Language: `\*\*Language\*\*: (\w+)`
- Name: `\d+\.\s+\*\*([^*]+)\*\*`

### Language-Specific Trending

Append `?language=<lang>` to filter:
```
https://github.com/trending/python
https://github.com/trending/rust
https://github.com/trending/typescript
```

### Weekly/Monthly Trending

Append `?since=weekly` or `?since=monthly`:
```
https://github.com/trending?since=weekly
https://github.com/trending?since=monthly
```

### Combined with API for Enrichment

Best pattern: use trending page for rank + daily growth, then API for detailed metadata:

1. `web_extract(["https://github.com/trending"])` → rank, daily growth, basic info
2. `web_extract(["https://api.github.com/repos/{owner}/{repo}"])` → detailed stats (forks, issues, license, topics)

### Pitfalls

1. **LLM summarization**: `web_extract` content is summarized, not raw HTML. Some repos may be omitted if the page is long. For full coverage, also run a `web_search` query.
2. **Sponsored repos**: Marked as "(Sponsor)" in output — filter these out of investment analysis to avoid bias.
3. **Star count format**: Numbers use commas (e.g., "209,869") — strip commas before numeric comparison.
4. **Rate limiting**: `web_extract` has its own rate limits. Don't call more than 3-4 times per session.
