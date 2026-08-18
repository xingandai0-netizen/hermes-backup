# @ Mention Input Pattern

## Component Structure

```tsx
interface MentionItem {
  id: string;
  name: string;
  type: 'image' | 'video';
}

interface MentionInputProps {
  value: string;
  onChange: (value: string) => void;
  mentions: MentionItem[];
  placeholder?: string;
}
```

## @ Detection Logic

```typescript
const handleInput = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
  const newValue = e.target.value;
  onChange(newValue);

  // Check for @ before cursor
  const cursorPos = e.target.selectionStart || 0;
  const textBeforeCursor = newValue.substring(0, cursorPos);
  const lastAtIndex = textBeforeCursor.lastIndexOf('@');

  if (lastAtIndex !== -1) {
    const textAfterAt = textBeforeCursor.substring(lastAtIndex + 1);
    // If no space after @, show menu
    if (!textAfterAt.includes(' ')) {
      setFilterText(textAfterAt);
      setShowMenu(true);
      return;
    }
  }
  setShowMenu(false);
}, [onChange]);
```

## Selection Logic

```typescript
const selectMention = useCallback((mention: MentionItem) => {
  const cursorPos = inputRef.current?.selectionStart || 0;
  const textBeforeCursor = value.substring(0, cursorPos);
  const lastAtIndex = textBeforeCursor.lastIndexOf('@');
  
  if (lastAtIndex !== -1) {
    const before = value.substring(0, lastAtIndex);
    const after = value.substring(cursorPos);
    const newValue = `${before}@${mention.name} ${after}`;
    onChange(newValue);
    setShowMenu(false);
  }
}, [value, onChange]);
```

## Default Mentions (No Upstream Assets)

```typescript
const defaultMentions: MentionItem[] = [
  { id: 'default-image-1', name: '图素材1', type: 'image' },
  { id: 'default-video-1', name: '视频素材1', type: 'video' },
];

const allMentions = (mentions.length > 0 ? mentions : defaultMentions)
  .filter(m => m.name.toLowerCase().includes(filterText.toLowerCase()));
```

## Keyboard Navigation

```typescript
const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
  if (!showMenu) return;

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    setSelectedIndex(prev => Math.min(prev + 1, allMentions.length - 1));
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    setSelectedIndex(prev => Math.max(prev - 1, 0));
  } else if (e.key === 'Enter' && allMentions.length > 0) {
    e.preventDefault();
    selectMention(allMentions[selectedIndex]);
  } else if (e.key === 'Escape') {
    setShowMenu(false);
  }
}, [showMenu, allMentions, selectedIndex, selectMention]);
```

## Menu UI Position

Position menu above input (bottom: '100%'):

```tsx
{showMenu && allMentions.length > 0 && (
  <div style={{
    position: 'absolute',
    bottom: '100%',
    left: 0,
    right: 0,
    background: '#1a1a2e',
    border: '1px solid rgba(255,255,255,0.1)',
    borderRadius: 8,
    padding: 4,
    zIndex: 100,
    maxHeight: 150,
    overflowY: 'auto',
  }}>
    {/* Menu items */}
  </div>
)}
```

## Pitfalls

1. **Always show default mentions** - When no upstream assets connected
2. **Filter by name** - Use `toLowerCase().includes(filterText.toLowerCase())`
3. **Position above input** - Use `bottom: '100%'` not `top`
4. **Keyboard navigation** - Arrow keys + Enter + Escape
5. **Close on outside click** - Use `useEffect` with `mousedown` listener
