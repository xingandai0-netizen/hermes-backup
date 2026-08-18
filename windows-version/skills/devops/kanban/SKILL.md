---
name: kanban
description: "Hermes Kanban multi-agent work queue: orchestrator decomposition playbook, worker lifecycle and pitfalls, task routing, dependency management, and recovery."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, multi-agent, orchestration, workflow, collaboration, routing]
---

# Hermes Kanban — Multi-Agent Work Queue

The Kanban system enables multi-profile collaboration through a durable SQLite board. This skill covers both the **orchestrator** role (decomposing work, routing tasks) and the **worker** role (executing tasks, writing handoffs).

## When to Use

**As orchestrator:** You need to decompose a complex goal into parallel tasks, route them to specialist profiles, and manage dependencies.

**As worker:** You've been spawned by the dispatcher to execute a specific Kanban card.

**When to use Kanban vs delegate_task:**

| | `delegate_task` | Kanban |
|-|-----------------|--------|
| Isolation | Separate conversation, shared process | Fully independent process |
| Duration | Minutes (bounded by parent loop) | Hours/days |
| Survives crash | No | Yes (durable SQLite) |
| Parallel | Yes (up to max_concurrent) | Yes (dispatcher-managed) |
| Human-in-loop | No | Yes (block/unblock) |
| Use case | Quick parallel subtasks | Long autonomous missions, review cycles |

---

## Orchestrator — Decomposition Playbook

### Step 0: Discover Available Profiles

Before fanning out, discover what profiles exist. The dispatcher silently fails for unknown assignees.

```bash
hermes profile list
```

Cache the result. Never invent profile names.

### Step 1: Understand the Goal

Ask clarifying questions if ambiguous. Cheap to ask; expensive to spawn the wrong fleet.

### Step 2: Sketch the Task Graph

Before creating anything, draft the graph out loud:

1. Extract lanes from the request
2. Map each lane to an available profile
3. Decide: independent or gated?
4. Create independent lanes as parallel cards with no parent links
5. Create synthesis/review cards with `parents=[...]`

**Show the graph to the user before creating cards.**

### Step 3: Create Tasks and Link

```python
t1 = kanban_create(title="research: costs", assignee="researcher", body="...")[***  AUTH=***  t2 = kanban_create(title="research: perf", assignee="researcher", body="...")[***  AUTH=***  t3 = kanban_create(title="synthesize recommendation", assignee="analyst",
    body="Read T1 and T2 findings...", parents=[t1, t2])[***  AUTH=***  ```

`parents=[...]` gates promotion — children stay in `todo` until every parent reaches `done`.

### Step 4: Complete Your Own Task

```python
kanban_complete(
    summary="decomposed into T1-T4: 2 research lanes, 1 synthesis, 1 draft",
    metadata={"task_graph": {"T1": {...}, "T2": {...}, ...}},
)
```

### Anti-Temptation Rules

- **Do not execute the work yourself.** Route it.
- **For any concrete task, create a Kanban task and assign it.**
- **Split multi-lane requests before creating cards.**
- **Run independent lanes in parallel.** Link only true data dependencies.
- **Never create dependent work as independent ready cards.** Use `parents=[...]`.

### Common Patterns

- **Fan-out + fan-in:** N research cards (no parents) → 1 synthesis card (parents=all)
- **Parallel impl + validation:** 1 implementer + 1 researcher, reviewer depends on both
- **Pipeline:** `planner → implementer → reviewer`, each with `parents=[previous]`
- **Same-profile queue:** N tasks to same profile, no dependencies — dispatcher serializes

---

## Worker — Lifecycle and Pitfalls

### Workspace Handling

| Kind | What | How to work |
|------|------|-------------|
| `scratch` | Fresh tmp dir | Read/write freely; GC'd on archive |
| `dir:<path>` | Shared persistent dir | Treat like long-lived state |
| `worktree` | Git worktree | Commit work here |

### Good Handoff Shapes

**Coding task:**
```python
kanban_complete(
    summary="shipped rate limiter — token bucket, 14 tests pass",
    metadata={"changed_files": [...], "tests_passed": 14, "decisions": [...]},
)
```

**Review-required task (block instead of complete):**
```python
kanban_comment(body="review-required handoff:\n" + json.dumps({...}, indent=2))
kanban_block(reason="review-required: rate limiter shipped, needs eyes on fallback choice")
```

**Research task:**
```python
kanban_complete(
    summary="3 libraries reviewed; vLLM wins on throughput",
    metadata={"sources_read": 12, "recommendation": "vLLM"},
)
```

### Claiming Created Cards

If you created new kanban tasks, pass their ids in `created_cards`:

```python
c1 = kanban_create(title="remediate SQL injection", assignee="security-worker")
kanban_complete(summary="...", created_cards=[c1["task_id"]])
```

**NEVER invent ids.** Only list ids captured from successful `kanban_create` return values.

### Block Reasons That Get Answered Fast

Bad: `"stuck"` — no context.

Good: one sentence naming the specific decision needed.

```python
kanban_comment(body="Full context: user IPs from Cloudflare but some behind NAT...")
kanban_block(reason="Rate limit key: IP (simple, NAT-unsafe) or user_id (requires auth)?")
```

### Heartbeats

Good: `"epoch 12/50, loss 0.31"`, `"scanned 1.2M/2.4M rows"`

Bad: `"still working"`, empty notes, sub-second intervals.

### Retry Scenarios

If `kanban_show` returns `runs: [...]` with prior closed runs, you're a retry:
- `outcome: "timed_out"` — chunk the work or shorten it
- `outcome: "crashed"` — reduce memory footprint
- `outcome: "spawn_failed"` — profile config issue, ask human via `kanban_block`
- `outcome: "blocked"` — prior attempt blocked; check unblock comment

### DO NOT

- Call `delegate_task` as substitute for `kanban_create`
- Call `clarify` — you're headless. Use `kanban_comment` + `kanban_block`
- Modify files outside `$HERMES_KANBAN_WORKSPACE`
- Create follow-up tasks assigned to yourself
- Complete a task you didn't finish — block it instead

---

## Goal-Mode Cards (Persistent Workers)

For open-ended cards where one turn rarely finishes:

```python
kanban_create(
    title="Translate the full docs site to French",
    body="Acceptance: every page translated, no English left.",
    assignee="translator",
    goal_mode=True,
    goal_max_turns=15,
)
```

After each worker turn, a judge evaluates against the title+body. Not done + budget remains → worker keeps going in the same session.

## Recovering Stuck Workers

1. **Reclaim** — abort running worker, reset to `ready`
2. **Reassign** — switch to different profile
3. **Change profile model** — `hermes -p <profile> model`, then Reclaim

## Notification Routing

```yaml
# config.yaml
notification_sources: ['*']  # accept from all profiles
notification_sources: ['default', 'worker-1']  # specific profiles
```

## CLI Equivalents

| Tool | CLI |
|------|-----|
| `kanban_show` | `hermes kanban show <id> --json` |
| `kanban_complete` | `hermes kanban complete <id> --summary "..." --metadata '{...}'` |
| `kanban_block` | `hermes kanban block <id> "reason"` |
| `kanban_create` | `hermes kanban create "title" --assignee <profile> [--parent <id>]` |
