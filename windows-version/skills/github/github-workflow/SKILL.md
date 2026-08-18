---
name: github-workflow
description: "Complete GitHub workflow via gh CLI and REST API: authentication, repository management, issues, pull requests, code review, and CI/CD."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Git, gh-cli, Pull-Requests, Issues, Code-Review, CI/CD, Repositories, Authentication]
    related_skills: [hermes-github-backup]
---

# GitHub Workflow

Complete guide for working with GitHub repositories via the `gh` CLI and REST API. Covers the full lifecycle: authentication, repo management, issues, PRs, code review, and CI/CD.

## When to Use

- Creating, cloning, forking, or configuring GitHub repos
- Managing issues (create, triage, label, assign, close)
- PR lifecycle (branch, commit, open, review, merge)
- Code review (local diff review, PR review with inline comments)
- CI/CD monitoring and auto-fixing
- Releases, secrets, and GitHub Actions management

## Prerequisites

All sections assume GitHub authentication. Run this detection block first:

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi

REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

**Every section shows `gh` first, then the `git` + `curl` fallback.**

---

## 1. Authentication

See [references/github-auth.md](references/github-auth.md) for the full auth setup guide (HTTPS tokens, SSH keys, gh CLI login, token extraction, troubleshooting).

**Quick path:**
- `gh auth login` for interactive browser login
- `echo "$TOKEN" | gh auth login --with-token` for headless
- `git config --global credential.helper store` for git-only HTTPS

---

## 2. Repository Management

See [references/github-repo-management.md](references/github-repo-management.md) for the full reference (clone, create, fork, settings, branch protection, secrets, releases, Actions workflows, gists).

**Quick commands:**

| Action | gh | git + curl |
|--------|-----|-----------|
| Clone | `gh repo clone o/r` | `git clone https://github.com/o/r.git` |
| Create | `gh repo create name --public` | `curl POST /user/repos` |
| Fork | `gh repo fork o/r --clone` | `curl POST /repos/o/r/forks` |
| Release | `gh release create v1.0` | `curl POST /repos/o/r/releases` |

---

## 3. Issues Management

See [references/github-issues.md](references/github-issues.md) for the full reference (view, create, manage, triage, bulk operations).

**Quick commands:**

| Action | gh | curl endpoint |
|--------|-----|--------------|
| List | `gh issue list` | `GET /repos/{o}/{r}/issues` |
| Create | `gh issue create ...` | `POST /repos/{o}/{r}/issues` |
| Label | `gh issue edit N --add-label ...` | `POST /repos/{o}/{r}/issues/N/labels` |
| Close | `gh issue close N` | `PATCH /repos/{o}/{r}/issues/N` |

**Templates:** [templates/bug-report.md](templates/bug-report.md), [templates/feature-request.md](templates/feature-request.md)

---

## 4. Pull Request Workflow

See [references/github-pr-workflow.md](references/github-pr-workflow.md) for the full lifecycle (branch creation, commits, push, create PR, monitor CI, auto-fix failures, merge).

**Quick commands:**

| Action | gh | git + curl |
|--------|-----|-----------|
| Create PR | `gh pr create --title "..." --body "..."` | `curl POST /repos/o/r/pulls` |
| Check CI | `gh pr checks --watch` | `curl GET /repos/o/r/commits/SHA/status` |
| Merge | `gh pr merge --squash --delete-branch` | `curl PUT /repos/o/r/pulls/N/merge` |
| View diff | `gh pr diff N` | `git diff main...HEAD` |

**PR templates:** [templates/pr-body-feature.md](templates/pr-body-feature.md), [templates/pr-body-bugfix.md](templates/pr-body-bugfix.md)

**CI troubleshooting:** [references/ci-troubleshooting.md](references/ci-troubleshooting.md)
**Conventional commits:** [references/conventional-commits.md](references/conventional-commits.md)

---

## 5. Code Review

See [references/github-code-review.md](references/github-code-review.md) for the full review workflow (local pre-push review, PR review, inline comments, formal approve/request-changes).

### Pre-Push Review Checklist

```bash
# Get scope
git diff main...HEAD --stat
git log main..HEAD --oneline

# Check for issues
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|FIXME\|debugger"
git diff main...HEAD | grep -in "password\|secret\|api_key\|token.*=\|private_key"
```

### Review Output Format

```
## Code Review Summary
### Critical
- **file:line** — Issue description. Suggestion.
### Warnings
- **file:line** — Issue description.
### Suggestions
- **file:line** — Suggestion.
### Looks Good
- Positive observations.
```

### Submit Review (gh)

```bash
gh pr review 123 --approve --body "LGTM!"
gh pr review 123 --request-changes --body "See inline comments."
```

**Review output template:** [references/review-output-template.md](references/review-output-template.md)

---

## 6. Auth Detection Helper Script

See [scripts/gh-env.sh](scripts/gh-env.sh) — source this at the start of any GitHub workflow to set up `AUTH`, `GITHUB_TOKEN`, `OWNER`, and `REPO` variables.

---

## Pitfalls

### Private Repo Raw Download Returns 404
**Problem**: `raw.githubusercontent.com/OWNER/REPO/main/file` returns 404 for private repos.
**Solution**: Use `gh api` to download, or `git clone` + copy, or make repo public.
```bash
# Download single file from private repo via gh CLI
gh api repos/OWNER/REPO/contents/path/to/file --jq '.content' | base64 -d > local-file

# Or clone and copy
git clone https://github.com/OWNER/REPO.git /tmp/repo
cp /tmp/repo/path/to/file ./local-file
```

### gh repo edit --visibility Requires Extra Flag
**Problem**: `gh repo edit --visibility public` fails with "requires --accept-visibility-change-consequences flag".
**Solution**: Add the flag: `gh repo edit OWNER/REPO --visibility public --accept-visibility-change-consequences`
**Note**: Token must have admin permissions on the repo. If 403, change visibility via GitHub web UI.

### Token Type Mismatch (Cannot Create Repos)
**Problem**: `gh repo create` fails with "Resource not accessible by personal access token" even though authenticated.
**Diagnosis**: Check `gh auth status` — if token starts with `github_pat_` (fine-grained), it cannot create repos. Need `ghp_` (classic) with `repo` scope.
**Fix**: Generate classic token at https://github.com/settings/tokens (select "Tokens classic"), check `repo` scope. See `cross-machine-ai-deployment` skill's `references/github-token-types.md` for full comparison.

### Push Fails Due to Large Files in node_modules
**Problem**: `git push` rejected with "file exceeds GitHub's file size limit of 100MB" — usually `node_modules` or `.next` was committed.
**Fix**: Add `.gitignore` before first commit. If already committed: `rm -rf .git && git init && git add -A && git commit -m "clean" && git push --force`.

## Quick Decision Guide

| Task | Section |
|------|---------|
| Set up GitHub access | §1 Authentication |
| Create/clone/fork/configure repos | §2 Repo Management |
| Bug reports, feature requests, triage | §3 Issues |
| Branch → commit → PR → merge | §4 PR Workflow |
| Review code changes | §5 Code Review |
| All of the above with `gh` CLI | Any section — `gh` always shown first |
