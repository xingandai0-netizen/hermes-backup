# Cyrclo Template Integration — Case Study

## Problem
User purchased Cyrclo Webflow template (136KB HTML + 166KB CSS + 10 JS files) and wanted it as the Antoken landing page.

## What Went Wrong (3 failed attempts)

### Attempt 1: Subagent created simplified React components
- Created 11 React component files (cyrclo-*.tsx)
- Missing critical HTML nesting (circle-container, circle-wrapper, circle-block)
- Missing CSS class names that drive layout
- Result: Broken layout, missing images, wrong structure

### Attempt 2: Subagent rewrote components with CSS analysis
- Better, but still missing wrapper divs
- circle-block had 0 height because circle-container was missing
- Result: Partially working but hero section broken

### Attempt 3: Manual hero fix
- Fixed hero nesting to match original HTML
- Still other sections had issues
- Result: Some sections worked, others didn't

### Final Solution: Static HTML + Rewrite
```bash
cp /path/to/cyrclo_raw/index.html frontend/public/cyrclo.html
# CSS renamed to match HTML reference exactly
mv cyrclo.css cyrclo.app.shared.8a67f88a8.css
# next.config.mjs: rewrite '/' → '/cyrclo.html'
```
Result: Perfect — all animations, images, interactions working.

## Key Lesson
**Webflow templates cannot be reliably converted to React components.** The HTML nesting is too complex (5-10 wrapper divs per section), CSS class dependencies are too specific, and JS interactions depend on exact DOM structure. Always serve as static HTML.

## File Structure
```
frontend/public/
├── cyrclo.html                              (136KB - main page)
├── css/
│   └── cyrclo.app.shared.8a67f88a8.css      (166KB - MUST match HTML reference)
└── js/
    ├── jquery-3.5.1.min.dc5e7f18c8.js
    ├── gsap.min.js
    ├── SplitText.min.js
    ├── ScrollTrigger.min.js
    ├── webfont.js
    ├── app.schunk.36b8fb49256177c8.js
    ├── app.schunk.edbe06d737675fa7.js
    ├── app.30adc4a3.63398216118c093e.js
    ├── app.fa7ceecc.6f5383adaa5cccec.js
    └── app.d288ae27.52d120005507afee.js
```
