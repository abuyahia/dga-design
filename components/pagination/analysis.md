# Component Analysis — Pagination

- **Manifest path**: `components/pagination/manifest.json` (assembly) · `components/pagination/manifest-complete.json` (_PaginationItem subcomponent)
- **Component name**: `Pagination` (assembly) + `_PaginationItem` (internal subcomponent)

---

## Source

`manifest.json` — Figma COMPONENT_SET export for the full Pagination bar (prev nav + page items + next nav).
`manifest-complete.json` — Figma COMPONENT_SET export for the `_PaginationItem` subcomponent used inside the bar.

---

## Detected Anatomy

**Pagination (assembly)**
1. `Button` (leading nav) — previous page icon button (instances of the Button component)
2. `_PaginationItem` instances — one per visible page number including ellipsis
3. `Button` (trailing nav) — next page icon button

**_PaginationItem (subcomponent)**
1. TEXT layer — the page number or "..." label
2. `Selector` RECTANGLE — a 3px bottom bar present only in `State=Current Page` → pseudo-element candidate

---

## Detected Axes

### Pagination (assembly)
| Axis | Values |
|------|--------|
| RTL  | False, True |
| Size | Large, Meduim [sic], Small |

### _PaginationItem (subcomponent)
| Axis     | Values |
|----------|--------|
| State    | Default, Hovered, Focsed [sic], Current Page, **Opened** |
| Size     | Large, Meduim [sic], Small |
| Overflow | No, **Yes** (yes = "..." trigger with page-jump dropdown) |

---

## Detected Variants

### Pagination
- `RTL=False, Size=Large`
- `RTL=True, Size=Large`
- `RTL=False, Size=Meduim` (typo for Medium)
- `RTL=True, Size=Meduim`
- `RTL=False, Size=Small`
- `RTL=True, Size=Small`

### _PaginationItem
- `State=Default, Size=Large/Meduim/Small, Overflow=No`
- `State=Hovered, Size=Large/Meduim/Small, Overflow=No`
- `State=Focsed, Size=Large/Meduim/Small, Overflow=No`
- `State=Current Page, Size=Large/Meduim/Small, Overflow=No`
- `State=Default/Hovered/Focsed, Size=Large/Meduim/Small, Overflow=Yes` — "..." trigger (1px border)
- `State=Opened, Size=Large/Meduim/Small, Overflow=Yes` — trigger + expanded page-jump dropdown panel

**Initial generation gap**: `manifest-complete.json` is 3376 lines. During initial generation only ~850 lines were read; the `State=Opened` variants with the dropdown panel (lines ~1302–2500+) were missed. Corrected in post-generation fix.

---

## Detected States

| State | CSS Mapping | Delta |
|-------|-------------|-------|
| Default | base | no bg, no border, no indicator |
| Hovered | `:hover` | +background-neutral-100 |
| Focsed → Focused | `:focus-visible` | +2px solid border-black outline |
| Current Page | `[aria-current="page"]` | +::after 3px green bottom bar |
| Overflow (closed) | `.pagination__item--overflow` | +1px solid border-black, cursor pointer |
| Overflow (opened) | `[aria-expanded="true"]` | +2px border + neutral-100 bg, dropdown visible |
| Pressed | `:active` | Not in Figma — best-practice addition |
| Disabled | `:disabled` | Not in Figma — best-practice addition |

---

## Detected Sizes

| Size   | Item Dimensions | Nav Dimensions | Item Padding | Font Size | Line Height |
|--------|-----------------|----------------|--------------|-----------|-------------|
| Large  | min-width: 40px, height: 40px | 40×40px fixed | 8px | 16px (text-md) | 24px |
| Medium | width: 32px, height: 32px | 32×32px fixed | 6px | 16px (text-md) | 24px |
| Small  | min-width: 24px, height: 24px | 24×24px fixed | 4px | 14px (text-sm) | 20px |

---

## Architecture Findings

1. **Assembly vs subcomponent split**: Pagination is a composite assembly. `_PaginationItem` is an internal subcomponent. Both are generated into the same `components/pagination/` folder since no separate folder exists for the subcomponent. The leading underscore (`_`) marks it as internal.
2. **Navigation buttons** are instances of the global Button component (transparent/icon-only shape). Pagination CSS provides minimal sizing and layout overrides only; full interactive state styling defers to Button component.
3. **RTL axis is real and produces meaningful CSS difference**: the visual order of items reverses and arrow icons flip direction.
4. **RTL implementation**: Use `[dir="rtl"]` attribute selector. Flexbox row direction is reversed by the browser's `direction: rtl` inherited from the parent. Nav arrow icons are flipped via `transform: scaleX(-1)`.
5. **Size discrepancy in assembly**: In the assembly manifest, single-digit items appear at 26px width (fitted to content), but the _PaginationItem spec defines 40px. Implementation uses `min-width` for large/small (flexible) and fixed `width` for medium, matching the _PaginationItem spec's display values (`inline-flex` for small, `flex` for large/medium).

---

## Token Findings

All token names below are **component-level semantic tokens** that do not yet exist in `token.css`. They must be added to `token.css` (global update — do not apply automatically).

| Component Token | Fallback Source | Value |
|-----------------|-----------------|-------|
| `--pagination-items-gap` | `--spacing-paginationpagination-items-padding` | 8px |
| `--pagination-item-lg-padding` | `--spacing-paginationpagination-item-lg-padding` | 8px |
| `--pagination-item-md-padding` | `--spacing-paginationpagination-item-md-padding` | 6px |
| `--pagination-item-sm-padding` | `--spacing-paginationpagination-item-sm-padding` | 4px |
| `--pagination-item-lg-size` | — | 40px |
| `--pagination-item-md-size` | — | 32px |
| `--pagination-item-sm-size` | — | 24px |
| `--pagination-nav-lg-size` | — | 40px |
| `--pagination-nav-md-size` | — | 32px |
| `--pagination-nav-sm-size` | — | 24px |
| `--pagination-item-radius` | `--Radius-radius-sm` | 4px |
| `--pagination-item-text-color` | `--Text-text-default` | #161616 |
| `--pagination-item-hover-bg` | `--Background-background-neutral-100` | #F3F4F6 |
| `--pagination-item-pressed-bg` | `--Background-background-neutral-200` | (not defined) |
| `--pagination-item-focus-border-color` | `--Border-border-black` | #161616 |
| `--pagination-item-focus-border-width` | — | 2px |
| `--pagination-item-current-indicator-bg` | `--Background-background-primary` | #1B8354 |
| `--pagination-item-current-indicator-radius` | `--radius-radius-full` | 9999px |
| `--pagination-item-overflow-border-color` | `--Border-border-black` | #161616 |
| `--pagination-item-disabled-text` | `--Text-text-disabled` | (not defined) |
| `--pagination-font-family` | `--Font-Family-font-family-text` | IBM Plex Sans Arabic |
| `--pagination-item-lg-font-size` | `--Size-Text-typo-size-text-md` | 16px |
| `--pagination-item-md-font-size` | `--Size-Text-typo-size-text-md` | 16px |
| `--pagination-item-sm-font-size` | `--Size-Text-typo-size-text-sm` | 14px |
| `--pagination-item-lg-line-height` | `--Line-Height-Text-line-heights-text-md` | 24px |
| `--pagination-item-md-line-height` | `--Line-Height-Text-line-heights-text-md` | 24px |
| `--pagination-item-sm-line-height` | `--Line-Height-Text-line-heights-text-sm` | 20px |
| `--pagination-item-overflow-open-bg` | `--Background-background-neutral-100` | #F3F4F6 |
| `--pagination-overflow-panel-z-index` | — | 100 |
| `--pagination-overflow-panel-padding` | `--spacing-paginationpagination-item-sm-padding` | 4px |
| `--pagination-overflow-panel-border-color` | `--Border-border-neutral-primary` | #D2D6DB |
| `--pagination-overflow-panel-bg` | `--Background-background-white` | #FFF |
| `--pagination-overflow-panel-shadow` | global elevation tokens | 0 20px 24px -4px rgba(16,24,40,0.08)… |
| `--pagination-overflow-option-width` | — | 60px |
| `--pagination-overflow-option-padding` | `--Global-spacing-md` | 8px |
| `--pagination-overflow-option-gap` | `--Global-spacing-md` | 8px |
| `--pagination-overflow-option-font-size` | `--Size-Text-typo-size-text-sm` | 14px |
| `--pagination-overflow-option-line-height` | `--Line-Height-Text-line-heights-text-sm` | 20px |

---

## Accessibility Findings

1. Container must be `<nav aria-label="Pagination">` — provides landmark and accessible name.
2. Current page item must have `aria-current="page"`.
3. Each page number button must have `aria-label="Page N"` (visible number alone is insufficient for screen readers if focus moves between numbers rapidly).
4. Overflow/ellipsis items must be `aria-hidden="true"` or rendered as `<span>` — they are non-interactive and decorative.
5. Disabled nav buttons must use `aria-disabled="true"` + visual indication if `disabled` attribute is not used (to preserve keyboard focus for AT).
6. Icon-only nav buttons must have accessible name via `aria-label="Previous page"` / `aria-label="Next page"`.

---

## Compliance Findings

1. `aria-current="page"` required — not optional.
2. Focus indicator (2px solid outline) must have 3:1 contrast ratio — `#161616` on white background passes.
3. Current page indicator (green bottom bar) — purely decorative; color not the sole conveyor of meaning (font-weight change also present). Acceptable.
4. Touch target for Small size (24px) is below the recommended 44px minimum. Noted as risk.

---

## Implementation Decisions

1. **Selector layer → `::after` pseudo-element** on `.pagination__item--current` / `[aria-current="page"]`. The `_PaginationItem` receives `position: relative`.
2. **Hovered state → `:hover`** on `.pagination__item`. No extra HTML element needed.
3. **Focused state → `:focus-visible`**. Uses `outline` (not `border`) to avoid layout shift. `outline-offset: 0` matches Figma's inset focus appearance.
4. **RTL via `[dir="rtl"]`** — no separate markup required. Arrow icons flip via `transform: scaleX(-1)`.
5. **Overflow items** rendered as `<button>` with `aria-expanded`/`aria-haspopup="listbox"`. The Figma `State=Opened` state confirms the "..." is an interactive trigger that opens a page-jump dropdown. The panel is a `<ul role="listbox">` with `<button role="option">` items. Selected item has `aria-selected="true"` + check icon.
6. **Nav buttons** use `<button type="button">` with icon SVG. Minimal pagination-specific sizing overrides only.
7. **Selector bottom offset**: Figma shows `bottom: -1px` for Small. Implemented as-is with overflow allowed via `overflow: visible` on the item. Medium shows `bottom: 2.5px` — corrected to `bottom: 0` (see Intentional Deviations).
8. **Selector width**: computed via `calc(100% - padding * 2)` to stay aligned with content area.

---

## Intentional Deviations From Figma

| # | Location | Figma Value | Implementation Value | Reason |
|---|----------|-------------|---------------------|--------|
| 1 | Small item indicator: `bottom: -1px` | -1px | -1px | Preserved. Parent needs `overflow: visible`. |
| 2 | Medium item indicator: `bottom: 2.5px` | 2.5px | 0 | Sub-pixel value causes rendering inconsistency across browsers. Zero bottom is more reliable. |
| 3 | Medium item indicator: `left: 4px` | 4px (but padding is 6px) | `calc(left: var(--pagination-item-md-padding))` = 6px | Design inconsistency — left=4px in a 32px item with 6px padding leaves the bar off-center. Using padding-based calc is correct. |
| 4 | Figma typo "Focsed" | "Focsed" | "focused" | Typo correction |
| 5 | Figma typo "Meduim" | "Meduim" | "medium" | Typo correction |
| 6 | No pressed/disabled states in Figma | missing | `:active`, `:disabled` added | Government platform standard requires all states |

---

## Risks

1. **Small touch target (24px)** may fail accessibility audit for touch interfaces. Flag for stakeholder review.
2. **`bottom: -1px`** on Small current indicator overflows the item. Parent containers must not clip with `overflow: hidden`.
3. **Font-family fallback**: "IBM Plex Sans Arabic" may not be loaded. Ensure font is referenced in the global stylesheet.
4. **Button component dependency**: Nav buttons are not fully styled by pagination.css. If Button component is not loaded, nav buttons will lack hover/focus styles.

---

## Assumptions

1. Navigation buttons use the Button component's transparent icon-only variant. Pagination CSS does not re-implement Button interactive states.
2. Items in the assembly may flex beyond their `min-width` when page numbers have more digits (e.g., "999"). This is intentional.
3. `aria-label="Page N"` is the expected accessible name pattern (confirmed standard practice).
4. The `Selector` bottom bar in `Current Page` state is purely decorative (confirmed: font-weight change also present, passing WCAG 1.4.1).

---

## Known Issues

None at time of generation.

---

## Missing Tokens

All component-level pagination tokens listed in **Token Findings** are missing from `token.css`. They must be defined before production use.

**Global update required** (do not apply automatically — document only):
- Add all `--pagination-*` tokens to `token.css` with mappings to existing Figma/Spacing/Radius/Color tokens.
- Define `--pagination-item-pressed-bg`, `--pagination-item-disabled-text` which have no direct Figma source.

---

## Missing Standards

1. No explicit pressed/active state defined in Figma for `_PaginationItem`.
2. Touch target standard for Small (24px) not met.
3. Transition/animation tokens (`--pagination-item-transition-duration`) not in Figma.

---

## Layer Classification

| Layer | Type | Role | Implementation |
|-------|------|------|----------------|
| Pagination root | COMPONENT_SET | Structural | `<nav class="pagination">` |
| Button (nav) | INSTANCE | Structural (defers to Button component) | `<button class="pagination__nav">` |
| _PaginationItem | INSTANCE | Structural | `<button class="pagination__item">` |
| TEXT (page number) | TEXT | Structural (content) | Text node inside button |
| Selector (RECTANGLE) | RECTANGLE | Interaction layer (current indicator) | `::after` pseudo-element |
| _PaginationItem root (Overflow=Yes) | COMPONENT | Structural (wrapper) | `<span class="pagination__overflow-wrapper">` — HTML requires trigger+panel to be siblings; wrapper provides positioning context |
| List Sections (FRAME) | FRAME | Structural (overflow panel) | `<ul class="pagination__overflow-panel">` |
| Dropdown List Item (INSTANCE) | INSTANCE | Structural (page jump option) | `<button class="pagination__overflow-option">` |
| Entered Text (TEXT) | TEXT | Structural (page number in option) | Text node inside option button |
| Check (INSTANCE) | INSTANCE | Structural (selected indicator icon) | `<svg class="pagination__overflow-check">` |

---

## State Delta Matrix

| State | Background | Border | ::after (Selector) | Font Weight |
|-------|-----------|--------|-------------------|-------------|
| Default | none | none | none | 400 |
| Hovered | neutral-100 | none | none | 400 |
| Focused | none | 2px solid border-black (outline) | none | 400 |
| Current Page | none | none | 3px green bar at bottom | 600 |
| Overflow (closed) | none | 1px solid border-black | none | 400 |
| Overflow (opened) | neutral-100 | 2px solid border-black | none | 400 |
| Pressed* | neutral-100 | none | none | 400 |
| Disabled* | none | none | none | 400 (reduced opacity) |

*Not in Figma — added as best-practice.

### Overflow Dropdown Option State Delta

| State | Background | Font Weight |
|-------|-----------|-------------|
| Default option | none | 400 |
| Hovered option | neutral-100 | 400 |
| Focused option | 2px outline border-black | 400 |
| Selected option | none | 600 + check icon visible |

---

## Pseudo-Element Decisions

| Layer | Decision | CSS Target | Reason |
|-------|----------|------------|--------|
| Selector (RECTANGLE, Current Page) | → `::after` | `.pagination__item[aria-current="page"]::after` | No semantic meaning, visual indicator only, exists only in Current Page state |

---

## Interaction Layer Decisions

No standalone interaction layers (ripple, hover overlay) detected in manifest. Hover is implemented as direct background color change on the item.

---

## Focus Layer Decisions

Focus state in Figma shows `border: 2px solid var(--Border-border-black)` added to the item. Implemented as CSS `outline` (not border) to avoid layout shift. `outline-offset: 0` replicates the inset appearance.

---

## Z-Index / Layering Decisions

```
.pagination__item { position: relative; z-index: 0; }
.pagination__item::after { position: absolute; z-index: 1; }  /* Selector bar */
```

No interaction circles or ripple layers detected. No z-index stacking issues.

---

## TODO

- [ ] Add all `--pagination-*` tokens to `token.css` (global file — do not modify automatically)
- [ ] Verify touch target compliance for Small size (24px) with product/accessibility team
- [ ] Verify that `bottom: -1px` for Small current indicator doesn't cause clipping in context
- [ ] Define `--pagination-item-pressed-bg` token mapping
- [ ] Define `--pagination-item-disabled-text` token mapping
- [ ] Confirm Button component class API for nav button integration
- [ ] Add overflow dropdown panel tokens to `token.css`: `--pagination-overflow-panel-*`, `--pagination-overflow-option-*`, `--pagination-item-overflow-open-bg`
- [ ] Add JS behavior: toggle `aria-expanded` on overflow trigger click, close panel on outside-click / Escape key
- [ ] Implement `State=Opened, Size=Meduim, Overflow=Yes` position validation (manifest section ~1800–1990 not fully read; Medium panel assumed same `left: 8px` as Large/Small based on consistent Figma coordinates pattern)
- [ ] Confirm Medium overflow panel position from design team (Figma typo "Meduim" makes locating the variant harder)
