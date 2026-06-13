# Component Analysis — Floating Button

- **Manifest path:** `components/floating-button/mainifest.json` _(note: filename typo in Figma export — preserved as-is)_
- **Component name:** Floating Button
- **Classification:** Primitive
- **Generated:** 2026-06-13

---

## Source

- Figma type: `COMPONENT_SET`
- Total Figma variants: 288
- Axes in manifest: RTL, State, Style, Icon only, Size, On color

---

## Detected Anatomy

| Layer | Type | Role |
|---|---|---|
| Root (`button`) | Structural | Component root — interactive control |
| `plus-sign` (INSTANCE) | Structural / Icon | Icon slot — replaced by `fab__icon` |
| `Button` (TEXT) | Structural | Label slot — replaced by `fab__label` |
| `Focus outline` (RECTANGLE) | Focus Layer | Focus ring — converted to `::after` pseudo-element |

---

## Detected Axes

| Axis | Values | Retained? |
|---|---|---|
| RTL | False, True | Partially — see RTL Decisions |
| State | Default, Hovered, Foucsed, Pressed, Disabled, Selected | Yes — via CSS selectors |
| Style | Primary- Neutral, Primary-Brand, Secondary-Solid | Yes — as CSS modifiers |
| Icon only | True, False | Yes — as HTML structure modes |
| Size | Small, Large | Yes — as CSS size modifier |
| On color | No, Yes | Yes — as CSS context modifier |

---

## Detected Variants

24 meaningful CSS variants (RTL=False baseline):
- 3 styles × 2 sizes × 2 on-color contexts × 2 icon modes
- States handled via CSS selectors; no markup duplication

---

## Detected States

| Figma State | CSS Selector | Note |
|---|---|---|
| Default | `.fab` (base) | — |
| Hovered | `.fab:hover:not(:disabled)` | — |
| Foucsed | `.fab:focus, .fab:focus-visible, .fab.is-focused` | Manifest typo: "Foucsed" |
| Pressed | `.fab:active, .fab.is-pressed` | — |
| Disabled | `.fab:disabled, .fab[aria-disabled="true"]` | — |
| Selected | `.fab[aria-pressed="true"], .fab.is-selected` | Toggle/selected state |

---

## Detected Sizes

| Figma Size | CSS Class | Padding | Icon | Notes |
|---|---|---|---|---|
| Small | `.fab` (default) | 16px all sides | 24px | `--spacing-lg` |
| Large | `.fab--lg` | 20px all sides | 24px | `--spacing-xl` |

Computed button diameter (icon-only):
- Small: 16 + 24 + 16 = 56px
- Large: 20 + 24 + 20 = 64px

---

## Architecture Findings

- The floating button is a circular action button (FAB pattern). Its `border-radius: 9999px` applies uniformly for both icon-only (circular) and labeled (pill) modes.
- No explicit width is set; the button sizes itself from padding + content.
- Icon-only vs. labeled is a pure HTML structure difference; no CSS modifier is required for icon-only mode.
- The gap between icon and label (labeled mode) is 8px (`--spacing-sm`).
- A `[dir="rtl"]` selector reverses flex direction for labeled mode. Icon-only is symmetric — RTL has no visual effect.

---

## Token Findings

All 41 component-level tokens (`--fab-*`) are missing from `token.css`. Provisional definitions are declared in a `:root` block at the top of `floating-button.css`.

**Tokens without a direct primitive equivalent:**

| Token | Figma value | Deviation |
|---|---|---|
| `--fab-bg-primary-neutral-on-color-hovered` | `rgba(255,255,255,0.80)` | No primitive; hardcoded in provisional block |
| `--fab-bg-primary-neutral-on-color-selected` | `rgba(255,255,255,0.70)` | No primitive; hardcoded |
| `--fab-bg-secondary-solid-on-color-default` | `rgba(255,255,255,0.20)` | No primitive; hardcoded |
| `--fab-bg-secondary-solid-on-color-hovered` | `rgba(255,255,255,0.20)` | No primitive; hardcoded |
| `--fab-bg-secondary-solid-on-color-focused` | `rgba(255,255,255,0.00)` | Maps to `transparent` |
| `--fab-bg-secondary-solid-on-color-pressed` | `rgba(255,255,255,0.40)` | No primitive; hardcoded |
| `--fab-bg-secondary-solid-on-color-selected` | `rgba(255,255,255,0.30)` | No primitive; hardcoded |
| `--fab-bg-disabled-on-color` | `rgba(255,255,255,0.20)` | Same value as `--button-primary-on-color-disabled-bg` |
| `--fab-text-disabled-on-color` | `rgba(255,255,255,0.40)` | Same as `--button-primary-on-color-disabled-text` |
| `--fab-text-primary-neutral-on-color` | `#161616` | Closest primitive: `--gray-950` (`#0d121c`) — minor deviation |
| `--fab-text-secondary-solid` | `#161616` | Closest primitive: `--gray-950` — minor deviation |
| `--fab-focus-ring-color` | `#161616` | Closest primitive: `--gray-950` — minor deviation |

---

## Accessibility Findings

1. **Icon-only buttons require `aria-label`** — The Figma icon-only variants have no visible label. HTML implementations must include `aria-label` or `aria-labelledby`.
2. **Focus ring color contrast risk** — Figma specifies `#161616` (dark) focus ring color for all styles, including Primary-Neutral (dark bg: `#0D121C`). The focus ring appears on the page background outside the button, so contrast is against the page background rather than the button. Risk: insufficient contrast if page background is also dark. Document in compliance.
3. **Selected state** — `aria-pressed="true"` required for toggle/selected semantics.
4. **Disabled state** — `[disabled]` is recommended over `aria-disabled` for `<button>` elements. Both are supported.
5. **Figma `On color=Yes` for Secondary-Solid focused** — background becomes fully transparent (`rgba(0,0,0,0)`). At full transparency, the button content (icon) may lack adequate background contrast. Flagged as medium accessibility risk.

---

## Compliance Findings

- No official compliance audit completed.
- WCAG 2.2 target level: AA.
- Focus ring: 3px solid border extending 5px beyond bounds satisfies the WCAG 2.2 Focus Appearance non-interference requirement if ring-to-background contrast ≥ 3:1.
- Focus ring color `#161616` on white page background = contrast ratio ≈ 19:1 (passes).
- Focus ring on dark page backgrounds: not specified by manifest; marked as risk.

---

## Implementation Decisions

1. **No `.fab--icon-only` CSS modifier** — Icon-only vs. labeled is a structural HTML difference. No CSS modifier needed; padding is identical for both modes. Labeled mode adds `fab__label`; icon-only omits it.
2. **Local CSS custom property pattern** — State background variables (`--_fab-bg-*`) are defined as local properties on `.fab` and overridden per style/context modifier. State selectors (`:hover`, `:active`, etc.) consume only the local variables. This avoids selector explosion.
3. **Provisional `:root` token block** — Since `--fab-*` tokens are not yet in `token.css`, provisional definitions are placed at the top of `floating-button.css` with `/* TODO: Move to token.css */` comments.
4. **Focus ring via `::after`** — Figma `Focus outline` RECTANGLE (position: absolute, left: -5px, top: -5px, border: 3px solid) is implemented as `::after` with `inset: -5px` and `border`.
5. **Focus: both `:focus` and `:focus-visible`** — Manifest shows general "Foucsed" state (not keyboard-only). Both pseudo-classes applied per button component precedent. `.is-focused` class added for static showcase display.
6. **Focus ring opacity approach** — `::after` is always present but `opacity: 0` by default; set to `opacity: 1` on focus. Avoids layout shift.
7. **Pressed cancels focus ring** — `fab:active::after { opacity: 0 }` matches Figma behavior where Pressed and Focused are mutually exclusive states.
8. **Transition: background only** — Only `background` is transitioned. No color transition to avoid flash when focus ring appears.

---

## Intentional Deviations From Figma

| Deviation | Reason |
|---|---|
| `--gray-950` (#0D121C) used for `#161616` text tokens | `#161616` has no primitive in `token.css`. `--gray-950` is the closest available value. Color difference is negligible (7px in lightness). |
| `--fab-bg-secondary-solid-on-color-focused` → `transparent` | Figma value is `rgba(255,255,255,0.00)`. `transparent` is semantically equivalent and avoids raw rgba in the provisional definition. |
| No fixed width on labeled variant | Figma shows `width: 116px` for the labeled small variant. This is a Figma frame constraint, not a CSS requirement. Component width is content-driven. |
| RTL for icon-only: no CSS delta applied | Circular icon-only button has no axis asymmetry. RTL produces no visual change for this mode. |

---

## Risks

1. **Focus ring on dark backgrounds** — Focus ring is always `--gray-950` regardless of style or on-color context. On dark page backgrounds (Primary-Neutral/Primary-Brand contexts), the ring may be invisible. Recommend adding a `--fab-focus-ring-color-on-color` token for on-color contexts.
2. **Secondary-Solid On-Color Focused = transparent** — When focused on a colored background, the Secondary-Solid FAB becomes fully transparent. This could cause the icon to lose visual containment. Consider a minimum background for focused on-color state.
3. **Minor color deviation** — `#161616` ≠ `--gray-950` (`#0D121C`). If exact Figma color fidelity is required, add `--color-text-strong: #161616` to `token.css`.
4. **Provisional tokens in component CSS** — The `:root` block in `floating-button.css` is a temporary measure. If `token.css` defines conflicting `--fab-*` tokens with different values, the component may render incorrectly. Token migration must be coordinated.

---

## Assumptions

1. The `plus-sign` Figma INSTANCE represents a generic icon slot; any 24×24 icon is acceptable.
2. The `Button` TEXT node in the labeled variant represents a generic label slot; any short label is acceptable.
3. Gap between icon and label (8px) applies to all styles and sizes in labeled mode.
4. Focus ring geometry (5px offset, 3px width) is fixed across all sizes.
5. Disabled state behavior is identical across all styles (same disabled background/text tokens).
6. `Primary-Brand` On-Color has the same backgrounds as `Primary-Brand` non-on-color (confirmed from manifest: identical background tokens).

---

## Component Classification

**Primitive Component**

Self-contained. No required child components. The icon slot accepts any inline SVG icon.

---

## Component Dependencies

- None required.
- Icons: any inline SVG passed to `fab__icon`. No icon component dependency declared.

---

## Dependency Confirmation

Not applicable for Primitive classification.

---

## Layer Classification

| Figma Layer | Type | Implementation Role | HTML Mapping |
|---|---|---|---|
| Root frame | COMPONENT | Structural | `<button class="fab">` |
| `plus-sign` | INSTANCE | Icon (Structural) | `<span class="fab__icon"><svg>` |
| `elements` | GROUP | Icon inner group | Inside `<svg>` |
| `Button` | TEXT | Structural (Label) | `<span class="fab__label">` |
| `Focus outline` | RECTANGLE | Focus Layer | `::after` pseudo-element |

---

## State Delta Matrix

| State | Background change | Text change | Focus ring | Notes |
|---|---|---|---|---|
| Default | base | base | hidden | — |
| Hovered | `*-hovered` | none | hidden | — |
| Focused | `*-focused` (same as default for most styles) | none | visible | `::after` opacity: 1 |
| Pressed | `*-pressed` | none | hidden | cancels focus ring |
| Selected | `*-selected` | none | hidden | `aria-pressed="true"` |
| Disabled | `--fab-bg-disabled` | `--fab-text-disabled` | hidden | pointer-events: none |

---

## Pseudo-Element Decisions

| Pseudo | Purpose | Source layer |
|---|---|---|
| `::after` | Focus ring: 3px solid border, inset -5px | `Focus outline` RECTANGLE |

No `::before` required. No ripple/hover overlay layers detected in manifest.

---

## Interaction Layer Decisions

No Interaction Circle, ripple, or state overlay layers were detected in the manifest. No pseudo-element interaction layers required.

---

## Focus Layer Decisions

- Strategy: `:focus` + `:focus-visible` (general focus, not keyboard-only)
- Implementation: `::after` with `opacity` toggle
- Geometry: `inset: -5px`, `border: 3px solid var(--fab-focus-ring-color)`
- The focus ring is outside the button bounds (grows 5px beyond all edges)

---

## Z-Index / Layering Decisions

| Element | z-index | Reason |
|---|---|---|
| `.fab` | `position: relative` | Establishes stacking context for `::after` |
| `.fab__icon` | `z-index: 1` | Sits above any future `::before` interactions |
| `.fab__label` | `z-index: 1` | Same |
| `.fab::after` | `z-index: 2` | Focus ring above content |

---

## Assembly Awareness

Floating Button is a Primitive. It may participate in future assemblies:
- Page shells (fixed-position FAB in bottom corner)
- Scroll-to-top patterns
- Action toolbars

Reusable boundaries must be preserved; do not merge into larger assemblies.

---

## Severity Classification

### High
- None detected.

### Medium
- Focus ring color on dark page backgrounds may have insufficient contrast (risk, not confirmed defect).
- Secondary-Solid On-Color Focused = transparent background — icon may lose visual containment.

### Low
- `#161616` ≠ `--gray-950` — minor color deviation.
- Provisional `:root` token block must be migrated to `token.css`.

### Advisory
- Consider adding `--fab-focus-ring-color-on-color: var(--white)` for on-color context focus ring.
- Add `--color-text-strong: #161616` to `token.css` to eliminate color deviation.

---

## Missing Tokens

All 41 `--fab-*` tokens are missing from `token.css`. Full list:

```
--fab-padding-sm
--fab-padding-lg
--fab-gap
--fab-radius
--fab-icon-size
--fab-label-font-family
--fab-label-font-size
--fab-label-font-weight
--fab-label-line-height
--fab-focus-ring-color
--fab-focus-ring-width
--fab-focus-ring-offset
--fab-bg-primary-neutral-default
--fab-bg-primary-neutral-hovered
--fab-bg-primary-neutral-pressed
--fab-bg-primary-neutral-selected
--fab-text-primary-neutral
--fab-bg-primary-neutral-on-color-default
--fab-bg-primary-neutral-on-color-hovered
--fab-bg-primary-neutral-on-color-focused
--fab-bg-primary-neutral-on-color-pressed
--fab-bg-primary-neutral-on-color-selected
--fab-text-primary-neutral-on-color
--fab-bg-primary-brand-default
--fab-bg-primary-brand-hovered
--fab-bg-primary-brand-pressed
--fab-bg-primary-brand-selected
--fab-text-primary-brand
--fab-bg-secondary-solid-default
--fab-bg-secondary-solid-hovered
--fab-bg-secondary-solid-pressed
--fab-bg-secondary-solid-selected
--fab-text-secondary-solid
--fab-bg-secondary-solid-on-color-default
--fab-bg-secondary-solid-on-color-hovered
--fab-bg-secondary-solid-on-color-focused
--fab-bg-secondary-solid-on-color-pressed
--fab-bg-secondary-solid-on-color-selected
--fab-text-secondary-solid-on-color
--fab-bg-disabled
--fab-bg-disabled-on-color
--fab-text-disabled
--fab-text-disabled-on-color
```

---

## Missing Standards

- No `--fab-focus-ring-color-on-color` token for on-color focus ring inversion.
- No official audit mapping exists yet for this component.

---

## Known Issues

- Manifest filename typo: `mainifest.json` (missing 'f'). Preserved as-is; referenced correctly in this analysis.
- Figma axis name typo: "Foucsed" → implemented as "focused" in all generated files.
- `#161616` used in Figma for text/focus-ring has no exact match in `token.css`.

---

## TODO

- [ ] Add all 41 `--fab-*` tokens to `token.css` and remove provisional `:root` block from `floating-button.css`.
- [ ] Add `--color-text-strong: #161616` to `token.css`.
- [ ] Add `--fab-focus-ring-color-on-color: var(--white)` token for on-color focus ring.
- [ ] Commission accessibility audit for focus ring color on dark backgrounds.
- [ ] Commission official compliance audit (WCAG 2.2 AA, Platform Code standards).
- [ ] Review Secondary-Solid On-Color Focused transparent background behavior.
