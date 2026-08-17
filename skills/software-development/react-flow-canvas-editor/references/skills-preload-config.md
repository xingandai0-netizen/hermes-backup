# Skills Auto-Load Configuration

## Problem
When building projects that benefit from design/UX skills (taste-skill, popular-web-designs, etc.), having to manually load them every session is wasteful. The user may demand: "设置成每次打开对话强制启动" (force load on every session start).

## Solution
```bash
hermes config set skills.preload superpowers,writing-plans,design-taste-system,taste-skill,popular-web-designs,baseline-ui
```

This adds to `~/.hermes/config.yaml`:
```yaml
skills:
  preload: superpowers,writing-plans,design-taste-system,taste-skill,popular-web-designs,baseline-ui
```

## Key Skills for UI Projects
- `taste-skill` — Anti-slop rules (no emoji, no neon colors, no generic cards)
- `popular-web-designs` — 54 real design systems (Linear, Vercel, Stripe, etc.)
- `design-taste-system` — Design taste engine
- `baseline-ui` — UI baseline checker
- `superpowers` — General agent capabilities
- `writing-plans` — Planning and documentation

## Verification
```bash
hermes config get skills.preload
# Should output the comma-separated list
```
