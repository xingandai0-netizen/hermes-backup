# SlideSage Workflow for Professional PPTX

## Overview

SlideSage (vedraut/slidesage) is a Node.js tool that generates professional .pptx presentations driven by storytelling and instructional design. It produces much better output than officecli for investor-facing decks.

## Setup

```bash
cd /tmp && git clone --depth 1 https://github.com/vedraut/slidesage.git
cd slidesage && npm install
```

## Storyboard Structure

Create `storyboard.json` with this structure:

```json
{
  "meta": {
    "title": "Presentation Title",
    "subtitle": "Subtitle",
    "author": "Author Name",
    "audience": "Target audience",
    "mode": "business",
    "style": "minimalist-luxury",
    "durationMin": 10,
    "governingThought": "One-line recommendation the whole deck supports.",
    "logo": "/path/to/logo.png"
  },
  "slides": [
    {
      "archetype": "cover",
      "actionTitle": "Full sentence takeaway ending with period.",
      "kicker": "Small eyebrow label",
      "body": ["Point 1", "Point 2", "Point 3"]
    }
  ]
}
```

## Slide Archetypes

| Archetype | Use When |
|-----------|----------|
| `cover` | Opening slide |
| `section` | Section divider (transition beat) |
| `content` | Single-column with bullets |
| `two-column` | Side-by-side comparison (use `columns` array) |
| `data` | Data-heavy with citations |
| `comparison` | Competitor comparison |
| `pipeline` | Timeline/steps (use `flow` array) |
| `quote` | Quote or testimonial |
| `callToAction` | Closing/ask slide |

## Action Title Rules (CRITICAL)

Every content slide MUST use a **full-sentence action title** ending with period (`.`).

- BAD: "市场数据" (topic label)
- GOOD: "AI电商市场2024年504亿元，预计2029年达1383亿元."

The QA script checks: `actionTitle` must end with `[.!?]`.

## Available Styles

| Style | Best For |
|-------|----------|
| `minimalist-luxury` | White/beige,高端品牌, **阿戴首选** |
| `futuristic-tech` | Dark theme, AI/tech startups |
| `corporate-bright` | Light professional |
| `japanese-editorial` | Editorial/magazine style |
| `soft-clay-3d` | Friendly, modern |
| `modern-illustration` | Product stories |
| `hand-drawn-editorial` | Creative, artistic |

## Generation Commands

```bash
# Validate
node scripts/validate-storyboard.mjs storyboard.json

# Generate
node scripts/generate.mjs --in storyboard.json --style minimalist-luxury --logo /path/to/logo.png --out output.pptx

# QA (must pass all checks)
node scripts/qa-report.mjs --storyboard storyboard.json --deck output.pptx
```

## Post-Processing

After generation, run python-pptx to fix fonts (especially for Chinese content):

```bash
cd /tmp && source pptx-env/bin/activate && python fix_fonts.py
```

See `pptx-post-processing.py` for the complete script.

## Pitfalls

- Action titles MUST end with period, exclamation, or question mark
- Each slide should have ≤5 bullets, each ≤16 words
- `governingThought` is required for business mode
- Logo path must be absolute
- SlideSage uses PptxGenJS (Node.js), not python-pptx
