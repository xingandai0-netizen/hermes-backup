---
name: academic-paper-workflow
description: "Academic paper workflow: AI detection rate reduction, Word document formatting, and DOCX beautification. Covers rewriting strategies, template-based formatting, and annotation extraction."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [academic, paper, docx, formatting, ai-detection, beautification, word]
---

# Academic Paper Workflow

Complete workflow for academic papers: writing with low AI detection, formatting to standards, and DOCX beautification.

## When to Use

- Writing or rewriting academic papers to reduce AI detection rate
- Formatting Word documents (.docx) to academic standards
- Extracting annotations and comments from documents
- Beautifying thesis/report layouts

---

## 1. AI Detection Rate Reduction

### Strategy

Rewrite paragraph by paragraph, maintaining academic quality while reducing AI patterns.

**Key techniques:**
- Vary sentence length and structure (mix short and long sentences)
- Use domain-specific jargon naturally (not forced)
- Add hedging language ("arguably", "tends to", "appears to")
- Include minor stylistic imperfections that humans naturally produce
- Avoid AI-typical patterns: excessive parallelism, triple structures, "In conclusion"
- Use active voice more often than AI typically does
- Add citations and references mid-paragraph (not just at ends)

**AI patterns to eliminate:**
- "It is worth noting that..." → Remove or rephrase
- "Furthermore/Moreover/Additionally" chains → Vary transitions
- "In today's rapidly evolving..." → Start with specific context
- Perfect paragraph symmetry → Vary paragraph lengths
- "This paper aims to..." → More direct opening

**Workflow:**
1. Read the full paper to understand context
2. Rewrite each paragraph individually
3. Preserve all data, citations, and technical accuracy
4. Vary structure between paragraphs
5. Read aloud to check naturalness

---

## 2. Academic Paper Formatting

### Standard Requirements

| Element | Standard |
|---------|----------|
| Body font | Times New Roman 12pt or 宋体 小四 |
| Line spacing | 1.5 or double |
| Margins | 2.54cm top/bottom, 3.17cm left/right (or as specified) |
| Heading 1 | Bold, centered, 16pt |
| Heading 2 | Bold, left-aligned, 14pt |
| Heading 3 | Bold, left-aligned, 12pt |
| Page numbers | Bottom center or bottom right |
| References | Hanging indent (0.5cm), alphabetical order |

### Common Fixes

```python
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document('paper.docx')

# Fix body font
for para in doc.paragraphs:
    if para.style.name == 'Normal':
        for run in para.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)

# Fix line spacing
from docx.shared import Pt
for para in doc.paragraphs:
    para.paragraph_format.line_spacing = 1.5

# Fix margins
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)
```

---

## 3. DOCX Beautification Engine

### Template-Based Approach

1. **Extract** formatting from a reference template
2. **Audit** the paper against the template
3. **Fix** non-compliant elements automatically

```python
# Extract template styles
template = Document('template.docx')
for style in template.styles:
    if style.type == 1:  # Paragraph style
        print(f"{style.name}: font={style.font.name}, size={style.font.size}")
```

### Common Beautification Tasks

- Unified font across all paragraphs
- Consistent heading hierarchy (no skipped levels)
- Proper figure/table captions with numbering
- Reference list formatting (hanging indent, consistent style)
- Table of contents generation
- Header/footer with page numbers

---

## 4. Annotation Extraction

Extract comments and tracked changes from .docx files:

```python
from docx import Document

doc = Document('reviewed.docx')

# Extract comments
for comment in doc.comments:
    print(f"Author: {comment.author}")
    print(f"Text: {comment.text}")
    print(f"Referenced: {comment.referred_to.text[:50]}...")
```

**Use cases:**
- Extract reviewer feedback
- Identify red-highlighted text (corrections)
- Automate response to common revision requests

---

## Pitfalls

- **AI detection tools vary** — what passes one detector may fail another
- **Formatting macros can break documents** — always work on a copy
- **Chinese academic formatting differs from Western** — check specific university requirements
- **Reference formatting depends on style guide** — APA, MLA, Chicago, GB/T 7714 all differ
- **python-docx can't handle all .docx features** — complex layouts may need manual adjustment
- **Track Changes must be accepted before formatting** — otherwise styles conflict
