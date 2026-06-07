# Chip — Manifest Analysis

```
component:       Chip
source:          components/chip/manifest.json
manifest_type:   COMPONENT_SET
total_variants:  288 (Figma) → 144 (CSS-meaningful, RTL axis excluded)
analyzed:        2026-06-06
```

---

## Detected Axes

| Axis | Values | CSS Impact |
|---|---|---|
| **Style** | `Primary`, `Neutral` | Background and text tokens differ per style |
| **State** | `Default`, `Focused`, `Hovered`, `Pressed`, `Selected`, `Disabled` | Background and text tokens change per state |
| **Size** | `Small`, `Medium`, `Large` | Height, font-size, line-height, font-weight |
| **Rounded** | `False`, `True` | `border-radius` only |
| **On-color** | `False`, `True` | Entire background and text surface switches to on-color token set |
| **RTL** | `False`, `True` | **Zero CSS differences.** See Architecture Findings §RTL. |

---

## Detected Variants

**288 Figma variants** break down as:  
`2 RTL × 2 Rounded × 3 Size × 6 State × 2 Style × 2 On-color = 288`

**144 CSS-meaningful variants** after RTL deduplication:  
`2 Rounded × 3 Size × 6 State × 2 Style × 2 On-color = 144`

---

## Detected States

| State | Visual Change | Children |
|---|---|---|
| Default | Base background + text | `[Text]` |
| Focused | Base background (unchanged) + focus outline | `[Text, Focus outline]` |
| Hovered | Lighter/different background | `[Text]` |
| Pressed | Darker/saturated background | `[Text]` |
| Selected | Inverted/strong background + reversed text | `[Text]` |
| Disabled | Gray background + muted text | `[Text]` |

---

## Architecture Findings

### RTL is a no-op
All 96 RTL=True variants were compared against their RTL=False counterparts. Zero differences exist in `cssProps` at any level. RTL must be handled at the container level via `[dir="rtl"]` and CSS logical properties. The 96 RTL variants are excluded from reference.json and chip.css.

### Focus outline is size-coupled to a fixed label
Figma models the focus outline as a fixed-size `RECTANGLE` node:
- Small: `55 × 28px`
- Medium: `59 × 32px`
- Large: `68 × 40px`

These dimensions assume the label is always "Item". They will break when label length changes. Implementation uses `inset: -4px` instead — this is an **intentional deviation**. See `chip.contract.md §Focus Behavior`.

### On-color surface is style-agnostic
Primary and Neutral on-color variants share identical token values for all states. The `On-color` axis is effectively a surface switch, not a style modifier. In CSS this is expressed as a single `.chip--on-color` modifier class that overrides both background and text, regardless of style.

### Padding is size-invariant
All three sizes use `padding: 0 var(--Global-spacing-lg, 12px)`. Only height changes per size. This is unusual — padding typically scales with size. Preserved as-is from Figma; flagged for design team review.

### Small size font-weight is heavier than Medium/Large
- Small: `font-weight: 600` (`--font-weight-semibold`)
- Medium: `font-weight: 500` (`--font-weight-medium`)
- Large: `font-weight: 500` (`--font-weight-medium`)

Reversed weight progression (heavier at smaller size) is atypical. Preserved as-is from Figma; flagged for design team review.

### Child node structure
- All non-focused states: `[Text]` only
- Focused state only: `[Text, Focus outline]`
- No icon slots exist in any variant. The chip has no `.chip__icon` anatomy.

---

## Token Findings

### No chip-scoped tokens exist in token.css
All `--chip-*` tokens referenced in `chip.css` are pending. Every token reference in chip.css has a corresponding `TODO` comment with the recommended primitive mapping.

### Font-size 10px (Small) — missing primitive
`token.css` has no `--fs-text-2xs` step. The Small chip font-size (10px) cannot be mapped to an existing primitive. Nearest match is `--fs-text-xs: 12px` (2px difference).

### Line-height 14px (Small) — missing primitive
`token.css` has no `--lh-text-2xs`. The Small line-height (14px) has no primitive. No token mapping is possible without a new primitive.

### `#161616` — missing primitive
Used for: Neutral text (off-color), on-color text (all states), focus outline color. `token.css` has no primitive for `#161616`. Nearest: `--gray-950: #0d121c` (darker). This is a token system gap affecting multiple components. Proposed token: `--near-black` or `--gray-925`.

### Focus outline border-width (3px) — missing token
`token.css` has `--border-width-thick: 2px` and `--border-width-heavy: 4px`. 3px has no token.

### On-color opacity backgrounds — no primitives
`rgba(255,255,255,0.80)`, `rgba(255,255,255,0.60)`, `rgba(255,255,255,0.70)`, `rgba(255,255,255,0.20)` are used as on-color backgrounds. `token.css` has opacity tokens (`--opacity-default: 0.8`, `--opacity-medium: 0.6`) but not as pre-composited color values.

### Cross-component token leak: Primary/Pressed text
Figma source uses `--Button-button-background-primary-pressed` for Primary Pressed text color. This is a Button-namespaced token used as a text color in a different component. chip.css proposes `--chip-text-primary-pressed` as the correct chip-scoped replacement.

### Figma token name typo
`--Chip-chip-background-on-color-diabled` (Figma source) contains a typo. Corrected to `--chip-on-color-bg-disabled` in all generated files.

### Radius token inconsistency in Figma source
Two forms of the full-radius token appear: `--radius-radius-full` and `--radius-radiusradius-full`. Both map to `--radius-full: 9999px` in token.css. chip.css uses `--chip-radius-rounded → var(--radius-full)`.

---

## Assumptions

| # | Assumption |
|---|---|
| A1 | RTL handled at container level via `[dir="rtl"]`. chip.css uses logical properties (`padding-inline`). |
| A2 | Large = default (no modifier). Small = `.chip--sm`. Medium = `.chip--md`. |
| A3 | Root element is `<button>` for interactive chips. `<span>` only for display-only. |
| A4 | Selected state maps to `aria-pressed="true"` (toggle) or `aria-selected="true"` (group). |
| A5 | No icon slot. The `.chip__icon` anatomy does not exist for this component. |
| A6 | `inset: -4px` focus outline is an intentional deviation from Figma fixed pixel widths. |
| A7 | `cursor: pointer`, `white-space: nowrap`, `user-select: none` are added as structural requirements not present in Figma manifest. |
| A8 | Primary and Neutral on-color variants share identical tokens — modeled as a single `.chip--on-color` modifier. |
| A9 | All `--chip-*` token references in chip.css assume those tokens will be added to token.css. Until then, the component will render with unresolved custom properties (visually broken). |

---

## Risks

| # | Severity | Risk |
|---|---|---|
| R1 | High | All chip-scoped tokens are missing from token.css. Component is non-functional until token.css is updated. |
| R2 | High | Small size font-size (10px) and line-height (14px) have no token.css primitive. `--chip-sm-font-size` and `--chip-sm-line-height` cannot be resolved until new primitives are added. |
| R3 | High | `#161616` has no primitive token. `--chip-text-neutral` and `--chip-focus-outline-color` will be unresolved. |
| R4 | Medium | Focus outline uses `inset: -4px` deviation. If the implementation is ever auto-tested against Figma pixel values, it will fail the visual diff. |
| R5 | Medium | SKILL.md is truncated at line 50. File schemas inferred from button component. Undocumented conventions may cause divergence. |
| R6 | Low | Small chip (20px) is below the 24px minimum touch target. Flagged in audit-rules and compliance.json. |
| R7 | Low | Padding is size-invariant — all sizes use 12px. May cause visual imbalance at Large. Preserved as-is. |
| R8 | Low | Font-weight is heavier at Small (600) than Medium/Large (500). Atypical progression. Preserved as-is. |

---

## Known Issues

| # | Issue | Action |
|---|---|---|
| KI-1 | `--chip-*` tokens absent from token.css | Token team: add all tokens listed in `analysis.md §Token Findings` |
| KI-2 | `#161616` has no primitive in token.css | Token team: propose `--near-black` or equivalent primitive |
| KI-3 | 10px font-size and 14px line-height have no primitive | Token team: add `--fs-text-2xs` and `--lh-text-2xs` to token.css |
| KI-4 | Focus outline 3px width has no token | Token team: add `--border-width-focus` or similar |
| KI-5 | On-color opacity backgrounds have no chip-scoped tokens | Token team: add `--chip-on-color-bg-*` with rgba values |
| KI-6 | `--Button-button-background-primary-pressed` cross-component reference in Figma | Design team: confirm `--chip-text-primary-pressed: var(--sa-900)` as canonical value |
| KI-7 | Figma typo `diabled` in token name | Figma team: rename to `disabled` in design token source |
| KI-8 | Small size touch target (20px) is below 24px platform minimum | Design team: review or document exception |
| KI-9 | Figma token `--Global-spacing-lg` resolves to 12px, but `--spacing-lg` in token.css = 16px; the correct mapping is `--spacing-md` = 12px | Token team: use `--spacing-md` (not `--spacing-lg`) as the primitive for `--chip-padding-inline` |
