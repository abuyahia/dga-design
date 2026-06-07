# Component Contract: Checkbox (checkbox-2)

**Schema version**: 1.1.0
**Component**: checkbox-2
**Generation**: v2
**Status**: implementation-ready
**Compliance status**: pending_audit

---

## Purpose

Standalone visual checkbox control. Renders a square selection box with checked, unchecked, and indeterminate states. Does not include a label. Intended for use inside a `form-field` or `checkbox-group` assembly.

---

## Anatomy

```
label.checkbox                         (root, position: relative, stacking context)
├── ::before                           (ripple — Interaction Layer on root, z-index: 0)
├── input.checkbox__input              (visually hidden native control, z-index: 3)
└── span.checkbox__box                 (visual square box, z-index: 1)
    ├── ::after                        (focus ring — Focus Layer on box, z-index: 2)
    ├── svg.checkbox__checkmark        (shown when checked)
    └── svg.checkbox__indeterminate    (shown when indeterminate)
```

**Layer classification:**

| Layer | Figma layer | Role | Implementation |
|---|---|---|---|
| Visual box | `_CheckboxBase1` | Structural | `<span class="checkbox__box">` |
| Checkmark | `checkmark` | Icon | `<svg class="checkbox__checkmark">` |
| Indeterminate mark | `Indeterminate mark` | Icon | `<svg class="checkbox__indeterminate">` |
| Ripple | `Interaction Circle` | Interaction | `.checkbox::before` (root pseudo-element) |
| Focus indicator | `Focus Ring` | Focus | `.checkbox__box::after` (box pseudo-element) |

**Z-index layering:**
```
.checkbox::before        z-index: 0   (ripple — behind everything)
.checkbox__box           z-index: 1   (above ripple)
.checkbox__box::after    z-index: 2   (focus ring — above box)
.checkbox__input         z-index: 3   (above box — receives pointer events)
```

---

## Axes

### Size

| Modifier | Figma name | Box size | Ripple | Focus ring |
|---|---|---|---|---|
| `.checkbox--xs` | x Small | 16px | 32px | 24px |
| `.checkbox--sm` | Small | 20px | 36px | ~28px (1.33px deviation from Figma 26.67px) |
| `.checkbox--md` | Medium | 24px | 40px | 32px |

Default: Medium. Without a size modifier, medium sizing applies via CSS custom property defaults.

### Style

| Modifier | Figma name | Checked background (token) | Checked background (value) |
|---|---|---|---|
| (none) / `.checkbox--primary` | Primary | `--checkbox-bg-primary-checked` → `--sa-600` | #1B8354 |
| `.checkbox--neutral` | Neutral | `--checkbox-bg-neutral-checked` → `--gray-950` | #0D121C |

Default: Primary. Without `.checkbox--neutral`, Primary token values apply.

---

## States

### Interaction States

| State | CSS mechanism | Visual delta |
|---|---|---|
| Default unchecked | Base styles | Border only, transparent fill |
| Default checked | `:checked:not(:indeterminate)` | Colored fill + checkmark visible |
| Default indeterminate | `:indeterminate` | Colored fill + dash mark visible |
| Hovered unchecked | `:hover` on root | Ripple appears |
| Hovered checked | `:hover + :checked` | Ripple + darkened fill |
| Hovered indeterminate | `:hover + :indeterminate` | Ripple + darkened fill |
| Pressed unchecked | `:active` on root | Ripple + light gray fill |
| Pressed checked | `:active + :checked` | Ripple + darker fill |
| Pressed indeterminate | `:active + :indeterminate` | Ripple + darker fill |
| Focused | `.checkbox__input:focus-visible` | Focus ring appears; ripple suppressed |
| Read-only | `.checkbox--readonly` | Disabled border, transparent fill, `pointer-events: none` |
| Disabled | `.checkbox--disabled` + `disabled` attr | Disabled border + light gray fill (checked), `pointer-events: none` |

### Unsupported States

- **Error**: Error styling is the responsibility of the parent `form-field` component.
- `Checked=False + Indeterminate=True`: Semantically invalid. Absent from manifest. Not implemented.

---

## Modifiers Reference

| Modifier | Effect |
|---|---|
| `.checkbox--xs` | 16px box |
| `.checkbox--sm` | 20px box |
| `.checkbox--md` | 24px box (default) |
| `.checkbox--primary` | Primary (green) style — explicit alias for default |
| `.checkbox--neutral` | Neutral (dark slate) style |
| `.checkbox--readonly` | Read-only visual + `pointer-events: none` |
| `.checkbox--disabled` | Disabled visual + `pointer-events: none` |

---

## Token Contract

Component CSS uses `--checkbox-*` semantic tokens exclusively. No primitive tokens appear in component selectors. The bridge layer in `.checkbox {}` maps each `--checkbox-*` token to a `token.css` primitive.

**Token bridge (token.css primitives):**

| Token | token.css primitive | Figma origin | Purpose |
|---|---|---|---|
| `--checkbox-border-default` | `var(--gray-500)` | `--Controls-control-border` | Default unchecked border |
| `--checkbox-bg-primary-checked` | `var(--sa-600)` | `--Controls-control-primary-checked` | Primary checked/focused fill |
| `--checkbox-bg-neutral-checked` | `var(--gray-950)` | `--Controls-control-neutral-checked` | Neutral checked/focused fill |
| `--checkbox-bg-primary-hovered` | `var(--sa-800)` | `--Controls-control-primary-hovered` | Primary hover fill (checked) |
| `--checkbox-bg-neutral-hovered` | `var(--gray-600)` | `--Controls-control-neutral-hovered` | Neutral hover fill (checked) |
| `--checkbox-bg-primary-pressed` | `var(--sa-900)` | `--Controls-control-primary-pressed` | Primary press fill (checked) |
| `--checkbox-bg-neutral-pressed` | `var(--gray-500)` | `--Controls-control-neutral-pressed` | Neutral press fill (checked) |
| `--checkbox-bg-unchecked-pressed` | `var(--gray-300)` | `--Controls-control-pressed` | Unchecked press fill |
| `--checkbox-ripple-bg` | `var(--gray-100)` | `--Controls-control-ripple-effect` | Ripple circle color |
| `--checkbox-border-disabled` | `var(--gray-400)` | `--Global-border-disabled` | Disabled + read-only border |
| `--checkbox-bg-disabled` | `var(--gray-200)` | `--Global-background-disabled` | Disabled checked fill |
| `--checkbox-focus-ring-color` | `#161616` ¹ | `--Border-border-black` | Focus ring border color |
| `--checkbox-radius` | `var(--radius-xs)` | — | Box corner radius |
| `--checkbox-ripple-radius` | `var(--radius-full)` | — | Ripple circle radius |
| `--checkbox-focus-ring-radius` | `var(--radius-xs)` | — | Focus ring corner radius |
| `--checkbox-mark-color` | `var(--white)` | — | Checkmark/indeterminate color |
| `--checkbox-mark-color-disabled` | `var(--gray-400)` | — | Mark color when disabled |
| `--checkbox-mark-color-readonly` | `var(--gray-400)` | — | Mark color when read-only |
| `--checkbox-transition-duration` | `var(--transition-fast)` | — | Transition duration |
| `--checkbox-transition-easing` | `var(--ease-in-out)` | — | Transition easing |

¹ `#161616` used as literal — `--Border-border-black` has no primitive alias in `token.css`. Same value used in `--accordion-normal-focus-ring`. Proposed follow-up: add `--ink-black: #161616` to `token.css`.

---

## CSS Classes Reference

| Class | Element | Required |
|---|---|---|
| `.checkbox` | `<label>` | Yes |
| `.checkbox__input` | `<input type="checkbox">` | Yes |
| `.checkbox__box` | `<span>` | Yes |
| `.checkbox__checkmark` | `<svg>` | Yes |
| `.checkbox__indeterminate` | `<svg>` | Yes |

---

## Pseudo-Element Reference

| Pseudo-element | Attached to | Role | Trigger |
|---|---|---|---|
| `::before` | `.checkbox` (root) | Ripple (Interaction Circle) | `:hover`, `:active` on root; suppressed on `:focus-visible` via `:has()` |
| `::after` | `.checkbox__box` | Focus Ring | `.checkbox__input:focus-visible ~` sibling selector |

---

## Accessibility Contract

| Requirement | Implementation | Standard |
|---|---|---|
| Accessible name | Consumer provides `aria-label` on input, or form-field wrapper provides it | WCAG 4.1.2 |
| Keyboard toggle | Native `<input type="checkbox">` — Space key toggle | WCAG 2.1.1 |
| Visible focus | Focus ring via `:focus-visible` + `.checkbox__box::after` | WCAG 2.4.7 |
| Indeterminate ARIA | JS sets `aria-checked="mixed"` when `input.indeterminate = true` | WCAG 4.1.2 |
| Read-only ARIA | `aria-readonly="true"` on input | WCAG 4.1.2 |
| Disabled | `disabled` attribute on input | HTML5 + WCAG |
| Decorative icons | `aria-hidden="true"` on both SVGs | WCAG 1.1.1 |
| Ripple suppression | Ripple hidden on focus-visible — mutually exclusive with focus ring | UX intent |
| Motion | Transitions are decorative only; `prefers-reduced-motion` not yet implemented | WCAG 2.3.3 |

---

## Usage Rules

**Do:**
- Always provide an accessible name on the `<input>`.
- Use `.checkbox--readonly` + `aria-readonly="true"` for read-only. Do not use `disabled`.
- Set `input.indeterminate = true` and `aria-checked="mixed"` via JS for indeterminate state.
- Wrap in `form-field` to add label, hint text, and error message.
- Apply exactly one size modifier and one style modifier.

**Do not:**
- Do not embed label text inside this component.
- Do not use `disabled` for read-only — it removes the element from tab order.
- Do not use `Checked=False + Indeterminate=True` — semantically invalid.
- Do not apply error styling on this component — use the `form-field` wrapper.
- Do not apply both `.checkbox--disabled` and `.checkbox--readonly` simultaneously.

---

## Assembly Notes

```
checkbox-2
  ↓ used in
form-field (adds label, hint, error)
  ↓ used in
checkbox-group (stacked/inline checkboxes)
  ↓ used in
form
```

Do not collapse checkbox-2 into form-field — they are separate components with independent reuse paths.
