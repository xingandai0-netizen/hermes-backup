#!/usr/bin/env python3
"""GitHub Trend Monitor - Daily Cron Pipeline"""
import urllib.request
import json
import os
from datetime import datetime
from pathlib import Path

# --- Step 1: Fetch from GitHub Search API ---
queries = {
    "trending_star_momentum": "https://api.github.com/search/repositories?q=stars:>500&sort=updated&order=desc&per_page=10",
    "agent_ecosystem": "https://api.github.com/search/repositories?q=agent+automation+stars:>500&sort=stars&order=desc&per_page=10",
    "mcp_ecosystem": "https://api.github.com/search/repositories?q=mcp+model-context-protocol+stars:>100&sort=stars&order=desc&per_page=10",
}

all_repos = []
seen = set()

for qname, url in queries.items():
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Auto-Tech-Trend-Bot/1.0",
            "Accept": "application/vnd.github.v3+json"
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = json.loads(resp.read().decode())
        items = raw.get("items", [])
        for r in items:
            name = r.get("full_name", "")
            if name not in seen:
                seen.add(name)
                all_repos.append({
                    "name": name,
                    "url": r.get("html_url", ""),
                    "stars": r.get("stargazers_count", 0),
                    "language": r.get("language"),
                    "description": (r.get("description") or "")[:120],
                    "topics": r.get("topics", []),
                    "forks": r.get("forks_count", 0),
                    "open_issues": r.get("open_issues_count", 0),
                    "updated_at": r.get("updated_at", ""),
                    "query": qname,
                })
        print(f"[{qname}] fetched {len(items)} repos (total_matching: {raw.get('total_count', 0)})")
    except Exception as e:
        print(f"[{qname}] ERROR: {e}")

# --- Step 2: Analyze ---
KEYWORDS_MCP = ["mcp", "model-context-protocol"]
KEYWORDS_AGENT = ["agent", "automation", "workflow", "orchestrat", "pipeline", "harness"]
KEYWORDS_API = ["api", "sdk", "cli", "tool", "framework", "library"]
KEYWORDS_AI = ["llm", "ai", "model", "inference", "fine-tuning", "gpt", "transformer"]

lang_count = {}
for r in all_repos:
    lang = r.get("language") or "N/A"
    lang_count[lang] = lang_count.get(lang, 0) + 1
lang_dist = dict(sorted(lang_count.items(), key=lambda x: -x[1]))

priority_order = {"高": 0, "中": 1, "低": 2}
opportunities = []
for r in all_repos:
    text = f"{r.get('description','').lower()} {r['name'].lower()} {' '.join(r.get('topics', []))}"
    matches, priority = [], "低"
    if any(k in text for k in KEYWORDS_MCP):
        matches.append("MCP集成"); priority = "高"
    if any(k in text for k in KEYWORDS_AGENT):
        matches.append("Agent/自动化")
        if priority != "高": priority = "中"
    if any(k in text for k in KEYWORDS_API):
        matches.append("API/CLI工具")
        if priority == "低": priority = "中"
    if any(k in text for k in KEYWORDS_AI):
        matches.append("AI/LLM能力")
        if priority == "低": priority = "中"
    if matches:
        opportunities.append({
            "repo": r["name"], "stars": r["stars"],
            "matches": matches, "priority": priority,
            "reason": f"涉及 {', '.join(matches)} — {r.get('description','')[:80]}"
        })
opportunities.sort(key=lambda x: (priority_order.get(x["priority"], 3), -x["stars"]))

top10 = sorted(all_repos, key=lambda x: -x["stars"])[:10]

# --- Step 3: Save JSON ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

report = {
    "generated_at": now_str,
    "queries": {
        "trending_star_momentum": {"repos": [r for r in all_repos if r.get("query") == "trending_star_momentum"]},
        "agent_ecosystem": {"repos": [r for r in all_repos if r.get("query") == "agent_ecosystem"]},
        "mcp_ecosystem": {"repos": [r for r in all_repos if r.get("query") == "mcp_ecosystem"]},
    },
    "language_distribution": lang_dist,
    "top_10_by_stars": [{"rank": i+1, "name": r["name"], "stars": r["stars"], "language": r.get("language") or "N/A", "description": r.get("description","")[:70], "url": r["url"]} for i, r in enumerate(top10)],
    "hermes_integration_opportunities": opportunities,
}

for path in [
    "/Users/macpro/.hermes/skills/github-trend-monitor/scripts/trending_repos.json",
    "/Users/macpro/reports/latest_data.json",
    f"/Users/macpro/reports/trend_data_{timestamp}.json",
]:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

# --- Step 4: Run log ---
os.makedirs("/Users/macpro/logs", exist_ok=True)
avg_stars = sum(r["stars"] for r in all_repos) / max(len(all_repos), 1)
high_count = len([o for o in opportunities if o["priority"] == "高"])
log_entry = {
    "timestamp": now_str, "status": "success",
    "repos_analyzed": len(all_repos), "high_priority_opportunities": high_count,
    "top_repo": f"{top10[0]['name']} ({top10[0]['stars']:,} ⭐)" if top10 else "N/A",
}
with open("/Users/macpro/logs/daily_run.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

# --- Output Summary ---
print(f"\n{'='*60}")
print(f"✅ GitHub趋势监控完成 — {now_str}")
print(f"{'='*60}")
print(f"📊 去重项目: {len(all_repos)} | 语言: {len(lang_dist)} | 平均⭐: {int(avg_stars):,}")
print(f"🎯 高优先机会: {high_count} | 总机会: {len(opportunities)}")
print(f"\n🏆 Top 10:")
for i, r in enumerate(top10, 1):
    print(f"  {i:2d}. {r['name']:<45} ⭐{r['stars']:>8,}  [{r.get('language') or 'N/A'}]")
print(f"\n📈 语言分布:")
for lang, cnt in list(lang_dist.items())[:8]:
    print(f"  {lang:<20} {cnt}个 ({cnt/len(all_repos)*100:.0f}%)")
print(f"\n🎯 Hermes集成机会 (高优先):")
for opp in [o for o in opportunities if o["priority"] == "高"][:5]:
    print(f"  🔴 {opp['repo']} ({opp['stars']:,}⭐) — {opp['reason'][:60]}")
print(f"\n🎯 Hermes集成机会 (中优先):")
for opp in [o for o in opportunities if o["priority"] == "中"][:5]:
    print(f"  🟡 {opp['repo']} ({opp['stars']:,}⭐) — {opp['reason'][:60]}")
