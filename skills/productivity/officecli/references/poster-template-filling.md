# Poster Template Filling Workflow

When asked to fill an empty poster template from a report/thesis, using a filled reference poster as guide.

## Step 1: Compare templates
```bash
officecli view <blank_template> text
officecli view <filled_reference> text
```
Identify which sections are empty vs filled in the blank template.

## Step 2: Locate empty shape IDs
```bash
officecli query <blank_template> 'shape:contains("Section Header Text")'
```
Each empty section has a shape ID (e.g., `@id=13`). Record all IDs.

## Step 3: Fill content

**A. Shape has placeholder text (e.g. "Aim:\n"):**
```bash
officecli set file.pptx '/slide[1]/shape[@id=N]' --find "Aim:" --replace "Aim:
New content here."
```

**B. Shape is completely empty:**
```bash
officecli set file.pptx '/slide[1]/shape[@id=N]' --prop text="New content"
```

**C. Header exists but no body shape below (need new textbox):**
Check vertical space first (see Pitfall: height management), then:
```bash
officecli add file.pptx '/slide[1]' --type textbox \
  --prop text="Body content" \
  --prop x=Xemu --prop y=Yemu --prop width=Wemu --prop height=Hemu \
  --prop font.latin="FontName" --prop size=Npt --prop color=text1
```

## Step 4: Verify (MANDATORY)
```bash
officecli view <file> issues        # fix ALL overflow warnings
officecli view <file> screenshot    # visual check with vision_analyze
officecli close <file>              # release lock before user opens in WPS/PowerPoint
```

## Critical Pitfalls

### Box height management
- **NEVER increase box heights** to fit more text — causes overlap with adjacent fixed-position boxes
- `--prop height=X` combined with `--find`/`--replace` in ONE command: height may not apply (gets overridden by autoFit). Set height in a **separate** command after text is set.
- After any height change, verify positions of adjacent shapes: `get <shape> --depth 0` and check y+height doesn't exceed next shape's y.

### Text content handling
- **Keep text concise** to fit within original box dimensions
- `\n` in `--prop text=` creates **separate XML `<p>` elements** with extra paragraph spacing, NOT simple line breaks. A 5-item list becomes 6 paragraphs with large gaps. Prefer short text with minimal newlines.
- **`--find`/`--replace` can duplicate content** if applied multiple times. After each replace, verify with `get --depth 1`. If duplication occurs, use `--prop text=` to overwrite entirely.
- Regex in `--find`: use `\\.` for literal dots, `.*` for wildcards. Wrap pattern in double quotes.

### Text overflow
- `officecli view <file> issues` catches overflow BEFORE visual problems appear
- Even section **headers** can overflow in tight templates — check them too
- Fix: reduce font size (`--prop size=20pt`), shorten text, or if absolutely necessary increase height (but verify adjacent shapes)
- `suggest.height=Ncm` in the issues output tells you the minimum height needed

### File locking
- `officecli close <file>` MUST be called before user opens in WPS/PowerPoint/Keynote
- If user reports "file locked", run `officecli close` first

## Content Guidelines
- Paraphrase from source, don't copy-paste
- Match the filled reference's style/tone, not the source document's
- Section headers are usually already present — only fill body content
- Images, tables, references usually already placed — don't touch
