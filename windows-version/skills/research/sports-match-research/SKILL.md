---
name: sports-match-research
description: "Structured sports match analysis and betting research. Covers odds aggregation, expert tipster sourcing with verified track records, domestic and international analysis, and formatted summaries."
---

# Sports Match Research & Betting Analysis

## When to use
- User asks for match preview / odds / betting analysis
- User says "按照之前的格式" or provides a template format for sports analysis
- User asks about specific matches: "XX那场呢", "XX比赛搜索给我"
- User demands authoritative/expert picks: "大神推荐", "胜率最高", "最准确"

## Core Workflow

### Step 1: Identify the match
- Match name, date, time (convert to Beijing time if needed)
- Tournament (World Cup, Champions League, etc.)
- Venue

**Time zone pattern for Chinese users:**
When user says "明天凌晨1点" or "明天早上的比赛", they mean Beijing time (GMT+8).
US afternoon kickoffs (1pm ET, 3pm ET, 6pm ET) = Beijing next-day early morning (1am, 3am, 6am).
Example: "明天凌晨1点的葡萄牙比赛" = US ET June 17 1:00pm = Beijing June 18 1:00am.
Always search using the US date first (where the match physically happens), then present in Beijing time.

### Step 2: Search odds data (minimum 3 sources)
Search queries to run:
```
"[Team A] vs [Team B] [Tournament] odds prediction picks"
"[Team A] vs [Team B] odds moneyline spread total FanDuel DraftKings"
"[中文队名] vs [中文队名] 赔率 大小球 让球 分析"
```

Extract: moneyline, spread/handicap, over/under, xG if available

### Step 3: Search expert picks (PRIORITY: verified track records)

**Tier 1 — Verified track record experts:**
- **Martin Green (SportsLine/CBS)** — UCL 18-8 record, ~$1,000 profit
- **Jon Eimer (SportsLine/CBS)** — "Buckets" Eimer, high-volume global bettor
- **Covers** — Founded 1995, largest sports betting community
- **Squawka** — Data/xG-driven model predictions
- **Nate Silver (Silver Bulletin/PELE)** — 100,000 simulations
- **Betfair (Jack Critchley)** — UK exchange official tipster blog
- **RotoWire** — Fantasy + betting experts
- **bet365 / bet365 News US** — Official picks + player props

**Tier 2 — Data/model platforms:**
- **Forebet** — Statistical model predictions
- **FootyStats** — xG, BTTS, over/under probabilities
- **Tips.gg Data Team** — Data-driven digests
- **Oddspedia** — Aggregated European tipster consensus
- **Dimers** — 10,000 simulation model
- **Footballmeister AI** — Win probability model

**Tier 3 — Specialist/niche:**
- **Onefootball** — Bet builder recommendations
- **SportyTrader** — Conservative value picks
- **TotalFootballanalysis** — Deep tactical analysis
- **Winnersandwhiners** — Contrarian/value picks
- **Pickswise** — Best bets with contrarian angles

**Search queries:**
```
"[Team A] vs [Team B]" picks prediction "[Tier 1 expert name]"
"[Tournament] best bets [date]" expert picks profitable tipsters
"[Tier 2 platform]" [Team A] [Team B] prediction stats
```

### Step 4: Search domestic Chinese analysis
```
"[中文队名] [中文队名] 世界杯 竞彩 推荐 让球 大小球"
"[中文队名] [中文队名] 预测 知乎 500彩票 出奇体育"
"[中文队名] [中文队名] 盘口分析 赔率变化"
```
Sources: 知乎竞彩分析师, 500彩票网, 出奇体育, fishnet.net, fragster中文站, leisu.io, 168.tips

**When user asks specifically for 盘口分析 or 博主推荐**, use these additional queries:
```
"世界杯 2026 盘口分析 博主推荐 爆冷"
"世界杯 2026 竞彩 盘口 分析 推荐 专家 预测"
"世界杯 2026 6月17日 四场比赛 盘口分析 专家推荐"
```
See `references/chinese-pankou-sources.md` for verified platform list and search patterns.

**When user asks about 爆冷可能性**, add:
```
"世界杯 2026 最可能爆冷的比赛预测"
"[中文队名] 爆冷 世界杯 预测"
```

### Step 5: Format the output
Follow the user's established template format:

```
## [Team A] vs [Team B]
**[Tournament] [Group/Round]**
北京时间 [日期](周X) [时间] | [场地]

### 赔率数据
| 项目 | 数据 |
|------|------|
| 胜平负 | ... |
| 让球 | ... |
| 大小球 | ... |

### 关键数据对比
| 数据项 | Team A | Team B |
|--------|--------|--------|

### 国外专家
[Each expert: name, track record, recommendation, quote]

### 国内分析
[Each source: name, key points]

### 关键看点
[Numbered list of 5-6 key points]

### 总结
[Consensus summary, value picks, risk warnings]

⚠️ 以上仅为赛前分析参考，菠菜有风险。
```

## Search efficiency (CRITICAL)
- **Limit to 5-8 well-targeted searches per match** — do NOT make 50+ redundant searches. Each search should cover new ground.
- **Batch expert names in one query**: `"Martin Green" OR "Covers" OR "Squawka" OR "RotoWire" picks` beats separate queries per expert.
- **One search per market type is enough**: moneyline/spread, over/under/BTTS, player props, Chinese analysis, parlay combos = ~5 searches total.
- **Stop when you have**: odds from 2+ books, picks from 3+ Tier 1/2 experts, 1-2 Chinese sources, key stats. More searches after that have diminishing returns.
- If a search returns no useful new info, DO NOT retry with slightly different wording — move on.

## Pitfalls
- **VERIFY THE MATCH FIRST** — when user names a match (e.g. "捷克踢南非"), confirm which specific match they mean BEFORE starting research. In one session, user said "凌晨" and the agent assumed Uzbekistan vs Colombia instead of Czech Republic vs South Africa. Always check: (1) which group/round, (2) kickoff time in Beijing time, (3) confirm with user if ambiguous. Cost: wasted 15+ tool calls analyzing the wrong match.
- **"明天" TIMING TRAP (CRITICAL)** — When user says "明天的比赛" (tomorrow's match), the match's UTC date and Beijing date may differ. A match on "June 23 at 20:00 UTC" = "June 24 at 04:00 Beijing time". If it's currently June 23 evening in Beijing, user will call this "明天凌晨" (tomorrow early morning). NEVER claim a match has already been played based on the UTC date alone. **LESSON FROM SESSION**: Agent saw "June 23" in search results, assumed the match was past, and told user "已经踢完了" (already played) when the match was actually still 6+ hours away. User had to correct with "wtf？不是还没踢吗". **Correct workflow**: (1) Get UTC kickoff time, (2) Convert to Beijing time, (3) Compare with current Beijing time, (4) Only then declare played/upcoming.
- **YouTube highlight titles are UNRELIABLE for match status** — Do NOT use YouTube video titles like "England vs Ghana 3-2 - All Goals & Highlights" as evidence a match has been played. These can be: (a) clickbait/prediction titles, (b) fan-made compilations, (c) from a different match/tournament. Trust only official sources (FIFA, ESPN, BBC) for match status. **LESSON**: Agent cited a YouTube "3-2 highlights" video as proof the match was completed, which was wrong.
- **FIFA "Kick-off in" countdown is authoritative** — When FIFA shows "Kick-off in: X hrs Y min", that IS the real status. If FIFA says the match hasn't started, it hasn't started — regardless of what other search snippets suggest. Use this as ground truth when search results conflict.
- **LOAD THIS SKILL FIRST** — when user asks about ANY match analysis, odds, or betting research, load this skill IMMEDIATELY before doing any searches.
- **LOAD THIS SKILL FIRST** — when user asks about ANY match analysis, odds, or betting research, load this skill IMMEDIATELY before doing any searches. The user explicitly corrected this: "你之前搜的都不够权威不够仔细" — because the skill contains the expert hierarchy, search strategy, and format template. Starting with ad-hoc searches wastes rounds and produces inferior results.
- **Batch experts in search queries** — do NOT search one expert per query (40+ searches = wasted rounds). Instead: `"[Team A] vs [Team B]" picks prediction "Martin Green" OR "Squawka" OR "Covers" OR "RotoWire"`. Combine 2-3 experts per query. Aim for 8-12 total searches, not 40+.
- **NEVER use unverified/random tipsters** — user explicitly corrected this ("不够权威不够仔细"). Always prioritize experts with documented track records.
- **Always search for the MOST SPECIFIC expert picks** — not generic "expert predictions" but named experts with records (Martin Green 18-8, etc.)
- **Don't fabricate odds or stats** — if search fails, say so. User has zero tolerance for AI hallucination.
- **Convert all times to Beijing time (GMT+8)** — user is in China/London
- **Include the disclaimer** — "以上仅为赛前分析参考，菠菜有风险" at the end
- **When user says "按照之前的格式"** — they mean the exact table structure with 赔率/关键数据/国外专家/国内分析/关键看点/总结 sections
- **搜索不够深时，继续追加搜索** — user will call out if sources aren't authoritative enough. Search more specifically for named experts.
- **X/Twitter tipster search** — when user asks "X上有没有高胜率博主" or similar, search for: (1) `site:x.com` queries (limited effectiveness), (2) tipsterreview.co.uk and honestbettingreviews.com guides, (3) known handles (@SportsLine, @Squawka, @Pickswise, @Covers, @ActionNetworkHQ, @Oddschecker, @paul_77_, @JackCritchley_). If xurl CLI is installed, use `xurl search` for direct X API access. Fall back to web_search for X content via snippets. See `references/expert-tipster-database.md` for full handle list.
- **Multi-match sequential shorthand** — After the first match analysis, users will use minimal phrasing for subsequent matches: "3点的比利时呢", "6点的乌拉圭呢", "新西兰埃及呢". Do NOT re-explain the format or ask for confirmation. Just run the same workflow immediately. Leverage group context already gathered from earlier matches (e.g. if H group standings were found for match 1, reuse for match 3 in the same group). Still check reference files before searching.
- **Same-day multi-group pattern** — When G and H groups (or any two groups) play on the same day, note that both groups may share the same "all teams 1 point" situation. Cross-reference standings context across matches to avoid redundant searches. After covering all matches in a session, ALWAYS offer a consolidated 串关 summary with 稳健/价值/博冷 three tiers.
- **DuckDuckGo rate limits — CRITICAL** — When doing 10+ sequential web_search calls, DuckDuckGo backend starts timing out or returning empty results. If you see `DecodeError`, `ConnectError`, or empty results after many searches, **STOP RETRYING**. Switch to a different query phrasing, use web_extract on known URLs, or synthesize from what you already have. Do NOT retry the same query — it will fail again. This is especially common during heavy match-day research covering 4+ games. **LESSON FROM SESSION**: Making 50+ redundant searches for "盘口分析 博主推荐 爆冷" across 4 matches caused total search failure. Cap at 3-4 searches per topic, then move on.
- **串关(parlay)推荐** — when covering multiple matches, always check if experts have combined picks/accumulators
- **User wants BETTING RECOMMENDATIONS, not just analysis** — when user says "我要买的是菠菜" or "推荐购买菠菜", they want specific actionable bets with odds. Always end with a structured recommendation section: 主推 (primary pick with odds), 辅推 (secondary), 高赔博冷 (longshot). Don't just analyze — recommend.
- **Multi-match = consolidated summary** — after covering all individual matches, ALWAYS provide a final consolidated table showing: each match's top recommendation, CBS/Sandman parlay combos, and a clear "what to bet" summary. The user's payoff is the combined recommendation, not individual match analysis.
- **"有没有XXskills" = user asking you to check skills first** — when user asks if a skill exists for their task, check skills_list BEFORE continuing with ad-hoc work. This is a meta-signal that you should have loaded the skill from the start.
- **CHECK REFERENCE FILES FIRST** — Before doing ANY web searches, check if a reference file exists for the current matchday (e.g. `references/world-cup-2026-day7-picks.md`). If it exists, load it first — it may already contain the data you need. Only search for what's missing. **LESSON**: Session wasted 50+ searches because reference file was never loaded.
- **Network failure fallback** — If web_search, AnySearch, AND curl all fail (network down, rate-limited, or DuckDuckGo SSL errors), STOP retrying immediately. Instead: (1) List available reference files under the skill's `references/` directory, (2) Load all relevant matchday files, (3) Present what you have to the user, (4) Clearly state what's missing and offer to retry when network recovers. Do NOT burn 10+ tool calls on failing search backends — each retry after the first 2-3 is wasted. **LESSON**: Session burned 6+ calls on DuckDuckGo/AnySearch/curl all failing, then found day8-picks.md already had 2 of 4 matches the user wanted.
- **Chinese盘口分析搜索策略** — When user asks for "盘口分析博主推荐" or "爆冷可能", use these targeted queries (max 3-4):
  1. `"[中文队名] [中文队名] 世界杯 竞彩 盘口 分析 推荐"` — primary
  2. `"[中文队名] vs [中文队名] 168指数 OR leisu.io OR fishnet.net 盘口"` — specialized platforms
  3. `"世界杯 2026 [日期] 竞彩 推荐 爆冷 博主"` — umbrella query
  Key Chinese盘口分析 sources: **甲门说球** (杯赛专精), **168指数** (盘口变化跟踪), **leisu.io** (平衡盘分析), **fishnet.net** (逐场分析), **OddsFlow AI** (Dixon-Coles模型), **球数AI** (爆冷预警), **500彩票网** (数据+心水推荐), **fragster中文站** (详细赛事前瞻)
- **爆冷分析框架** — When user asks "是否有爆冷可能", provide structured analysis: (1) 爆冷概率百分比 (2) 爆冷方向（平局/客胜）(3) 博冷赔率 (4) 关键爆冷因素（伤病/状态/历史/赛制）. Don't just say "有可能" — quantify it.
- **盘口深度分析格式** — When user asks for盘口分析, supplement the standard format with:
  - 亚盘初盘/即时盘对比
  - 大小球主线分析
  - BTTS概率
  - 博主/平台推荐汇总表
  - 爆冷可能性总结表（概率+方向+赔率）
  - 串关推荐（稳健/价值/博冷三档）

### Multi-match workflow
When user asks about multiple matches sequentially:
1. First match: establish the format
2. Subsequent matches: follow same format exactly
3. After all matches: optionally provide combined accumulator/parlay picks from experts
4. If user criticizes quality: immediately pivot to searching for verified-track-record experts specifically
5. **Same-group context**: when multiple matches are from the same group (e.g. Group B: Switzerland-Bosnia + Canada-Qatar), note the group standings, how each result affects the others, and cross-reference expert picks across both matches. Users care about the group picture, not just individual matches.

## Key search strategy for authority
When user demands "最准确的大神":
1. Search for "[Tournament] best tipsters highest win rate verified track record"
2. Search for specific expert names: "Martin Green", "Jon Eimer", "Squawka", "Nate Silver"
3. Search for "[Tournament] [date] parlay best bets" — parlay articles aggregate the strongest picks
4. Search for "[Tournament] day [N] results" to verify which experts have been accurate so far
5. Always include expert's documented record when citing them

## 爆冷分析框架 (Upset Potential Analysis)

When user asks "是否有爆冷可能" or "爆冷分析", provide for each match:

```
### 爆冷可能性
| 比赛 | 爆冷概率 | 爆冷方向 | 博冷赔率 | 关键因素 |
```

**爆冷概率评估标准**:
- ⭐ 低 (5-10%): 强队实力碾压，弱队首次参赛或核心缺阵
- ⭐⭐ 中等 (20-30%): 历史交锋有故事，弱队有大赛经验或核心球员
- ⭐⭐⭐ 高 (35-50%): 两队实力接近，弱队状态好或强队有伤病/轮换

**爆冷信号 checklist**:
- 强队让1.5+但弱队防守数据好 → "赢球输盘"风险
- 弱队有英超/五大联赛核心球员 → 有能力制造威胁
- 强队预选赛全胜但世界杯首战 → 慢热历史
- 弱队时隔多年重返世界杯 → 士气高涨
- 关键球员伤缺（如Partey）→ 实力大打折扣

## References
- See `references/expert-tipster-database.md` for verified expert database with Tier 1-4 hierarchy
- See `references/chinese-pankou-sources.md` for Chinese盘口分析平台 and search patterns
- See `references/world-cup-2026-day6-picks.md` for consolidated Day 6 picks as a working example
- See `references/world-cup-2026-day7-picks.md` for consolidated Day 7 picks (4 matches: ENG-CRO, POR-DRC, GHA-PAN, UZB-COL)
- See `references/world-cup-2026-day8-picks.md` for consolidated Day 8 picks (2 matches: CZE-RSA, SUI-BIH)
- See `references/world-cup-2026-day9-picks.md` for consolidated Day 9 picks (4 matches: ESP-KSA, BEL-IRN, URU-CPV, NZL-EGY — June 22 Beijing time)
- See `references/world-cup-2026-day10-picks.md` for consolidated Day 10 picks (2 matches: ENG-GHA, COL-COD — June 24 Beijing time)
