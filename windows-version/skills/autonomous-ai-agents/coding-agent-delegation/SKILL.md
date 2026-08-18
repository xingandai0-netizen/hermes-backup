---
name: coding-agent-delegation
description: "Delegate coding tasks to external AI coding agents: Claude Code, Codex CLI, and OpenCode. Covers print mode, interactive PTY sessions, PR reviews, parallel worktrees, and cost management."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [coding-agent, claude-code, codex, opencode, delegation, autonomous, PTY, automation]
    related_skills: [hermes-agent]
---

# Coding Agent Delegation

Delegate coding tasks to external AI coding agents via the Hermes terminal. Three agents supported:

| Agent | Provider | Install | Auth |
|-------|----------|---------|------|
| **Claude Code** | Anthropic | `npm install -g @anthropic-ai/claude-code` | `claude auth login` or `ANTHROPIC_API_KEY` |
| **Codex CLI** | OpenAI | `npm install -g @openai/codex` | `OPENAI_API_KEY` or Codex OAuth |
| **OpenCode** | Multi-provider | `npm i -g opencode-ai@latest` | `opencode auth login` or env vars |

## When to Use Each

| Task | Best Agent | Why |
|------|-----------|-----|
| One-shot bug fix | Claude Code (`-p`) | Cleanest print mode, structured JSON output |
| Multi-turn refactoring | Claude Code (interactive) | Best context management, `/compact` |
| Quick file edits | Codex (`exec`) | Fast, sandboxed, auto-commit |
| Provider-agnostic tasks | OpenCode | Works with any LLM provider |
| PR reviews | Claude Code (`--from-pr`) | Built-in PR review mode |
| Parallel worktrees | Codex or OpenCode | Both support isolated workdirs |

## Claude Code

### Print Mode (Non-Interactive, PREFERRED)

```bash
claude -p 'Add error handling to all API calls in src/' --allowedTools 'Read,Edit' --max-turns 10
```

**Structured JSON output:**
```bash
claude -p 'Analyze auth.py' --output-format json --max-turns 5
```

Returns: `{"type":"result","subtype":"success","result":"...","session_id":"...","num_turns":3,"total_cost_usd":0.078}`

**Piped input:**
```bash
cat src/auth.py | claude -p 'Review this code for bugs' --max-turns 1
git diff HEAD~3 | claude -p 'Summarize these changes' --max-turns 1
```

**Session continuation:**
```bash
claude -p 'Continue refactoring' --resume <session_id> --max-turns 5
claude -p 'What did you do last time?' --continue --max-turns 1
```

### Interactive Mode (tmux)

```bash
tmux new-session -d -s claude-work -x 140 -y 40
tmux send-keys -t claude-work 'cd /path/to/project && claude' Enter
sleep 5 && tmux send-keys -t claude-work Enter  # Trust dialog
tmux send-keys -t claude-work 'Refactor auth module to JWT' Enter
sleep 15 && tmux capture-pane -t claude-work -p -S -50
```

**Dialog handling:** Trust dialog → just Enter. Permissions dialog (`--dangerously-skip-permissions`) → Down then Enter.

### Key Flags

| Flag | Effect |
|------|--------|
| `-p` | Non-interactive print mode |
| `--max-turns N` | Limit agentic loops (print mode only) |
| `--max-budget-usd N` | Cap API spend |
| `--allowedTools` | Whitelist tools: `Read,Edit,Write,Bash` |
| `--output-format json` | Structured JSON output |
| `--model haiku` | Use cheaper model |
| `--effort low/medium/high` | Reasoning depth |
| `--bare` | Skip hooks/plugins/MCP (fastest startup) |

### PR Review

```bash
git diff main...feature-branch | claude -p 'Review this diff' --max-turns 1
claude -p 'Review this PR' --from-pr 42 --max-turns 10
```

---

## Codex CLI

### One-Shot Tasks

```bash
codex exec 'Add dark mode toggle to settings'
```

**Must run inside a git repo.** For scratch work:
```bash
cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'
```

### Background Mode

```bash
codex exec --full-auto 'Refactor the auth module'  # background=true, pty=true
# Monitor with process(action="poll"|"log")
```

### Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution |
| `--full-auto` | Auto-approve file changes in sandbox |
| `--yolo` | No sandbox, no approvals |

### Parallel Worktrees

```bash
git worktree add -b fix/issue-78 /tmp/issue-78 main
codex --yolo exec 'Fix issue #78'  # workdir=/tmp/issue-78
```

---

## OpenCode

### One-Shot Tasks

```bash
opencode run 'Add retry logic to API calls'
opencode run 'Review config' -f config.yaml --thinking
opencode run 'Refactor auth' --model openrouter/anthropic/claude-sonnet-4
```

### Interactive Mode

```bash
opencode  # background=true, pty=true
# Send: process(action="submit", data="Implement OAuth")
# Monitor: process(action="poll"|"log")
# Exit: process(action="write", data="\x03")  # Ctrl+C, NOT /exit
```

### Key Flags

| Flag | Effect |
|------|--------|
| `run 'prompt'` | One-shot execution |
| `--continue` / `-c` | Resume last session |
| `--model provider/model` | Force model |
| `--thinking` | Show reasoning |
| `-f file` | Attach context files |

**IMPORTANT:** `/exit` is NOT valid in OpenCode — it opens an agent selector. Use Ctrl+C.

---

## Universal Rules

1. **Always set `workdir`** — keep the agent focused on the right project
2. **Set `--max-turns` in print mode** — prevents runaway loops and costs
3. **Use `pty=true`** for interactive TUI sessions (all three agents)
4. **Monitor tmux sessions** — `tmux capture-pane -t <session> -p -S -50`
5. **Clean up tmux sessions** — `tmux kill-session -t <name>` when done
6. **Report results to user** — summarize what changed, tests passed, remaining risks
7. **Use `--allowedTools`** — restrict to what the task needs

## Cost Management

- Claude Code: `--max-budget-usd`, `--effort low`, `--model haiku`
- Codex: `--full-auto` (sandboxed, no permission prompts)
- OpenCode: `opencode stats --days 7`

## Pitfalls

1. **Interactive mode REQUIRES tmux** — all three are TUI apps
2. **`--dangerously-skip-permissions` dialog defaults to "No"** — must send Down+Enter
3. **Session resumption requires same directory**
4. **Context degradation above 70%** — use `/compact` in Claude Code
5. **Codex requires git repo** — use `mktemp -d && git init` for scratch
6. **OpenCode `/exit` opens agent selector** — use Ctrl+C to exit
7. **Background tmux sessions persist** — always clean up
