# DeepSeek Code Review Patterns

## Typical Issues Found During Review

### P0 Blockers (must fix)
1. **API Key exposed to frontend** — remove apiKey from settings store, all requests through backend
2. **Credit deduction without transaction protection** — use Supabase RPC atomic operation
3. **Stripe webhook not bound to user** — pass metadata when creating Checkout Session
4. **OAuth callback no error handling** — add try-catch, redirect to login on failure

### P1 Performance Issues
1. **Global state subscription** — use atomFamily for precise subscriptions
2. **Stale useCallback closures** — remove unnecessary dependencies, use useRef
3. **useMemo cache return values** — avoid returning new objects causing re-renders
4. **viewportAtom subscription** — use store.get() instead of useAtom

### P2 Architecture Issues
1. **Inconsistent field paths** — unify to top-level assetUrl
2. **Unused dependencies** — remove zustand
3. **Code duplication** — extract useAssetUpload Hook
4. **Direct client upload** — unify through backend /api/upload

### P3 Robustness
1. **any types** — use concrete types
2. **Uncleaned timers** — add useEffect cleanup
3. **Error boundaries** — wrap ReactFlow

## DeepSeek Review Scoring Dimensions

| Dimension | Max | Focus |
|-----------|-----|-------|
| Type safety | 10 | No `as NodeData`, correct generics |
| Error handling | 10 | Upload failure prompts, API error handling |
| Performance | 10 | atomFamily, React.memo |
| Maintainability | 10 | Clean code, single responsibility |

## Iterative Review Flow

```
Round 1: Initial review → find 10-15 issues
Round 2: Post-fix verification → confirm most resolved
Round 3: Final review → confirm commercial baseline
Round 4: Backend review → find 5-8 issues
Round 5: Backend fix → confirm backend usable
Round 6: Final production → DeepSeek provides complete code
```

## Module File Generation Template

```bash
# Generate module file
cat > /tmp/antoken-final-v{N}-module{M}.txt << 'EOF'
# Module {M}: {Module Name} ({Version})

## Changes This Round
- Change 1 (specific description)
- Change 2 (specific description)

## {filename}
```tsx
{complete code}
```
EOF

# Copy to clipboard
cat /tmp/antoken-final-v{N}-module{M}.txt | pbcopy
```
