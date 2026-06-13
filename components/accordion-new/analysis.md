# Component Analysis

- Manifest path: `components/accordion-new/mainifest-1.json` + `components/accordion-new/mainifest-2.json`
- Component name: Accordion

---

## Source

Three source files in this folder:

| File | Type | Variants | Notes |
|---|---|---|---|
| `mainifest-1.json` | Accordion COMPONENT_SET | 60 | Default/Pressed/Disabled collapsed; Hovered/Focused expanded; all sizes, alignments, flush modes |
| `mainifest-2.json` | Accordion COMPONENT_SET | 60 | Hovered/Focused collapsed; Default/Pressed/Disabled expanded; complements mainifest-1 |
| `mainifest-list.json` | Accordion list COMPONENT_SET | 2 | Assembly of multiple accordion items; RTL=False + RTL=True; analyzed separately |

Combined raw variants: 120. Meaningful axes: Size × State × Expanded × Flush × Icon alignment = 3 × 5 × 2 × 2 × 2 = 120.

---

## Detected Anatomy

```
.accordion                      ← root item (div), has border-top divider
├── .accordion__trigger         ← <button>, toggle trigger, owns aria-expanded
│   ├── .accordion__title       ← <span>, heading text, flex: 1
│   └── .accordion__icon        ← <svg aria-hidden>, chevron, rotates on expand
└── .accordion__panel           ← <div>, collapsible content region
    └── .accordion__body        ← content slot (text, rich content)
```

---

## Detected Axes

| Axis | Values | CSS implementation |
|---|---|---|
| Size | Small, Medium, Large | Modifier class `.accordion--sm`, `.accordion--md` (Large = default) |
| Icon alignment | Trailing (default), Leading | Modifier class `.accordion--icon-leading` |
| State | Default, Hovered, Pressed, Focused, Disabled | CSS pseudo-selectors on `.accordion__trigger` |
| Expanded | True, False | `aria-expanded` on trigger + adjacent sibling panel |
| Flush | True, False | Modifier class `.accordion--flush` |
| RTL | Not present in manifest | CSS logical properties throughout; parent sets `dir="rtl"` |

---

## Detected Variants

Raw variant count: 120 (60 per manifest file). After axis collapse: 5 States × 3 Sizes × 2 Icon alignments × 2 Flush modes × 2 Expanded states = 120.
No duplicate axes detected between mainifest-1 and mainifest-2 — they cover complementary state/expanded combinations.

---

## Detected States

| State | Trigger | Visual delta |
|---|---|---|
| Default | (base) | No background |
| Hovered | `:hover` | `::before` bg = `var(--Button-button-background-neutral-hovered, #F3F4F6)` |
| Pressed | `:active` | `::before` bg = `var(--Button-button-background-neutral-pressed, #E5E7EB)` |
| Focused | `:focus-visible` | `outline: 2px solid var(--Border-border-black)` inset; Flush mode uses `::after` bleed |
| Disabled | `[disabled]` | Title/icon color → `var(--Global-text-default-disabled, #9DA4AE)`; no bg states |

---

## Detected Sizes

| Size | padding-block | padding-inline | CSS modifier |
|---|---|---|---|
| Large | `var(--Global-spacing-xl, 16px)` | `var(--Global-spacing-xl, 16px)` | (default) |
| Medium | `var(--Global-spacing-lg, 12px)` | `var(--Global-spacing-xl, 16px)` | `.accordion--md` |
| Small | `var(--Global-spacing-md, 8px)` | `var(--Global-spacing-xl, 16px)` | `.accordion--sm` |

Typography is identical across all sizes (font-size, weight, line-height unchanged).

---

## Architecture Findings

1. **Primitive classification**: Individual accordion item is a self-contained primitive. The Accordion list (mainifest-list.json) is an Assembly that composes multiple accordion items.
2. **Two-manifest split**: The Figma exports were split across two files. Both represent the same COMPONENT_SET. Combined, they cover the full matrix.
3. **Icon rotation**: Figma uses separate `arrow-down-01` and `arrow-up-01` icon instances per expanded state. Implementation collapses to a single icon rotated 180° via CSS `transform`. This is the standard accordion pattern and reduces DOM complexity.
4. **Content indentation**: Content panel is indented 48px on the icon side (= 16px base padding + 16px gap + 16px icon). In Flush+Leading mode the indent is 32px (= 16px gap + 16px icon, no base padding).
5. **RTL axis absent from accordion manifests**: Only RTL=False in mainifest-1 and mainifest-2. RTL support is implemented via CSS logical properties (`padding-inline`, `inset-inline`, `margin-inline`) — the parent document sets `dir="rtl"`.

---

## Component Classification

**Primitive Component**

- Self-contained accordion item
- No required child component dependencies
- Accordion list (mainifest-list.json) is the Assembly counterpart

---

## Component Dependencies

None.

---

## Dependency Confirmation

Not applicable — Primitive component.

---

## Layer Classification

| Figma layer | Type | Role | Implementation |
|---|---|---|---|
| `Accordion` (root) | COMPONENT | Structural | `.accordion` div |
| `Accordion header` | FRAME | Structural | `.accordion__trigger` button |
| `Accordion Title` | TEXT | Structural | `.accordion__title` span |
| `arrow-down-01` / `arrow-up-01` | INSTANCE | Icon Layer | `.accordion__icon` SVG, rotated via CSS |
| `Background` RECTANGLE | RECTANGLE (absolute, mix-blend-mode) | Interaction Layer | `.accordion__trigger::before` pseudo |
| `Accordion content` | FRAME | Structural | `.accordion__panel` div |
| `Content` | TEXT | Structural | `.accordion__body` div |

---

## State Delta Matrix

| State | Background (`::before`) | Title color | Icon color | Border/outline |
|---|---|---|---|---|
| Default | none | `--accordion-title-color` | currentColor | none |
| Hovered | `--accordion-bg-hovered` | `--accordion-title-color` | currentColor | none |
| Pressed | `--accordion-bg-pressed` | `--accordion-title-color` | currentColor | none |
| Focused | none | `--accordion-title-color` | currentColor | 2px solid `--accordion-focus-ring-color` |
| Disabled | none | `--accordion-title-color-disabled` | 0.4 opacity | none |

---

## Pseudo-Element Decisions

| Pseudo | Purpose | Why |
|---|---|---|
| `::before` on `.accordion__trigger` | Hover/pressed background overlay | Background RECTANGLE is `position: absolute`, `mix-blend-mode: multiply`, purely visual — interaction layer |
| `::after` on `.accordion__trigger` (Flush only) | Focus ring bleed | Flush focus ring extends -16px beyond 0-padded header; standard `outline` cannot bleed — needs positioned `::after` |

---

## Interaction Layer Decisions

- `Background` RECTANGLE in Figma uses `mix-blend-mode: multiply` over a white background — equivalent to a plain semi-transparent or solid `background-color` overlay. `multiply` blend on white produces the same flat color result, so `mix-blend-mode` is NOT reproduced in CSS.
- Interaction layer is `pointer-events: none` and `z-index: 0`, structural content sits at `z-index: 1`.

---

## Focus Layer Decisions

**Strategy: `:focus-visible`**

Reasoning: The Figma Focused state exists alongside Hovered and Pressed states as distinct named states. This implies keyboard-only focus behavior — `:focus-visible` is appropriate. Users clicking with a pointer should not see the focus ring.

**Non-flush**: `outline: 2px solid var(--accordion-focus-ring-color); outline-offset: -2px` directly on `.accordion__trigger`.

**Flush**: Figma shows a RECTANGLE `left: -16px` with `border: 2px solid`. Implementation: suppress default `outline`, add `::after` with `inset-inline: calc(-1 * var(--accordion-padding-inline))` to replicate the bleed.

---

## Z-Index / Layering Decisions

```
z-index: 0 → .accordion__trigger::before  (interaction background)
z-index: 1 → .accordion__title, .accordion__icon  (structural content)
z-index: 2 → .accordion__trigger::after  (focus ring in flush mode, sits above content)
```

`.accordion__trigger` has `position: relative` to establish stacking context.

---

## Severity Classification

**High:** None at generation.

**Medium:**
- All `--accordion-*` tokens are missing from `token.css` — using global token fallbacks directly in component file.
- Flush focus ring bleed is an approximation — exact geometry depends on parent container context.

**Low:**
- Icon rotation animation (transition) is an enhancement not present in Figma — motion policy not confirmed.
- `mix-blend-mode: multiply` not reproduced (acceptable given white background context).

**Advisory:**
- Add `accordion-list` generation pass for the Assembly (mainifest-list.json).
- Confirm icon system — `arrow-down-01` implies Carbon/HeroIcons; substitute appropriate SVG.

---

## Assembly Awareness

This accordion item participates in:

```
accordion (item)
    ↓
accordion-list (assembly)
```

The list assembly manages group behavior (e.g. single-expand policy), border-bottom terminus, and RTL container.

---

## Intentional Deviations From Figma

1. **Single arrow icon with CSS rotation** replaces two separate `arrow-down-01` / `arrow-up-01` instances — reduces DOM duplication, standard accordion pattern.
2. **`mix-blend-mode: multiply` not applied** — produces identical visual output on white backgrounds; avoids stacking context side effects.
3. **Flush focus bleed via `::after`** approximates the absolute-positioned RECTANGLE from Figma — pixel-exact bleed requires parent `overflow: clip` context.
4. **Icon rotate transition** (200ms ease-in-out) added as enhancement — not present in Figma.

---

## Risks

- Flush `::before` bleed with negative `inset-inline` will overflow visibly if parent has `overflow: visible` and no clipping context. Parent should use `overflow: clip`.
- `position: relative` + `overflow: visible` on `.accordion__trigger` is required for the `::before` bleed to work. Do not add `overflow: hidden` to the trigger.

---

## Assumptions

1. All RTL=False-only manifests imply RTL is parent-controlled (`dir="rtl"` on ancestor). Logical CSS properties ensure automatic RTL.
2. Font size does not change across sizes — only padding changes.
3. Leading content panel flush indent = 32px = icon(16px) + gap(16px), confirmed by `var(--Global-spacing-4xl, 32px)` in mainifest-2.json.
4. Icon color follows `currentColor` of the parent trigger (matches title color in Figma).

---

## Known Issues

None at generation time.

---

## Missing Tokens

All `--accordion-*` tokens below are proposed — not yet in `token.css`:

| Token | Proposed mapping | Fallback value |
|---|---|---|
| `--accordion-border-color` | `var(--Border-border-neutral-primary)` | `#D2D6DB` |
| `--accordion-title-color` | `var(--Text-text-default)` | `#161616` |
| `--accordion-title-color-disabled` | `var(--Global-text-default-disabled)` | `#9DA4AE` |
| `--accordion-content-color` | `var(--Text-text-primary-paragraph)` | `#384250` |
| `--accordion-bg-hovered` | `var(--Button-button-background-neutral-hovered)` | `#F3F4F6` |
| `--accordion-bg-pressed` | `var(--Button-button-background-neutral-pressed)` | `#E5E7EB` |
| `--accordion-focus-ring-color` | `var(--Border-border-black)` | `#161616` |
| `--accordion-focus-ring-width` | `2px` | — |
| `--accordion-title-font-family` | `var(--Font-Family-font-family-text)` | `"IBM Plex Sans Arabic"` |
| `--accordion-title-font-size` | `var(--Size-Text-typo-size-text-md)` | `16px` |
| `--accordion-title-font-weight` | `600` | — |
| `--accordion-title-line-height` | `var(--Line-Height-Text-line-heights-text-md)` | `24px` |
| `--accordion-content-font-size` | `var(--Size-Text-typo-size-text-md)` | `16px` |
| `--accordion-content-font-weight` | `400` | — |
| `--accordion-content-line-height` | `var(--Line-Height-Text-line-heights-text-md)` | `24px` |
| `--accordion-lg-padding-block` | `var(--Global-spacing-xl)` | `16px` |
| `--accordion-md-padding-block` | `var(--Global-spacing-lg)` | `12px` |
| `--accordion-sm-padding-block` | `var(--Global-spacing-md)` | `8px` |
| `--accordion-padding-inline` | `var(--Global-spacing-xl)` | `16px` |
| `--accordion-content-padding-top` | `var(--Global-spacing-md)` | `8px` |
| `--accordion-content-padding-bottom` | `var(--Global-spacing-3xl)` | `24px` |
| `--accordion-content-icon-indent` | `var(--Global-spacing-6xl)` | `48px` |
| `--accordion-content-icon-indent-flush` | `var(--Global-spacing-4xl)` | `32px` |
| `--accordion-gap` | `var(--Global-spacing-xl)` | `16px` |
| `--accordion-content-gap` | `var(--Global-spacing-md)` | `8px` |
| `--accordion-icon-size` | `16px` | — |
| `--accordion-transition-duration` | (missing — proposed: `var(--transition-fast)`) | `200ms` |
| `--accordion-transition-easing` | (missing — proposed: `var(--ease-in-out)`) | `ease-in-out` |

---

## Missing Standards

- No component-level token entry for accordion in `token.css`.

---

## TODO

- [ ] Add all `--accordion-*` tokens to `token.css`
- [ ] Generate `accordion-list` component from `mainifest-list.json` (Assembly)
- [ ] Confirm icon system (Carbon `arrow-down-01` vs HeroIcons vs custom)
- [ ] Confirm icon rotation animation is acceptable per motion policy
- [ ] Verify Flush focus ring bleed pixel accuracy with design team
- [ ] Confirm `mix-blend-mode` omission is acceptable
