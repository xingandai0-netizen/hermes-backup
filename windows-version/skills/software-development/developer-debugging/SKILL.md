---
name: developer-debugging
description: "开发者调试完整指南：4阶段根因分析方法论、Python调试（pdb/debugpy）、Node.js调试（Chrome DevTools）、Hermes TUI调试、常见陷阱。合并了 systematic-debugging。"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, python, nodejs, debugpy, chrome-devtools, hermes-agent, tui, slash-commands]
    related_skills: [systematic-debugging, hermes-agent]
---

# Developer Debugging

Debug applications across Python, Node.js, and Hermes TUI. Each section covers setup, common workflows, and pitfalls.

## When to Use

- Python script crashes or produces unexpected results
- Node.js application debugging (inspect protocol)
- Hermes TUI slash commands not working correctly
- Need breakpoints, step-through, or variable inspection

## 1. Python Debugging (pdb + debugpy)

### Quick pdb

```python
# Insert breakpoint in code
import pdb; pdb.set_trace()

# Or run with pdb
python -m pdb script.py
```

**pdb commands:** `n` (next), `s` (step into), `c` (continue), `p expr` (print), `l` (list), `w` (where/stack), `q` (quit)

### debugpy (Remote Debugging)

```python
import debugpy
debugpy.listen(5678)
print("Waiting for debugger attach...")
debugpy.wait_for_client()
# Your code here
```

**Attach from VS Code:** Run → Python: Remote Attach → localhost:5678

**Or from CLI with DAP:**
```bash
pip install debugpy
python -m debugpy --listen 5678 --wait-for-client script.py
```

### Common Pitfalls

- `debugpy.wait_for_client()` blocks until debugger attaches — don't use in production
- Port 5678 must be free — check with `lsof -i :5678`
- In Docker/remote: use `0.0.0.0` instead of `localhost`

---

## 2. Node.js Debugging (Chrome DevTools Protocol)

### Start with inspect

```bash
node --inspect script.js
node --inspect-brk script.js  # Break on first line
```

### CLI Debugger

```bash
node inspect script.js
```

Commands: `cont` (continue), `next` (step), `step` (into), `out` (out), `repl` (evaluate), `watch('expr')`, `unwatch('expr')`

### Breakpoints via source

```javascript
// In code
debugger;  // Pauses when inspector is connected
```

### Chrome DevTools

1. Start: `node --inspect-brk script.js`
2. Open: `chrome://inspect`
3. Click "inspect" on your target
4. Full DevTools: Sources tab, breakpoints, console, profiler

### Pitfalls

- `--inspect-brk` pauses at first line — use `--inspect` to run immediately
- Port 9229 is default — use `--inspect=PORT` for custom
- In Docker: `--inspect=0.0.0.0:9229` for remote access
- Source maps: if debugging transpiled code, ensure source maps are generated

---

## 3. Hermes TUI Slash Command Debugging

### Architecture

```
Python backend (hermes_cli/commands.py)     <- COMMAND_REGISTRY (source of truth)
       │
       ▼
TUI gateway (tui_gateway/server.py)         <- slash.exec / command.dispatch
       │
       ▼
TUI frontend (ui-tui/src/app/slash/)        <- local handlers + fallthrough
```

### Command Shows in TUI but Not Autocomplete

The command is in the TUI codebase but missing from `COMMAND_REGISTRY` in `hermes_cli/commands.py`. Autocomplete data ships from Python.

**Fix:** Add a `CommandDef` entry:
```python
CommandDef("commandname", "Description", "Category",
           cli_only=True, aliases=("alias",),
           args_hint="[arg1|arg2]", subcommands=("arg1", "arg2"))
```

### Command Shows in Autocomplete but Doesn't Work

Check the handler in `tui_gateway/server.py` and `ui-tui/src/app/createSlashHandler.ts`. Local TUI handlers take precedence over gateway dispatch.

### Command Behavior Differs Between CLI and TUI

Check both `cli.py::process_command` and the TUI's local handler. They may have different implementations.

### Command Persists Config but Doesn't Apply Live

For TUI-local commands, updating config is not enough. Also patch the nanostore state immediately:
```typescript
patchUiState({ details_mode: newMode });
```

### Gateway Ignores the Command

Check `GATEWAY_KNOWN_COMMANDS` (derived from `COMMAND_REGISTRY`). If the command is `cli_only` with a `gateway_config_gate`, verify the gate is truthy.

### Rebuild and Test

```bash
cd hermes-agent && npm --prefix ui-tui run build
hermes --tui
# Type / and verify command appears in autocomplete
```

### Pitfalls

- Set the correct category in `CommandDef` ("Session", "Configuration", "Tools & Skills", etc.)
- Aliases are registered in the `aliases` tuple — everything downstream derives from it
- `cli_only=True` won't work in gateway unless you add `gateway_config_gate`
- Rebuild TUI before testing — `tsx watch` may lag on first launch

---

## 4. Systematic Debugging Methodology

When you hit a bug you can't immediately solve:

### Phase 1: Understand

- Read the error message carefully — it usually tells you exactly what's wrong
- Reproduce the issue reliably
- Check recent changes (`git diff`, `git log`)

### Phase 2: Isolate

- Binary search: comment out half the code, see if bug persists
- Add print/log statements at key points
- Check inputs vs expected inputs

### Phase 3: Hypothesize

- Form a theory about the root cause
- Test it with a minimal change
- If wrong, go back to Phase 2

### Phase 4: Fix and Verify

- Make the fix
- Run tests
- Verify the original issue is resolved
- Check for regressions

---

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture — the pattern may be fundamentally wrong.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem |

## Decision Guide

| Problem | Tool |
|---------|------|
| Python crash/exception | pdb or debugpy |
| Node.js issue | `node --inspect` + Chrome DevTools |
| Hermes slash command bug | Python registry + TUI frontend check |
| Complex multi-file bug | Systematic debugging methodology (Phases 1-4) |
| Remote/container debugging | debugpy (Python) or `--inspect=0.0.0.0` (Node) |
