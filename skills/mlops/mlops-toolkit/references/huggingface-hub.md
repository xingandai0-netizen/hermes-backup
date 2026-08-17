# HuggingFace CLI (`hf`) Reference

The `hf` command is the modern CLI for interacting with HuggingFace Hub. Replaces deprecated `huggingface-cli`.

## Install

```bash
curl -LsSf https://hf.co/cli/install.sh | bash -s
```

## Core Commands

### Download/Upload
- `hf download REPO_ID` — Download files from Hub
- `hf upload REPO_ID` — Upload files/folders (single-commit)
- `hf upload-large-folder REPO_ID LOCAL_PATH` — Resumable uploads of large directories
- `hf sync` — Sync local directory with bucket

### Authentication
- `hf auth login` / `hf auth logout` — Manage sessions
- `hf auth list` / `hf auth switch` — Toggle between tokens
- `hf auth whoami` — Current account

### Repository Management
- `hf repos create` / `hf repos delete` — Create/remove repos
- `hf repos duplicate` — Clone to new ID
- `hf repos move` — Transfer between namespaces
- `hf repos branch` / `hf repos tag` — Git-like references

### Datasets & Models
- `hf datasets list`, `info`, `parquet` — Dataset operations
- `hf datasets sql SQL` — Raw SQL via DuckDB against parquet URLs
- `hf models list`, `info` — Model operations
- `hf papers list` — Daily papers

### Discussions & PRs
- `hf discussions list`, `create`, `comment`, `close`, `merge`
- `hf discussions diff` — View PR changes

### Infrastructure
- **Endpoints**: `hf endpoints deploy`, `pause`, `resume`, `scale-to-zero`
- **Jobs**: `hf jobs uv` for Python scripts with inline dependencies
- **Spaces**: `hf spaces dev-mode`, `hot-reload`

### Storage
- **Buckets**: `hf buckets create`, `cp`, `mv`, `rm`, `sync`
- **Cache**: `hf cache list`, `prune`, `verify`
- **Webhooks**: `hf webhooks create`, `watch`, `enable`/`disable`
- **Collections**: `hf collections add-item`, `update`, `list`

## Global Flags

- `--format json` — Machine-readable output
- `-q` / `--quiet` — IDs only

## Extensions & Skills

- `hf extensions install REPO_ID` — Extend CLI via GitHub repos
- `hf skills add` — Manage AI assistant skills
