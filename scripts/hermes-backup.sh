#!/bin/bash
# Hermes daily backup to private GitHub repo
# xingandai0-netizen/hermes-backup
# Excludes: rebuildable code, temp files, secrets

set -euo pipefail

BACKUP_DIR="$HOME/.hermes/.backup-repo"
SRC_DIR="$HOME/.hermes"

echo "[$(date '+%H:%M:%S')] Starting backup..."

# --- Clone or update repo ---
if [ -d "$BACKUP_DIR/.git" ]; then
  cd "$BACKUP_DIR"
  git fetch origin main 2>/dev/null || git fetch origin master 2>/dev/null || true
  BRANCH=$(git remote show origin 2>/dev/null | grep 'HEAD branch' | awk '{print $NF}' || echo "main")
  git reset --hard "origin/$BRANCH" 2>/dev/null || true
  git clean -fd
else
  rm -rf "$BACKUP_DIR"
  gh repo clone xingandai0-netizen/hermes-backup "$BACKUP_DIR" 2>/dev/null || {
    git clone "https://github.com/xingandai0-netizen/hermes-backup.git" "$BACKUP_DIR"
  }
  cd "$BACKUP_DIR"
fi

# --- Gitignore for safety ---
cat > .gitignore <<'EOF'
.env
.backup-repo
*.db
*.db-wal
*.db-shm
EOF

# --- Rsync: only valuable, non-rebuildable data ---
rsync -a --delete \
  --exclude='.env' \
  --exclude='.backup-repo' \
  --exclude='.git' \
  --exclude='hermes-agent/' \
  --exclude='node/' \
  --exclude='checkpoints/' \
  --exclude='cache/' \
  --exclude='logs/' \
  --exclude='bin/' \
  --exclude='audio_cache/' \
  --exclude='pastes/' \
  --exclude='shared-memory/' \
  --exclude='memories/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='*.db' \
  --exclude='*.db-wal' \
  --exclude='*.db-shm' \
  --exclude='.DS_Store' \
  "$SRC_DIR/" "$BACKUP_DIR/"

# --- Commit and push ---
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S %Z')
git add -A

if git diff --cached --quiet; then
  echo "[$(date '+%H:%M:%S')] No changes — skip."
  exit 0
fi

git -c user.name="Hermes Backup" \
    -c user.email="backup@hermes.local" \
    commit -m "Daily backup — $TIMESTAMP"

echo "[$(date '+%H:%M:%S')] Pushing to GitHub..."
git push origin HEAD 2>&1

echo "[$(date '+%H:%M:%S')] Backup done ✓"
