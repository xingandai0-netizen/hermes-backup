# Multiline Edit Pitfalls

## Problem: sed multiline replacements corrupt files

When using `sed` for multiline replacements in TypeScript/JavaScript files, the command can fail silently or corrupt the file with duplicate line numbers.

**Symptom**: File has lines like `1|"use client";` instead of `"use client";`

**Cause**: `sed` doesn't handle multiline patterns well in macOS. The `read_file` tool returns content with line numbers, and `write_file` writes them back.

## Solution: Use patch tool or Python script

### Option 1: Use patch tool (preferred)
```python
patch(path, old_string, new_string)
```

### Option 2: Use Python script with proper line handling
```python
from hermes_tools import read_file, write_file

result = read_file("path/to/file.tsx")
content = result["content"]

# Strip line numbers if present
lines = content.split("\n")
fixed_lines = []
for line in lines:
    if "|" in line:
        parts = line.split("|", 2)
        if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit():
            fixed_lines.append(parts[2])
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

content = "\n".join(fixed_lines)
write_file("path/to/file.tsx", content)
```

## Verification

After any multiline edit:
1. Run `npx tsc --noEmit` to check TypeScript
2. Check first 10 lines of file for corruption
3. If corrupted, use `git checkout <file>` to restore and retry with patch

## Key Lesson

**Never use `sed` for multiline replacements on TypeScript files.** Use `patch` tool instead - it handles context matching correctly.
