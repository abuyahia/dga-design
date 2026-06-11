# Component Analysis

- **Manifest path:** `components/content-switcher/mainifest.json`
- **Component name:** Content Switcher

## Source

Figma plugin export: `mainifest.json` (filename contains typo "mainifest", preserved as exported).
Secondary export: `mainifest-items.json` — defines the `_Content Switcher Item` subcomponent with full state matrix.
Source type: `COMPONENT_SET` with 12 container variants + 144 item variants.

## Detected Anatomy

**Container:**
- `content-switcher` root: `display: inline-flex`, `align-items: flex-start`, no gap, no padding
- Horizontal segmented control wrapping N items

**Item (structural):**
- `_Content Switcher Item` INSTANCE node
- Positions: `First`, `Mid`, `Last` (from items manifest)
- Contains one TEXT child (label)
- No icon slots detected

**Item children:**
- `Item` / `عنصر` — TEXT node (label)
- `Focus outline` — absolute positioned layer (focus indicator, pseudo-element candidate)

## Detected Axes

| Axis | Values | CSS Impact |
|------|--------|------------|
| Size | Small, Medium, Large | Yes — height, padding-x, font-size, line-height |
| OnColor | False, True | Yes — background, border, text color scheme |
| RTL | False, True | None — browser handles via `dir="rtl"`; structural radius is identical |

## Detected Variants

**Container manifest:** 12 variants (2 RTL × 2 OnColor × 3 Size).
**Items manifest:** 144 variants (2 RTL × 4 ItemType × 4 State × 2 OnColor × 3 Size).

Meaningful CSS implementation variants: 2 (OnColor) × 3 (Size) = 6 class combinations.
RTL axis discarded from CSS (see Architecture Findings).

## Detected States

From items manifest (`mainifest-items.json`):

| State | Source |
|-------|--------|
| Normal | items manifest |
| Hovered | items manifest |
| Selected | items manifest |
| Focused | items manifest |

Disabled state: NOT present in either manifest.

## Detected Sizes

| Size | Height | Padding X | Font Size | Line Height |
|------|--------|-----------|-----------|-------------|
| Small | 32px | 8px (`--spacing-buttonbuttons-sm-padding`) | 16px (`text-md`) | 24px |
| Medium | 40px | 12px (`--spacing-buttonbuttons-md-padding`) | 18px (`text-Ig`) | 28px |
| Large | 48px | 16px (`--spacing-buttonbuttons-lg-padding`) | 20px (`text-xl`) | 30px |

## Architecture Findings

**1. RTL axis discarded from CSS.**
RTL=True vs RTL=False changes only which item is shown as "selected" in the static Figma preview (first vs last). The structural border-radius is identical between both. CSS logical properties (`border-inline`, `border-start-start-radius`, etc.) plus browser `dir="rtl"` handling produce correct RTL layout without extra selectors.

**2. Item positions are structural.**
`:first-child` receives the left-cap rounding. `:last-child` receives the right-cap rounding. No positional modifier classes needed. Works for any N ≥ 2 items.

**3. Hover token delta is invisible with current fallback values.**
Normal: `--Button-button-background-neutral-default` → `#F3F4F6`
Hovered: `--Button-button-background-neutral-hovered` → `#F3F4F6`
Both primitives resolve to the same value. Hover delta is token-dependent and will become visible once `--content-switcher-item-bg-hovered` is defined with a distinct value.

**4. Focus indicator uses two-layer ring.**
Figma Focused state: outer `border: 2px solid --Border-border-black` on the item itself + inner `Focus outline` layer (`position: absolute; inset: 2px; border: 1px solid --Border-border-white`). Implemented via `:focus-visible` + `::after` pseudo-element.

**5. Focused state is always shown on the selected item in Figma.**
The items manifest only shows Focused on selected items. In production, any item (selected or not) can receive keyboard focus. CSS must handle both cases.

**6. OnColor hover is unchanged from normal.**
In OnColor=True, both normal and hovered states use `--Button-button-background-transparent-hovered`. No hover delta for OnColor mode.

## Token Findings

### OnColor=False
| Purpose | Figma token | Proposed component token |
|---------|------------|--------------------------|
| Default bg | `--Button-button-background-neutral-default` | `--content-switcher-item-bg-default` |
| Hover bg | `--Button-button-background-neutral-hovered` | `--content-switcher-item-bg-hovered` |
| Selected bg | `--Button-button-background-black-default` | `--content-switcher-item-bg-selected` |
| Default border | `--Border-border-neutral-primary` | `--content-switcher-item-border` |
| Default text | `--Text-text-default` | `--content-switcher-item-text-default` |
| Selected text | `--Text-text-oncolor-primary` | `--content-switcher-item-text-selected` |
| Focus outer | `--Border-border-black` | `--content-switcher-focus-ring` |
| Focus inner | `--Border-border-white` | `--content-switcher-focus-ring-inner` |

### OnColor=True
| Purpose | Figma token | Proposed component token |
|---------|------------|--------------------------|
| Default/hover bg | `--Button-button-background-transparent-hovered` | `--content-switcher-item-bg-default-oncolor` |
| Selected bg | `--Button-button-background-primary-default` | `--content-switcher-item-bg-selected-oncolor` |
| Border | `--Border-border-transparent-10` | `--content-switcher-item-border-oncolor` |
| Text (all) | `--Text-text-oncolor-primary` | `--content-switcher-item-text-oncolor` |
| Focus outer | `--Border-border-black` | `--content-switcher-focus-ring` |
| Focus inner | `--Border-border-white` | `--content-switcher-focus-ring-inner` |

### Sizing
| Purpose | Proposed component token | Fallback |
|---------|--------------------------|---------|
| Radius | `--content-switcher-radius` | `var(--radius-md)` |
| Small height | `--content-switcher-sm-height` | `32px` |
| Small padding-x | `--content-switcher-sm-padding-x` | `var(--spacing-buttonbuttons-sm-padding)` |
| Medium height | `--content-switcher-md-height` | `40px` |
| Medium padding-x | `--content-switcher-md-padding-x` | `var(--spacing-buttonbuttons-md-padding)` |
| Large height | `--content-switcher-lg-height` | `48px` |
| Large padding-x | `--content-switcher-lg-padding-x` | `var(--spacing-buttonbuttons-lg-padding)` |
| Small font-size | `--content-switcher-sm-font-size` | `var(--Size-Text-typo-size-text-md)` |
| Medium font-size | `--content-switcher-md-font-size` | `var(--Size-Text-typo-size-text-Ig)` |
| Large font-size | `--content-switcher-lg-font-size` | `var(--Size-Text-typo-size-text-xl)` |
| Small line-height | `--content-switcher-sm-line-height` | `var(--Line-Height-Text-line-heights-text-md)` |
| Medium line-height | `--content-switcher-md-line-height` | `var(--Line-Height-Text-line-heights-text-Ig)` |
| Large line-height | `--content-switcher-lg-line-height` | `var(--Line-Height-Text-line-heights-text-xl)` |
| Font family | `--content-switcher-font-family` | `var(--Font-Family-font-family-text)` |

## Accessibility Findings

1. **ARIA pattern:** Role `tablist` (container) + `tab` (items). Panels use `tabpanel`. JavaScript required for activation and keyboard navigation.
2. **Keyboard:** Arrow Left/Right cycles items. Home/End jump to first/last. Tab exits the group (roving tabindex pattern).
3. **Focus indicator:** Sourced from items manifest — two-layer ring (dark outer, white inner). Implemented via `:focus-visible` + `::after`.
4. **min-width:** 76px from manifest — adequate touch target for large enough text.
5. **Font:** IBM Plex Sans Arabic — RTL-compatible.
6. **aria-selected:** Selected item `aria-selected="true"`, others `"false"`.
7. **tabindex:** Active item `tabindex="0"`, inactive `tabindex="-1"` (roving tabindex).

## Compliance Findings

1. No official compliance claim made.
2. Focus indicator sourced from items manifest (`Focus outline` layer).
3. Disabled state not in manifest — not implemented; marked as TODO.
4. Hover delta is invisible with current token fallbacks — token-dependent.

## Implementation Decisions

1. **RTL axis discarded.** CSS logical properties handle all directional behavior.
2. **Selection via `aria-selected`.** No `.selected` modifier class.
3. **Item position via `:first-child` / `:last-child`.** No positional modifier classes.
4. **Size via modifier classes:** `--sm`, `--md`, `--lg`.
5. **OnColor via modifier class:** `--on-color`.
6. **Focus via `:focus-visible` + `::after`.** Matches Figma two-layer ring.
7. **`Focus outline` layer → `::after` pseudo-element.** Absolute positioned, inset 2px, 1px white border.
8. **Hover state added.** Token-driven; visually inactive with current fallback values.

## Intentional Deviations From Figma

1. **RTL axis dropped.** Handled natively by browser with `dir="rtl"` and CSS logical properties.
2. **Focus state not limited to selected items.** Figma only shows focus on selected items; CSS applies focus ring to any focused item.
3. **`border` on focus replaced with `outline`.** Avoids layout shift; `::after` provides inner ring.
4. **`Focus outline` converted to `::after`.** Not standalone HTML.
5. **Disabled state added as TODO.** Not in manifest.

## Risks

1. All `--content-switcher-*` tokens missing — CSS uses proposed names; fallback to primitives via comments.
2. Hover delta invisible until tokens are defined with distinct values.
3. Keyboard navigation requires JavaScript not included in CSS/HTML templates.

## Assumptions

1. `mainifest-items.json` defines the `_Content Switcher Item` sub-component. Items are rendered inline.
2. RTL is controlled by `dir="rtl"` on the container or ancestor.
3. OnColor mode is set by context or explicit modifier class on the container.
4. Any item can be selected — selection order is not fixed to first/last.

## Known Issues

1. `--Button-button-background-neutral-hovered` resolves to same fallback as `--neutral-default` — hover is invisible with current tokens.
2. Medium size font-size token uses `text-Ig` (unusual casing) — may be a typo in the design system.
3. Disabled state not present in manifest — not included in implementation.

## Missing Tokens

- `--content-switcher-item-bg-default`
- `--content-switcher-item-bg-hovered`
- `--content-switcher-item-bg-selected`
- `--content-switcher-item-border`
- `--content-switcher-item-text-default`
- `--content-switcher-item-text-selected`
- `--content-switcher-item-bg-default-oncolor`
- `--content-switcher-item-bg-selected-oncolor`
- `--content-switcher-item-border-oncolor`
- `--content-switcher-item-text-oncolor`
- `--content-switcher-focus-ring`
- `--content-switcher-focus-ring-inner`
- `--content-switcher-radius`
- `--content-switcher-font-family`
- `--content-switcher-sm-height`
- `--content-switcher-sm-padding-x`
- `--content-switcher-sm-font-size`
- `--content-switcher-sm-line-height`
- `--content-switcher-md-height`
- `--content-switcher-md-padding-x`
- `--content-switcher-md-font-size`
- `--content-switcher-md-line-height`
- `--content-switcher-lg-height`
- `--content-switcher-lg-padding-x`
- `--content-switcher-lg-font-size`
- `--content-switcher-lg-line-height`

## Missing Standards

- Disabled state visual specification
- Hover token values (distinct from normal)

## Layer Classification

| Layer | Figma Type | Implementation Role |
|-------|-----------|---------------------|
| Content Switcher (container) | COMPONENT_SET | Structural — tablist container |
| _Content Switcher Item | INSTANCE | Structural — interactive tab item |
| Item / عنصر | TEXT | Structural — label text node |
| Focus outline | FRAME (absolute) | Focus layer — converted to `::after` pseudo-element |

## State Delta Matrix

| State | Background (OnColor=F) | Border | Text | Extras |
|-------|----------------------|--------|------|--------|
| Normal | `item-bg-default` | `item-border` (inline sides) | `item-text-default` | — |
| Hovered | `item-bg-hovered` | `item-border` (same) | `item-text-default` | Token-dependent delta |
| Selected | `item-bg-selected` | none | `item-text-selected` | — |
| Focused | `item-bg-selected` | — | `item-text-selected` | outer 2px ring + inner 1px ring |

OnColor=True uses the `oncolor` token variants with same structural pattern.

## Pseudo-Element Decisions

| Figma Layer | Decision | Reason |
|-------------|----------|--------|
| `Focus outline` | `::after` | Absolute positioned, visual-only focus indicator; matches Figma inset ring exactly |

## Interaction Layer Decisions

No interaction/ripple/hover-overlay layers found. No `::before` needed.

## Focus Layer Decisions

`Focus outline` layer in Focused state → `::after` pseudo-element.
- `content: ''`
- `position: absolute`
- `inset: 2px`
- `border: 1px solid var(--content-switcher-focus-ring-inner)`
- `border-radius: calc(var(--content-switcher-radius) - 2px)` on cap items, `0` on mid items
- `pointer-events: none`

Outer focus ring implemented via `outline: 2px solid var(--content-switcher-focus-ring)` on `:focus-visible`.

Focus strategy: `:focus-visible` (keyboard-only). Justification: items are interactive controls (`button` with `role="tab"`); pointer focus does not need the visible ring.

## Z-Index / Layering Decisions

No complex layering. `position: relative` on `.content-switcher__item` required for `::after` focus ring. `z-index: 1` on focused item to render focus ring above adjacent items.

## TODO

- Add all missing tokens to `token.css` (see Missing Tokens list)
- Verify `text-Ig` token naming — possible typo
- Add keyboard interaction JavaScript for `tablist` activation pattern
- Review hover token values with designer to define a distinct hovered background
- Define and implement disabled state when available from design
- Review focus ring offset and thickness with accessibility team
- Confirm `--content-switcher-focus-ring` maps to platform-level focus color
