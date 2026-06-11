# Pagination Component Contract

Platform Code Design System — Internal component contract.

---

## Anatomy

```
<nav class="pagination pagination--{size}" [dir="rtl"]>
  <button class="pagination__nav pagination__nav--prev">  ← icon  </button>
  <button class="pagination__item">                        N        </button>
  <button class="pagination__item" aria-current="page">   N        </button>

  <!-- Overflow wrapper — positioning context (trigger + panel must be siblings, not parent/child) -->
  <span class="pagination__overflow-wrapper">
    <button class="pagination__item pagination__item--overflow"
            aria-label="More pages" aria-expanded="false" aria-haspopup="listbox">
      ...
    </button>
    <ul class="pagination__overflow-panel" role="listbox" aria-label="Jump to page">
      <li>
        <button class="pagination__overflow-option pagination__overflow-option--selected"
                role="option" aria-selected="true">
          <svg class="pagination__overflow-check">...</svg>  N
        </button>
      </li>
      <li><button class="pagination__overflow-option" role="option">N</button></li>
      ...
    </ul>
  </span>

  <button class="pagination__item">                        N        </button>
  <button class="pagination__nav pagination__nav--next">  → icon  </button>
</nav>
```

---

## Root Element

| Attribute | Required | Value |
|-----------|----------|-------|
| `class="pagination"` | Yes | Root class — always present |
| `class="pagination--{size}"` | Yes | Size modifier — see Sizes |
| `aria-label` | Yes | Accessible name (e.g., "Pagination") |
| `dir="rtl"` | Conditional | Add for right-to-left layouts |

---

## Classes

### Root
| Class | Description |
|-------|-------------|
| `.pagination` | Root container — `display: inline-flex` |
| `.pagination--lg` | Large size (40px items) |
| `.pagination--md` | Medium size (32px items) |
| `.pagination--sm` | Small size (24px items) |

### Navigation Buttons
| Class | Description |
|-------|-------------|
| `.pagination__nav` | Base nav button (prev or next) |
| `.pagination__nav--prev` | Previous page button (left arrow in LTR) |
| `.pagination__nav--next` | Next page button (right arrow in LTR) |

### Page Items
| Class | Description |
|-------|-------------|
| `.pagination__item` | Page number button |
| `.pagination__item--current` | CSS alternative to `aria-current="page"` for non-button contexts |
| `.pagination__item--overflow` | Overflow trigger button — opens page-jump dropdown |

### Overflow Wrapper
| Class | Description |
|-------|-------------|
| `.pagination__overflow-wrapper` | Positioning context for trigger + panel (maps to Figma `_PaginationItem` component root). Required because HTML forbids `<button>` inside `<button>`. |

### Overflow Dropdown Panel
| Class | Description |
|-------|-------------|
| `.pagination__overflow-panel` | Absolutely positioned page-jump list (hidden by default; visible when `aria-expanded="true"` on the trigger) |
| `.pagination__overflow-option` | Individual page number option button inside the panel |
| `.pagination__overflow-option--selected` | Currently selected page option (bold + check icon) |
| `.pagination__overflow-check` | Check SVG icon inside the selected option |

---

## States

### Navigation Buttons
| State | Trigger | Visual Change |
|-------|---------|---------------|
| Default | — | transparent background |
| Hovered | `:hover` | neutral-100 background |
| Pressed | `:active` | neutral-100 background |
| Focused | `:focus-visible` | 2px solid outline (border-black) |
| Disabled | `disabled` attr or `aria-disabled="true"` | 40% opacity, no pointer events |

### Page Items
| State | Trigger | Visual Change |
|-------|---------|---------------|
| Default | — | transparent background, weight 400 |
| Hovered | `:hover` | neutral-100 background |
| Pressed | `:active` | neutral-100 background |
| Focused | `:focus-visible` | 2px solid outline (border-black) |
| Current Page | `aria-current="page"` or `.pagination__item--current` | weight 600 + 3px green bottom bar (`::after`) |
| Disabled | `disabled` attr or `aria-disabled="true"` | 40% opacity, no pointer events |
| Overflow (closed) | `.pagination__item--overflow` | 1px solid border, interactive (cursor: pointer) |
| Overflow (open) | `[aria-expanded="true"]` | 2px solid border + neutral-100 bg, panel visible |

---

## Sizes

| Modifier | Item Size | Nav Size | Padding | Font Size |
|----------|-----------|----------|---------|-----------|
| `.pagination--lg` | 40×40px (min-width) | 40×40px | 8px | 16px |
| `.pagination--md` | 32×32px (fixed) | 32×32px | 6px | 16px |
| `.pagination--sm` | 24px height (min-width) | 24×24px | 4px | 14px |

---

## RTL

Apply `dir="rtl"` directly on the `<nav class="pagination">` element.

Behavior:
- Flexbox item order visually reverses (browser-native).
- Arrow SVG icons flip horizontally via `transform: scaleX(-1)`.
- No separate RTL markup required.

Semantics in RTL:
- `.pagination__nav--prev` = "previous page" → arrow points right (→) visually.
- `.pagination__nav--next` = "next page" → arrow points left (←) visually.

---

## Accessibility Contract

| Requirement | Implementation |
|-------------|----------------|
| Landmark | `<nav aria-label="Pagination">` |
| Current page | `aria-current="page"` on the active item button |
| Nav button names | `aria-label="Previous page"` / `aria-label="Next page"` |
| Page number names | `aria-label="Page N"` on each item button |
| Overflow trigger | `aria-label="More pages"`, `aria-expanded`, `aria-haspopup="listbox"` on overflow button |
| Overflow panel | `role="listbox"` + `aria-label="Jump to page"` on the `<ul>` |
| Overflow options | `role="option"` on each `<button>`; `aria-selected="true"` on the selected page |
| Disabled nav buttons | `aria-disabled="true"` or `disabled` attribute |
| Focus visibility | `:focus-visible` 2px solid outline — never suppressed |
| Color not sole indicator | Current page uses font-weight change + bottom bar |

---

## Token Interface

All component tokens below must be defined in `token.css` before production use.
See `analysis.md` — Missing Tokens for mapping details.

```css
--pagination-items-gap
--pagination-item-lg-padding
--pagination-item-md-padding
--pagination-item-sm-padding
--pagination-item-lg-size
--pagination-item-md-size
--pagination-item-sm-size
--pagination-nav-lg-size
--pagination-nav-md-size
--pagination-nav-sm-size
--pagination-item-radius
--pagination-item-text-color
--pagination-item-hover-bg
--pagination-item-pressed-bg
--pagination-item-focus-border-color
--pagination-item-focus-border-width
--pagination-item-current-indicator-bg
--pagination-item-current-indicator-radius
--pagination-item-overflow-border-color
--pagination-item-disabled-text
--pagination-font-family
--pagination-item-lg-font-size
--pagination-item-md-font-size
--pagination-item-sm-font-size
--pagination-item-lg-line-height
--pagination-item-md-line-height
--pagination-item-sm-line-height
--pagination-item-overflow-open-bg
--pagination-overflow-panel-z-index
--pagination-overflow-panel-padding
--pagination-overflow-panel-border-color
--pagination-overflow-panel-bg
--pagination-overflow-panel-shadow
--pagination-overflow-option-width
--pagination-overflow-option-padding
--pagination-overflow-option-gap
--pagination-overflow-option-font-size
--pagination-overflow-option-line-height
```

---

## Dependencies

| Dependency | Required | Notes |
|------------|----------|-------|
| `token.css` | Yes | Global design tokens (CSS variables) |
| `pagination.css` | Yes | This component |
| `button.css` | Optional | Provides full interactive states for nav buttons |

---

## Assembly Notes

Pagination participates in:
- `form` assemblies (e.g., paginated search results, data tables)
- Standalone page-navigation contexts

Navigation buttons (`pagination__nav`) are thin wrappers over the Button component's transparent icon-only variant. If Button component CSS is loaded, nav button hover/focus states will be augmented.

---

## Known Deviations from Figma

See `analysis.md` — Intentional Deviations From Figma for full list.

Summary:
1. Medium current-indicator `bottom` corrected from `2.5px` to `0`.
2. Medium current-indicator `left` corrected from `4px` to `var(--pagination-item-md-padding, 6px)`.
3. Focus state implemented as CSS `outline` (not `border`) to avoid layout shift.
4. Figma typo "Focsed" corrected to `focused`.
5. Figma typo "Meduim" corrected to `medium`.
