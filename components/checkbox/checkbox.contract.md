# Checkbox — Component Contract

```
contract_version: 1.0.0
component_id:     checkbox
status:           stable
category:         form-input
last_reviewed:    2026-06-07
```

---

## 1. Purpose

A Checkbox allows the user to select one or more options from a set, or toggle a binary state. It is a **form input** — not a button.

Use Checkbox when:
- The user can select zero or more items from a list.
- The user needs to confirm acceptance of a condition.
- A parent item needs to reflect the partial selection of its children (indeterminate state).

Do NOT use Checkbox when:
- The user must choose exactly one option from mutually exclusive choices — use Radio instead.
- The action triggers immediately on toggle — use Toggle/Switch instead.

---

## 2. Anatomy

```
label.checkbox-wrapper                   ← accessible wrapper (optional, at form-field level)
  input.checkbox__input[type=checkbox]   ← visually hidden native input (required)
  span.checkbox                          ← visual control root
    span.checkbox__control               ← the visual box
      span.checkbox__checkmark           ← visible when checked (not indeterminate)
        svg.checkbox__icon               ← checkmark SVG
      span.checkbox__indeterminate-mark  ← visible when indeterminate
        svg.checkbox__icon               ← dash SVG
    span.checkbox__focus-ring            ← absolute focus indicator
```

---

## 3. CSS Modifiers

### Size modifiers (apply to `.checkbox`)

| Modifier | Dimension |
|----------|-----------|
| `.checkbox--md` | 24×24px (default) |
| `.checkbox--sm` | 20×20px |
| `.checkbox--xs` | 16×16px |

### Style modifiers (apply to `.checkbox`)

| Modifier | Selected background |
|----------|-------------------|
| `.checkbox--primary` | `--checkbox-bg-selected-primary` (#1B8354 green) |
| `.checkbox--neutral` | `--checkbox-bg-selected-neutral` (#161616 dark) |

### Check-state modifiers (apply to `.checkbox`)

| Modifier | Meaning |
|----------|---------|
| _(none)_ | Unchecked — shows border, no background |
| `.checkbox--checked` | Checked — shows selected background + checkmark icon |
| `.checkbox--indeterminate` | Indeterminate — shows selected background + dash icon |

> `--indeterminate` implies `--checked` background semantics. Never apply both `.checkbox--checked` and `.checkbox--indeterminate` simultaneously — `.checkbox--indeterminate` takes precedence visually.

### Interaction-state modifiers (apply to `.checkbox`)

| Modifier | Visual |
|----------|--------|
| _(hover via `:hover`)_ | Subtle background on unchecked control |
| _(active via `:active`)_ | Slight background shift |
| `.checkbox--focused` | Focus ring visible (also auto-triggers via `input:focus-visible`) |
| `.checkbox--readonly` | `opacity: 0.7`, pointer-events: none |
| `.checkbox--disabled` | `opacity: 0.5`, pointer-events: none, cursor: not-allowed |

---

## 4. HTML Contract

### Standard unchecked (primary, medium)
```html
<label class="checkbox-wrapper">
  <input type="checkbox" class="checkbox__input" id="option-1" />
  <span class="checkbox checkbox--md checkbox--primary" aria-hidden="true">
    <span class="checkbox__control">
      <span class="checkbox__checkmark">
        <svg class="checkbox__icon" aria-hidden="true" viewBox="0 0 12 9.116" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M1.5 4.5L4.833 7.833L10.5 1.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </span>
      <span class="checkbox__indeterminate-mark">
        <svg class="checkbox__icon" aria-hidden="true" viewBox="0 0 12 3" xmlns="http://www.w3.org/2000/svg">
          <rect width="12" height="3" rx="1.5" fill="currentColor"/>
        </svg>
      </span>
    </span>
    <span class="checkbox__focus-ring"></span>
  </span>
  <span class="checkbox-label">Option label</span>
</label>
```

### Checked state
```html
<input type="checkbox" class="checkbox__input" id="option-2" checked />
<span class="checkbox checkbox--md checkbox--primary checkbox--checked" aria-hidden="true">
  ...
</span>
```

### Indeterminate state (requires JS)
```html
<input type="checkbox" class="checkbox__input" id="parent" aria-checked="mixed" />
<span class="checkbox checkbox--md checkbox--primary checkbox--indeterminate" aria-hidden="true">
  ...
</span>
<script>
  document.getElementById('parent').indeterminate = true;
</script>
```

### Disabled
```html
<input type="checkbox" class="checkbox__input" id="option-3" disabled />
<span class="checkbox checkbox--md checkbox--primary checkbox--disabled" aria-hidden="true">
  ...
</span>
```

### Read-only
```html
<input type="checkbox" class="checkbox__input" id="option-4" aria-readonly="true" tabindex="0" />
<span class="checkbox checkbox--md checkbox--primary checkbox--readonly" aria-hidden="true">
  ...
</span>
```

---

## 5. Accessibility Contract

| Requirement | Mechanism |
|------------|-----------|
| Accessible name | Label text inside `<label>` or `aria-label` on `<input>` |
| Checked state | Native `<input type="checkbox" checked>` |
| Indeterminate state | `input.indeterminate = true` (JS) + `aria-checked="mixed"` |
| Disabled | `<input disabled>` — removes from tab order |
| Discoverable disabled | `aria-disabled="true"` without HTML `disabled` — keeps in tab order |
| Read-only | `aria-readonly="true"` + pointer-events: none via `.checkbox--readonly` |
| Focus visible | Native `:focus-visible` activates `.checkbox__focus-ring` |
| Icon semantics | All SVGs carry `aria-hidden="true"` |

---

## 6. Focus Ring

The focus ring is an absolute-positioned span extending 4px beyond the control on all sides.

| Size | Outer dimensions | Offset |
|------|-----------------|--------|
| md | 32×32px | −4px all sides |
| sm | 28×28px | −4px all sides |
| xs | 24×24px | −4px all sides |

The ring uses `inset 0 0 0 2px var(--checkbox-focus-ring-color)` and `mix-blend-mode: multiply`.

**Important:** The outer `.checkbox` must have `overflow: visible` for the focus ring to be visible outside the control bounds.

---

## 7. States Summary

| State | aria | CSS modifier | pointer-events |
|-------|------|-------------|----------------|
| Default | — | — | auto |
| Hovered | — | `:hover` (auto) | auto |
| Pressed | — | `:active` (auto) | auto |
| Focused | — | `.checkbox--focused` / `:focus-visible` | auto |
| Read-only | `aria-readonly="true"` | `.checkbox--readonly` | none |
| Disabled | `disabled` or `aria-disabled="true"` | `.checkbox--disabled` | none |

---

## 8. Token Surface

| Token | Usage |
|-------|-------|
| `--checkbox-border-unselected` | Border shadow when unchecked |
| `--checkbox-bg-selected-primary` | Background when checked/indeterminate — Primary style |
| `--checkbox-bg-selected-neutral` | Background when checked/indeterminate — Neutral style |
| `--checkbox-icon-oncolor` | SVG fill for checkmark and dash icons |
| `--checkbox-focus-ring-color` | Focus ring inset shadow color |
| `--checkbox-border-radius` | Border radius of the control box |
| `--checkbox-size-md` | Root dimension for medium size |
| `--checkbox-size-sm` | Root dimension for small size |
| `--checkbox-size-xs` | Root dimension for x-small size |
| `--checkbox-opacity-readonly` | Opacity for read-only state (0.7) |
| `--checkbox-opacity-disabled` | Opacity for disabled state (0.5) |
| `--checkbox-focus-ring-width` | Focus ring inset width (2px) |
| `--checkbox-focus-ring-offset` | Focus ring offset beyond control (4px) |
| `--checkbox-bg-hover` | Control background on hover (unchecked) — **missing, define in token.css** |
| `--checkbox-bg-pressed` | Control background on active/press — **missing, define in token.css** |
| `--checkbox-transition-duration` | Transition duration — **missing** |
| `--checkbox-transition-easing` | Transition easing — **missing** |

---

## 9. Assembly Notes

This component is the **checkbox control only**. It is intended to participate in:

- `checkbox-field` — control + label + optional helper/error text
- `checkbox-group` — labeled set of checkbox-fields
- `form-field` — full form row with validation

When building a parent/child selection pattern (indeterminate state), the parent checkbox's indeterminate and checked states must be managed by the containing component, not this component.

---

## 10. What This Component Does NOT Handle

- Label text
- Helper text
- Error/validation messages
- Error/invalid visual state (not in manifest — to be added)
- Group legend
- Select-all logic
