# IDA Pro MCP vs Ghidra MCP — Detailed Comparison

## Summary Scorecard

| Category | Winner | Margin |
|---|---|---|
| Tool count | **Ghidra MCP** | 253 vs 97 — 2.6x more |
| Decompilation quality | **IDA Pro MCP** | Hex-Rays is industry-leading |
| Cross-reference analysis | **IDA Pro MCP** | `find_path` + `xref_sig` are unique |
| Type/struct manipulation | **Tie / Ghidra MCP** | Ghidra has more CRUD tools; IDA has better inference |
| Memory operations | **Tie** | Different strengths, both capable |
| Debugging capabilities | **Tie** | IDA: more register detail; Ghidra: P-code emulation + ASLR |
| Scripting/automation | **Ghidra MCP** | Built-in workflows + convention enforcement |
| Batch/headless | **Ghidra MCP** | Free, Docker, multi-program, Ghidra Server |
| Platform support | **Tie** | Both cross-platform; Ghidra is free |
| Community/ecosystem | **Ghidra MCP** | 3.2K stars, 1000+ commits, active RFCs |

## When to Choose Which

- **IDA Pro MCP**: already have IDA Pro licenses, need Hex-Rays decompilation quality, want signature generation, commercial RE shop
- **Ghidra MCP**: cost matters, need headless/CI/Docker, want largest tool surface, cross-binary documentation, prefer open-source

## IDA Pro MCP Unique Features
- `find_path(from, to, max_depth)` — BFS shortest path between functions
- `xref_sig` — generate signatures for all xrefs to address
- `create_sig` / `scan_sig` — FLIRT signature maker
- MCP Resources model (`ida://idb/metadata`, etc.)
- Hex-Rays type inference with confidence scoring
- `py_eval` / `py_exec_file` — unrestricted Python with full IDA SDK

## Ghidra MCP Unique Features
- P-code emulation (`emulate_function`, `emulate_hash_batch`) — run functions without live process
- ASLR translation (`debugger_dynamic_to_static`)
- Cross-binary documentation (`bulk_fuzzy_match`, `archive_ingest_function`)
- Ghidra Server integration (version control, checkout)
- Hungarian notation enforcement
- 7 built-in AI documentation workflows
- Docker-ready headless operation
- 288 total tools (253 Ghidra + 22 WinDbg proxy + 5 oracle + 8 bridge)

## IDA Pro Known Vulnerabilities (for research)

| CVE | CVSS | Type | Affected |
|-----|------|------|----------|
| CVE-2026-45181 | 6.5 | RCE via argument injection in .i64 files | IDA Pro 9.2/9.3 < 9.3sp2 |
| CVE-2024-44083 | 7.5 | DoS via resource allocation | IDA Pro ≤ 8.4 |
| CVE-2011-4783 | N/A | IDAPython arbitrary code execution | IDAPython < 1.5.2.3 |
| ida-pro-mcp #201 | 9.4 | py_eval RCE via DNS rebinding | MCP server (fixed) |
