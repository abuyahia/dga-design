# Card — Component Contract

```
contract_version: 1.0.1
component_id:     card
status:           stable
category:         content
last_reviewed:    2026-09-13
```

---

## 1. Component Type

**Composite**

The Card owns its surface, layout, slots, and interactive states. Button and Checkbox are composed as independent child components and maintain their own contracts.

---

## 2. Purpose

A Card groups related content into a visually contained, bordered surface. Media/icon, title/body wrappers and actions are optional composition slots. Three behavioral variants exist:

- **Default** — Static content container with optional actions
- **Expandable** — Interactive container with a toggle to reveal additional content
- **Selectable** — Interactive container with a checkbox for selection

---

## 3. When to Use / When NOT to Use

| Situation | Use Card? |
|---|---|
| Display related information as a unit | Yes |
| Allow user to expand/collapse additional content | Yes — use Expandable type |
| Allow user to select from a set of items | Yes — use Selectable type |
| Display navigation links | No — use Link or Navigation patterns |
| Display tabular data | No — use Table |
| Display a single action with no content context | No — use Button |

---

## 4. Anatomy

```
.card                           ← required root surface
  [media/icon component]        ← optional consumer-owned slot, such as Avatar
  .card__content                ← optional title + body column
    .card__title                ← heading (p or h2–h6 per context)
    .card__body                 ← body text (p)
  .card__actions                ← action area (varies by Type)
  .card__expandable-content     ← hidden slot (Expandable type only)
  .card__checkbox-wrapper       ← checkbox slot (Selectable type only)
```

### Slot Rules

| Slot | Type | Required | Notes |
|---|---|---|---|
| Media/icon component | All | No | Optional. Avatar is one valid choice; Card sets no styles on child-component internals. |
| `.card__content` | All | No | Groups title/body when that structure is used. |
| `.card__title` | All | No | Use an appropriate heading level when the Card owns a titled content block. |
| `.card__body` | All | No | Optional body text |
| `.card__actions` | All | No | Optional action area; Expandable uses it when the toggle is present. |
| `.card__expandable-content` | Expandable | Yes | Hidden by default; shown when expanded |
| `.card__checkbox-wrapper` | Selectable | Yes | Contains Checkbox component |

---

## 5. Dependencies

Required: None

Optional:
- **Avatar** (`avatar--40`, icon type) — one optional media/icon-slot choice
- **Button** (`btn--secondary-outline`) — Default type secondary action
- **Button** (`btn--primary`) — Default type primary action
- **Checkbox** — Selectable type selection control

Card-owned (not reusable):
- `.card__toggle` — minimal icon-only toggle for Expandable type

---

## 6. HTML Contract

### Default Card
```html
<div class="card" role="group" aria-labelledby="card-title-1">
  <div class="card__content">
    <p class="card__title" id="card-title-1">Card Title</p>
    <p class="card__body">Card content placeholder text goes here.</p>
  </div>
  <div class="card__actions">
    <button class="btn btn--secondary-outline" type="button">
      <span class="btn__text">Action</span>
    </button>
    <button class="btn btn--primary" type="button">
      <span class="btn__text">Action</span>
    </button>
  </div>
</div>
```

The reference `template.html` demonstrates an Avatar-equipped Card. Avatar is
optional: current Services, Contact CTA, Contact, and Service Detail compositions
also use the Card surface without it. A plain `.card` may rely on its surrounding
`section`/`aside` semantics; add `role="group"` and an accessible name only when
the Card itself needs to expose a named group.

### Expandable Card — Collapsed
```html
<div class="card card--expandable" role="group" aria-labelledby="card-title-2">
  <div class="avatar avatar--40" role="img" aria-label="User">
    <span class="avatar__icon" aria-hidden="true">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M12 12C14.761 12 17 9.761 17 7C17 4.239 14.761 2 12 2C9.239 2 7 4.239 7 7C7 9.761 9.239 12 12 12Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
        <path d="M20.59 22C20.59 18.13 16.74 15 12 15C7.26 15 3.41 18.13 3.41 22" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
      </svg>
    </span>
  </div>
  <div class="card__content">
    <p class="card__title" id="card-title-2">Card Title</p>
    <p class="card__body">Card content placeholder text goes here.</p>
  </div>
  <div class="card__actions">
    <button class="card__toggle"
            type="button"
            aria-expanded="false"
            aria-controls="card-expandable-2"
            aria-label="Expand card">
      <svg class="card__toggle-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>
  <div class="card__expandable-content" id="card-expandable-2" hidden>
    <!-- additional content -->
  </div>
</div>
```

### Expandable Card — Expanded
```html
<div class="card card--expandable card--expanded" role="group" aria-labelledby="card-title-2">
  <!-- ... same structure ... -->
  <div class="card__actions">
    <button class="card__toggle"
            type="button"
            aria-expanded="true"
            aria-controls="card-expandable-2"
            aria-label="Collapse card">
      <svg class="card__toggle-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>
  <div class="card__expandable-content" id="card-expandable-2">
    <p>Additional content revealed on expand.</p>
  </div>
</div>
```

### Selectable Card — Unselected
```html
<div class="card card--selectable" role="group" aria-labelledby="card-title-3">
  <div class="avatar avatar--40" role="img" aria-label="User">
    <span class="avatar__icon" aria-hidden="true">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M12 12C14.761 12 17 9.761 17 7C17 4.239 14.761 2 12 2C9.239 2 7 4.239 7 7C7 9.761 9.239 12 12 12Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
        <path d="M20.59 22C20.59 18.13 16.74 15 12 15C7.26 15 3.41 18.13 3.41 22" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
      </svg>
    </span>
  </div>
  <div class="card__content">
    <p class="card__title" id="card-title-3">Card Title</p>
    <p class="card__body">Card content placeholder text goes here.</p>
  </div>
  <div class="card__checkbox-wrapper">
    <!-- Checkbox component -->
    <input type="checkbox" id="card-check-3" class="checkbox__input">
    <label for="card-check-3" class="sr-only">Select this card</label>
  </div>
</div>
```

### Selectable Card — Selected
```html
<div class="card card--selectable card--selected" role="group" aria-labelledby="card-title-3">
  <!-- ... same structure ... -->
  <div class="card__checkbox-wrapper">
    <input type="checkbox" id="card-check-3" class="checkbox__input" checked>
    <label for="card-check-3" class="sr-only">Select this card</label>
  </div>
</div>
```

### Disabled Expandable Card
```html
<div class="card card--expandable card--disabled" aria-disabled="true" role="group" aria-labelledby="card-title-4">
  <!-- content — same structure, interactive children should also carry disabled -->
  <div class="card__actions">
    <button class="card__toggle" type="button" disabled aria-disabled="true">
      <!-- toggle icon -->
    </button>
  </div>
</div>
```

---

## 7. CSS Class Contract

| Class | Purpose | Required |
|---|---|---|
| `.card` | Base card styles | Yes |
| `.card--expandable` | Expandable type modifier | Only for Expandable type |
| `.card--selectable` | Selectable type modifier | Only for Selectable type |
| `.card--expanded` | Expanded state modifier | Only when Expandable card is expanded |
| `.card--selected` | Selected state modifier | Only when Selectable card is selected |
| `.card--disabled` | Disabled state modifier | When card is disabled (alternative to `aria-disabled`) |
| `.card__content` | Optional title + body wrapper | No |
| `.card__title` | Optional heading text | No |
| `.card__body` | Body text | No |
| `.card__actions` | Action area | Conditional |
| `.card__toggle` | Expand/collapse button | Expandable type only |
| `.card__toggle-icon` | SVG inside toggle | Expandable type only |
| `.card__expandable-content` | Hidden content slot | Expandable type only |
| `.card__checkbox-wrapper` | Checkbox slot wrapper | Selectable type only |
| `.is-hover` | Showcase-only hover state | **Never in production** |
| `.is-focused` | Showcase-only focused state | **Never in production** |

---

## 8. State Management

| State | How to apply |
|---|---|
| Default | Base styles only |
| Hover | CSS `:hover` on `.card--expandable` and `.card--selectable` — handled by stylesheet |
| Focused | CSS `:focus-within` — handled by stylesheet when child element receives focus |
| Disabled | `aria-disabled="true"` on `.card` root + `.card--disabled` class |
| Expanded | Add `.card--expanded` to root + set `aria-expanded="true"` on `.card__toggle` + remove `hidden` from `.card__expandable-content` |
| Selected | Add `.card--selected` to root + check the checkbox inside `.card__checkbox-wrapper` |

**Note:** The `.is-hover` and `.is-focused` CSS classes are **showcase-only** — do not use in production HTML.

---

## 9. Accessibility Contract

| Requirement | Rule |
|---|---|
| Card grouping | When the Card itself needs named-group semantics, use `role="group"` with an accessible name such as `aria-labelledby` pointing to its heading. Do not add a redundant group role when a surrounding semantic element already supplies the relationship. |
| Icon decoration | Icon SVG must carry `aria-hidden="true"`. `.card__icon-wrapper` may also carry `aria-hidden="true"`. |
| Expandable — toggle accessible name | `.card__toggle` must have `aria-label` (e.g., "Expand card" / "Collapse card") |
| Expandable — toggle state | `.card__toggle` must carry `aria-expanded="true"` or `"false"` |
| Expandable — panel connection | `.card__toggle` must carry `aria-controls` pointing to `.card__expandable-content` id |
| Selectable — checkbox label | Checkbox inside `.card__checkbox-wrapper` must have an accessible label |
| Disabled — card | `aria-disabled="true"` on the card root communicates the disabled state |
| Disabled — children | Interactive child elements (toggle, checkbox) should also carry `disabled` or `aria-disabled="true"` |
| Heading level | `.card__title` element choice (p, h2–h6) must respect the document heading outline |

---

## 10. RTL Behavior

The card layout responds automatically to `dir="rtl"` on any ancestor element.

- `flex-direction: column` is direction-neutral
- Text inside `.card__title` and `.card__body` inherits document text direction
- No additional class or attribute is needed on the card itself

---

## 11. Content Rules

**Card title:**
- Maximum 60 characters recommended (longer titles may wrap to 3+ lines)
- Use appropriate heading level for document outline context

**Card body:**
- Optional; omit if no supporting text is needed
- Recommended 1–3 sentences

**Media/icon:**
- Optional and owned by the composed child component or consumer-specific slot
- Decorative SVG/images must carry `aria-hidden="true"` or an empty `alt`
- Card does not impose Avatar or a fixed icon class on every composition

**Forbidden:**
- No interactive elements nested inside `.card__title` or `.card__body`
- No `<button>` or `<a>` directly inside `.card__actions` unless they are Button component instances or `.card__toggle`

---

## 12. Token Surface (Compliance Anchor)

These are the tokens this component reads. Define them in `token.css` to enable theming:

```
--card-width                 --card-padding               --card-gap
--card-radius                --card-border-default        --card-bg-default
--card-bg-hover              --card-border-focused        --card-bg-disabled
--card-border-disabled       --card-text-default          --card-text-disabled
--card-content-gap           --card-actions-gap
--card-font-family           --card-title-font-size       --card-title-line-height
--card-body-font-size        --card-body-line-height
--card-toggle-radius         --card-toggle-icon-color     --card-toggle-transition-duration
```

All listed tokens are registered in `token.css` and consumed by `card.css`.
Their mapped values use the established spacing, color, radius, typography and
motion primitives. `production_ready` and historical audit statuses remain
unchanged by this documentation correction.

---

## 13. Compliance Mapping

| Standard | Criterion | Status |
|---|---|---|
| WCAG 2.1 AA | 1.1.1 Non-text Content | mapped |
| WCAG 2.1 AA | 1.4.3 Contrast (Minimum) | mapped |
| WCAG 2.1 AA | 2.1.1 Keyboard | mapped |
| WCAG 2.1 AA | 2.4.7 Focus Visible | mapped |
| WCAG 2.1 AA | 4.1.2 Name, Role, Value | mapped |
| PLATFORM-CODE-DS | PLATFORM-CODE-CARD-001 (tokens) | mapped |
| PLATFORM-CODE-DS | PLATFORM-CODE-CARD-002 (RTL) | mapped |
| PLATFORM-CODE-DS | PLATFORM-CODE-CARD-003 (semantic HTML) | mapped |
| PLATFORM-CODE-A11Y | PLATFORM-CODE-A11Y-001 (Arabic font) | mapped |

`PLATFORM-CODE-CARD-*` identifiers are internal mapping IDs. They are not official government or external standards.

---

## 14. Audit Readiness

**Automated rules defined:** 8 rules in `audit-rules.json`

**Run context:**
- Static analysis: CARD-TOKEN-001, CARD-RTL-001
- DOM inspection: CARD-A11Y-001, CARD-A11Y-002, CARD-A11Y-003, CARD-A11Y-004, CARD-A11Y-005, CARD-STRUCT-001

**Current validation_status:** `not_run` on all rules.

---

## 15. AI Usage Notes

**Choosing type:**
- Default to Default type for informational content with two actions
- Use Expandable when content overflow needs progressive disclosure
- Use Selectable when the user needs to pick from multiple cards

**Generating accessible HTML:**
- Add `role="group"` and an accessible name when the Card itself needs named-group semantics
- Treat Avatar/media/icon content as optional; hide decorative graphics from assistive technology
- For Expandable: always add `aria-expanded`, `aria-controls`, and `aria-label` to `.card__toggle`
- For Selectable: always provide an accessible label on the checkbox
- For Disabled: always add `aria-disabled="true"` to the card root

**Forbidden patterns:**
- Do not use `.is-hover` or `.is-focused` outside the showcase
- Do not nest a Button component inside `.card__toggle` — it is card-owned
- Do not add `tabindex` to the card root — it is not an interactive element

---

## 16. Known Limitations

| Limitation | Impact | Workaround |
|---|---|---|
| Component audit rules remain historically `not_run` | The registered token surface is documented but full Card qualification is not claimed | Run the dedicated Card qualification work before changing audit or production-ready status |
| Selectable card click-to-select requires custom JS | Card body clicks do not toggle checkbox automatically | Wire click handler: card click → checkbox toggle |
| Default type has no hover/focus states | Static card cannot communicate hover context | Expected behavior per Figma — Default type is not interactive |
| Fixed width 360px may not suit all layouts | Card does not fill container by default | Override `--card-width` or set `width: 100%` on `.card` |
