# Component Analysis

- **Manifest path:** `components/tag/manifest.json`, `components/tag/status-tag.json`
- **Component name:** Tag, Status Tag
- **Generated:** 2026-06-09

---

## Source

Two Figma COMPONENT_SET exports in the same folder:

| File | Component Set | Variants |
|---|---|---|
| `manifest.json` | Tag | 288 |
| `status-tag.json` | Status Tag | 90 |

Both are display-only (non-interactive) label components sharing the Tag token namespace.

---

## Detected Anatomy

### Tag

```
.tag                        ← root <span> (inline-flex container)
  .tag__icon  [optional]    ← icon wrapper, aria-hidden="true"
  .tag__text                ← visible label text
```

### Status Tag

```
.status-tag                 ← root <span> (inline-flex, always pill-shaped)
  .status-tag__dot          ← colored status indicator circle, aria-hidden="true"
  .status-tag__text         ← visible label text
```

---

## Detected Axes

### Tag (manifest.json)

| Axis | Values | CSS Strategy |
|---|---|---|
| RTL | False, True | `[dir="rtl"]` selector — icon order via flex |
| Size | x Small, Small, Medium | Modifier classes: `--xs`, `--sm`, default=Medium |
| Style | Neutral, Error, Info, Success, Warning, On-Color | Modifier classes: default=Neutral, `--error`, `--info`, `--success`, `--warning`, `--on-color` |
| Outline | False, True | Modifier class: `--outline` (removes bg, darkens border) |
| Rounded | False, True | Modifier class: `--rounded` (radius-full vs radius-sm) |
| Icon only | False, True | Modifier class: `--icon-only` (square container, no text) |

### Status Tag (status-tag.json)

| Axis | Values | CSS Strategy |
|---|---|---|
| RTL | False, True | `[dir="rtl"]` selector — dot/text order reversal |
| Size | x Small, Small, Medium | Modifier classes: `--xs`, `--sm`, default=Medium |
| Style | Neutral, Blue, Green, Red, Yellow | default=Neutral, `--blue`, `--green`, `--red`, `--yellow` |
| Status | Subtle, Ghost, Inverted | default=Subtle, `--ghost`, `--inverted` |

---

## Detected Variants

### Tag — meaningful variants (RTL excluded as layout-only)

288 total = 2 (RTL) × 3 (Size) × 6 (Style) × 2 (Outline) × 2 (Rounded) × 2 (Icon only)
→ 144 design variants per direction

### Status Tag — meaningful variants (RTL excluded)

90 total = 2 (RTL) × 5 (Style) × 3 (Status) × 3 (Size)
→ 45 design variants per direction

---

## Detected States

No interactive states in either manifest. Both components are display-only.
No hover, focus, pressed, or disabled variants detected in Figma.

Tag and Status Tag are non-interactive by default. If made interactive (e.g., dismissible tag with a close button), the interactive control should be a separate child element, not the tag root itself.

---

## Detected Sizes

### Tag

| Size | Height | Padding-inline | Gap | Icon | Font-size | Line-height | Weight |
|---|---|---|---|---|---|---|---|
| x Small | 20px | 8px | 4px | 10px | 10px | 14px | 600 (semibold) |
| Small | 24px | 8px | 4px | 14px | 12px | 18px | 500 (medium) |
| Medium (default) | 32px | 12px | 4px | 18px | 16px | 24px | 500 (medium) |

**Note:** x Small uses semibold (600) while Small and Medium use medium (500). This is intentional per Figma and is documented as a deliberate typographic density trade-off.

### Tag Icon-only

| Size | Width | Height | Icon | Padding |
|---|---|---|---|---|
| x Small | 20px | 20px | 10px | 2px |
| Small | 24px | 24px | 14px | 2px |
| Medium (default) | 32px | 32px | 18px | 2px |

### Status Tag

| Size | Height | Padding-inline | Gap | Dot | Font-size | Line-height | Weight |
|---|---|---|---|---|---|---|---|
| x Small | 20px | 8px | 8px | 10px | 10px | 14px | 500 (medium) |
| Small | 24px | 8px | 8px | 10px | 14px | 20px | 500 (medium) |
| Medium (default) | 32px | 16px | 8px | 10px | 16px | 24px | 500 (medium) |

**Note:** Status Tag uses `--spacing-sm (8px)` gap at all sizes, while Tag uses `--spacing-xs (4px)` gap. Different gap scale despite shared naming convention.

**Note:** Status Tag Small font-size is 14px (sm text scale) while Tag Small font-size is 12px (xs text scale). Intentional per Figma design.

---

## Architecture Findings

1. **Two component sets, one folder:** `manifest.json` (Tag) and `status-tag.json` (Status Tag) share the `components/tag/` directory. Generated as `.tag` and `.status-tag` BEM namespaces in a single `tag.css`.

2. **RTL is a layout-only axis:** Both components use the same visual tokens for RTL and LTR. The difference is `flex-direction: row-reverse` under `[dir="rtl"]` and `text-align: right` for text content. No separate visual token set needed. RTL axis is discarded from `reference.json` variant matrix and handled via global CSS direction support.

3. **Tag is not interactive:** The root element should be `<span>` (non-semantic inline). No `role="button"` unless the component is explicitly made interactive. If a tag needs a dismiss action, the close button should be a separate child `<button>` inside the tag, not part of this component's base implementation.

4. **Status indicator (dot) is a structural element:** The `Status indicator` ELLIPSE in Figma is rendered as `.status-tag__dot` — a real HTML `<span>` with `border-radius: 50%`. It is `aria-hidden="true"` because the color carries semantic meaning that must be expressed via the text label, not the dot color alone.

5. **On-Color style has no border:** `outline=False` + `style=On-Color` has no border property. Only the outline variant of On-Color adds a `rgba(255,255,255,0.60)` border. Other styles always have a border in their default (non-outline) state.

6. **Outline removes background:** All `Outline=True` variants have `background: none` regardless of style. The border color shifts to the "solid" (darker) token variant. Text color remains the same as the filled variant.

7. **Ghost status removes background:** Status Tag `Ghost` has `background: none`, the dot retains style color, but text shifts to neutral (gray-800) regardless of style. This cross-style text behavior is unique to Ghost.

8. **Component token namespace not yet in token.css:** All `--tag-*` and `--status-tag-*` tokens are proposed in `tag.css` as a `:root` block. These must be moved to `token.css` before the component is production-ready.

---

## Token Findings

All tokens in this file are proposed component-level tokens. None are currently in `token.css`.

The component CSS consumes:
- Primitive tokens from `token.css` (via fallbacks in the proposed component token definitions)
- Figma token names (`--Tag-tag-*`) mapped to `--tag-*` component token names

---

## Accessibility Findings

1. **Non-interactive tag:** No keyboard interaction needed. `<span>` with visible text satisfies accessibility for informational labels.

2. **Icon-only tag:** Requires `aria-label` on the root element. The `.tag__icon` child must carry `aria-hidden="true"`.

3. **Status dot color:** The colored dot in Status Tag conveys meaning (state type). Color alone is not sufficient. The text label adjacent to the dot must communicate the same state. `aria-hidden="true"` on `.status-tag__dot` is correct — the dot is decorative when text is present.

4. **IBM Plex Sans Arabic:** Font family supports Arabic (RTL) content. Both components must inherit `--tag-font-family` to ensure Arabic character rendering.

5. **No focus ring needed:** Components are non-interactive. Focus ring CSS is not required. If a dismissible variant is introduced, the close button child must implement its own focus ring.

6. **Minimum touch target:** Icon-only tags at x Small (20×20px) and Small (24×24px) fall below the recommended 44×44px touch target. At those sizes, tags should remain non-interactive. Only Medium (32×32px) icon-only may be used as an interactive control, and only with appropriate touch target wrapping.

---

## Compliance Findings

1. **WCAG 1.4.1 Use of Color:** Status Tag dot color alone does not convey state. The text label must always be present. `aria-hidden` on dot is correct.

2. **WCAG 1.4.3 Contrast:** Text colors in filled variants reference design tokens. Estimated contrast ratios:
   - Neutral: #1F2A37 on #F9FAFB ≈ 15:1 (pass)
   - Error: #912018 on #FEF3F2 ≈ 7:1 (pass)
   - Info: #1849A9 on #EFF8FF ≈ 7:1 (pass)
   - Success: #085D3A on #ECFDF3 ≈ 7.5:1 (pass)
   - Warning: #93370D on #FFFAEB ≈ 7:1 (pass)
   - On-Color: #FFF on rgba(255,255,255,0.20) over dark bg — depends on page background. Mark for manual review.

3. **WCAG 1.4.11 Non-text Contrast:** Outline variants expose colored borders. All outline border tokens appear to meet 3:1 threshold but require per-deployment verification.

---

## Implementation Decisions

1. **Single CSS file for Tag + Status Tag:** Both live in `tag.css` under `.tag` and `.status-tag` BEM namespaces. Keeps the folder self-contained without fragmenting related styles.

2. **Size modifiers:** `--xs` and `--sm` for x Small and Small sizes. Medium is the default (no modifier). Follows button convention.

3. **Style modifiers named after design semantics:** `--error`, `--info`, `--success`, `--warning`, `--on-color`. Neutral is the default.

4. **Status Tag Style modifiers named after Figma axis values:** `--blue`, `--green`, `--red`, `--yellow`. These are Figma-defined names. Considered mapping to semantic names (`--info`, `--success`, `--error`, `--warning`) but chose to preserve Figma names to maintain a direct manifest-to-class traceability.

5. **Proposed `:root` token block in tag.css:** Component tokens are defined inline with fallbacks. This allows the showcase to render without modifying global `token.css`. Must be extracted to `token.css` for production.

6. **RTL via `[dir="rtl"]`:** Uses `flex-direction: row-reverse` on the root container under `[dir="rtl"]`. Does not use `padding-inline-start/end` for this component because the fixed padding-inline is symmetric.

---

## Intentional Deviations From Figma

1. **x Small font-weight 600 → carried through:** Figma uses `font-weight: 600` only for x Small. Preserved as-is. Documented as intentional typographic compression.

2. **Status Tag Small font-size 14px:** Figma uses `typo-size-text-sm` (14px) for Status Tag Small vs. `typo-size-text-xs` (12px) for Tag Small. Different scales intentionally — Status Tag prioritizes legibility at smaller sizes due to the dot indicator adding visual weight.

3. **Status Tag gap is always 8px:** All three Status Tag sizes use 8px gap, unlike Tag which uses 4px gap. Preserved per Figma — the dot requires more spacing for visual separation.

---

## Layer Classification

### Tag

| Layer | Figma Type | Role | Implementation |
|---|---|---|---|
| Tag root | COMPONENT | Structural | `.tag` root element |
| Lead icon | INSTANCE | Icon | `.tag__icon` wrapper + SVG |
| Text | TEXT | Structural | `.tag__text` span |

No interaction layers. No focus layers. No pseudo-element candidates in base Tag.

### Status Tag

| Layer | Figma Type | Role | Implementation |
|---|---|---|---|
| Status Tag root | COMPONENT | Structural | `.status-tag` root element |
| Status indicator | ELLIPSE | Structural icon | `.status-tag__dot` span (circle via border-radius: 50%) |
| Text | TEXT | Structural | `.status-tag__text` span |

The `Status indicator` ELLIPSE is a **structural element** — it directly conveys status information and must be a real HTML element (not a pseudo-element). It is not an interaction layer.

---

## State Delta Matrix

### Tag
No state deltas — non-interactive component. Default state only.

### Status Tag

| Status | Background | Dot color | Text color |
|---|---|---|---|
| Subtle (default) | Style-specific bg | Style icon color | Style text color |
| Ghost | none | Style icon color | Neutral (gray-800) |
| Inverted | Style-specific dark bg | rgba(255,255,255,0.60) | White |

---

## Pseudo-Element Decisions

No pseudo-elements used in Tag or Status Tag.

- No interaction layers found (display-only components)
- No focus ring layers found (non-interactive)
- Status dot rendered as real `<span>` (semantic, not decorative-only)

---

## Interaction Layer Decisions

No interaction layers. Components are non-interactive display elements.

---

## Focus Layer Decisions

No focus styles required. Components are `<span>` elements with no keyboard interaction.

If a close/dismiss button is introduced inside a tag, the button child must implement its own `:focus-visible` ring.

---

## Z-Index / Layering Decisions

No layering required. Components are flat inline-flex containers with no overlapping elements.

---

## Risks

1. **On-Color background opacity:** `rgba(255,255,255,0.20)` is semi-transparent. Contrast ratio depends on the page background color behind the tag. Cannot be audited automatically.

2. **x Small touch target:** 20×20px icon-only tag is too small for touch interaction. Non-interactive use only.

3. **Component tokens not in token.css:** Until `--tag-*` tokens are added to `token.css`, the component is not fully token-driven. Changes to design tokens require updating both `tag.css` and `token.css`.

4. **Status Tag "Blue/Green/Red/Yellow" naming:** These are Figma axis value names. They differ from the semantic token system (`--info`, `--success`, `--error`, `--warning`). If design system naming is standardized, modifier class names would need to change.

---

## Assumptions

1. Tag is always non-interactive at the root level. Dismiss functionality is out of scope for this base component.
2. RTL reversal uses `[dir="rtl"]` on an ancestor element, not `dir` attribute on the tag itself.
3. Font weight 600 for x Small is intentional and should be preserved.
4. `--fs-text-2xs` (10px) and `--lh-text-2xs` (14px) are missing from `token.css`. Fallback hardcoded values used in proposed token block.
5. Status Tag is always pill-shaped (`border-radius: full`). No shape modifier needed.
6. Icon SVGs are provided by the consuming application. The component only provides the wrapper dimensions.

---

## Known Issues

None at generation time.

---

## Missing Tokens

The following tokens are referenced in tag.css but do not exist in `token.css`:

| Token | Proposed Value | Reason |
|---|---|---|
| `--tag-xs-font-size` | 10px | `--fs-text-2xs` missing from token.css |
| `--tag-xs-line-height` | 14px | `--lh-text-2xs` missing from token.css |
| `--tag-xs-icon-size` | 10px | No 10px icon-size primitive in token.css |
| `--tag-sm-icon-size` | 14px | No 14px icon-size primitive in token.css |
| `--tag-icon-size` | 18px | No 18px icon-size primitive in token.css |
| `--tag-on-color-bg` | rgba(255,255,255,0.20) | No semi-transparent white primitive token |
| `--tag-on-color-border-outline` | rgba(255,255,255,0.60) | No semi-transparent white border primitive |
| `--status-tag-*-inverted-dot` | rgba(255,255,255,0.60) | No semi-transparent white primitive token |
| `--status-tag-xs-font-size` | 10px | `--fs-text-2xs` missing from token.css |
| `--status-tag-xs-line-height` | 14px | `--lh-text-2xs` missing from token.css |

All other `--tag-*` and `--status-tag-*` tokens are proposed and must be added to `token.css`.

---

## Missing Standards

- `PLATFORM-CODE-TAG-005`: Minimum touch target audit rule pending implementation for icon-only xs/sm sizes.
- No automated contrast check for On-Color variant (opacity-based background).

---

## TODO

- [ ] Add all `--tag-*` and `--status-tag-*` tokens to `token.css`
- [ ] Add `--fs-text-2xs: 10px` and `--lh-text-2xs: 14px` to `token.css`
- [ ] Verify On-Color contrast ratio with actual deployment backgrounds
- [ ] Implement dismissible tag variant (separate initiative — adds close button child)
- [ ] Implement interactive/clickable tag variant (separate initiative — wraps in `<button>` or `<a>`)
- [ ] Add touch target audit rule for icon-only xs/sm (PLATFORM-CODE-TAG-005)
- [ ] Map Status Tag style names (Blue/Green/Red/Yellow) to semantic equivalents if design system naming is standardized
