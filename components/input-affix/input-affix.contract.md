# Input Affix — Component Contract

```
contract_version: 1.0.0
component_id:     input-affix
status:           stable
category:         form / subcomponent
last_reviewed:    2026-06-06
```

---

## 1. Purpose

An Input Affix is a prefix or suffix attachment that visually joins the leading or trailing edge of a text-input field. It provides context for the input value (currency symbol, unit, country code) or an interactive dropdown trigger.

It is NOT a standalone component. It is a **subcomponent** that participates in:
- `text-input` (direct host)
- `form-field` (via text-input)

> AI Rule: If the content is a read-only label, use `Type=Text`. If it opens a select or dropdown, use `Type=Dropdown`.

---

## 2. When to Use / When NOT to Use

| Situation | Use Affix? |
|---|---|
| Show a currency symbol next to an amount field | Yes — Text affix |
| Show a country code before a phone number field | Yes — Text affix |
| Allow selecting a unit (kg / lb) attached to an input | Yes — Dropdown affix |
| Allow selecting a country code from a list | Yes — Dropdown affix |
| Display an icon inside the input field itself | No — use input icon slot |
| Display helper text below the input | No — use form-field hint slot |

---

## 3. Anatomy

```
.input-affix                          ← root (button or div)
  .input-affix__icon  [optional]      ← decorative SVG icon (Dropdown only)
  .input-affix__text                  ← visible label text
  .input-affix__arrow [optional]      ← chevron icon (Dropdown only)
```

**Slot rules:**

| Slot | Required | Notes |
|---|---|---|
| `.input-affix__text` | Always | Visible label |
| `.input-affix__icon` | Optional | Dropdown type only. Must carry `aria-hidden="true"` |
| `.input-affix__arrow` | Optional | Dropdown type only. Must carry `aria-hidden="true"` |

---

## 4. HTML Contract

### Text affix (read-only label)

```html
<div class="input-affix input-affix--text input-affix--solid" aria-hidden="true">
  <span class="input-affix__text">USD</span>
</div>
```

> Note: `aria-hidden="true"` is recommended on Text affixes when the label is visually redundant with the input's placeholder or label. Remove if the affix text adds unique context not captured elsewhere.

### Dropdown affix (interactive trigger)

```html
<button class="input-affix input-affix--dropdown input-affix--solid" type="button" aria-expanded="false">
  <svg class="input-affix__icon" aria-hidden="true" focusable="false"><!-- icon SVG --></svg>
  <span class="input-affix__text">USD</span>
  <svg class="input-affix__arrow" aria-hidden="true" focusable="false"><!-- chevron SVG --></svg>
</button>
```

### Medium size

Add `.input-affix--md` to the root element:

```html
<button class="input-affix input-affix--dropdown input-affix--solid input-affix--md" type="button" aria-expanded="false">
  ...
</button>
```

### Subtle style

Replace `.input-affix--solid` with `.input-affix--subtle`:

```html
<button class="input-affix input-affix--dropdown input-affix--subtle" type="button" aria-expanded="false">
  ...
</button>
```

### Disabled

```html
<!-- Dropdown (button) -->
<button class="input-affix input-affix--dropdown input-affix--solid" type="button" disabled>
  ...
</button>

<!-- Text (div) — [disabled] is invalid on div, use aria-disabled -->
<div class="input-affix input-affix--text input-affix--solid" aria-disabled="true" aria-hidden="true">
  <span class="input-affix__text">USD</span>
</div>
```

### Selected (Dropdown only)

```html
<button class="input-affix input-affix--dropdown input-affix--solid" type="button" aria-selected="true" aria-expanded="false">
  <svg class="input-affix__icon" aria-hidden="true" focusable="false"><!-- icon --></svg>
  <span class="input-affix__text">USD</span>
  <svg class="input-affix__arrow" aria-hidden="true" focusable="false"><!-- chevron --></svg>
</button>
```

---

## 5. Class Modifier Reference

| Modifier | Applies to | Effect |
|---|---|---|
| `.input-affix--text` | Root | Text type — non-interactive, renders as div |
| `.input-affix--dropdown` | Root | Dropdown type — interactive, renders as button |
| `.input-affix--solid` | Root | Solid style — filled background on Default state |
| `.input-affix--subtle` | Root | Subtle style — transparent on Default state |
| `.input-affix--md` | Root | Medium size (32px height, 12px inline padding, 14px font) |

**Default state (no modifier)** = Large size.

---

## 6. States

| State | CSS expression | Applies to |
|---|---|---|
| Default | base selector | Both types |
| Hovered | `:hover` | Dropdown only |
| Pressed | `:active` | Dropdown only |
| Focused | `:focus-visible` | Dropdown only |
| Selected | `[aria-selected="true"]` | Dropdown only |
| Disabled | `[disabled]` / `[aria-disabled="true"]` | Both types |

---

## 7. RTL Support

RTL layout is handled by `[dir="rtl"]` on the page ancestor. The affix does not require a separate RTL class. The flex container direction reversal automatically places the icon and arrow in the correct order.

```html
<html dir="rtl">
  <!-- affix renders correctly without any additional class -->
</html>
```

---

## 8. Token Reference

All visual values use `--input-affix-*` CSS custom properties. See `reference.json` for the full token map.

**Critical tokens (all pending registration in token.css):**

```css
--input-affix-bg-solid-default
--input-affix-bg-hovered
--input-affix-bg-pressed
--input-affix-bg-focused
--input-affix-bg-selected
--input-affix-bg-disabled
--input-affix-text-default
--input-affix-text-placeholder
--input-affix-text-selected
--input-affix-text-disabled
--input-affix-focus-ring-color
--input-affix-focus-ring-width
--input-affix-font-family
--input-affix-lg-height
--input-affix-lg-padding-inline
--input-affix-md-height
--input-affix-md-padding-inline
--input-affix-radius
```

---

## 9. Accessibility Contract

| Rule | Detail |
|---|---|
| Dropdown root element | `<button type="button">` |
| Text root element | `<div>` |
| Dropdown accessible name | Visible text in `.input-affix__text` |
| Expanded state | `aria-expanded="true"/"false"` on Dropdown root when controlling a panel |
| Selected state | `aria-selected="true"` — requires parent `role="listbox"` context |
| Disabled Dropdown | `disabled` attribute on `<button>` |
| Disabled Text | `aria-disabled="true"` on `<div>` |
| Icons | `aria-hidden="true"` and `focusable="false"` on all icon SVGs |
| Focus ring | CSS `outline` (not `border`) — 4px solid, color `--input-affix-focus-ring-color` |

---

## 10. Assembly Context

This component is designed to participate in:

1. **text-input** — as a prefix or suffix slot
2. **form-field** — via text-input
3. **form** — via form-field

Do not use input-affix in isolation without a connected `<input>` element. The affix is visually meaningless without the input it modifies.
