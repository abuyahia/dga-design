# Floating Button — Component Contract

```
contract_version: 1.0.0
component_id:     floating-button
status:           stable
category:         action
last_reviewed:    2026-06-13
```

---

## Component Type

Primitive

---

## Dependencies

- None

---

## 1. Purpose

A Floating Action Button (FAB) represents the **primary or persistent action** on a screen. It floats above the main content layer.

Use it for a single, high-emphasis action: create, add, compose, navigate.

> AI Rule: Use at most one FAB per screen. It represents the most important action available, not a secondary choice.

---

## 2. When to Use / When NOT to Use

| Situation | Use FAB? |
|---|---|
| The most important action on the screen | Yes |
| Add, create, or compose a primary item | Yes |
| Scrolling to top (persistent action) | Yes |
| Secondary action alongside another FAB | No — use a regular button |
| Destructive action (delete, remove) | No — FAB implies affirmative action |
| Navigation to another page | Prefer Link or navigation button |
| Multiple equally important actions | No — pick the primary action |

---

## 3. HTML Anatomy

### Icon-Only (circular — default mode)

```html
<button type="button" class="fab" aria-label="Add item">
  <span class="fab__icon" aria-hidden="true">
    <svg><!-- 24×24 icon --></svg>
  </span>
</button>
```

### With Label (pill mode)

```html
<button type="button" class="fab" aria-label="Add item">
  <span class="fab__icon" aria-hidden="true">
    <svg><!-- 24×24 icon --></svg>
  </span>
  <span class="fab__label">Add</span>
</button>
```

---

## 4. Class Reference

### Root

| Class | Description |
|---|---|
| `.fab` | Required. Base class. Defaults to Primary-Neutral style, Small size. |

### Style Modifiers

| Class | Description |
|---|---|
| _(none)_ | Primary-Neutral — dark background, white icon/text |
| `.fab--primary-brand` | Primary-Brand — brand green background, white icon/text |
| `.fab--secondary-solid` | Secondary-Solid — light background, dark icon/text |

### Context Modifier

| Class | Description |
|---|---|
| `.fab--on-color` | On-color context — button is on a colored/dark background. Changes token set. Combine with any style modifier. |

### Size Modifiers

| Class | Description |
|---|---|
| _(none)_ | Small — 16px padding, 56px diameter (icon-only) |
| `.fab--lg` | Large — 20px padding, 64px diameter (icon-only) |

### State Helpers (showcase / JS-driven)

| Class | Equivalent CSS state |
|---|---|
| `.is-focused` | `:focus` |
| `.is-pressed` | `:active` |
| `.is-selected` | `[aria-pressed="true"]` |

### Anatomy Elements

| Class | Description |
|---|---|
| `.fab__icon` | Icon wrapper. Required. Contains inline SVG. |
| `.fab__label` | Text label. Optional. Present only in labeled mode. |

---

## 5. States

| State | Trigger | HTML |
|---|---|---|
| Default | — | base |
| Hovered | User hovers | `:hover` (CSS) |
| Focused | User focuses (any method) | `:focus` / `:focus-visible` |
| Pressed | User clicks/taps | `:active` |
| Disabled | Not interactive | `disabled` attribute |
| Selected | Toggle is on | `aria-pressed="true"` |

---

## 6. Accessibility

### Required attributes

- **Icon-only mode:** `aria-label` on `<button>` is **required** — no visible text exists.
- **Labeled mode:** `aria-label` is recommended but optional if label text is sufficiently descriptive.
- `aria-hidden="true"` on `.fab__icon` — the icon is decorative; the label or `aria-label` provides the accessible name.
- `type="button"` — always required to prevent accidental form submission.

### Focus ring

- Implemented as `::after` pseudo-element.
- Extends 5px beyond the button boundary.
- Width: 3px solid `var(--fab-focus-ring-color)`.
- Present on both `:focus` and `:focus-visible`.
- Suppressed during `:active` (press cancels focus ring).

### Disabled

Prefer `disabled` attribute over `aria-disabled="true"` for `<button>` elements. Both are supported.

When disabled:
- `pointer-events: none` — prevents hover/active interference.
- Do not remove `disabled` attribute for styling purposes.

### Selected / Toggle state

- Use `aria-pressed="true"` to communicate selected/active toggle state.
- Announce state change via ARIA live region if not obvious from context.

---

## 7. Examples

### Primary-Neutral, Small, Icon-Only

```html
<button type="button" class="fab" aria-label="Add item">
  <span class="fab__icon" aria-hidden="true">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </span>
</button>
```

### Primary-Brand, Large, Icon-Only

```html
<button type="button" class="fab fab--primary-brand fab--lg" aria-label="Create">
  <span class="fab__icon" aria-hidden="true">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </span>
</button>
```

### Secondary-Solid, Small, With Label

```html
<button type="button" class="fab fab--secondary-solid">
  <span class="fab__icon" aria-hidden="true">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </span>
  <span class="fab__label">Add</span>
</button>
```

### On-Color Context (on dark background)

```html
<button type="button" class="fab fab--on-color" aria-label="Add item">
  <span class="fab__icon" aria-hidden="true">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </span>
</button>
```

### Disabled

```html
<button type="button" class="fab" aria-label="Add item" disabled>
  <span class="fab__icon" aria-hidden="true">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </span>
</button>
```

### Selected (Toggle Active)

```html
<button type="button" class="fab" aria-label="Remove item" aria-pressed="true">
  <span class="fab__icon" aria-hidden="true">
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </span>
</button>
```

---

## 8. Positioning

The FAB is not positioned by the component itself. Position it via layout:

```css
.fab-wrapper {
  position: fixed;
  inset-block-end: var(--spacing-4xl);   /* 40px from bottom */
  inset-inline-end: var(--spacing-4xl);  /* 40px from edge */
  z-index: 100;
}
```

Use `inset-inline-end` (not `right`) for RTL compatibility.

---

## 9. RTL

For labeled mode, flex direction reverses automatically via:

```css
[dir="rtl"] .fab {
  flex-direction: row-reverse;
}
```

For icon-only mode: no change needed (circular, symmetric).

---

## 10. Token Dependency

All `--fab-*` tokens are provisionally defined in `floating-button.css`. They must be migrated to `token.css` before production use.

See `analysis.md → Missing Tokens` for the full list.

---

## 11. Known Issues

- Focus ring color (`--fab-focus-ring-color`) uses `--gray-950` (#0D121C). On dark page backgrounds, this ring may have insufficient contrast. A separate on-color focus ring token is needed.
- Secondary-Solid On-Color Focused state produces a fully transparent background. Icon visual containment may be lost.
