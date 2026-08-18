# Legacy x-cli Reference (Archived)

> Absorbed from `xitter` skill (archived 2026-06-21). xurl is the successor tool.

## x-cli (Third-Party Python CLI)

**Install:** `uv tool install git+https://github.com/Infatoshi/x-cli.git`

**Credentials:** 5 env vars in `~/.config/x-cli/.env`:
- `X_API_KEY`, `X_API_SECRET`, `X_BEARER_TOKEN`, `X_ACCESS_TOKEN`, `X_ACCESS_TOKEN_SECRET`

**Quick commands:**
```bash
x-cli tweet post "hello world"
x-cli tweet search "AI agents" --max 20
x-cli user get openai
x-cli me mentions --max 20
x-cli like 1234567890
x-cli retweet 1234567890
```

**Output modes:** `-j` (JSON), `-p` (pretty), `-md` (markdown), `-v` (verbose)

**Why xurl replaced this:** xurl is maintained by X developer platform, supports OAuth 2.0 PKCE with auto-refresh, and covers a substantially larger API surface.
