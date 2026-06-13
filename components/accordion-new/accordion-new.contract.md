# Accordion — Component Contract

```
contract_version: 1.0.0
component_id:     accordion-new
status:           stable
category:         disclosure
last_reviewed:    2026-06-12
```

---

## Component Type

Primitive

---

## Dependencies

None.

---

## 1. Purpose

An Accordion item reveals or conceals a block of content when its header is activated. It uses progressive disclosure to reduce cognitive load and page length.

Use an accordion when users need selective access to content sections and can orient themselves from the title alone. Do NOT use when all content should be visible by default or when the hidden content is critical to task completion.

---

## 2. Anatomy

```
.accordion                         ← root div, owns border-top divider
├── .accordion__trigger            ← <button>, toggle control
│   ├── .accordion__title          ← heading text (flex: 1)
│   └── .accordion__icon           ← chevron SVG, aria-hidden, rotates on expand
└── .accordion__panel              ← collapsible region (hidden when collapsed)
    └── .accordion__body           ← content slot
```

---

## 3. HTML Contract

### Default — collapsed (Trailing icon, Medium, Flush=False)

```html
<div class="accordion accordion--md">
  <button
    class="accordion__trigger"
    type="button"
    id="accordion-trigger-1"
    aria-expanded="false"
    aria-controls="accordion-panel-1"
  >
    <span class="accordion__title">Accordion Title</span>
    <svg class="accordion__icon" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none">
      <path d="M3.5 6l4.5 4.5 4.5-4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </button>
  <div
    class="accordion__panel"
    id="accordion-panel-1"
    role="region"
    aria-labelledby="accordion-trigger-1"
  >
    <div class="accordion__body">
      Content text goes here.
    </div>
  </div>
</div>
```

### Expanded state

Set `aria-expanded="true"` on the trigger — the panel becomes visible via CSS.

```html
<button
  class="accordion__trigger"
  type="button"
  id="accordion-trigger-1"
  aria-expanded="true"
  aria-controls="accordion-panel-1"
>
  ...
</button>
```

### Disabled state

```html
<button class="accordion__trigger" type="button" disabled aria-expanded="false">
  <span class="accordion__title">Disabled Accordion</span>
  <svg class="accordion__icon" aria-hidden="true" ...></svg>
</button>
```

---

## 4. Modifier Classes

| Class | Effect |
|---|---|
| `.accordion--sm` | Small size — 8px padding-block on header |
| `.accordion--md` | Medium size — 12px padding-block on header |
| (none) | Large size — 16px padding-block on header (default) |
| `.accordion--icon-leading` | Icon placed at inline-start of header; content panel indented on inline-start |
| `.accordion--flush` | Zero horizontal padding on header; interaction background and focus ring bleed to fill parent container |

Modifiers can be combined:

```html
<div class="accordion accordion--sm accordion--flush accordion--icon-leading">
```

---

## 5. States

| State | Trigger | Notes |
|---|---|---|
| Default | (base) | No background |
| Hovered | `:hover` on trigger | Background overlay via `::before` |
| Pressed | `:active` on trigger | Darker background overlay via `::before` |
| Focused | `:focus-visible` on trigger | 2px inset outline; Flush uses bleed `::after` |
| Disabled | `[disabled]` on trigger | Muted title color; no bg states; cursor: not-allowed |

---

## 6. Expanded / Collapsed

Expansion is controlled by `aria-expanded` on the trigger button.

- `aria-expanded="false"` → panel hidden
- `aria-expanded="true"` → panel visible

The icon rotates 180° via CSS transform when `aria-expanded="true"`.

JavaScript responsibility: toggle `aria-expanded` value on click. No class toggling required.

---

## 7. Icon

The icon slot uses a single down-chevron SVG. CSS rotates it 180° when expanded.

- Always set `aria-hidden="true"` on the icon — it is purely decorative.
- Do not add alt text or title to the icon SVG.
- The icon follows `currentColor` for stroke/fill — it inherits the trigger's text color.

---

## 8. Flush Variant

The flush variant removes horizontal padding from the header, aligning the title to the container edge. The interaction background (hover/pressed) and focus ring extend beyond the header bounds to fill the parent container width.

**Requirement:** The parent container must have `overflow: clip` (or `overflow: hidden`) to prevent the bleed overlay from extending outside the desired boundary.

```html
<div style="overflow: clip; padding-inline: 16px;">
  <div class="accordion accordion--flush">
    ...
  </div>
</div>
```

---

## 9. RTL Support

No RTL modifier class required. Set `dir="rtl"` on an ancestor element. All padding, margin, and position values use CSS logical properties (`padding-inline-start`, `padding-inline-end`, `inset-inline-start`, etc.) which automatically mirror in RTL.

---

## 10. Accessibility Contract

| Requirement | Implementation |
|---|---|
| Trigger is a native button | `<button type="button">` |
| Expanded state communicated | `aria-expanded="true/false"` on button |
| Panel linked to trigger | `aria-controls` on button, matching `id` on panel |
| Panel labels itself | `role="region"` + `aria-labelledby` pointing to trigger `id` |
| Icon is decorative | `aria-hidden="true"` on SVG |
| Keyboard activation | Native button handles Enter and Space |
| Focus indicator | `:focus-visible` with 2px solid outline (inset) |
| Disabled communicates state | `disabled` attribute (native semantics) |

---

## 11. Token Dependency

All tokens below are pending addition to `token.css`. Component uses global token fallbacks in the interim.

```
--accordion-border-color
--accordion-title-color
--accordion-title-color-disabled
--accordion-content-color
--accordion-bg-hovered
--accordion-bg-pressed
--accordion-focus-ring-color
--accordion-focus-ring-width
--accordion-title-font-family
--accordion-title-font-size
--accordion-title-font-weight
--accordion-title-line-height
--accordion-content-font-size
--accordion-content-font-weight
--accordion-content-line-height
--accordion-lg-padding-block
--accordion-md-padding-block
--accordion-sm-padding-block
--accordion-padding-inline
--accordion-content-padding-top
--accordion-content-padding-bottom
--accordion-content-icon-indent
--accordion-content-icon-indent-flush
--accordion-gap
--accordion-content-gap
--accordion-icon-size
--accordion-transition-duration
--accordion-transition-easing
```

---

## 12. Do / Do Not

| Do | Do Not |
|---|---|
| Use `<button>` for the trigger | Use `<div>` or `<a>` as the trigger |
| Set `aria-expanded` on the button | Set `aria-expanded` on the panel |
| Rotate the icon with CSS | Swap DOM icon elements on expand/collapse |
| Use `[disabled]` attribute | Use only `aria-disabled` for functional disable |
| Wrap flush accordion in an `overflow: clip` container | Use flush without a containing boundary |
| Put accordion items in a list wrapper (accordion-list) | Use isolated accordions without a group wrapper |
