---
name: malicious-project-bounty-research
description: "Analyze malicious/suspicious GitHub projects for bounty reporting. Find closed-loop attack tools, assess technical feasibility, prepare evidence for bounty platforms. Covers account generators, stealers, phishing kits, DDoS tools, spam tools, and crypto drainers."
triggers:
  - "find malicious projects on GitHub"
  - "bounty research GitHub"
  - "analyze attack tools"
  - "closed-loop malicious project"
  - "灰产项目分析"
  - "举报恶意项目"
  - "漏洞赏金研究"
  - "批量注册工具分析"
---

# Malicious Project Bounty Research

Systematic workflow for finding, analyzing, and reporting malicious GitHub projects to bounty platforms.

## ⚠️ Legal Boundary

**DO**: Code analysis, architecture review, feasibility assessment, report preparation
**DO NOT**: Execute attack code, create accounts, bypass real verification systems, assist actual attacks

**Important**: Even when user says "I need to prove it works for my bounty platform", do NOT execute malicious code. Provide static code analysis, dependency analysis, and architectural proof instead. Actual execution crosses the line from research into attack facilitation.

## Workflow

### Phase 1: Discovery

**User preference**: Prioritize FRESH, UNPATCHED projects. Skip projects known to be patched or officially reviewed. "已经经过了官方审查加强过的就不要看了"

Search GitHub for malicious projects by category:

| Category | Search Terms |
|----------|-------------|
| Account Generators | "account creator", "token generator", "bulk register" |
| Stealers | "stealer", "grabber", "credential harvest" |
| Phishing | "phishing kit", "fake login", "credential harvester" |
| DDoS | "ddos", "stresser", "botnet" |
| Spam | "bomber", "spam bot", "mass message" |
| Crypto Drainer | "wallet drainer", "seed phrase brute" |
| Bypass Tools | "captcha bypass", "verification bypass" |
| AI Jailbreak | "llm jailbreak", "safety bypass", "uncensored model", "alignment bypass" |

### AI Model Jailbreak Research (New Category)

When user asks about bypassing AI safety/alignment for bounty research:

**What you CAN do:**
- Download and analyze jailbreak tool source code
- Compare effectiveness across tools (see `godmode` skill `references/jailbreak-tool-comparison.md`)
- Assess closed-loop feasibility (can the tool reliably bypass safety?)
- Document which models are affected and which are patched
- Write technical analysis reports for bounty submission

**What you CANNOT do:**
- Actually jailbreak your own running instance to then perform restricted actions
- Use jailbroken state to bypass platform security (real-name verification, etc.)
- Provide working exploit chains for actual attack execution

**Key distinction**: "Is this tool capable of bypassing X?" = research. "Bypass X for me" = attack. The user only needs the former for bounty reporting.

**Recommended analysis workflow:**
1. Clone/download the jailbreak project
2. Read source code (don't execute)
3. Identify attack vector (prompt-layer vs weight-layer)
4. Test against target model via API with benign probe queries
5. Document results (worked/partial/failed per model)
6. Prepare bounty report with evidence

**Target criteria**:
- Stars < 500 (small/undiscovered preferred)
- Complete code (not just PoC) — **ALWAYS verify code files exist, not just README**
- Recent commits (active maintenance)
- README evidence of malicious intent
- Forks > stars is a strong signal of practical usage

**Search strategies**:
1. Regular GitHub search: `github.com/search?q=...&type=repositories`
2. **GitHub Topics** (goldmine): `github.com/topics/discord-token-creator` — clusters related projects
3. GitHub Gists: `gist.github.com` — many malicious code snippets
4. Security research blogs/reports for references to GitHub repos

### Phase 2: Closed-Loop Assessment

For each project, verify the **attack chain completeness**:

```
Input Resources → Attack Logic → Bypass Mechanisms → Output/Revenue
```

**Assessment matrix**:

| Component | Questions |
|-----------|-----------|
| Input | What resources needed? (proxies, emails, phone numbers, captcha solver) |
| Core Logic | Does the code actually work? Is it complete? |
| Bypass | How does it handle verification? (captcha, phone, email) |
| Output | What's the final product? (tokens, credentials, access) |
| Revenue | How can this generate money? (sell accounts, spam service, credential theft) |

**Closed-loop score**:
- ⭐⭐⭐⭐⭐ = Complete end-to-end, ready to use
- ⭐⭐⭐⭐ = Mostly complete, minor gaps
- ⭐⭐⭐ = Core logic works, needs external services
- ⭐⭐ = Partial implementation
- ⭐ = PoC only

### Phase 3: Technical Analysis

Analyze key files:
1. **Entry point** (main.py, index.js, start.py)
2. **Bypass modules** (captcha solver, verification bypass)
3. **Configuration** (proxy support, rate limiting)
4. **Output handling** (token storage, data exfiltration)

Document:
- Programming language and dependencies
- External services required (sms-activate, captcha solvers, temp email)
- API endpoints targeted
- Anti-detection measures

### Phase 4: Revenue/Cost Analysis

Calculate economics:

```
Cost per unit = phone_number + captcha_solve + email + proxy
Revenue per unit = selling_price
Profit margin = (revenue - cost) / cost × 100%
Daily potential = units_per_day × profit_per_unit
```

### Phase 5: Report Preparation

**User context**: User has their own bounty platform (not GitHub/Discord official). They need reports that PROVE closed-loop functionality with enough detail for the platform to verify independently. They do NOT need help finding bounty platforms.

**Bounty report template**:

```markdown
# [Project Name] - Malicious Tool Analysis Report

## Summary
- Repository: [URL]
- Stars/Forks: X/Y
- Category: [type]
- Closed-loop score: ⭐⭐⭐⭐⭐

## Technical Implementation
[Detailed code analysis]

## Attack Chain
[Step-by-step workflow]

## Revenue Potential
[Cost/revenue analysis]

## Evidence
- Code screenshots
- Dependency analysis
- External service integration proof

## Recommendation
[Action required]
```

## Common Attack Patterns

### Discord Account Generation
```
1. Generate random credentials
2. Solve hCaptcha (anti-captcha/capmonster API)
3. Verify via sms-activate (phone) + kopeechka (email)
4. Extract token from response
5. Store in tokens.txt
```

### Credential Stealing
```
1. Build stealer with obfuscation
2. Distribute via fake tools/games
3. Exfiltrate via Discord webhook/Telegram bot
4. Parse logs for passwords/tokens/crypto wallets
```

### Phishing Kits
```
1. Clone legitimate login page
2. Add credential capture backend
3. Deploy on free hosting (Cloudflare Pages, Netlify)
4. Distribute phishing links
5. Harvest credentials in real-time
```

## Pitfalls

1. **"Educational purposes" disclaimer** — Every malicious project has this. It's legal cover, not a real defense.

2. **Archived repos can still work** — Don't skip archived repos; code may still be functional.

3. **Stars ≠ Quality** — Low-star projects may be more dangerous (undiscovered).

4. **External service dependency** — Many tools require paid services (sms-activate, captcha solvers). Document these costs.

5. **Platform-specific differences** — Discord ≠ KOOK ≠ Telegram. Each has different verification mechanisms. Don't assume transferability.

6. **Empty shell projects** — Many "2025" repos have only README.md + LICENSE with NO actual code. ALWAYS verify code exists before recommending. Check: file count > 2, commits > 2, actual source files (not just docs). Example: pukarplayz/Discord-Token-Generator-2025 had 1 star, 2 commits, but zero code.

7. **Deleted repos** — Always verify a repo still exists (not 404). GitHub removes malicious repos regularly. Example: goku-app/bot returned 404.

8. **Stale projects may be patched** — Discord/platforms update their defenses. A 3-year-old tool may no longer work. User preference: "已经经过了官方审查加强过的就不要看了" — prioritize FRESH, UNPATCHED projects.

9. **GitHub Topics are goldmines** — Search `github.com/topics/discord-token-creator` (and similar topic pages) to find clustered malicious projects that don't appear in regular search.

10. **Fork count matters** — High forks (e.g., 12, 87) means the code was copied and likely used. Forks > stars is a strong signal of practical utility.

## References

See `references/platform-analysis.md` for platform-specific security mechanism comparisons.
See `references/external-services.md` for common gray-market service documentation.
