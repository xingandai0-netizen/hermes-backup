# 批注任务档案

## 任务2 (搁置 2026-05-02)
- 阻塞原因: antokex.com不在Hermes的_supports_reasoning_extra_body() whitelist中
- 白名单: 仅OpenRouter, Nous, GitHub
- 且mimo-v2.5为非reasoning模型, reasoning参数被忽略
- Hermes源码: ~/.hermes/hermes-agent/run_agent.py (lines ~6240-6320)

## 任务4 (搁置 2026-05-02)
- Claude Code CLI: v2.1.119, installed at /Users/macpro/.local/bin/claude
- 状态: loggedIn=false, authMethod=none
- 阻塞原因: tokex.top无Claude模型，仅6个模型(mimo/minimax系列)
- 支持ANTHROPIC_BASE_URL但无可用模型

## tokex.top 模型列表
mimo-v2-flash, mimo-v2-omni, mimo-v2-pro, mimo-v2.5, mimo-v2.5-pro, minimaxai/minimax-m2.7

## API Keys
- ~/.hermes/.env: XIAOMI_API_KEY, OPENAI_API_KEY, OPENROUTER_API_KEY (均51字符)
- 无有效Anthropic key
