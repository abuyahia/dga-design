# Content Switcher — Component Contract

**Name:** Content Switcher
**BEM Root:** `content-switcher`
**Source:** `components/content-switcher/mainifest.json`
**Type:** Composite interactive component — segmented control / tablist

---

## Anatomy

| Element | Selector | ARIA Role | Notes |
|---------|----------|-----------|-------|
| Container | `.content-switcher` | `tablist` | Wraps all items |
| Item | `.content-switcher__item` | `tab` | Interactive button |
| Label | Text node inside item | — | Plain text content |

---

## HTML Contract

### Container

```
<div class="content-switcher content-switcher--{size}" role="tablist" aria-label="...">
```

Required:
- `role="tablist"`
- `aria-label` OR `aria-labelledby` pointing to a visible label element
- Exactly one size modifier: `content-switcher--sm`, `content-switcher--md`, `content-switcher--lg`

Optional:
- `content-switcher--on-color` for the OnColor=True color scheme
- `dir="rtl"` for right-to-left layout (no extra CSS class required)

### Item

```
<button class="content-switcher__item" role="tab" aria-selected="true|false"
        aria-controls="{panelId}" id="{tabId}" tabindex="0|-1" type="button">
  Label
</button>
```

Required:
- `role="tab"`
- `aria-selected="true"` on the active item; `aria-selected="false"` on all others
- `tabindex="0"` on the active item; `tabindex="-1"` on all inactive items (roving tabindex)
- `type="button"` to prevent form submission

Recommended:
- `aria-controls="{panelId}"` — id of the associated `role="tabpanel"` element
- `id="{tabId}"` — used by panel's `aria-labelledby`

Prohibited:
- Do NOT use `<div>` or `<span>` as the item element when keyboard interaction is required
- Do NOT use a `.selected` class — selection is driven exclusively by `aria-selected`
- Do NOT add `disabled` attribute — use `aria-disabled="true"` if needed

---

## Modifier Classes

| Class | Axis | Values |
|-------|------|--------|
| `content-switcher--sm` | Size | Small: height 32px, padding-x 8px, font 16px |
| `content-switcher--md` | Size | Medium: height 40px, padding-x 12px, font 18px |
| `content-switcher--lg` | Size | Large: height 48px, padding-x 16px, font 20px |
| `content-switcher--on-color` | OnColor | Green selected on transparent unselected |

Exactly one size modifier is required. OnColor is optional.

---

## CSS States

| State | Selector | Description |
|-------|----------|-------------|
| Default (unselected) | `.content-switcher__item` | Neutral bg, default text, inline borders |
| Hovered (unselected) | `.content-switcher__item:not([aria-selected="true"]):hover` | Hover bg token (token-dependent delta) |
| Selected | `.content-switcher__item[aria-selected="true"]` | Dark/primary bg, on-color text, no borders |
| Focused | `.content-switcher__item:focus-visible` | Outer dark outline + inner white `::after` ring |
| Disabled | `.content-switcher__item[aria-disabled="true"]` | Opacity 0.38, no pointer events |

---

## Item Position Rules

| Position | Selector | Border Radius | Border Behavior |
|----------|----------|---------------|-----------------|
| First | `:first-child` | Left cap (start-start + end-start) | No inline-start border |
| Middle | `:not(:first-child):not(:last-child)` | None | Both inline borders |
| Last | `:last-child` | Right cap (start-end + end-end) | No inline-end border |
| Any selected | `[aria-selected="true"]` | Inherited | No inline borders |

---

## RTL Support

RTL layout is handled by adding `dir="rtl"` on the container or any ancestor element. No additional modifier class is required. CSS logical properties (`border-inline-start`, `border-start-start-radius`, `padding-inline`, etc.) ensure correct directional behavior automatically.

---

## Focus Ring Implementation

The focus ring is sourced from `mainifest-items.json` (`Focus outline` layer in the Focused state):

1. **Outer ring:** `outline: 2px solid var(--content-switcher-focus-ring)` on `:focus-visible`
2. **Inner ring:** `::after` pseudo-element — `position: absolute; inset: 2px; border: 1px solid var(--content-switcher-focus-ring-inner)`
3. **Focus strategy:** `:focus-visible` only (keyboard-initiated focus)

---

## ARIA / Keyboard Pattern

This component implements the [ARIA Tabs Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/).

- Container: `role="tablist"`
- Items: `role="tab"` with `aria-selected`
- Panels: `role="tabpanel"` with `aria-labelledby` referencing the tab `id` (rendered separately)
- **Keyboard:**
  - `ArrowLeft` / `ArrowRight` — move focus between tabs (roving tabindex)
  - `Home` — focus first tab
  - `End` — focus last tab
  - `Tab` — exit the tablist
  - `Enter` / `Space` — activate focused tab (if not automatically activated on focus)

JavaScript is required for keyboard interaction and panel switching.

---

## Token Dependencies

All `--content-switcher-*` tokens are currently undefined in `token.css`. The CSS uses the proposed token names. Fallback primitives are documented in `analysis.md`.

Key tokens:
- `--content-switcher-item-bg-default` → neutral background
- `--content-switcher-item-bg-selected` → dark selected background
- `--content-switcher-item-bg-selected-oncolor` → green selected background (OnColor)
- `--content-switcher-item-border` → neutral divider border
- `--content-switcher-focus-ring` → outer focus ring color (dark)
- `--content-switcher-focus-ring-inner` → inner focus ring color (white)
- `--content-switcher-radius` → item cap border radius

See `analysis.md` — Missing Tokens for the complete list.

---

## Assembly Participation

This component participates as a standalone control. It may appear inside:
- Page headers
- Filter bars
- Dashboard controls
- Form field groups

It does not require a parent component to function but does require JavaScript for interactivity.
