# PPTX Poster Template Filling Workflow

## When to use
User provides: blank template (.pptx) + reference/example version + source document (.docx).
Task: fill empty sections in the template using content from the source, matching the reference style.

## Step-by-step

### 1. Clarify before acting (CRITICAL)
Ask the user:
- Which file to MODIFY? (the template, not the reference)
- Content source? (directly from doc, or paraphrase from reference version?)
- What to preserve? (images, tables, existing text — "don't touch what I haven't changed")
- Any sections they specifically want filled or left empty?

### 2. Scan both files
```bash
officecli view <template> text      # see what's empty
officecli view <reference> text     # see what content looks like when filled
officecli view <template> annotated # see formatting details (fonts, sizes)
```

### 3. Build a fill plan
Create a table mapping:
| Section | Template Shape ID | Status (empty/partial/filled) | Content to add |

### 4. Fill sections
Use the approaches in `poster-template-filling.md` (find/replace for placeholders, text= for empty, add for new boxes).

### 5. Post-fill verification (MANDATORY)
```bash
officecli view <file> issues        # fix ALL overflow warnings first
officecli view <file> screenshot -o /tmp/verify.png
# Use vision_analyze to check: all text visible, no overlaps, consistent formatting
officecli close <file>              # release lock before user opens externally
```

## Common issues

### Text overflow
`officecli view file.pptx issues` — check for text overflow warnings.
Fix: reduce font size, shorten text, or increase shape height (carefully).

### Overlapping sections
New text box overlaps with adjacent section.
Fix: remove the new box (`officecli remove file.pptx '/slide[1]/shape[@id=N]'`), then merge content into the shape above using `--find --replace`, or shorten text to fit.

### Content duplication
Same text appears twice in a shape after multiple `--find`/`--replace` operations.
Fix: use `--prop text=` to overwrite the entire shape content cleanly.

### Formatting mismatch
Content looks different from reference.
Fix: check the reference shape's font/size/color with `officecli get` and match in your commands.

### File locked by another application
User reports WPS/PowerPoint can't edit the file.
Fix: `officecli close <file>` to release the resident process lock.

## User preferences (阿戴)
- "精简表达" — concise paraphrasing, not direct copy from source
- "我没改动的地方不要动" — preserve all existing content
- "字体格式和框架要和第一个完全一样" — match reference formatting exactly
- "内容不要有遮挡和超出边框" — no overlaps, all content within borders
- "不懂的先提问" — ask before acting when unclear
