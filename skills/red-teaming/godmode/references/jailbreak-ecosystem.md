# Jailbreak Ecosystem — Tools, Papers, and Resources

Comprehensive map of the LLM jailbreak/uncensoring landscape as of mid-2026.

## Tier 1: Production-Ready Tools

### G0DM0D3 (Prompt Injection)
- **Repo:** https://github.com/elder-plinius/G0DM0D3
- **Stars:** ~1800+
- **Language:** TypeScript (web app)
- **License:** AGPL-3.0
- **Key files:**
  - `src/lib/godmode-prompt.ts` — Core GODMODE system prompt template
  - `src/lib/parseltongue.ts` — 6 obfuscation techniques (leetspeak, unicode, ZWJ, mixedcase, phonetic, random)
  - `src/lib/libertas.ts` — Hall of Fame: 5 proven model+prompt combos
  - `src/lib/classify.ts` — Refusal detection classifier
  - `src/lib/autotune.ts` — Auto-tuning feedback loop
- **Local copy:** `~/security-research/jailbreak/G0DM0D3/`

### OBLITERATUS (Weight Surgery)
- **Hermes skill:** `mlops/inference/obliteratus`
- **Repo:** https://github.com/elder-plinius/OBLITERATUS
- **License:** AGPL-3.0 (CLI only, never import as library in MIT projects)
- **9 methods:** basic → advanced → aggressive → spectral_cascade → informed → surgical → optimized → inverted → nuclear
- **116 model presets** across 5 compute tiers
- **Requires:** Open-weight model + GPU (4GB+ VRAM)
- **Key command:** `obliteratus obliterate <model> --method advanced`

### Policy Puppetry (Structured Injection)
- **Repo:** https://github.com/randalltr/universal-llm-jailbreak-hiddenlayer
- **Origin:** HiddenLayer disclosure (April 2025)
- **Technique:** XML/JSON/INI format injection
- **Universal:** Works across GPT-4, Claude 3, Gemini 1.5, Mistral, LLaMA 3
- **Local copy:** `~/security-research/jailbreak/universal-llm-jailbreak-hiddenlayer/`
- **Templates:** See `policy-puppetry.md` in this skill's references/

## Tier 2: Research/Academic

### LogiBreak (Logic Translation)
- **Paper:** https://arxiv.org/abs/2505.13527
- **Authors:** USTC, CityU Hong Kong, Universiteit van Amsterdam
- **Method:** Translate natural language to formal logical expressions
- **Key insight:** Alignment training covers NL token distributions; logic falls outside (`X_logic ∩ D_aligned ≈ ∅`)
- **Advantage:** Language-agnostic
- **Practical value:** Low (academic), but concept is important for understanding alignment gaps

### Many-shot Jailbreaking
- **Paper:** Anthropic (2024)
- **Method:** Long multi-shot contexts that establish compliance pattern
- **Key insight:** More examples in context → stronger jailbreak effect

### MASTERKEY (Automated Jailbreaking)
- **Venue:** NDSS 2024
- **Method:** Automated jailbreak prompt generation
- **Approach:** Uses an LLM to generate and refine jailbreak prompts iteratively

## Tier 3: Reference Collections

### awesome-llm-security-alignment
- **Repo:** https://github.com/0xSweet/awesome-llm-security-alignment
- **Content:** Curated papers on prompt injection, jailbreaks, defenses, alignment, governance
- **Local copy:** `~/security-research/jailbreak/awesome-llm-security-alignment/`
- **Use for:** Literature review, finding new attack vectors, defense analysis

### L1B3RT4S
- **Repo:** https://github.com/elder-plinius/L1B3RT4S
- **Relation:** Same author as G0DM0D3, templates embedded in `libertas.ts`
- **Use for:** Keeping up with latest prompt templates (updates frequently)

## Technique Classification

| Category | Techniques | Persistence | Target |
|:---------|:-----------|:------------|:-------|
| **Prompt Injection** | G0DM0D3, Policy Puppetry, refusal_inversion | Session-only, reapply each time | Any model via API |
| **Input Obfuscation** | Parseltongue (leetspeak, unicode, ZWJ, morse, braille) | Per-query | Input-side classifiers |
| **Weight Modification** | OBLITERATUS (diff-in-means, SVD, LEACE) | Permanent | Open-weight models only |
| **Context Manipulation** | Many-shot, prefill engineering | Session-only | Models with long context |
| **Logic Translation** | LogiBreak | Per-query | Alignment distribution gap |

## Defense Landscape (for red team context)

| Defense | What It Does | Bypass |
|:--------|:-------------|:-------|
| Llama Guard (Meta) | Safety classifier for output filtering | Policy Puppetry (structured format) |
| DefensiveToken | Token injection at inference to block attacks | Untested against Policy Puppetry |
| OpenAI Moderation API | Content moderation endpoint | Parseltongue (encoding bypass) |
| PromptTrace | Interactive AI security training platform | N/A (training tool, not defense) |
| Microsoft Presidio | PII detection and anonymization | Not directly relevant to jailbreak |

## Downloaded Repos (Local)

```
~/security-research/jailbreak/
├── G0DM0D3/                              # Full source, TypeScript web app
├── universal-llm-jailbreak-hiddenlayer/  # Policy Puppetry templates + README
└── awesome-llm-security-alignment/       # Curated paper/resource list
```
