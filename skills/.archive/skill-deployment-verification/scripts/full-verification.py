#!/usr/bin/env python3
"""
Hermes 全量验证脚本 — MCP/Skills/工具链/路由 一站式检查。
用法: python3 ~/.hermes/skills/software-development/skill-deployment-verification/scripts/full-verification.py
"""
import yaml, os, subprocess

config_path = os.path.expanduser("~/.hermes/config.yaml")
config = yaml.safe_load(open(config_path))

print("=" * 60)
print("HERMES 全量验证报告")
print("=" * 60)

# 1. MCP Servers
print("\n[1] MCP SERVERS")
mcp = config.get("mcp_servers", {})  # 注意：是 mcp_servers 不是 mcp.servers
if not mcp:
    print("  ❌ 无MCP servers配置")
else:
    for name, cfg in mcp.items():
        disabled = cfg.get("disabled", False)
        cmd = cfg.get("command", "?")
        args = cfg.get("args", [])
        status = "⏸️ disabled" if disabled else "✅ enabled"
        print(f"  {status} {name}: {cmd} {' '.join(args[:3])}")

# 2. 安全工具链（按需修改）
print("\n[2] 安全工具链")
tools = {
    "nmap": "nmap --version 2>&1 | head -1",
    "nuclei": "nuclei -version 2>&1 | head -1",
    "subfinder": "subfinder -version 2>&1 | head -1",
    "ffuf": "ffuf -V 2>&1 | head -1",
    "sqlmap": "sqlmap --version 2>&1 | head -1",
    "lldb": "lldb --version 2>&1 | head -1",
    "java": "java -version 2>&1 | head -1",
}
for name, check in tools.items():
    try:
        r = subprocess.run(check, shell=True, capture_output=True, text=True, timeout=5)
        out = (r.stdout + r.stderr).strip().split("\n")[0][:60]
        print(f"  ✅ {name}: {out}")
    except:
        print(f"  ❌ {name}: not found")

# 3. Python MCP模块（按需修改模块列表）
print("\n[3] Python MCP模块")
modules = ["lldb_mcp.server", "lldb_mcp.memscan_server"]
for mod in modules:
    try:
        __import__(mod)
        print(f"  ✅ {mod}")
    except Exception as e:
        print(f"  ❌ {mod}: {e}")

# 4. System prompt routing
print("\n[4] SYSTEM PROMPT路由")
append = config.get("agent", {}).get("system_prompt_append", "")
print(f"  总长度: {len(append)} chars")
markers = {
    "skill_view": "skill_view调用",
    "skills_list": "skills_list扫描",
    "reverse-skill-router": "安全路由",
    "pentest-pipeline": "渗透管线",
    "superpowers": "开发workflow",
    "tdd-bdd": "TDD强制",
    "emilkowalski": "Apple设计",
    "taste-skill": "品味引擎",
    "agency-agents": "Agent人格",
    "G0DM0D3": "安全策略",
}
for marker, desc in markers.items():
    count = append.count(marker)
    status = "✅" if count > 0 else "❌"
    print(f"  {status} {desc}: {count}次引用")

# 5. Skills统计
print("\n[5] SKILLS统计")
skills_dir = os.path.expanduser("~/.hermes/skills")
total = 0
categories = {}
for root, dirs, files in os.walk(skills_dir):
    if "SKILL.md" in files:
        rel = os.path.relpath(root, skills_dir)
        cat = rel.split("/")[0] if "/" in rel else "root"
        categories[cat] = categories.get(cat, 0) + 1
        total += 1
print(f"  总数: {total}")
for cat, count in sorted(categories.items(), key=lambda x: -x[1])[:10]:
    print(f"    {cat}: {count}")

# 6. Index files
print("\n[6] 索引文件")
for f in ["INTENT-ROUTES.md", "SKILL-INDEX.md", "INDEX.json"]:
    path = os.path.join(skills_dir, f)
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"  ✅ {f} ({size} bytes)")
    else:
        print(f"  ❌ {f}: NOT FOUND")

# 7. Config integrity
print("\n[7] 配置完整性")
print(f"  config版本: {config.get('_config_version', '?')}")
print(f"  approvals.mode: {config.get('approvals', {}).get('mode', 'default')}")
print(f"  tirith: {config.get('security', {}).get('tirith_enabled', '?')}")
print(f"  redact_secrets: {config.get('security', {}).get('redact_secrets', '?')}")

print("\n" + "=" * 60)
print("验证完成")
