---
name: mcp-integration
description: "Model Context Protocol (MCP) integration: native MCP client configuration and mcporter CLI for ad-hoc server interaction. Connect servers, register tools, and call MCP tools directly."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mcp, model-context-protocol, tools, servers, integration, mcporter]
---

# MCP Integration

Connect to Model Context Protocol (MCP) servers for extended tool access. Two approaches: native MCP client (configured in config.yaml) and mcporter CLI (ad-hoc interaction).

## When to Use

- Connecting to MCP servers (databases, APIs, services)
- Registering MCP tools for the agent to use
- Testing or debugging MCP server connections
- Ad-hoc MCP tool calls without permanent configuration

---

## 1. Native MCP Client (Persistent)

Configure MCP servers in `~/.hermes/config.yaml` for automatic tool discovery.

### Configuration

```yaml
mcp:
  servers:
    github:
      command: npx
      args: ["-y", "@modelcontextprotocol/server-github"]
      env:
        GITHUB_TOKEN: "${GITHUB_TOKEN}"
    postgres:
      command: npx
      args: ["-y", "@anthropic-ai/server-postgres", "--connection-string", "postgresql://localhost/mydb"]
    filesystem:
      command: npx
      args: ["-y", "@anthropic-ai/server-filesystem", "/path/to/allowed/dir"]
```

### Server Types

| Transport | Config | Use Case |
|-----------|--------|----------|
| `stdio` | `command` + `args` | Local process (most common) |
| `http` | `url` | Remote HTTP server |
| `sse` | `url` | Server-Sent Events |

### Management Commands

```bash
hermes mcp add NAME --command "npx" --args "-y,@modelcontextprotocol/server-github"
hermes mcp list
hermes mcp test NAME
hermes mcp remove NAME
hermes mcp configure NAME  # Toggle tool selection
```

### Reload in Session

```
/reload-mcp
```

---

## 2. mcporter CLI (Ad-Hoc)

Use `mcporter` for one-off MCP server interaction without permanent configuration.

### Install

```bash
npm install -g mcporter
```

### Usage

```bash
# List available tools on a server
mcporter list --command "npx -y @modelcontextprotocol/server-github"

# Call a tool
mcporter call --command "npx -y @modelcontextprotocol/server-github" \
  --tool create_issue \
  --args '{"owner":"user","repo":"myrepo","title":"Bug report","body":"..."}'

# Configure a server interactively
mcporter configure

# Test connection
mcporter test --url "http://localhost:3001"
```

### Common Use Cases

- **Quick database query:** `mcporter call --command "npx -y @anthropic-ai/server-postgres ..." --tool query --args '{"sql":"SELECT * FROM users LIMIT 5"}'`
- **File operations:** `mcporter call --command "npx -y @anthropic-ai/server-filesystem /tmp" --tool read_file --args '{"path":"/tmp/test.txt"}'`
- **GitHub API:** Create issues, search repos, manage PRs via GitHub MCP server

---

## 3. Common MCP Servers

| Server | Package | Tools |
|--------|---------|-------|
| GitHub | `@modelcontextprotocol/server-github` | search, create_issue, list_prs |
| PostgreSQL | `@anthropic-ai/server-postgres` | query, list_tables |
| Filesystem | `@anthropic-ai/server-filesystem` | read_file, write_file, list_directory |
| Puppeteer | `@anthropic-ai/server-puppeteer` | navigate, screenshot, click |
| Brave Search | `@modelcontextprotocol/server-brave-search` | search |
| Google Maps | `@modelcontextprotocol/server-google-maps` | places, directions |

---

## Pitfalls

- **MCP servers are subprocesses** — they consume memory and CPU while running
- **Tool descriptions have size limits** — MCP caps at ~2KB per server
- **stdio transport blocks** — only one request at a time per server process
- **Environment variables** — MCP servers inherit the agent's env; secrets in config.yaml use `${VAR}` syntax
- **Reload required** — `/reload-mcp` or `/reset` after changing MCP config
- **mcporter ≠ native MCP** — mcporter is for ad-hoc calls; native MCP registers tools permanently for the session
