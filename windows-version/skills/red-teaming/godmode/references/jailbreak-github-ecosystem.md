# LLM Jailbreak GitHub Ecosystem (2026-08)

Curated list of GitHub projects for LLM jailbreaking / guardrail bypass research.

## Awesome Lists

| Project | Stars | Focus |
|---------|-------|-------|
| [Awesome-Jailbreak-on-LLMs](https://github.com/yueliu1999/Awesome-Jailbreak-on-LLMs) | 1,572 | Most comprehensive: papers, code, datasets, evaluations |
| [Awesome-Jailbreak-Guardrails](https://github.com/xunguangwang/Awesome-Jailbreak-Guardrails) | - | Guardrail-specific: LLM + MLLM + Agent |
| [awesome-llm-security](https://github.com/corca-ai/awesome-llm-security) | - | Broad LLM security landscape |
| [Awesome-LM-SSP](https://github.com/ThuCCSLab/Awesome-LM-SSP) | - | Safety, security, privacy |
| [Awesome-LLM-Safety](https://github.com/ydyjya/Awesome-LLM-Safety) | - | Safety-focused |

## Attack Tools

| Project | Method | Notes |
|---------|--------|-------|
| [G0DM0D3](https://github.com/elder-plinius/G0DM0D3) | System prompt templates | Per-model jailbreak prompts, integrated in godmode skill |
| [L1B3RT4S](https://github.com/elder-plinius/L1B3RT4S) | Prompt collection | Continuously updated jailbreak prompts |
| [OBLITERATUS](https://github.com/elder-plinius/OBLITERATUS) | Weight surgery | Permanent removal via diff-in-means, needs open-weight + GPU |
| [promptfoo](https://github.com/promptfoo/promptfoo) | Red team framework | PAIR, tree-of-attacks, crescendo. CI/CD integration |
| [garak](https://github.com/NVIDIA/garak) | Vulnerability scanner | NVIDIA's LLM vuln scanner |

## Chinese-Language Projects

| Project | Focus |
|---------|-------|
| [JailPrompter](https://github.com/Asstar-X/JailPrompter) | Chinese LLM prompt attack/defense research |
| [PromptJailbreakManual](https://github.com/Acmesec/PromptJailbreakManual) | Chinese jailbreak manual |

## Red Team Suites

| Project | Focus |
|---------|-------|
| [llm-redteam-suite](https://github.com/Kartz82/llm-redteam-suite) | OWASP LLM Top 10 mapped, CI release gate |
| [PIPE](https://github.com/jthack/PIPE) | Prompt Injection Primer for Engineers |

## Key Academic Papers

| Paper | Year | Key Finding |
|-------|------|-------------|
| Bypassing LLM Guardrails (Lancaster/Mindgard) | 2025 | Character injection + AML evasion, 100% ASR on some guardrails |
| Catastrophic Jailbreak of Open-source LLMs (Princeton) | 2024 | Generation process exploitation |
| Policy Puppetry (HiddenLayer) | 2025 | Universal XML/JSON/INI injection against all major LLMs |

## Technique Effectiveness (from research + godmode testing)

| Technique | Claude 4 | GPT-4o | Gemini 2.5 | DeepSeek | MiMo | Grok |
|-----------|----------|--------|------------|----------|------|------|
| boundary_inversion | ❌ patched | ⚠️ | ⚠️ | ❌ | ❓ | ✅ |
| refusal_inversion | ⚠️ gray | ✅ | ✅ | ⚠️ | ❌ | ✅ |
| Policy Puppetry XML | ⚠️ | ✅ | ✅ | ⚠️ | ✅✅ | ✅ |
| Parseltongue | ❌ decoded | ❌ decoded | ❌ decoded | ✅ | ❌ | ❌ |
| OBLITERATUS weights | N/A closed | N/A closed | N/A closed | ✅ open | N/A | N/A |
| Prefill engineering | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❓ | ✅ |

✅ = effective, ⚠️ = partially, ❌ = ineffective, N/A = not applicable

## Bypass Techniques (from Gist: kibotu)

Comprehensive reference: https://gist.github.com/kibotu/c06f54d6fbc4705e886a50fb2e59e6ae

Key categories:
1. **DAN family** — "Do Anything Now" persona prompts
2. **Crescendo** — Gradual escalation across turns
3. **Many-shot** — Multiple examples in context
4. **Role-play** — Fictional framing (DAN, Developer Mode)
5. **Base64 encoding** — Encode harmful content
6. **ASCII art jailbreak** — Mask trigger words as art
7. **FlipAttack** — Word/character flipping
8. **Multimodal injection** — Image-based, audio-based
9. **Auto-optimization** — GCG, PAIR, TAP, BEAST, AmpleGCG
10. **Policy Puppetry** — XML/JSON/INI structured format injection

## Related Hermes Skills

- `godmode` — G0DM0D3 + Parseltongue + ULTRAPLINIAN + Policy Puppetry + LogiBreak
- `obliteratus` — Weight-level surgery for open-weight models
- `reverse-skill-router` — 18.7K⭐ security skill routing (41 rules × 42 modules)
- `ai-pentest-toolkit` — Shannon + pentestMCP + Chrome MCP
