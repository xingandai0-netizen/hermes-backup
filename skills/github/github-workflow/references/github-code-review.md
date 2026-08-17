# GitHub Code Review

## Pre-Push Review

```bash
git diff main...HEAD --stat
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|FIXME"
git diff main...HEAD | grep -in "password\|secret\|api_key"
```

## Review Output Format

```
## Code Review Summary
### Critical
- **file:line** — Issue. Suggestion.
### Warnings
- **file:line** — Issue.
### Suggestions
- **file:line** — Suggestion.
### Looks Good
- Positive notes.
```

## PR Review (gh)

```bash
gh pr view 123
gh pr diff 123
gh pr review 123 --approve --body "LGTM!"
gh pr review 123 --request-changes --body "See inline comments."
```

## Inline Comments (curl)

```bash
HEAD_SHA=*** Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/123/comments \
  -d '{"body":"...","path":"src/auth.py","commit_id":"'$HEAD_SHA'","line":45,"side":"RIGHT"}'
```

## Review Checklist

- Correctness: edge cases, error handling
- Security: no hardcoded secrets, input validation, no SQL injection/XSS
- Code Quality: clear naming, DRY, single responsibility
- Testing: new paths tested, happy + error cases
- Performance: no N+1, appropriate caching
- Documentation: public APIs documented, non-obvious logic commented
