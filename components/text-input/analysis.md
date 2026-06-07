# Component Analysis

- **Manifest path**: `components/text-input/manifest.json`
- **Component name**: Text Input
- **Analysis date**: 2026-06-06
- **Analyst**: Platform Component Builder (automated)

---

## Source

- `manifest.json` — Figma plugin export, `COMPONENT_SET` containing 288 `COMPONENT` nodes.
- Manifest file size: ~2.8 MB.
- Reference implementations: `button`, `label`, `input-affix`.

---

## Detected Anatomy

```
.text-input                       ← root wrapper (flex-column, label-gap)
  .text-input__label              ← label area (<label> element)
  .text-input__field              ← input field border box (relative, overflow:hidden for ::after)
    .text-input__field::after     ← bottom underline accent (focused / pressed states)
    .text-input__inner            ← inner padding container (Icon-Text-stack in Figma)
      .text-input__input          ← native <input type="text"> element
```

Figma child elements mapped to HTML:
| Figma element        | HTML mapping               |
|----------------------|----------------------------|
| `Label` (INSTANCE)   | `<label class="text-input__label">` |
| `Input Field` (FRAME)| `.text-input__field`       |
| `Icon-Text-stack` (FRAME) | `.text-input__inner`  |
| `Text` (FRAME)       | absorbed into `.text-input__inner` |
| `Entered Text` / `Placeholder Text` (TEXT) | `<input>` + `::placeholder` |
| `Thin underline` (RECTANGLE) | `.text-input__field::after` (pseudo-element) |
| `Type Cursor` (RECTANGLE) | browser cursor, not implementable |

---

## Detected Axes

| Axis    | Values                                        | Notes |
|---------|-----------------------------------------------|-------|
| RTL     | True, False                                   | **Discarded** — see Intentional Deviations |
| State   | Default, Hovered, Focused, Pressed, Disabled, Read-only | 6 states |
| Filled  | True, False                                   | **Partially discarded** — absorbed into `::placeholder` |
| Error   | True, False                                   | CSS modifier `.text-input--error` |
| Size    | Large (40px), Medium (32px)                   | CSS modifier `.text-input--md` |
| Style   | Default, Filled darker, Filled lighter        | CSS modifiers `--filled-darker`, `--filled-lighter` |

---

## Detected Variants

Total Figma variants: **288**
(2 RTL × 6 states × 2 Filled × 2 Error × 2 Size × 3 Style)

CSS-meaningful variant matrix (RTL and Filled collapsed):
6 states × 2 error × 2 size × 3 style = **72 CSS-meaningful combinations**

Key canonical variants for reference.json: **18** (one per state × error × size combination, default style only).

---

## Detected States

| State     | CSS trigger                                         | Border token                         | Background token        |
|-----------|-----------------------------------------------------|--------------------------------------|-------------------------|
| Default   | base class                                          | `--text-input-border-default` (#9DA4AE) | `--text-input-bg-default` (#FFF) |
| Hovered   | `:hover` on `.text-input__field`                    | `--text-input-border-hovered` (#384250) | same as default |
| Focused   | `:focus-within` on `.text-input__field`             | no border → underline via `::after` | same as default |
| Pressed   | `:active` on `.text-input__field`                   | `--text-input-border-default` (#9DA4AE) | `--text-input-bg-pressed` (#F3F4F6) |
| Disabled  | `.text-input--disabled`                             | `--text-input-border-disabled` (#D2D6DB) | same as default |
| Read-only | `.text-input--readonly`                             | `--text-input-border-readonly` (#D2D6DB) | same as default |

Error overrides state borders for Default, Hovered:
- Error Default/Hovered: `--text-input-border-error` (#B42318)

Pressed state overrides error border (uses `--text-input-border-default`).

---

## Detected Sizes

| Size   | Height | Font-size token         | Line-height token        | CSS modifier |
|--------|--------|-------------------------|--------------------------|--------------|
| Large  | 40px   | `--text-input-lg-font-size` (16px) | `--text-input-lg-line-height` (24px) | base |
| Medium | 32px   | `--text-input-md-font-size` (14px) | `--text-input-md-line-height` (20px) | `.text-input--md` |

---

## Architecture Findings

1. **Focused state restructuring** — In Figma, the Focused state completely changes the `Input Field` layout (switches to `flex-direction: column`, drops explicit border/background). In CSS, this is implemented as: border becomes transparent + `::after` pseudo-element shows a 2px bottom accent. The `::after` approach avoids layout shift and is more semantically correct than changing flex direction.

2. **Underline as ::after pseudo-element** — The Figma `Thin underline` RECTANGLE is a `position: absolute; bottom: 0; width: 100%; height: 2px` element. CSS `::after` with `content: ''` and identical positioning is the correct implementation. This avoids adding a non-semantic element to the DOM.

3. **Type Cursor not implementable** — The Figma shows a custom `Type Cursor` rectangle during focus. This is the browser's native text cursor. It is not implementable in CSS without hacks. Not implemented. Documented as intentional deviation.

4. **Filled axis** — Figma's `Filled=True/False` represents a runtime state (user has or has not entered text). Both states use the same CSS for the field. The only difference is text color (`--text-input-text-filled` vs `::placeholder` color `--text-input-text-placeholder`). This is handled natively by the `<input>::placeholder` CSS. No JS class toggle needed for basic implementation.

5. **RTL axis** — All RTL=True and RTL=False variants produce identical CSS when `padding-inline-start`/`padding-inline-end` logical properties are used. RTL is handled via `dir="rtl"` attribute on an ancestor element.

6. **Style axis as modifier class** — The three background styles (Default=white, Filled darker=#F3F4F6, Filled lighter=#FCFCFD) are implemented as CSS modifier classes. `Filled darker` and `Filled lighter` drop the border in the default state (Figma shows no border for these filled-background styles in the no-error state).

7. **Assembly boundary preserved** — `text-input` is a standalone base component. The `input-affix` component is a separate adjacent component. Do not merge them. Assembly context (`form-field`, `form`) should compose these separately.

8. **No icon slot in base text-input** — The Figma `Icon-Text-stack` does not contain an icon in any variant of the base `Text Input` component set. Icon support is the responsibility of `input-affix`. The `Icon-Text-stack` frame in Figma is a layout container that exists in the file but only contains the text.

---

## Token Findings

All tokens below are **missing from token.css** and must be added.

Currently used as inline `var()` fallbacks in `text-input.css`.

### Border tokens (missing)
- `--text-input-border-default` — proposed: `var(--Form-field-border-default, #9DA4AE)`
- `--text-input-border-hovered` — proposed: `var(--Form-field-border-hovered, #384250)`
- `--text-input-border-error` — proposed: `var(--Form-field-border-error, #B42318)`
- `--text-input-border-disabled` — proposed: `var(--Border-border-disabled, #D2D6DB)`
- `--text-input-border-readonly` — proposed: `var(--Border-border-neutral-primary, #D2D6DB)`

### Background tokens (missing)
- `--text-input-bg-default` — proposed: `var(--Form-field-background-default, #FFF)`
- `--text-input-bg-pressed` — proposed: `var(--Form-field-background-darker, #F3F4F6)`
- `--text-input-bg-darker` — proposed: `var(--Form-field-background-darker, #F3F4F6)`
- `--text-input-bg-lighter` — proposed: `var(--Form-field-background-lighter, #FCFCFD)`

### Underline accent tokens (missing)
- `--text-input-underline-default` — proposed: `var(--Form-field-border-pressed, #0D121C)`
- `--text-input-underline-error` — proposed: `var(--Form-field-border-error, #B42318)`
- `--text-input-underline-height` — proposed: `2px`

### Text color tokens (missing)
- `--text-input-text-placeholder` — proposed: `var(--Form-field-text-placeholder, #6C737F)`
- `--text-input-text-filled` — proposed: `var(--Form-field-text-filled, #161616)`
- `--text-input-text-focused` — proposed: `var(--Form-field-text-focused, #384250)`
- `--text-input-text-readonly` — proposed: `var(--Form-field-text-readonly, #161616)`
- `--text-input-text-disabled` — proposed: `var(--Global-text-default-disabled, #9DA4AE)`
- `--text-input-label-color` — proposed: `var(--Form-field-text-label, #161616)`

### Typography tokens (missing)
- `--text-input-font-family` — proposed: `"IBM Plex Sans Arabic"`
- `--text-input-lg-font-size` — proposed: `var(--Size-Text-typo-size-text-md, 16px)`
- `--text-input-lg-line-height` — proposed: `var(--Line-Height-Text-line-heights-text-md, 24px)`
- `--text-input-md-font-size` — proposed: `var(--Size-Text-typo-size-text-sm, 14px)`
- `--text-input-md-line-height` — proposed: `var(--Line-Height-Text-line-heights-text-sm, 20px)`

### Size tokens (missing)
- `--text-input-lg-height` — proposed: `40px`
- `--text-input-md-height` — proposed: `32px`

### Spacing tokens (missing)
- `--text-input-field-gap` — proposed: `var(--Form-field-label-gap, 8px)`
- `--text-input-padding-inline-start` — proposed: `var(--spacing-forminput-container-padding-left, 8px)`
- `--text-input-padding-inline-end` — proposed: `var(--spacing-forminput-container-padding-right, 16px)`
- `--text-input-icon-text-gap` — proposed: `var(--Form-icon-enteredtext, 8px)`

### Radius tokens (missing)
- `--text-input-radius` — proposed: `var(--Radius-radius-sm, 4px)`

---

## Accessibility Findings

1. **No native `<label>` bypass risk** — The component uses a real `<label>` element with `for` attribute. This provides correct browser/AT association.
2. **Required state** — If a `required` attribute is present on the `<input>`, no additional ARIA is needed. `aria-required="true"` is acceptable for non-HTML5 contexts.
3. **Error state announcement** — `.text-input--error` changes visual border/color only. Consumers must add `aria-describedby` pointing to an error message element. Contract documents this as consumer responsibility.
4. **Disabled state** — `<input disabled>` provides native AT support. No additional `aria-disabled` needed on the input itself. The wrapper `.text-input--disabled` is for CSS only.
5. **Read-only state** — `<input readonly>` provides native AT support (`"read-only"` is announced by screen readers).
6. **Focus indicator** — The `::after` underline provides a visible focus indicator. It must have at least 3:1 contrast ratio (WCAG 2.4.11). `#0D121C` on `#FFF` = ~21:1 ✓.
7. **Placeholder contrast** — `--text-input-text-placeholder` (#6C737F) on white (#FFF) = ~4.8:1. Passes WCAG 1.4.3 AA (3:1 minimum for placeholder text). ✓

---

## Compliance Findings

- `aria-describedby` for error messages: **consumer responsibility** — not part of this component.
- `type="text"` is the default; consumers should override for email/tel/search/number inputs.
- No `autocomplete` attribute in template — consumers should add per their use case.
- `<input>` inside `.text-input__field` is not inside the `<label>`. `for` attribute association is required.

---

## Implementation Decisions

1. **RTL discarded** — Using CSS logical properties throughout. `padding-inline-start: 8px; padding-inline-end: 16px`. RTL axis produces no diff.
2. **Filled axis as ::placeholder** — `Filled=True/False` is a JS runtime state mapped to CSS `::placeholder`. No class modifier.
3. **Thin underline as ::after** — `position: absolute; bottom: 0; left: 0; right: 0; height: 2px`. No DOM element added.
4. **Type Cursor not implemented** — Browser native cursor. No implementation.
5. **Focused state** — Implemented as `:focus-within` on `.text-input__field`. Border set to `transparent` on focus. `::after` shows underline.
6. **Pressed state** — Implemented as `:active` on `.text-input__field`. Darker background + partial-width underline (50%) kept as visual approximation since exact pixel value (112px/320px = 35%) is layout-dependent.
7. **Style=Filled darker/lighter** — In Figma, these styles have no border in the default non-error state. Border is only shown when error=true. Implemented as: `.text-input--filled-darker .text-input__field { border-color: transparent; background: --text-input-bg-darker }`.

---

## Intentional Deviations From Figma

| Deviation | Reason |
|-----------|--------|
| RTL axis discarded | CSS logical properties achieve RTL automatically. Separate RTL CSS would be identical. |
| Type Cursor element removed | Browser renders native text cursor. Not implementable in CSS without suppressing native behavior. |
| Thin underline as `::after` instead of DOM element | Avoids non-semantic `<span>` or `<div>` in markup. Equivalent visual output. |
| Pressed underline width set to 50% instead of 112px | Figma uses fixed 112px on a 320px-wide component. Responsive implementation needs relative width. 35% approximation; 50% used for visual clarity. |
| Input Field `flex-direction: column` removed from Focused state | Figma restructures layout on focus; HTML does not need this since the `::after` underline overlay achieves the same visual. |

---

## Risks

1. **`:focus-within` browser support** — Supported in all modern browsers (Chrome 60+, Firefox 52+, Safari 10.1+). IE not supported. Risk: none for modern platform.
2. **Pressed underline width** — Fixed-pixel width in Figma is non-responsive. Responsive approximation (50%) diverges from exact Figma spec.
3. **Error state on Pressed/Disabled** — Figma shows `Error=True` variants for Disabled, but with the same border as non-error disabled. This is correct: when disabled, error styling is suppressed. CSS specificity handles this automatically.
4. **input-affix assembly** — The `text-input` component does not include prefix/suffix affixes. If assembled without `input-affix`, consumers may assume icon support is built-in.

---

## Assumptions

1. The `Filled=True` / `Filled=False` states control only the text color of the input value (filled vs placeholder). This is assumed to be handled by the browser's `::placeholder` pseudo-element.
2. The `Label` INSTANCE in Figma refers to the existing `label` component. In implementation, the label is a native `<label>` element styled with `.text-input__label` — not the full label component. This is intentional to keep the component self-contained.
3. Disabled state assumes no background change (same as default). Figma manifest for disabled state didn't show an explicit background token change from default.
4. The "Pressed" state in Figma is a transient click state. Mapped to CSS `:active`. In the DOM, the sequence is: default → hover → active → focused.

---

## Known Issues

1. **Missing tokens in token.css** — All `--text-input-*` tokens are undefined globally. They are scoped with fallback values in `text-input.css`. This is a temporary measure pending token.css update.
2. **Pressed underline width not pixel-exact** — See Intentional Deviations.
3. **Error message slot not in scope** — Error helper text (red message below the field) is a form-field assembly concern, not a text-input concern.

---

## Missing Tokens

All `--text-input-*` tokens listed in Token Findings above need to be added to `token.css` in a `/* Text Input tokens */` section.

Figma source tokens mapped but not yet in component namespace:
- `--Form-field-border-default` → `--text-input-border-default`
- `--Form-field-border-hovered` → `--text-input-border-hovered`
- `--Form-field-border-error` → `--text-input-border-error`
- `--Border-border-disabled` → `--text-input-border-disabled`
- `--Border-border-neutral-primary` → `--text-input-border-readonly`
- `--Form-field-background-default` → `--text-input-bg-default`
- `--Form-field-background-darker` → `--text-input-bg-darker`, `--text-input-bg-pressed`
- `--Form-field-background-lighter` → `--text-input-bg-lighter`
- `--Form-field-border-pressed` → `--text-input-underline-default`
- `--Form-field-text-placeholder` → `--text-input-text-placeholder`
- `--Form-field-text-filled` → `--text-input-text-filled`
- `--Form-field-text-focused` → `--text-input-text-focused`
- `--Form-field-text-readonly` → `--text-input-text-readonly`
- `--Global-text-default-disabled` → `--text-input-text-disabled`
- `--Form-field-text-label` → `--text-input-label-color`

---

## Missing Standards

- `autocomplete` attribute guidance — should be documented in contract.
- Error message association pattern (`aria-describedby`) — should be documented as consumer responsibility in contract. ✓ Done.

---

## TODO

- [ ] Add all `--text-input-*` token definitions to `token.css` under `/* Text Input tokens */` section.
- [ ] Validate `:focus-within` underline animation (scale or fade) — Figma does not specify transition. Consider `transition: transform 0.15s ease`.
- [ ] Confirm with design team whether pressed underline should be full-width or partial-width on resize.
- [ ] Add `input-affix` assembly example to showcases once `input-affix` is stable.
- [ ] Run WCAG 2.1 AA audit with real token values from token.css to update compliance.json status.
- [ ] Verify `--text-input-text-placeholder` contrast (#6C737F on backgrounds) for all three Style variants.
