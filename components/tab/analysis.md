# Component Analysis

- **Manifest paths:** `components/tab/horizontal-tabs.json`, `horizontal-tabs-list.json`, `vertical-tabs.json`, `vertical-tabs-list.json`
- **Component name:** Tab (Horizontal Tab, Vertical Tab, Tab List)
- **Generated:** 2026-06-09

---

## Source

Four Figma COMPONENT_SET exports in the same folder:

| File | Component Set | Variants |
|---|---|---|
| `horizontal-tabs.json` | Horizontal Tab | 64 |
| `horizontal-tabs-list.json` | Horizontal Tab List | 10 |
| `vertical-tabs.json` | Vertical Tab | 60 |
| `vertical-tabs-list.json` | Vertical Tab List | 12 |

---

## Detected Anatomy

### Horizontal Tab (`.tab--h`)

```
.tab                         ← root <button> (role="tab")
  .tab__icon  [optional]     ← SVG icon wrapper, aria-hidden="true"
  .tab__text                 ← visible label text
  .tab__indicator            ← selection bar (3px bottom bar, ::before pseudo-element)
  ::after                    ← focus ring (::after pseudo-element)
```

### Vertical Tab (`.tab--v`)

```
.tab .tab--v                 ← root <button> (role="tab")
  .tab__icon  [optional]     ← SVG icon wrapper, aria-hidden="true"
  .tab__text                 ← visible label text
  .tab__indicator            ← selection bar (3px left bar, ::before pseudo-element)
  ::after                    ← focus ring (::after pseudo-element)
```

### Horizontal Tab List (`.tab-list--h`)

```
.tab-list                    ← root <div> (role="tablist")
  .tab-list__divider         ← 3px gray bar at bottom (::after pseudo-element)
  [.tab--h ...]              ← tab button instances
```

### Vertical Tab List (`.tab-list--v`)

```
.tab-list .tab-list--v       ← root <div> (role="tablist")
  [.tab--v ...]              ← tab button instances (stacked vertically)
```

---

## Detected Axes

### Horizontal Tab

| Axis | Values | CSS Strategy |
|---|---|---|
| RTL | False, True | `[dir="rtl"]` — selection indicator flips for vertical; horizontal divider stays at bottom |
| State | Default, Hovered, Pressed, Focused, Disabled | CSS: `:hover`, `:active`, `:focus-visible`, `[disabled]`/`[aria-disabled]` |
| Size | Small, Medium, Large | Modifier: `--sm`, default=Medium, `--lg` |
| Selected | True, False | `[aria-selected="true"]` — indicator visible, font-weight 700 |
| More Tab | No, Yes | Out-of-scope overflow trigger (documented below) |

### Horizontal Tab List

| Axis | Values | CSS Strategy |
|---|---|---|
| RTL | False, True | `[dir="rtl"]` |
| Size | Small, Medium, Large | Modifier: `--sm`, default=Medium, `--lg` |
| Tab Icons | True, False | No CSS difference — affects tab instance children only |
| Flush | True, False | Modifier: `--flush` — removes horizontal padding from list container |

### Vertical Tab

| Axis | Values | CSS Strategy |
|---|---|---|
| RTL | False, True | `[dir="rtl"]` — selection indicator moves from left to right |
| State | Default, Hovered, Pressed, Focused, Disabled | Same as Horizontal Tab |
| Size | Small, Medium, Large | Modifier: `--sm`, default=Medium, `--lg` |
| Selected | True, False | `[aria-selected="true"]` — indicator visible, font-weight 600 |

### Vertical Tab List

| Axis | Values | CSS Strategy |
|---|---|---|
| RTL | False, True | `[dir="rtl"]` |
| Size | Small, Medium, Large | Modifier: `--sm`, default=Medium, `--lg` |
| Tab Icons | True, False | No CSS difference — affects tab instance children only |

---

## Detected Variants

- Horizontal Tab: 64 = 2 RTL × [5 states × 3 sizes × 2 selected (More Tab=No)] + [2 states (Closed/Open, More Tab=Yes)] × 2 RTL
- Horizontal Tab List: 10 = 2 RTL × (1 md+icons+flush=F + 1 lg+icons+flush=F + 1 md+icons+flush=T + 1 sm+no-icons+flush=F + 1 sm+no-icons+flush=T)
- Vertical Tab: 60 = 2 RTL × 5 states × 3 sizes × 2 selected
- Vertical Tab List: 12 = 2 RTL × 3 sizes × 2 tab-icons

---

## Detected States

| State | Figma Name | CSS Selector | Notes |
|---|---|---|---|
| Default | Default | (base) | |
| Hovered | Hovered | `:hover` | Background + **dark black indicator** (unselected only). Selected: no change. |
| Pressed | Pressed | `:active` | Background + **dark black indicator** (unselected only). Selected: no change. |
| Focused | Focused | `:focus-visible` | `box-shadow` ring on button. Text → active color. No indicator for unselected. Green indicator for selected. |
| Disabled | Disabled | `[disabled]`, `aria-disabled="true"` | Text color change only |
| Selected | Selected=True | `[aria-selected="true"]` | Green indicator visible, font-weight change |

**Selected=True + Hovered/Pressed:** Background unchanged. Green indicator stays visible.
**Unselected + Hover/Pressed:** Gray background + **dark indicator** (`--Border-border-black: #161616`). Not hidden.

---

## Detected Sizes

### Horizontal Tab

| Size | V-Padding | H-Padding | Font | Weight (unselected/selected) |
|---|---|---|---|---|
| Small | 8px | 12px | 14px/20px | 500/700 |
| Medium (default) | 12px | 16px | 14px/20px | 500/700 |
| Large | 16px | 16px | 14px/20px | 500/700 |

Note: All horizontal tab sizes use 14px/20px text. Large has uniform 16px padding (same h and v).

### Vertical Tab

| Size | V-Padding | H-Padding | Font | Weight (unselected/selected) |
|---|---|---|---|---|
| Small | 2px | 6px | 14px/20px | 400/600 |
| Medium (default) | 6px | 12px | 14px/20px | 400/600 |
| Large | 8px | 12px | 16px/24px | 400/600 |

Note: Vertical Large switches to 16px/24px font (md scale). All others use 14px/20px (sm scale).

---

## Architecture Findings

1. **Four component sets, one assembly:** The tab folder exports two individual tab button types (horizontal, vertical) and two tab list containers. Generated as a single `tab.css` covering `.tab`, `.tab--h`, `.tab--v`, `.tab-list`, `.tab-list--h`, `.tab-list--v`.

2. **Tab button uses ARIA role, not semantic element semantics alone:** Must be `<button role="tab">` inside `<div role="tablist">`. Keyboard navigation (ArrowLeft/Right for horizontal, ArrowUp/Down for vertical) must be implemented via JavaScript.

3. **Selection indicator is a positioned structural element:** The "Selection indicator" + "Selector" layers in Figma are implemented as a `::before` pseudo-element on `.tab`. For horizontal: 3px bar at bottom. For vertical: 3px bar at left side. The indicator is `display: none` when `aria-selected="false"` and `display: block` when `aria-selected="true"`.

4. **Focus ring uses `box-shadow` on the button:** The Figma "Focus outline" RECTANGLE is an inner white border + the button itself gets a `3px solid black` outer border in focus state. CSS equivalent: `box-shadow: inset 0 0 0 1px white, 0 0 0 3px #161616` applied on `:focus-visible`. No `::after` used.

5. **Hover/Pressed background applies only to unselected tabs:** Selected tabs show no background change on hover/press. CSS specificity correctly handles this: `:hover` is overridden by `[aria-selected="true"]` which removes the background.

6. **Tab Icons axis produces no CSS delta:** Whether Tab Icons=True or False, the tab list container CSS is identical. Icon presence is handled by presence/absence of `.tab__icon` child elements.

7. **Flush modifier (horizontal list only):** Flush=True and Flush=False show no Figma CSS difference in the container itself. Flush is treated as removing any container horizontal padding. This allows tabs to be flush with the container edge.

8. **More Tab=Yes is out of scope:** The "More Tab" state (Closed/Open) represents an overflow button that contains a `Button` INSTANCE child. It is a different component pattern (overflow trigger/dropdown). It is documented but not implemented in this component package.

9. **RTL selection indicator flips:** For vertical tabs under `[dir="rtl"]`, the 3px selection bar moves from `left` to `right`. For horizontal tabs, the indicator stays at the bottom in both directions.

10. **Vertical tab list width is 150px fixed in Figma:** This is a canvas preview width. In CSS, vertical tab list width should be `width: 100%` or controlled by the parent layout. Not implemented as a fixed width.

---

## Token Findings

No component-level `--tab-*` tokens exist in `token.css`. All proposed tokens are defined in `tab.css` `:root` block with primitive fallbacks.

Key Figma token references:
- `--Tab-horizontal-tab-md-button-v-padding: 12px` → `var(--space-12)`
- `--Tab-horizontal-tab-md-button-h-padding: 16px` → `var(--space-16)`
- `--Tab-horizontal-tab-sm-button-v-padding: 8px` → `var(--space-8)`
- `--Tab-horizontal-tab-sm-button-h-padding: 12px` → `var(--space-12)`
- `--Tab-vertical-tab-md-button-v-padding: 6px` → 6px (no exact primitive)
- `--Tab-vertical-tab-md-button-h-padding: 12px` → `var(--space-12)`
- `--Tab-vertical-tab-sm-button-v-padding: 2px` → `var(--space-2)`
- `--Tab-vertical-tab-sm-button-h-padding: 6px` → 6px (no exact primitive)
- `--Tab-tab-button-gap: 4px` → `var(--space-4)`
- `--Text-text-default: #161616` → near-black (no direct match in token.css primitives; gray-950 = #0d121c, closest is gray-900 = #111927)
- `--Text-text-primary-paragraph: #384250` → gray-700
- `--Global-text-default-disabled: #9DA4AE` → gray-400
- `--Border-border-primary: #1B8354` → sa-600
- `--Border-border-neutral-primary: #D2D6DB` → gray-300
- `--Button-button-background-neutral-hovered: #F3F4F6` → gray-100
- `--Button-button-background-neutral-pressed: #E5E7EB` → gray-200

---

## Accessibility Findings

1. **ARIA Tabs pattern required:** `.tab-list` must have `role="tablist"`. Each `.tab` must have `role="tab"`, `aria-selected`, `aria-controls` (pointing to panel id), and `id`. Tab panels need `role="tabpanel"` and `aria-labelledby`.

2. **Keyboard navigation is JavaScript-only:** Arrow key navigation between tabs cannot be implemented in CSS. The contract documents the required JS behavior, but CSS cannot enforce it.

3. **`<button>` as tab element:** The root element for `.tab` must be `<button>` (not `<span>`, `<a>`, or `<div>`) to ensure keyboard focusability without `tabindex`.

4. **Focus ring visibility:** The Figma focus outline uses white border which is invisible on white backgrounds. Implementation adds an outer dark `box-shadow` to create a two-layer focus ring (white inner + dark outer) that is visible on any background.

5. **Disabled tabs:** `[disabled]` attribute prevents interaction but may remove from tab order. Use `aria-disabled="true"` on disabled tabs to keep them in the tab order for screen reader discovery while preventing activation.

6. **IBM Plex Sans Arabic:** Font family supports Arabic RTL text.

---

## Compliance Findings

1. **WCAG 1.4.3:** Text contrast ratios estimated to pass:
   - Default text (#161616 on white) ≈ 18:1 (pass)
   - Paragraph text (#384250 on white) ≈ 8.5:1 (pass)
   - Disabled text (#9DA4AE on white) ≈ 2.9:1 — exempt per WCAG inactive component exception
2. **WCAG 2.1.1:** `<button>` ensures keyboard accessibility. Arrow key navigation requires JS.
3. **WCAG 2.4.7:** Focus visible via `::after` focus ring.
4. **WCAG 4.1.2:** `role="tab"`, `aria-selected`, `aria-controls` required.

---

## Implementation Decisions

1. **Single `tab.css` for all four sets:** Shared base styles on `.tab` and `.tab-list`, orientation-specific styles on `.tab--h`/`.tab--v` and `.tab-list--h`/`.tab-list--v`.

2. **`::before` for selection indicator:** The indicator never has semantic meaning — it is a visual affordance. It is absolutely positioned and toggled via `[aria-selected="true"]`.

3. **`box-shadow` for focus ring:** Applied directly on `.tab:focus-visible`. `inset 0 0 0 1px white` (inner white) + `0 0 0 3px #161616` (outer black). No `::after` needed — cleaner than a pseudo-element, no z-index layering required.

4. **`[aria-selected]` for selected state:** Using ARIA attributes as CSS hooks rather than a `.is-selected` class. This ties visual state directly to accessibility state, preventing them from diverging.

5. **`[aria-disabled="true"]` preferred over `[disabled]`:** `[disabled]` is valid but removes the element from tab order; `aria-disabled` keeps it accessible. Both selectors are supported in CSS.

6. **Vertical tab list is width: 100%:** The 150px Figma width is dropped. Consuming layout controls the column width.

7. **Flush modifier affects tab list padding:** `.tab-list--flush` removes the 16px implicit left/right padding from the tab list container.

---

## Intentional Deviations From Figma

1. **Focus ring — `box-shadow` instead of `::after`:** Figma: button gets `border: 3px solid #161616` + inner positioned child `border: 1px solid white`. CSS: `box-shadow: inset 0 0 0 1px white, 0 0 0 3px #161616` on `:focus-visible`. Equivalent visual output, simpler implementation.

2. **Vertical tab list width is not fixed:** 150px Figma canvas width removed. Tab list fills its container.

3. **More Tab (overflow) not implemented:** The More Tab=Yes/Closed/Open Figma variants represent an overflow dropdown trigger. This pattern requires JavaScript and is out of scope for the base CSS-only component.

4. **Selected+Hover behavior made explicit:** When a tab is selected, hover/pressed backgrounds are suppressed. This is inferred from Figma (selected variants show no background on hover) and made explicit in CSS.

---

## Layer Classification

### Horizontal Tab

| Layer | Figma Type | Role | Implementation |
|---|---|---|---|
| Tab root | COMPONENT | Structural | `.tab` `<button>` |
| Leading Icon | INSTANCE | Icon | `.tab__icon` wrapper |
| Tab title FRAME | FRAME | Structural wrapper | Collapsed — text directly in `.tab__text` |
| Text | TEXT | Structural | `.tab__text` |
| Selection indicator FRAME | FRAME | Structural indicator | `::before` pseudo-element |
| Selector RECTANGLE | RECTANGLE | Visual indicator | Part of `::before` |
| Focus outline RECTANGLE | RECTANGLE | Focus layer | `box-shadow` on `.tab:focus-visible` (no pseudo-element) |
| Hover/Pressed background | (implied) | Interaction layer | `:hover`/`:active` CSS — unselected adds dark indicator |

### Vertical Tab

Same as Horizontal Tab. Selection indicator positioned left (not bottom).

### Horizontal Tab List

| Layer | Figma Type | Role | Implementation |
|---|---|---|---|
| List root | COMPONENT | Structural | `.tab-list` `<div>` |
| Divider RECTANGLE | RECTANGLE | Structural separator | `::after` pseudo-element on `.tab-list--h` |
| Tabs FRAME | FRAME | Layout wrapper | Implicit (tabs are direct children) |
| Horizontal Tab INSTANCE | INSTANCE | Structural | `.tab--h` instances |

---

## State Delta Matrix

### Horizontal Tab — Unselected (5 states)

| State | Background | Text color | Text weight | Indicator |
|---|---|---|---|---|
| Default | none | --tab-text-idle (#384250) | 500 | none |
| Hovered | --tab-bg-hover (#F3F4F6) | --tab-text-active (#161616) | 500 | **dark (#161616)** |
| Pressed | --tab-bg-pressed (#E5E7EB) | --tab-text-active (#161616) | 500 | **dark (#161616)** |
| Focused | none | --tab-text-active (#161616) | 500 | none |
| Disabled | none | --tab-text-disabled (#9DA4AE) | 500 | none |

### Horizontal Tab — Selected (5 states)

| State | Background | Text color | Text weight | Indicator |
|---|---|---|---|---|
| Default | none | --tab-text-active (#161616) | 700 | **green** (#1B8354) |
| Hovered | none | --tab-text-active (#161616) | 700 | **green** (#1B8354) |
| Pressed | none | --tab-text-active (#161616) | 700 | **green** (#1B8354) |
| Focused | none | --tab-text-active (#161616) | 700 | **green** (#1B8354) |
| Disabled | none | --tab-text-disabled (#9DA4AE) | 700 | **gray** (#9DA4AE) |

### Vertical Tab — Unselected (5 states)

| State | Background | Text color | Text weight | Indicator |
|---|---|---|---|---|
| Default | none | --tab-text-idle (#384250) | **400** | none |
| Hovered | --tab-bg-hover (#F3F4F6) | --tab-text-active (#161616) | **400** | **dark (#161616)** |
| Pressed | --tab-bg-pressed (#E5E7EB) | --tab-text-active (#161616) | **400** | **dark (#161616)** |
| Focused | none | --tab-text-active (#161616) | **400** | none |
| Disabled | none | --tab-text-disabled (#9DA4AE) | **400** | none |

### Vertical Tab — Selected (5 states)

| State | Background | Text color | Text weight | Indicator |
|---|---|---|---|---|
| Default | none | --tab-text-active (#161616) | **600** | **green** (#1B8354) |
| Hovered | none | --tab-text-active (#161616) | **600** | **green** (#1B8354) |
| Pressed | none | --tab-text-active (#161616) | **600** | **green** (#1B8354) |
| Focused | none | --tab-text-active (#161616) | **600** | **green** (#1B8354) |
| Disabled | none | --tab-text-disabled (#9DA4AE) | **500** | **gray** (#9DA4AE) |

Key differences between H and V:
- Unselected weight: 500 (H) vs 400 (V)
- Selected weight: 700 (H) vs 600 (V)
- Disabled+Selected weight: 700 (H, no drop) vs **500** (V, drops from 600)
- Large size uses 16px/24px font (V only; H is always 14px/20px)

---

## Pseudo-Element Decisions

### `::before` — Selection indicator
- **Horizontal Tab:** absolute, bottom: 0, left: var(--tab-sm-h-padding) / right: var(--tab-sm-h-padding), height: 3px, border-radius: full, background: --tab-indicator-color
- **Vertical Tab:** absolute, top: var(--tab-v-v-padding), bottom: var(--tab-v-v-padding), left: 0 (RTL: right: 0), width: 3px, border-radius: full, background: --tab-indicator-color
- Shown only when `[aria-selected="true"]`

### Focus ring — `:focus-visible` box-shadow
- Applied on `.tab:focus-visible` directly (no pseudo-element)
- `box-shadow: inset 0 0 0 1px white, 0 0 0 3px var(--gray-900, #161616)`
- `border-radius` changes to `var(--radius-xs, 2px)` on focus (Figma: `--Radius-radius-xs`)
- Provides: inset white inner ring + outer 3px dark ring
- No layout shift (box-shadow is off-flow)

---

## Interaction Layer Decisions

Hover and pressed states use background color applied directly to the `.tab` element (not a separate layer) via `:hover`/`:active` CSS selectors. These apply only to unselected tabs; selected tabs suppress hover/pressed backgrounds.

---

## Focus Layer Decisions

"Focus outline" RECTANGLE in Figma is a focus-only layer (visible only in Focused state). Implemented as `::after`. Removed from DOM — no standalone HTML needed.

---

## Z-Index / Layering Decisions

```css
.tab { position: relative; }
.tab::before { /* indicator — no z-index needed, pointer-events: none */ }
.tab__icon, .tab__text { /* normal flow, no z-index */ }
/* No ::after — focus ring uses box-shadow on :focus-visible, no stacking context needed */
```

Tab list divider (`.tab-list--h::after`) is at `z-index: 0`. Tab buttons are `z-index: 1` so they sit above the divider.

---

## Risks

1. **Arrow key JS required:** The CSS-only component renders correctly but is not keyboard-navigable between tabs without additional JavaScript.
2. **Text-default #161616:** The Figma `--Text-text-default` value (#161616) doesn't map to any token.css primitive. `--gray-950 = #0d121c` is close but not identical. Hardcoded fallback used.
3. **Vertical tab 6px padding:** `--space-6` does not exist in token.css. Hardcoded 6px fallback used.
4. **Vertical Large font-size 16px:** Size switch at Large is unique to vertical tabs. Not present in horizontal.

---

## Assumptions

1. The ARIA Tabs pattern is required. `<button role="tab">` is the only valid tab root.
2. RTL layout uses `[dir="rtl"]` on an ancestor element.
3. Flush=True removes container horizontal padding. The Figma CSS delta is not visible.
4. More Tab (overflow) is out of scope.
5. Tab panel content is provided by the consuming application.
6. Arrow key navigation is implemented by the consuming application's JavaScript.

---

## Known Issues

1. **Showcase states matrices were incomplete (fixed 2026-06-09):** The horizontal states matrix was missing Hover (selected) and Pressed (selected) rows. The vertical states matrix was missing Hover (selected), Pressed (selected), and Focused (selected) rows. The CSS was already correct for all these states — the gap was showcase-only. All 10 state combinations are now documented in both matrices.

---

## Missing Tokens

| Token | Proposed Value | Reason |
|---|---|---|
| `--tab-vertical-sm-v-padding` | 2px | `--space-2` exists but named differently |
| `--tab-vertical-sm-h-padding` | 6px | No `--space-6` primitive in token.css |
| `--tab-vertical-md-v-padding` | 6px | No `--space-6` primitive |
| `--tab-text-default` | #161616 | Figma `--Text-text-default` ≠ any token.css primitive |
| All `--tab-*` tokens | Various | Not yet in token.css |

---

## Missing Standards

- `PLATFORM-CODE-TAB-005`: Arrow key navigation JavaScript requirement — no audit rule exists for JS behavior.

---

## TODO

- [ ] Add all `--tab-*` tokens to `token.css`
- [ ] Add `--space-6: 6px` to token.css (or verify it already exists under a different name)
- [ ] Verify `--Text-text-default` (#161616) mapping to token.css
- [ ] Implement Arrow key JavaScript for keyboard tab navigation
- [ ] Implement More Tab overflow button (separate component initiative)
- [ ] Consider whether tab panel (`role="tabpanel"`) markup should be bundled in this package
