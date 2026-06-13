# Inline Alert — Component Contract

```
contract_version: 1.0.0
component_id:     inline-alert
status:           stable
category:         feedback
last_reviewed:    2026-06-13
```

---

## 1. Component Type

Composite

---

## 2. Purpose

The Inline Alert communicates system status, contextual feedback, or important information to the user within the page flow. It is not a toast (which auto-dismisses) and not a modal (which blocks interaction). It is a persistent, dismissible notification that lives inline with page content.

> AI Rule: Use Inline Alert when the notification is relevant to the current page context and the user may need to act on it. Use a toast for transient confirmations that require no action.

---

## 3. When to Use / When NOT to Use

| Situation | Use Inline Alert? |
|---|---|
| Communicate form-level validation errors | Yes |
| Communicate successful form submission | Yes |
| Warn about an irreversible action before it happens | Yes — use `destructive` or `warning` type |
| Provide contextual guidance or tips | Yes — use `info` or `neutral` type |
| Confirm a transient action (file saved, copied) | No — use a Toast |
| Block the user until they acknowledge | No — use a Dialog/Modal |
| Show a page-level error (500, network) | Maybe — consider a Banner instead |

---

## 4. Dependencies

Required:
- None

Optional:
- Button component — for action buttons that require full `.btn` behavioral parity (focus management, disabled states, loading states). The inline-alert provides its own `.inline-alert__action` styles that cover the common case.

---

## 5. Anatomy

```
.inline-alert                      ← root (div, role="alert")
├── ::before                       ← vertical accent bar (decorative)
├── .inline-alert__header          ← Title row
│   ├── .inline-alert__icon-wrap   ← Featured icon circle (40×40)
│   │   └── .inline-alert__icon    ← SVG icon (20×20, aria-hidden)
│   ├── .inline-alert__content     ← Text area
│   │   ├── .inline-alert__title   ← Alert title (p)
│   │   └── .inline-alert__body    ← Supporting text (p, optional)
│   └── .inline-alert__close       ← Dismiss button (button)
│       └── SVG × icon (aria-hidden)
└── .inline-alert__actions         ← Action buttons row (optional)
    ├── .inline-alert__action.inline-alert__action--primary
    └── .inline-alert__action.inline-alert__action--secondary
```

---

## 6. Variants

### Type (semantic severity)

| Modifier | Semantic | Accent | Icon |
|---|---|---|---|
| _(none)_ | Neutral | Gray | help-circle |
| `.inline-alert--info` | Informational | Blue | help-circle |
| `.inline-alert--destructive` | Error / Destructive | Red | help-circle |
| `.inline-alert--warning` | Caution | Amber | alert-02 |
| `.inline-alert--success` | Confirmation | Green | tick-02 |

### Background

| Modifier | Effect |
|---|---|
| _(none)_ | White background, neutral border |
| `.inline-alert--color-bg` | Tinted background + type-colored border |

### Layout

| Modifier | Effect |
|---|---|
| _(none)_ | Desktop — horizontal header row, compact action buttons |
| `.inline-alert--mobile` | Mobile — stacked column layout, full-width action buttons |

Mobile layout also activates automatically via `@media (max-width: 768px)`.

### Directionality

| Mechanism | Effect |
|---|---|
| `dir="rtl"` on root or ancestor | Right-to-left layout via CSS logical properties |

---

## 7. HTML API

### Root element

```html
<div class="inline-alert [modifier classes]"
     role="alert"
     aria-live="polite">
```

Use `aria-live="assertive"` for Destructive type alerts that require immediate user attention.

### Close button

```html
<button type="button"
        class="inline-alert__close"
        aria-label="Dismiss notification">
```

### Icon

```html
<div class="inline-alert__icon-wrap">
  <svg class="inline-alert__icon" aria-hidden="true" focusable="false">
    <!-- icon path -->
  </svg>
</div>
```

### Action buttons

```html
<div class="inline-alert__actions">
  <button type="button" class="inline-alert__action inline-alert__action--primary">Primary Action</button>
  <button type="button" class="inline-alert__action inline-alert__action--secondary">Secondary Action</button>
</div>
```

The `.inline-alert__actions` element is **optional**. Omit it entirely when no actions are needed.

---

## 8. States

| State | Implementation |
|---|---|
| Visible | Default — no modifier |
| Dismissed | `hidden` attribute on root OR `display: none` via JavaScript |
| Close `:hover` | Browser default or extend in component CSS |
| Close `:focus-visible` | Outline ring applied via `:focus-visible` |
| Action `:focus-visible` | Outline ring applied via `:focus-visible` |

---

## 9. CSS Modifiers Summary

| Class | Description |
|---|---|
| `.inline-alert` | Root element — required |
| `.inline-alert--info` | Info type |
| `.inline-alert--destructive` | Destructive / Error type |
| `.inline-alert--warning` | Warning type |
| `.inline-alert--success` | Success type |
| `.inline-alert--color-bg` | Tinted background variant |
| `.inline-alert--mobile` | Mobile layout (also responds to media query) |
| `.inline-alert__header` | Header row — required child |
| `.inline-alert__icon-wrap` | Icon circle container |
| `.inline-alert__icon` | SVG icon inside wrap |
| `.inline-alert__content` | Text container |
| `.inline-alert__title` | Alert title text |
| `.inline-alert__body` | Supporting/body text (optional) |
| `.inline-alert__close` | Dismiss button |
| `.inline-alert__actions` | Actions row (optional) |
| `.inline-alert__action` | Action button base |
| `.inline-alert__action--primary` | Primary action button |
| `.inline-alert__action--secondary` | Secondary action button |

---

## 10. Accessibility Contract

| Requirement | Implementation |
|---|---|
| `role="alert"` on root | Required |
| `aria-live` on root | `"polite"` default; `"assertive"` for Destructive |
| Close button has accessible name | `aria-label="Dismiss notification"` |
| Icon is decorative | `aria-hidden="true"` on all icon SVGs |
| Color is not sole differentiator | Icon shape and text convey type meaning alongside color |
| Keyboard operable | Close button and action buttons are native `<button>` elements |
| Focus visible | `:focus-visible` outline on close and action buttons |

---

## 11. Token Reference

### Spacing

| Token | Fallback | Used For |
|---|---|---|
| `--inline-alert-padding-block` | `16px` | Vertical padding |
| `--inline-alert-padding-inline` | `24px` | Horizontal padding |
| `--inline-alert-gap` | `16px` | Gap between header and actions |
| `--inline-alert-header-gap` | `12px` | Gap between icon, content, close |
| `--inline-alert-content-gap` | `8px` | Gap between title and body |
| `--inline-alert-actions-gap` | `8px` | Gap between action buttons |
| `--inline-alert-actions-padding-inline` | `40px` | Actions indent |

### Surface

| Token | Fallback | Used For |
|---|---|---|
| `--inline-alert-bg` | `#FFF` | Root background |
| `--inline-alert-border-color` | `#D2D6DB` | Root border |
| `--inline-alert-border-radius` | `8px` | Root corner radius |
| `--inline-alert-icon-bg` | `#F9FAFB` | Icon circle background |
| `--inline-alert-icon-radius` | `9999px` | Icon circle radius |
| `--inline-alert-accent-bg` | `#E5E7EB` | Accent bar color |
| `--inline-alert-accent-width` | `8px` | Accent bar width |
| `--inline-alert-accent-opacity` | `0.7` | Accent bar opacity |

### Typography

| Token | Fallback | Used For |
|---|---|---|
| `--inline-alert-title-color` | `#1F2A37` | Title text color |
| `--inline-alert-title-font-size` | `16px` | Title font size |
| `--inline-alert-title-font-weight` | `600` | Title font weight |
| `--inline-alert-title-line-height` | `24px` | Title line height |
| `--inline-alert-body-color` | `#384250` | Body text color |
| `--inline-alert-body-font-size` | `14px` | Body font size |
| `--inline-alert-body-font-weight` | `400` | Body font weight |
| `--inline-alert-body-line-height` | `20px` | Body line height |

### Close Button

| Token | Fallback | Used For |
|---|---|---|
| `--inline-alert-close-size` | `32px` | Close button size |
| `--inline-alert-close-radius` | `4px` | Close button radius |

---

## 12. Do / Don't

| Do | Don't |
|---|---|
| Use `role="alert"` on the root | Use `div` without `role="alert"` |
| Provide `aria-label` on the close button | Leave the close button label-less |
| Use `aria-hidden` on all icon SVGs | Let icon SVGs pollute the accessibility tree |
| Omit `.inline-alert__actions` when no actions are needed | Render an empty actions container |
| Use `aria-live="assertive"` for urgent destructive alerts | Use `assertive` for every alert type |
| Dismiss via JavaScript (`hidden` or removal) | Use CSS `visibility: hidden` alone (still occupies space) |
