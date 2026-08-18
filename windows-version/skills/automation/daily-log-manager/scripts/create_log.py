#!/usr/bin/env python3
"""Create daily log directory and write log file."""
import os
import sys

log_dir = os.path.expanduser("~/.hermes/daily-logs/2026/06")
os.makedirs(log_dir, exist_ok=True)
print(f"Directory: {log_dir}")

log_path = os.path.join(log_dir, "2026-06-03.md")
content = sys.stdin.read()
with open(log_path, 'w') as f:
    f.write(content)
print(f"Written: {log_path} ({len(content)} chars)")
