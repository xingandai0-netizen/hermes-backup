#!/usr/bin/env python3
"""Add Chrome DevTools MCP server to Hermes config.yaml"""
import os

config_path = os.path.expanduser("~/.hermes/config.yaml")

with open(config_path) as f:
    config = f.read()

# Find the servers: {} line and replace it
old = "  servers: {}"
new = """  servers:
    chrome-devtools:
      command: npx
      args:
      - "-y"
      - "chrome-devtools-mcp@latest"
      - "--autoConnect"
      description: "Chrome DevTools MCP - AI browser automation for security testing"
    vulnclaw-chrome:
      command: vulnclaw
      args:
      - "mcp"
      - "chrome"
      description: "VulnClaw Chrome DevTools MCP - pentest browser automation"
    vulnclaw-burp:
      command: vulnclaw
      args:
      - "mcp"
      - "burp"
      description: "VulnClaw Burp MCP - HTTP intercept and replay"
    pentest-mcp:
      command: python3
      args:
      - "~/security-research/pentestMCP/pentestMCP.py"
      description: "pentestMCP - 20+ security tools via MCP protocol"
      disabled: true"""

if old in config:
    config = config.replace(old, new)
    with open(config_path, 'w') as f:
        f.write(config)
    print("SUCCESS: MCP servers added to config.yaml")
else:
    print("ERROR: Could not find 'servers: {}' in config.yaml")
    # Check if servers already configured
    if "chrome-devtools:" in config:
        print("Chrome DevTools MCP already configured")
    else:
        print("Manual config needed")
