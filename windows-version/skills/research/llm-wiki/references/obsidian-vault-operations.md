# Obsidian Vault Operations

Filesystem-first Obsidian vault operations: reading, listing, searching, creating, and editing notes.

## Vault Path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `${HERMES_HOME:-~/.hermes}/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Read a note

Use `read_file` with the resolved absolute path. Prefer over `cat` for line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path.

- All markdown notes: `pattern: "*.md"` under vault path
- Subfolder: search under that subfolder's absolute path

## Search

- Filenames: `search_files` with `target: "files"` and filename `pattern`
- Contents: `search_files` with `target: "content"`, regex as `pattern`, `file_glob: "*.md"`

## Create a note

Use `write_file` with resolved absolute path and full markdown content.

## Append to a note

- Read target with `read_file`
- Use `patch` for anchored append (after heading, before trailing block)
- Use `write_file` when rewriting whole note is clearer

## Targeted edits

Use `patch` for focused changes when current content gives stable context.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. Use when creating notes to link related content.
