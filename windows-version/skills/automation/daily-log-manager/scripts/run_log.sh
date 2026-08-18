#!/bin/bash
set -e
mkdir -p ~/.hermes/daily-logs/2026/06/
python3 /Users/macpro/.hermes/skills/automation/daily-log-manager/scripts/write_log_20260603.py
ls -la ~/.hermes/daily-logs/2026/06/2026-06-03.md
echo "DONE"
