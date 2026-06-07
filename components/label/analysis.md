# Component Analysis — Label

- **Manifest path:** `components/label/manifest.json`
- **Component name:** Label
- **Generated:** 2026-06-06

---

## Source

Figma COMPONENT_SET with 16 COMPONENT children.
Figma variables referenced: `--Form-label-gap`, `--Form-field-text-label`, `--Form-field-border-error`, `--Global-input-text-disabled`, `--Font-Family-font-family-text`, `--Size-Text-typo-size-text-sm`, `--Size-Text-typo-size-text-md`, `--Line-Height-Text-line-heights-text-sm`, `--Line-Height-Text-line-heights-text-md`.

---

## Detected Anatomy

```
label.label                       ← semantic <label> element, inline-flex container
  span.label__required            ← required asterisk "*", aria-hidden="true"
  span.label__text                ← visible label text
```

The required asterisk is an optional slot. When a field is not required, `.label__required` is omitted.

---

## Detected Axes

| Axis | Figma key | Values |
|---|---|---|
| Type | `Type` | Regular (Default), Semibold |
| Size | `Size` | Medium, Large |
| Disabled | `Disabled` | False, True |
| RTL | `RTL` | False, True |

---

## Detected Variants

16 total variants: 2 Type × 2 Size × 2 Disabled × 2 RTL = 16. All present in manifest.

| ID | type | size | disabled | rtl |
|---|---|---|---|---|
| regular-medium-enabled-ltr | regular | medium | false | false |
| regular-medium-enabled-rtl | regular | medium | false | true |
| regular-medium-disabled-ltr | regular | medium | true | false |
| regular-medium-disabled-rtl | regular | medium | true | true |
| semibold-medium-enabled-ltr | semibold | medium | false | false |
| semibold-medium-enabled-rtl | semibold | medium | false | true |
| semibold-medium-disabled-ltr | semibold | medium | true | false |
| semibold-medium-disabled-rtl | semibold | medium | true | true |
| regular-large-enabled-ltr | regular | large | false | false |
| regular-large-enabled-rtl | regular | large | false | true |
| regular-large-disabled-ltr | regular | large | true | false |
| regular-large-disabled-rtl | regular | large | true | true |
| semibold-large-enabled-ltr | semibold | large | false | false |
| semibold-large-enabled-rtl | semibold | large | false | true |
| semibold-large-disabled-ltr | semibold | large | true | false |
| semibold-large-disabled-rtl | semibold | large | true | true |

---

## Detected States

Label is not an interactive element. It does not receive keyboard focus independently. Only two states apply:

- **Enabled** (default)
- **Disabled** — all text colors shift to disabled muted value

No hover, focus, pressed, or selected states exist on this component.

---

## Detected Sizes

| Size | font-size | line-height | CSS modifier |
|---|---|---|---|
| Medium (default) | 14px → `var(--fs-text-sm)` | 20px → `var(--lh-text-sm)` | none (default) |
| Large | 16px → `var(--fs-text-md)` | 24px → `var(--lh-text-md)` | `.label--large` |

---

## Architecture Findings

1. **Standalone component.** Label is a reusable micro-component. It participates in assemblies: text-input → form-field → form. Do not merge into composite components.

2. **Semantic element.** Must render as `<label>` for correct browser form association. The `for` attribute or nesting model provides accessibility linkage to the form control.

3. **RTL via inheritance.** The component does not require RTL-specific CSS. With `direction: rtl` inherited from `[dir="rtl"]` on an ancestor (`<html>` or wrapping container), `inline-flex` children visually reverse automatically. DOM child order stays constant `[Required asterisk, Text]` in all variants. See Intentional Deviations for rationale.

4. **Required asterisk is a conditional slot.** The `.label__required` span is optional. When the associated field is not required, the span is omitted entirely. The label must function correctly with or without it.

5. **Gap uniform across all variants.** The `gap: 4px` between asterisk and text is identical across all 16 Figma variants — no size-conditional gap. Mapped to `--label-gap`.

---

## Token Findings

### Mapped Figma variables → component tokens → token.css primitives

| Figma variable | Component token | token.css primitive | Status |
|---|---|---|---|
| `--Form-label-gap` (4px) | `--label-gap` | `var(--spacing-xs)` → `var(--space-4)` = 4px | **Missing in token.css** |
| `--Form-field-text-label` (#161616) | `--label-text-color` | none — #161616 has no exact primitive in token.css | **Missing in token.css** |
| `--Form-field-border-error` (#B42318) | `--label-required-color` | `var(--error-700)` = #b42318 ✓ | **Missing in token.css** |
| `--Global-input-text-disabled` (#9DA4AE) | `--label-text-color-disabled` | `var(--gray-400)` = #9da4ae ✓ | **Missing in token.css** |
| `--Font-Family-font-family-text` | `--label-font-family` | `var(--font-sans)` ✓ | **Missing in token.css** |
| `--Size-Text-typo-size-text-sm` (14px) | `--label-font-size-md` | `var(--fs-text-sm)` = 14px ✓ | **Missing in token.css** |
| `--Size-Text-typo-size-text-md` (16px) | `--label-font-size-lg` | `var(--fs-text-md)` = 16px ✓ | **Missing in token.css** |
| `--Line-Height-Text-line-heights-text-sm` (20px) | `--label-line-height-md` | `var(--lh-text-sm)` = 20px ✓ | **Missing in token.css** |
| `--Line-Height-Text-line-heights-text-md` (24px) | `--label-line-height-lg` | `var(--lh-text-md)` = 24px ✓ | **Missing in token.css** |
| `font-weight: 400` | `--label-font-weight-regular` | `var(--font-weight-body)` = 400 ✓ | **Missing in token.css** |
| `font-weight: 600` | `--label-font-weight-semibold` | `var(--font-weight-semibold)` = 600 ✓ | **Missing in token.css** |

**Note on `#161616`:** This value does not correspond to any primitive in token.css. `--gray-900` is `#111927` (not a match). A global semantic token `--label-text-color` or a shared form-field text color token should be added to token.css. Fallback `#161616` is used inline in the component token definition until resolved.

---

## Accessibility Findings

1. **Required asterisk must be `aria-hidden="true"`.** The `*` is a visual indicator only. The `aria-required="true"` attribute must be placed on the associated form control (input/select/textarea), not on the label.

2. **Label must be associated with its form control.** Via `for="field-id"` attribute (preferred) or nesting the control inside the label. Unassociated labels are an accessibility failure.

3. **Disabled state uses `aria-disabled="true"`.** The `<label>` element has no native `:disabled` pseudo-class. Class-based `.label--disabled` and `aria-disabled="true"` attribute are used together. `pointer-events: none` is applied but does not affect screen reader announcement.

4. **No focus management needed.** Label is not focusable by itself. Focus is managed by the associated form control.

---

## Compliance Findings

1. Semantic `<label>` element — mapped, pending audit.
2. Required state communicated via `aria-required` on form control (not on label) — mapped, pending audit.
3. Disabled state communicated via `aria-disabled="true"` — mapped, pending audit.
4. Component-level tokens defined; token.css gap documented — pending resolution.

---

## Implementation Decisions

1. **Default size = Medium.** No `.label--medium` modifier needed. Large adds `.label--large`.
2. **Default type = Regular.** No modifier needed. Semibold adds `.label--semibold`.
3. **Component tokens scoped on `.label`.** All `--label-*` tokens are defined on `.label` as CSS custom properties. This makes the component self-contained and functional before token.css is updated. When token.css is updated with the `/* Label tokens */` section, the `.label` scoped definitions can be removed.
4. **RTL via dir attribute inheritance.** No RTL-specific CSS rules added to the component. The browser's inline-flex RTL behaviour is relied upon. See Intentional Deviations.

---

## Intentional Deviations From Figma

| Deviation | Figma behaviour | Implementation | Reason |
|---|---|---|---|
| RTL child DOM order | RTL variants have children as [Text, Asterisk] in Figma | DOM always [Asterisk, Text]; RTL handled via CSS direction | Inline-flex + `direction:rtl` produces identical visual output. Constant DOM order is cleaner and avoids JS for child reordering. |
| `text-align: right` on RTL text | Figma RTL Text children have `text-align: right` | Not applied; inherited from `direction: rtl` context | Direction context handles text alignment. Applying it explicitly would be redundant and hard-code directional intent. |

---

## Risks

1. **`--label-text-color: #161616` is unresolvable from existing token.css.** Until a semantic global token is added, this value is hardcoded in the component token definition. Risk: if the design system later adopts a different dark text color, the label must be updated separately.
2. **Component tokens not in token.css.** The component is self-contained (tokens scoped on `.label`), but this deviates from the established convention of defining component tokens in token.css globally. Risk: theming overrides won't work via token.css alone until the tokens are moved.

---

## Assumptions

1. The label component always renders as a `<label>` HTML element. Span-based or div-based rendering is not supported.
2. The `for` attribute or nesting model is the consumer's responsibility; the component does not enforce it.
3. `aria-required="true"` on the associated form control is the consumer's responsibility; the presence of `.label__required` is a visual-only indicator.
4. RTL direction is set at or above the component level (e.g., `<html dir="rtl">`). The component does not self-declare direction.
5. No icon slot is present or needed in this component.

---

## Known Issues

- None at generation time.

---

## Missing Tokens

The following component-level tokens must be added to the `/* Label state tokens */` section in `token.css`:

```css
/* Label state tokens */
--label-gap:                    var(--spacing-xs);
--label-font-family:            var(--font-sans);
--label-font-size-md:           var(--fs-text-sm);
--label-line-height-md:         var(--lh-text-sm);
--label-font-size-lg:           var(--fs-text-md);
--label-line-height-lg:         var(--lh-text-md);
--label-font-weight-regular:    var(--font-weight-body);
--label-font-weight-semibold:   var(--font-weight-semibold);
--label-text-color:             #161616;
--label-required-color:         var(--error-700);
--label-text-color-disabled:    var(--gray-400);
--label-required-color-disabled: var(--gray-400);
```

`#161616` has no exact match in current token.css primitives. Recommend adding a form-field text semantic token or a near-black global: `--color-text-form: #161616`.

---

## Missing Standards

- No formal WCAG contrast audit has been run on label text colors. Estimated: #161616 text on white background = ~19:1 (passes). Disabled gray-400 (#9DA4AE) on white = ~2.5:1 — exempt per WCAG 1.4.3 for inactive components.

---

## TODO

- [ ] Add `/* Label state tokens */` section to `token.css`
- [ ] Resolve `--label-text-color: #161616` as a global semantic token in token.css
- [ ] Formal WCAG audit: contrast ratios for all text color combinations
- [ ] Verify `aria-required` behaviour across screen readers (NVDA, JAWS, VoiceOver)
- [ ] Generate showcase page (optional)
