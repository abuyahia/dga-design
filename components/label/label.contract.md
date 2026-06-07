# Label — Component Contract

```
contract_version: 1.0.0
component_id:     label
status:           stable
category:         form
last_reviewed:    2026-06-06
```

---

## 1. Purpose

A Label provides a visible text description for a form field. It semantically associates with its form control to enable keyboard navigation and screen reader announcements.

It optionally renders a required asterisk (`*`) as a visual indicator when the field is required. The `*` is presentational only — the required state must be communicated to assistive technology via `aria-required="true"` on the associated form control.

> AI Rule: If a form field needs a visible text label, use Label. Do not use a `<span>` or `<div>` as a substitute.

---

## 2. When to Use / When NOT to Use

| Situation | Use Label? |
|---|---|
| Visible text label for a form field (input, select, textarea) | Yes |
| Required field indicator | Yes — add `.label__required` with `aria-hidden="true"` |
| Decorative text inside a form | No — use plain text or a heading |
| Label for a non-form element (button, link) | No — use `aria-label` on the target element |
| Hidden label (screen reader only) | No — use `sr-only` class on a `<label>` or `aria-label` |

---

## 3. Anatomy

```
label.label                       ← root element, semantic <label>
  span.label__required  [optional] ← required asterisk, aria-hidden="true"
  span.label__text                 ← visible label text
```

**Slot rules:**

| Slot | Required | Notes |
|---|---|---|
| `.label__text` | Always | The visible text content of the label |
| `.label__required` | Optional | Only when the associated field is required. Always set `aria-hidden="true"`. |

---

## 4. HTML Contract

### Standard label (required field)
```html
<label class="label" for="field-id">
  <span class="label__required" aria-hidden="true">*</span>
  <span class="label__text">Full Name</span>
</label>
<input id="field-id" type="text" aria-required="true" />
```

### Standard label (optional field — no asterisk)
```html
<label class="label" for="field-id">
  <span class="label__text">Middle Name</span>
</label>
<input id="field-id" type="text" />
```

### Large size
```html
<label class="label label--large" for="field-id">
  <span class="label__required" aria-hidden="true">*</span>
  <span class="label__text">Email Address</span>
</label>
```

### Semibold type
```html
<label class="label label--semibold" for="field-id">
  <span class="label__required" aria-hidden="true">*</span>
  <span class="label__text">National ID</span>
</label>
```

### Disabled state
```html
<label class="label label--disabled" aria-disabled="true" for="field-id">
  <span class="label__required" aria-hidden="true">*</span>
  <span class="label__text">Label</span>
</label>
```

### RTL (Arabic)
```html
<!-- dir="rtl" can be set on an ancestor (<html>, <body>, or a wrapping div) -->
<label class="label" dir="rtl" for="field-id-ar">
  <span class="label__required" aria-hidden="true">*</span>
  <span class="label__text">عنوان</span>
</label>
```

---

## 5. CSS Modifiers

| Modifier | Applies | Description |
|---|---|---|
| _(none)_ | base | Medium size, Regular weight, enabled |
| `.label--large` | size | Large size: 16px / 24px line-height |
| `.label--semibold` | type | Semibold weight: font-weight 600 |
| `.label--disabled` | state | Disabled visual state — all text muted to `--label-text-color-disabled` |

Modifiers combine freely:

```html
<label class="label label--large label--semibold label--disabled" ...>
```

---

## 6. HTML Attributes

| Attribute | Required | Values | Notes |
|---|---|---|---|
| `for` | Recommended | field element `id` | Associates label with its form control. Alternatively, nest the control inside the label. |
| `aria-disabled` | When disabled | `"true"` | Add alongside `.label--disabled`. The `<label>` element has no native `:disabled` state. |
| `dir` | For explicit RTL | `"rtl"` | Set on this element or an ancestor. Do not hardcode direction in CSS. |

---

## 7. Axes Summary

| Axis | CSS expression | Values |
|---|---|---|
| `type` | class modifier | `regular` (default, no class), `semibold` (`.label--semibold`) |
| `size` | class modifier | `medium` (default, no class), `large` (`.label--large`) |
| `disabled` | class + attribute | `false` (default), `true` (`.label--disabled` + `aria-disabled="true"`) |
| `rtl` | `dir` attribute | `false` (default), `true` (`dir="rtl"` on element or ancestor) |

---

## 8. Accessibility Contract

1. **`<label>` element is mandatory.** Using `<div>` or `<span>` breaks keyboard and screen reader association.

2. **Required asterisk must be `aria-hidden="true"`.** The visual `*` is decorative. Required state is communicated programmatically via `aria-required="true"` on the form control.

3. **Form control association is mandatory.** Use `for="id"` or nesting. An unassociated label does not announce to screen readers when the form field receives focus.

4. **Disabled label.** `aria-disabled="true"` is set on the `<label>` when the associated field is disabled. This is informational — the `<label>` itself is not interactive.

5. **Contrast.** Enabled text (`#161616` on white) ≈ 19:1 — passes WCAG AA and AAA. Disabled text (`#9DA4AE` on white) ≈ 2.5:1 — exempt per WCAG 1.4.3 for inactive UI components.

---

## 9. Token Summary

| Token | Value | Notes |
|---|---|---|
| `--label-gap` | `var(--spacing-xs, 4px)` | Gap between asterisk and text |
| `--label-text-color` | `#161616` | Enabled text color — no primitive match in token.css |
| `--label-required-color` | `var(--error-700, #B42318)` | Required asterisk color |
| `--label-text-color-disabled` | `var(--gray-400, #9DA4AE)` | Disabled text color |
| `--label-required-color-disabled` | `var(--gray-400, #9DA4AE)` | Disabled asterisk color |
| `--label-font-family` | `var(--font-sans)` | IBM Plex Sans Arabic |
| `--label-font-size-md` | `var(--fs-text-sm, 14px)` | Medium size |
| `--label-font-size-lg` | `var(--fs-text-md, 16px)` | Large size |
| `--label-line-height-md` | `var(--lh-text-sm, 20px)` | Medium line-height |
| `--label-line-height-lg` | `var(--lh-text-md, 24px)` | Large line-height |
| `--label-font-weight-regular` | `var(--font-weight-body, 400)` | Regular type |
| `--label-font-weight-semibold` | `var(--font-weight-semibold, 600)` | Semibold type |

---

## 10. Assembly Participation

Label participates in the following assemblies (do not merge):

```
label  →  text-input  →  form-field  →  form
label  →  select      →  form-field  →  form
label  →  textarea    →  form-field  →  form
```

The label is always a sibling of (or wraps) the form control. The assembly manages layout — the label component manages only its own text rendering.
