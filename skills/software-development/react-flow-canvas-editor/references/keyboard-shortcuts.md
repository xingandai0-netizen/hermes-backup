# Keyboard Shortcut Patterns

## Delete Key Handling

### Problem
Delete key doesn't work when focus is on input/textarea elements.

### Solution
Smart handling that checks if input has content.

```typescript
useEffect(() => {
  const handler = (e: KeyboardEvent) => {
    const target = e.target as HTMLElement;
    const tag = target.tagName;
    const isInputFocused = tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT";
    
    // Delete / Backspace
    if ((e.key === "Delete" || e.key === "Backspace") && selectedNodeId) {
      // If focus is on input, check if input is empty
      if (isInputFocused) {
        const inputValue = (target as HTMLInputElement | HTMLTextAreaElement).value;
        // Only delete node if input is empty
        if (inputValue && inputValue.length > 0) {
          return; // Input has content, don't delete node
        }
      }
      e.preventDefault();
      removeNode(selectedNodeId);
    }
  };

  window.addEventListener("keydown", handler);
  return () => window.removeEventListener("keydown", handler);
}, [undo, redo, removeNode, selectedNodeId]);
```

## Behavior Matrix

| Focus State | Input Content | Delete Key Action |
|-------------|---------------|-------------------|
| No input focused | N/A | Delete node |
| Input focused | Empty | Delete node |
| Input focused | Has content | Delete text (default) |

## Pitfalls
1. **Don't block all input focus** - User may want to delete node while input is focused but empty
2. **Check value.length** - Not just truthy check (empty string is falsy)
3. **Prevent default only when deleting node** - Let browser handle text deletion otherwise
