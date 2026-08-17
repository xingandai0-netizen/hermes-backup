# Antoken Wheel Scroll Bug (UNRESOLVED — 2026-06-29)

## Problem
When scrolling the mouse wheel inside TextNode's textarea, the canvas also scrolls.

## Tried Solutions (all ineffective)
1. `onWheel={(e) => e.stopPropagation()}`
2. `addEventListener + { passive: false } + e.preventDefault()`
3. `useEffect + addEventListener + manual scrollTop`
4. Adding `onWheel={(e) => e.stopPropagation()}` to container div

## Key Findings
- MentionInput (in dialog) works correctly
- TextNode textarea (in node card) does NOT work
- Difference: dialog has `data-dialog="true"`

## Possible Root Cause
1. ReactFlow captures wheel events at canvas level
2. Event bubbling path differs (dialog vs node card)

## References
- MentionInput: ref callback + addEventListener + { passive: false }
- ImageNode dialog: onWheel={(e) => e.stopPropagation()}
