# Component Analysis

- **Manifest path**: `components/checkbox-2/manifest.json`
- **Component name**: Checkbox (checkbox-2)
- **Figma type**: COMPONENT\_SET
- **Generation**: v2 (regenerated — updated skill with semantic layer analysis)

---

## Source

Figma plugin manifest export. Root node: `COMPONENT_SET "Checkbox"`. Total COMPONENT entries: 108.

---

## Detected Anatomy

| Element | Figma node name | Figma type | Implementation role |
|---|---|---|---|
| Component root | (COMPONENT_SET) | — | `<label class="checkbox">` |
| Native control | — | — | `<input type="checkbox" class="checkbox__input">` |
| Visual box | `_CheckboxBase1` | INSTANCE | `<span class="checkbox__box">` |
| Checkmark | `checkmark` | FRAME | `<svg class="checkbox__checkmark">` |
| Indeterminate mark | `Indeterminate mark` | FRAME | `<svg class="checkbox__indeterminate">` |
| Ripple | `Interaction Circle` | RECTANGLE | `.checkbox::before` (pseudo-element) |
| Focus indicator | `Focus Ring` | RECTANGLE | `.checkbox__box::after` (pseudo-element) |

---

## Layer Classification

| Layer | Figma type | Layer role | Implementation decision |
|---|---|---|---|
| `_CheckboxBase1` | INSTANCE | **Structural Layer** | Rendered as `<span class="checkbox__box">` — real DOM element |
| `checkmark` | FRAME | **Icon Layer** | Rendered as inline SVG `.checkbox__checkmark` — state-driven visibility |
| `Indeterminate mark` | FRAME | **Icon Layer** | Rendered as inline SVG `.checkbox__indeterminate` — state-driven visibility |
| `Interaction Circle` | RECTANGLE | **Interaction Layer** | Converted to `.checkbox::before` pseudo-element — no standalone HTML |
| `Focus Ring` | RECTANGLE | **Focus Layer** | Converted to `.checkbox__box::after` pseudo-element — no standalone HTML |

---

## Detected Axes

| Axis | Values | Notes |
|---|---|---|
| Checked | `True`, `False` | Maps to `:checked` / `:not(:checked)` |
| Indeterminate | `True`, `False` | Maps to `:indeterminate` pseudo-class. JS must set `input.indeterminate = true` |
| State | `Default`, `Hovered`, `Pressed`, `Focused`, `Read-only`, `Disabled` | See state delta matrix |
| Size | `x Small`, `Small`, `Medium` | 16px / 20px / 24px box |
| Style | `Primary`, `Neutral` | Controls checked/hovered/pressed background color |

---

## Detected Variants

3 effective checked states × 6 interaction states × 3 sizes × 2 styles = **108 Figma components**.

Effective checked states:
- Unchecked (`Checked=False, Indeterminate=False`)
- Checked (`Checked=True, Indeterminate=False`)
- Indeterminate (`Checked=True, Indeterminate=True`)

`Checked=False, Indeterminate=True` does not appear in the manifest. Semantically invalid. Not implemented.

---

## Detected States

| State | Layers present (delta from Default) | CSS mechanism |
|---|---|---|
| Default | `_CheckboxBase1` only | Base selector |
| Hovered | + `Interaction Circle` (ripple) | `:hover` on root |
| Pressed | + `Interaction Circle` (ripple) | `:active` on root |
| Focused | + `Focus Ring` | `:focus-visible` on input |
| Read-only | No overlays; border uses disabled color | `.checkbox--readonly` class |
| Disabled | No overlays; border + bg use disabled color | `.checkbox--disabled` class |

Interaction Circle and Focus Ring are **mutually exclusive** in the Figma.

---

## Detected Sizes

| Class | Figma name | Box | Ripple | Focus ring |
|---|---|---|---|---|
| `.checkbox--xs` | x Small | 16px | 32px | 24px |
| `.checkbox--sm` | Small | 20px | 36px | 26.67px |
| `.checkbox--md` | Medium | 24px | 40px | 32px |

Ripple = box + 16px. Focus ring = box + 8px (computed as `calc(var(--checkbox-size) + 8px)`).

Note: Small focus ring (26.67px in Figma) is approximated as 28px via `calc(20 + 8)` — deviation of 1.33px documented below.

---

## State Delta Matrix

Δ = change from Default state. ← = same as Default.

| Property | Default | Hovered | Pressed | Focused | Read-only | Disabled |
|---|---|---|---|---|---|---|
| `::before` ripple opacity | 0 | **1** | **1** | 0 (suppressed) | — | — |
| `::after` focus ring opacity | 0 | 0 | 0 | **1** | — | — |
| `::before` / `::after` display | auto | auto | auto | auto | **none** | **none** |
| Box border-color (unchecked) | `--checkbox-border-default` | ← | ← | ← | **`--checkbox-border-disabled`** | **`--checkbox-border-disabled`** |
| Box bg (unchecked) | transparent | transparent | **`--checkbox-bg-unchecked-pressed`** | transparent | transparent | transparent |
| Box bg (primary, checked/indet) | `--checkbox-bg-primary-checked` | **`--checkbox-bg-primary-hovered`** | **`--checkbox-bg-primary-pressed`** | ← | **transparent** | **`--checkbox-bg-disabled`** |
| Box bg (neutral, checked/indet) | `--checkbox-bg-neutral-checked` | **`--checkbox-bg-neutral-hovered`** | **`--checkbox-bg-neutral-pressed`** | ← | **transparent** | **`--checkbox-bg-disabled`** |
| Box border (checked) | matches bg | **matches hovered bg** | **matches pressed bg** | ← | **`--checkbox-border-disabled`** | **`--checkbox-border-disabled`** |
| Checkmark / indet mark color | `--checkbox-mark-color` | ← | ← | ← | **`--checkbox-mark-color-readonly`** | **`--checkbox-mark-color-disabled`** |
| Cursor | pointer | pointer | pointer | pointer | **default** | **not-allowed** |
| pointer-events | auto | auto | auto | auto | **none** | **none** |

---

## Architecture Findings

1. **Standalone component**: `checkbox-2` is the isolated visual control box only. No label or form-field wrapper.
2. **Assembly order**: `checkbox-2` → `form-field` → `form`. Do not merge label into this component.
3. **No Error state in manifest**: Error state belongs to the parent form-field component.
4. **No RTL axis**: Component is geometrically symmetric — RTL axis discarded.
5. **`Checked=False, Indeterminate=True` absent**: Not in manifest. Semantically invalid. Not implemented.
6. **Disabled collapse**: Both Primary and Neutral styles use identical Global tokens in disabled/read-only states. CSS does not branch on style modifier for these states.
7. **Focused = checked background**: `--Controls-control-primary-focused` (#1B8354) = `--Controls-control-primary-checked` (#1B8354). Focused state distinguished only by focus ring, not background color change.

---

## Pseudo-Element Decisions

| Layer | Pseudo-element | Attached to | Reason |
|---|---|---|---|
| `Interaction Circle` | `::before` | `.checkbox` (root) | Interaction layer rule: attach to root component. The ripple is a sibling of the box at Figma component level, not inside the box. Using root avoids z-index clipping issues. |
| `Focus Ring` | `::after` | `.checkbox__box` | Focus ring geometry is relative to the box dimensions (box + 8px each side). Attaching to box keeps geometry self-contained and allows `input:focus-visible ~` sibling selector. |

---

## Interaction Layer Decisions

- `Interaction Circle` → `.checkbox::before`
- Triggered by `:hover` and `:active` on `.checkbox`
- Suppressed by `.checkbox:has(.checkbox__input:focus-visible)::before { opacity: 0 }` — requires `:has()` (Chrome 105+, Firefox 121+, Safari 15.4+)
- Fallback without `:has()`: ripple and focus ring may both show on keyboard-focus + hover. Visual-only degradation. Acceptable.
- Size: CSS custom property `--checkbox-ripple-size` (16px larger than box per size tier)
- Positioned: `position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%)`
- Overflows the `.checkbox` layout box — parent must allow `overflow: visible` (default)

---

## Focus Layer Decisions

- `Focus Ring` → `.checkbox__box::after`
- Triggered by `.checkbox__input:focus-visible ~ .checkbox__box::after { opacity: 1 }`
- Size: `calc(var(--checkbox-size) + 8px)` — matches Figma for xs (24px) and md (32px); 1.33px deviation for sm (28px computed vs 26.67px Figma)
- Style: `2px solid var(--checkbox-focus-ring-color)`, `mix-blend-mode: multiply`
- `mix-blend-mode: multiply` preserved from Figma — creates a visually darkened focus ring without solid fill

---

## Z-Index / Layering Decisions

```
.checkbox (root, position: relative)          — stacking context root
  ::before (ripple)        z-index: 0         — Interaction Layer: behind all controls
  .checkbox__input          z-index: 3         — above box: receives pointer events + focus
  .checkbox__box            z-index: 1         — Structural Layer: above ripple
    ::after (focus ring)   z-index: 2         — Focus Layer: above box
    svg icons              z-index: auto      — inside box, above box bg
```

The input (z-index:3) sits above the box to ensure it can receive mouse events and keyboard focus. Since it is `opacity:0`, it does not obscure the visual box.

---

## Token Findings

### Critical finding
`--Controls-*` and `--Global-*` tokens referenced in the Figma manifest **do not exist** in `token.css`. They are Figma variable names only. Component tokens must bridge to actual `token.css` primitives.

### Token bridge mapping

| Component token | Figma token | Value | token.css primitive |
|---|---|---|---|
| `--checkbox-border-default` | `--Controls-control-border` | #6C737F | `var(--gray-500)` |
| `--checkbox-bg-primary-checked` | `--Controls-control-primary-checked` | #1B8354 | `var(--sa-600)` |
| `--checkbox-bg-neutral-checked` | `--Controls-control-neutral-checked` | #0D121C | `var(--gray-950)` |
| `--checkbox-bg-primary-hovered` | `--Controls-control-primary-hovered` | #14573A | `var(--sa-800)` |
| `--checkbox-bg-neutral-hovered` | `--Controls-control-neutral-hovered` | #4D5761 | `var(--gray-600)` |
| `--checkbox-bg-primary-pressed` | `--Controls-control-primary-pressed` | #104631 | `var(--sa-900)` |
| `--checkbox-bg-neutral-pressed` | `--Controls-control-neutral-pressed` | #6C737F | `var(--gray-500)` |
| `--checkbox-bg-unchecked-pressed` | `--Controls-control-pressed` | #D2D6DB | `var(--gray-300)` |
| `--checkbox-ripple-bg` | `--Controls-control-ripple-effect` | #F3F4F6 | `var(--gray-100)` |
| `--checkbox-border-disabled` | `--Global-border-disabled` | #9DA4AE | `var(--gray-400)` |
| `--checkbox-bg-disabled` | `--Global-background-disabled` | #E5E7EB | `var(--gray-200)` |
| `--checkbox-focus-ring-color` | `--Border-border-black` | #161616 | **no primitive** — see Missing Tokens |
| `--checkbox-radius` | `--radius-xs` | 2px | `var(--radius-xs)` ✓ |
| `--checkbox-ripple-radius` | `--radius-full` | 9999px | `var(--radius-full)` ✓ |
| `--checkbox-focus-ring-radius` | `--global-radius2` | 2px | `var(--radius-xs)` (same value, different Figma collection) |
| `--checkbox-mark-color` | (inferred: white) | #ffffff | `var(--white)` ✓ |
| `--checkbox-mark-color-disabled` | (inferred) | #9DA4AE | `var(--gray-400)` |
| `--checkbox-mark-color-readonly` | (inferred) | #9DA4AE | `var(--gray-400)` |
| `--checkbox-transition-duration` | (inferred) | 100ms | `var(--transition-fast)` ✓ |
| `--checkbox-transition-easing` | (inferred) | cubic-bezier | `var(--ease-in-out)` ✓ |

---

## Accessibility Findings

1. Accessible name: not provided by this component — consumer or form-field is responsible.
2. Indeterminate: CSS `:indeterminate` triggered by JS `input.indeterminate = true`. Screen reader ARIA requires `aria-checked="mixed"` separately — also set via JS.
3. Read-only: uses `aria-readonly="true"` on input. Does NOT use `disabled` (preserves tab order).
4. Disabled: uses `disabled` attribute. Removes from tab order — acceptable for disabled controls.
5. Focus ring: visible on `:focus-visible` — suppressed on mouse click. Meets WCAG 2.4.7.
6. `mix-blend-mode: multiply` on focus ring: no contrast impact — the ring is black (#161616) which is always visible.
7. Touch target: smallest box (16px) is below WCAG 2.5.5 (44px AAA). Consumer must provide adequate padding.
8. SVGs use `aria-hidden="true"` — decorative, no semantic meaning.

---

## Compliance Findings

- No official compliance claim. Status: `pending_audit`.
- No `--Controls-*` tokens in `token.css` — component bridges to primitives. Non-blocking for function.
- `#161616` focus ring color lacks a named primitive — used inline per existing button/accordion precedent.

---

## Implementation Decisions

1. **Root element**: `<label>` — native click-to-toggle.
2. **Ripple**: `.checkbox::before` — attached to root, not box, per Interaction Layer rule.
3. **Focus ring**: `.checkbox__box::after` — attached to control, geometry is box-relative.
4. **Ripple suppression on focus**: `:has(.checkbox__input:focus-visible)` — modern CSS, documented fallback.
5. **Indeterminate**: CSS `:indeterminate` + JS required.
6. **Read-only**: `.checkbox--readonly` class + `aria-readonly="true"`.
7. **Disabled**: `.checkbox--disabled` class + `disabled` attribute.
8. **Token bridge**: Component tokens defined in `.checkbox {}` block, mapped to `token.css` primitives.
9. **Transition**: `var(--transition-fast)` + `var(--ease-in-out)` — both exist in `token.css`.
10. **Disabled style collapse**: No style branching in disabled/read-only — same tokens for both Primary and Neutral.

---

## Intentional Deviations From Figma

| Deviation | Reason |
|---|---|
| Ripple on `.checkbox::before` not sibling `<span>` | Interaction Layer rule: pseudo-element on root |
| Focus ring on `.checkbox__box::after` not sibling `<span>` | Focus Layer rule: pseudo-element on control |
| `Controls-*` tokens not used directly | They do not exist in token.css — bridged to primitives |
| Focus ring for Small: 28px vs Figma 26.67px | `calc(20 + 8)` rounding; no intermediate token available |
| Read-only mark color = `--gray-400` | Manifest shows no fill on readonly checked; mark must be visible on white bg |
| Disabled mark color = `--gray-400` | Figma fill is #E5E7EB — white mark would be invisible |
| SVG icons provided as inline paths | Figma shows empty FRAME nodes — actual icon must be defined |
| `Checked=False, Indeterminate=True` not implemented | Absent from manifest; semantically invalid |

---

## Risks

1. **Ripple overflow**: Ripple (up to 40px) overflows the 24px layout box. Parent must allow `overflow: visible`.
2. **`:has()` fallback**: Without `:has()` support, ripple and focus ring may show simultaneously on focus+hover.
3. **Focus ring overflow**: Focus ring (up to 32px) overflows 24px box. Same overflow consideration.
4. **Token bridge fragility**: If `token.css` primitives are renamed, the token bridge breaks silently (falls back to no value = initial).
5. **`#161616` not a named token**: If the global token `--ink-black` or similar is added later, this must be updated.

---

## Assumptions

1. `--Controls-control-primary-focused` = `--sa-600` = same as primary checked. Confirmed by value.
2. `--Controls-control-neutral-focused` = `--gray-950` = same as neutral checked. Confirmed by value.
3. Checkmark and indeterminate mark colors are white on colored backgrounds.
4. Read-only and disabled mark color = `--gray-400` (#9DA4AE). Confirmed as reasonable — not specified in Figma manifest export.
5. Ripple and focus ring are mutually exclusive per Figma state definitions.
6. `--global-radius2` (Figma focus ring collection) = 2px = same as `--radius-xs`. Mapped to `var(--radius-xs)`.
7. Hovered unchecked: ripple shows but box appearance unchanged (no border/bg change). Confirmed by manifest.

---

## Known Issues

1. Focus ring size for Small (20px box): CSS computes 28px; Figma specifies 26.67px. 1.33px deviation.
2. The focus ring may co-exist with the ripple on keyboard-focus + hover in browsers without `:has()` support.
3. Transition is not applied to `color` property (mark color) — disabled/read-only mark color changes are instant. No Figma specification for mark color transition.

---

## Missing Tokens

These `--checkbox-*` tokens must be added to `token.css` (component section, after button tokens):

```css
/* Checkbox state tokens */
--checkbox-border-default:        var(--gray-500);
--checkbox-bg-primary-checked:    var(--sa-600);
--checkbox-bg-neutral-checked:    var(--gray-950);
--checkbox-bg-primary-hovered:    var(--sa-800);
--checkbox-bg-neutral-hovered:    var(--gray-600);
--checkbox-bg-primary-pressed:    var(--sa-900);
--checkbox-bg-neutral-pressed:    var(--gray-500);
--checkbox-bg-unchecked-pressed:  var(--gray-300);
--checkbox-ripple-bg:             var(--gray-100);
--checkbox-border-disabled:       var(--gray-400);
--checkbox-bg-disabled:           var(--gray-200);
--checkbox-focus-ring-color:      #161616;   /* TODO: needs --ink-black in global palette */
--checkbox-mark-color:            var(--white);
--checkbox-mark-color-disabled:   var(--gray-400);
--checkbox-mark-color-readonly:   var(--gray-400);
--checkbox-radius:                var(--radius-xs);
--checkbox-ripple-radius:         var(--radius-full);
--checkbox-focus-ring-radius:     var(--radius-xs);
--checkbox-transition-duration:   var(--transition-fast);
--checkbox-transition-easing:     var(--ease-in-out);
```

**Global palette gap**: `#161616` appears in button, accordion, and checkbox but has no named primitive token (`--ink-black`, `--black-text`, or similar). Add `--ink-black: #161616;` to `token.css` color section as a follow-up.

---

## Missing Standards

1. No `--checkbox-*` tokens in `token.css` — component bridges inline.
2. `#161616` has no named token — used as a hardcoded value in component bridge (not in selector).
3. No Error state in Figma for this component — form-field assembly owns error state.
4. WCAG 2.5.5 touch target (44px) not enforced — consumer responsibility.
5. `aria-checked="mixed"` JS wiring not in template — consumer responsibility.

---

## TODO

- [ ] Add all `--checkbox-*` tokens to `token.css`
- [ ] Add `--ink-black: #161616` to global color section of `token.css`
- [ ] Verify all `--gray-*`, `--sa-*` primitive mappings against production Figma values
- [ ] Formal accessibility audit (WCAG 1.4.3 contrast, 2.4.7 focus, 4.1.2 ARIA)
- [ ] Confirm read-only and disabled mark colors with design team
- [ ] Confirm checkmark SVG paths with icon library
- [ ] Test `:has()` fallback behavior in legacy browser environments
- [ ] Document `aria-checked="mixed"` JS wiring in consumer docs / form-field assembly
- [ ] Formal touch target audit for xSmall (16px) in context of form-field assembly
