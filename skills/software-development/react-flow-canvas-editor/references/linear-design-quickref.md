# Linear Design System — Quick Reference

Used when building developer tools and dark-mode dashboards. Source: `popular-web-designs` skill → `templates/linear.app.md`.

## Color Palette

### Backgrounds
- Marketing Black: `#08090a`
- Panel Dark: `#0f1011`
- Level 3 Surface: `#191a1b`
- Secondary Surface: `#28282c`

### Text
- Primary: `#f7f8f8` (NOT pure white)
- Secondary: `#d0d6e0`
- Tertiary: `#8a8f98`
- Muted: `#62666d`

### Accent (ONE color only)
- Brand: `#5e6ad2` (indigo backgrounds)
- Bright: `#7170ff` (interactive elements)
- Hover: `#828fff`

### Borders (semi-transparent white, NEVER solid dark)
- Subtle: `rgba(255,255,255,0.05)`
- Default: `rgba(255,255,255,0.08)`

### Buttons (nearly transparent)
- Background: `rgba(255,255,255,0.02)` to `rgba(255,255,255,0.05)`
- Radius: 6px

## Typography
- Font: Inter Variable with `font-feature-settings: "cv01", "ss03"`
- Default emphasis weight: 510 (between regular and medium)
- Max weight: 590 (NEVER 700/bold)
- Display sizes: negative letter-spacing (-1.056px at 48px)

## Rules
- No pure white text — use `#f7f8f8`
- No solid colored button backgrounds — use transparency
- No positive letter-spacing on display text
- No visible/opaque borders — use semi-transparent white
- Surface elevation via background opacity stepping, not shadows
