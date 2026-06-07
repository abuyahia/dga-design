# Text Input — Component Contract

```
contract_version: 1.0.0
component_id:     text-input
status:           stable
category:         form
last_reviewed:    2026-06-06
```

---

## 1. Purpose

Text Input captures a single line of freeform text from the user. It is used inside forms and composes with the label component, input-affix (prefix/suffix icons), and a form-field error message at the assembly layer.

It is NOT for:
- Multi-line text → use Textarea
- Selecting from options → use Select or Combobox
- Number entry with increment/decrement controls → use Number Input

---

## 2. When to Use / When NOT to Use

| Situation | Use Text Input? |
|---|---|
| Short freeform text (name, email, search) | Yes |
| Multi-line content | No — use Textarea |
| Selecting from a fixed list | No — use Select |
| Structured format (date, phone) | Yes — set `type` appropriately |
| With prefix icon or affix label | Yes — compose with input-affix |
| Display-only value | Prefer read-only text input or plain text |

---

## 3. Anatomy

```
.text-input                     ← root wrapper (flex-column, label-gap)
  .text-input__label            ← <label> element (text-sm, label color)
  .text-input__field            ← border box (relative, overflow:hidden)
    .text-input__field::after   ← focus/pressed underline accent (2px, absolute bottom)
    .text-input__inner          ← inner padding container (inline padding + flex)
      .text-input__input        ← native <input> element
```

**Slot rules:**

| Slot | Required | Notes |
|---|---|---|
| `.text-input__label` | Required | Must be a `<label>` with `for` matching input `id` |
| `.text-input__field` | Required | Do not remove — hosts underline, border, and state styling |
| `.text-input__inner` | Required | Do not remove — provides padding |
| `.text-input__input` | Required | Must be a native `<input>` element |

---

## 4. HTML Contract

### Standard text input (large, default)
```html
<div class="text-input">
  <label class="text-input__label" for="field-id">Label</label>
  <div class="text-input__field">
    <div class="text-input__inner">
      <input
        class="text-input__input"
        type="text"
        id="field-id"
        name="field-name"
        placeholder="Placeholder text"
      />
    </div>
  </div>
</div>
```

### Medium size
```html
<div class="text-input text-input--md">
  ...
</div>
```

### Required field
```html
<div class="text-input">
  <label class="text-input__label" for="field-id">
    Label <span aria-hidden="true">*</span>
  </label>
  <div class="text-input__field">
    <div class="text-input__inner">
      <input class="text-input__input" type="text" id="field-id"
        placeholder="Placeholder text" required aria-required="true" />
    </div>
  </div>
</div>
```

### Error state
```html
<!-- Consumer provides error message element and aria-describedby linkage -->
<div class="text-input text-input--error">
  <label class="text-input__label" for="field-id">Label</label>
  <div class="text-input__field">
    <div class="text-input__inner">
      <input class="text-input__input" type="text" id="field-id"
        aria-describedby="field-error" aria-invalid="true"
        placeholder="Placeholder text" />
    </div>
  </div>
</div>
<span id="field-error" role="alert">Error message text</span>
```

### Disabled
```html
<div class="text-input text-input--disabled">
  <label class="text-input__label" for="field-id">Label</label>
  <div class="text-input__field">
    <div class="text-input__inner">
      <input class="text-input__input" type="text" id="field-id"
        placeholder="Placeholder text" disabled />
    </div>
  </div>
</div>
```

> **Note:** `disabled` on the `<input>` provides native AT support. The `.text-input--disabled` class is for CSS styling only. Do not add `aria-disabled` to the input — use the native attribute.

### Read-only
```html
<div class="text-input text-input--readonly">
  <label class="text-input__label" for="field-id">Label</label>
  <div class="text-input__field">
    <div class="text-input__inner">
      <input class="text-input__input" type="text" id="field-id"
        value="Display value" readonly />
    </div>
  </div>
</div>
```

### Filled Darker style
```html
<div class="text-input text-input--filled-darker">
  ...
</div>
```

### Filled Lighter style
```html
<div class="text-input text-input--filled-lighter">
  ...
</div>
```

### RTL
```html
<!-- Apply dir="rtl" to .text-input, its parent, or <html> -->
<div class="text-input" dir="rtl">
  <label class="text-input__label" for="field-id">التسمية</label>
  <div class="text-input__field">
    <div class="text-input__inner">
      <input class="text-input__input" type="text" id="field-id"
        placeholder="نص توضيحي" />
    </div>
  </div>
</div>
```

---

## 5. Modifier Classes

| Class | Description |
|---|---|
| `.text-input--md` | Medium size (32px height, 14px font) |
| `.text-input--error` | Error state (error border color, error underline on focus) |
| `.text-input--disabled` | Disabled state (muted border, muted text, no interactions) |
| `.text-input--readonly` | Read-only state (neutral border, focus ring suppressed) |
| `.text-input--filled-darker` | Filled darker background style (no default border) |
| `.text-input--filled-lighter` | Filled lighter background style (no default border) |

**Modifier combinations:**

| Combination | Valid? | Notes |
|---|---|---|
| `--md` + `--error` | Yes | Medium size with error |
| `--error` + `--disabled` | Yes | Disabled takes visual priority — error border suppressed |
| `--error` + `--readonly` | Yes | Error border shown (design decision: readonly can still be invalid) |
| `--filled-darker` + `--error` | Yes | Error border overrides transparent border |
| `--disabled` + `--readonly` | Not recommended | Use one or the other |

---

## 6. States

| State | CSS trigger | Description |
|---|---|---|
| Default | base | Resting state |
| Hovered | `:hover` on `.text-input__field` | Border darkens |
| Focused | `:focus-within` on `.text-input__field` | Border transparent + 2px underline shown |
| Pressed | `:active` on `.text-input__field` | Darker background + partial underline |
| Disabled | `.text-input--disabled` | Muted border, no interactions |
| Read-only | `.text-input--readonly` | Neutral border, focus ring suppressed |

---

## 7. Accessibility

### Required attributes

| Context | Required attribute |
|---|---|
| Always | `id` on input, `for` on label — must match |
| Required field | `required` + `aria-required="true"` on input |
| Error state | `aria-invalid="true"` + `aria-describedby="[error-id]"` on input |
| Read-only | `readonly` on input (native AT announcement) |
| Disabled | `disabled` on input (native AT announcement) |
| RTL | `dir="rtl"` on `.text-input` or ancestor |

### Error message responsibility
The text-input component provides only the visual error state (`.text-input--error`). The error message text element and its `id` are the responsibility of the consuming assembly (form-field, form).

### Focus indicator
The focus underline (2px, `#0D121C` on white) provides a WCAG 2.4.11 compliant focus indicator (~21:1 contrast). Do not suppress the `::after` indicator.

### Placeholder contrast
`--text-input-text-placeholder` (#6C737F) on `#FFF` = ~4.8:1. Passes WCAG 1.4.3 for normal-size text.

---

## 8. `type` Attribute

Set `type` based on the data being collected:

| Data type | Recommended `type` |
|---|---|
| Free text | `text` (default) |
| Email address | `email` |
| Phone number | `tel` |
| Search query | `search` |
| URL | `url` |
| Password | `password` |
| Number | `number` |

---

## 9. `autocomplete` Attribute

Set `autocomplete` per the field's purpose. Examples:
- `autocomplete="name"` — full name
- `autocomplete="email"` — email address
- `autocomplete="off"` — disable (only for truly unique values)

---

## 10. Assembly Context

```
text-input
  ↓ composes with input-affix (prefix / suffix icons / text)
  ↓ composes with form-field (label + input + hint + error message)
  ↓ composes with form (multiple form-fields + submit button)
```

Do not embed error message text inside `.text-input`. That belongs in the `form-field` assembly layer.

---

## 11. Token Dependencies

All `--text-input-*` tokens must be defined in `token.css`. See `analysis.md` Missing Tokens section for the full list. Until added to `token.css`, fallback values in `text-input.css` are active.

---

## 12. AI Generation Rules

```
AI rule: text-input root element is always <div class="text-input">.
AI rule: label is always <label class="text-input__label" for="...">. Never <span> or <p>.
AI rule: input is always <input class="text-input__input"> inside .text-input__inner inside .text-input__field.
AI rule: error state uses .text-input--error on root + aria-invalid="true" + aria-describedby on input.
AI rule: disabled uses .text-input--disabled on root + disabled attribute on input.
AI rule: read-only uses .text-input--readonly on root + readonly attribute on input.
AI rule: RTL uses dir="rtl" on root or ancestor. Never override padding-left/right in component CSS for RTL.
AI rule: Do not add inline styles to any .text-input* element.
AI rule: The .text-input__field::after underline must not be removed or overridden to display:none.
```
