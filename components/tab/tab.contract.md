# Tab — Component Contract

```
contract_version: 1.0.0
component_id:     tab
status:           stable
category:         navigation
last_reviewed:    2026-06-09
```

---

## 1. Purpose

**Tab** implements the WAI-ARIA [Tabs design pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/). It provides horizontal and vertical tab navigation for switching between related content panels.

> AI Rule: Use Tab when multiple views share a screen and the user switches between them without navigating away. Use a Sidebar or Nav component for site-level navigation.

---

## 2. When to Use / When NOT to Use

| Situation | Use Tab? |
|---|---|
| Switch between related content sections on the same page | Yes |
| Display/hide associated content panels | Yes |
| Vertical sidebar navigation list (settings pages) | Yes — Vertical Tab List |
| Primary site navigation (Header, Sidebar) | No — use Nav component |
| Multi-step wizard flow | No — use Stepper |
| Filter data in a table | No — use FilterChip or SegmentedControl |

---

## 3. Anatomy

### Horizontal Tab List

```
.tab-list .tab-list--h          ← container <div>, role="tablist"
  .tab .tab--h                  ← tab button <button>, role="tab"
    .tab__icon  [optional]      ← icon wrapper, aria-hidden="true"
    .tab__text                  ← visible label
    ::before                    ← selection indicator (3px bottom bar)
    ::after                     ← focus ring
  ::after                       ← divider bar (3px gray, bottom)
```

### Vertical Tab List

```
.tab-list .tab-list--v          ← container <div>, role="tablist"
  .tab .tab--v                  ← tab button <button>, role="tab"
    .tab__icon  [optional]      ← icon wrapper, aria-hidden="true"
    .tab__text                  ← visible label
    ::before                    ← selection indicator (3px left bar)
    ::after                     ← focus ring
```

### Tab Panel

```
.tab-panel                      ← content panel <div>, role="tabpanel"
```

---

## 4. HTML Contract

### Horizontal Tab List (standard)

```html
<div class="tab-list tab-list--h" role="tablist" aria-label="Section name">
  <button class="tab tab--h" role="tab" aria-selected="true"
          aria-controls="panel-1" id="tab-1" type="button">
    <span class="tab__text">First Tab</span>
  </button>
  <button class="tab tab--h" role="tab" aria-selected="false"
          aria-controls="panel-2" id="tab-2" type="button" tabindex="-1">
    <span class="tab__text">Second Tab</span>
  </button>
</div>

<div class="tab-panel" role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  Panel 1 content
</div>
<div class="tab-panel" role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  Panel 2 content
</div>
```

### Horizontal Tab with leading icon

```html
<button class="tab tab--h" role="tab" aria-selected="true"
        aria-controls="panel-1" id="tab-1" type="button">
  <span class="tab__icon" aria-hidden="true">
    <svg>...</svg>
  </span>
  <span class="tab__text">Tab Label</span>
</button>
```

### Horizontal Tab — Small size

```html
<div class="tab-list tab-list--h" role="tablist" aria-label="Small tabs">
  <button class="tab tab--h tab--sm" role="tab" aria-selected="true"
          aria-controls="sm-panel-1" id="sm-tab-1" type="button">
    <span class="tab__text">First</span>
  </button>
  <!-- ... -->
</div>
```

### Horizontal Tab List — Flush

```html
<div class="tab-list tab-list--h tab-list--flush" role="tablist" aria-label="Flush tabs">
  <button class="tab tab--h" role="tab" aria-selected="true"
          aria-controls="flush-1" id="ftab-1" type="button">
    <span class="tab__text">First</span>
  </button>
</div>
```

### Vertical Tab List

```html
<div class="tab-list tab-list--v" role="tablist"
     aria-label="Settings navigation" aria-orientation="vertical">
  <button class="tab tab--v" role="tab" aria-selected="true"
          aria-controls="v-panel-1" id="v-tab-1" type="button">
    <span class="tab__icon" aria-hidden="true"><svg>...</svg></span>
    <span class="tab__text">General</span>
  </button>
  <button class="tab tab--v" role="tab" aria-selected="false"
          aria-controls="v-panel-2" id="v-tab-2" type="button" tabindex="-1">
    <span class="tab__text">Security</span>
  </button>
</div>
```

### Disabled tab

```html
<!-- aria-disabled keeps the tab in the tab order for screen readers -->
<button class="tab tab--h" role="tab" aria-selected="false"
        aria-controls="panel-x" id="tab-x" type="button"
        tabindex="-1" aria-disabled="true">
  <span class="tab__text">Disabled Tab</span>
</button>
```

---

## 5. Modifier Reference

### Tab button — Orientation modifiers (required)

| Modifier | Description |
|---|---|
| `.tab--h` | Horizontal tab. Selection indicator at bottom. |
| `.tab--v` | Vertical tab. Selection indicator at left edge (RTL: right). |

### Tab button — Size modifiers

| Modifier | Figma size | H-padding | V-padding | Notes |
|---|---|---|---|---|
| `.tab--sm` | Small | 12px (h) / 6px (v) | 8px (h) / 2px (v) | See size differences below |
| _(none)_ | Medium | 16px (h) / 12px (v) | 12px (h) / 6px (v) | Default |
| `.tab--lg` | Large | 16px (h&v) / 12px (v) | 16px (h) / 8px (v) | |

Note: Horizontal and vertical have independent size token sets.

### Vertical tab font differs at Large:

| Size | Font | Weight (idle/selected) |
|---|---|---|
| Small / Medium | 14px / 20px | 400 / 600 |
| Large | 16px / 24px | 400 / 600 |

### Horizontal tab font is constant:

| All sizes | Font | Weight (idle/selected) |
|---|---|---|
| Small / Medium / Large | 14px / 20px | 500 / 700 |

### Tab List — Orientation modifiers (required)

| Modifier | Description |
|---|---|
| `.tab-list--h` | Horizontal row with bottom divider. |
| `.tab-list--v` | Vertical column stack. |

### Tab List — Other modifiers

| Modifier | Description |
|---|---|
| `.tab-list--flush` | Removes horizontal padding from list container. Horizontal only. |
| `.tab--sm` | Apply to tab list to set Small size context (pair with `.tab--sm` on tabs). |
| `.tab--lg` | Apply to tab list to set Large size context (pair with `.tab--lg` on tabs). |

---

## 6. ARIA Requirements

### 6.1 Tab list

```html
<div class="tab-list tab-list--h" role="tablist"
     aria-label="...">   <!-- OR aria-labelledby="heading-id" -->
```

- `role="tablist"` — required.
- `aria-label` or `aria-labelledby` — required. Identifies the tab group to screen readers.
- `aria-orientation="vertical"` — required for vertical tab lists.

### 6.2 Tab button

```html
<button class="tab tab--h" role="tab"
        aria-selected="true|false"
        aria-controls="panel-id"
        id="tab-id"
        tabindex="-1|0">
```

- `role="tab"` — required.
- `aria-selected="true"` — on the currently active tab only. All others: `aria-selected="false"`.
- `aria-controls="panel-id"` — must match the `id` of the associated `role="tabpanel"`.
- `id` — must match `aria-labelledby` on the associated panel.
- `tabindex="-1"` — on all non-selected tabs. Only the selected tab has `tabindex="0"` (or no tabindex). Managed by JavaScript.

### 6.3 Tab panel

```html
<div class="tab-panel" role="tabpanel"
     id="panel-id"
     aria-labelledby="tab-id">
```

- `role="tabpanel"` — required.
- `id` — must match `aria-controls` on the associated tab.
- `aria-labelledby` — must match the `id` of the associated tab.
- `hidden` — use HTML `hidden` attribute on inactive panels (CSS `display: none`).

---

## 7. Keyboard Navigation (JavaScript Required)

The following keyboard behavior must be implemented by the consuming application:

| Key | Horizontal Tab | Vertical Tab |
|---|---|---|
| `Tab` | Focus enters tablist → selected tab focused | Same |
| `ArrowRight` | Move focus to next tab | — |
| `ArrowLeft` | Move focus to previous tab | — |
| `ArrowDown` | — | Move focus to next tab |
| `ArrowUp` | — | Move focus to previous tab |
| `Home` | Focus first tab | Focus first tab |
| `End` | Focus last tab | Focus last tab |
| `Space` / `Enter` | Activate focused tab | Activate focused tab |

**Automatic vs Manual activation:** The platform standard is automatic activation (focusing a tab activates it). Manual activation (requires Enter/Space to activate) is an alternative. Document your choice.

**CSS cannot implement keyboard navigation.** The `tabindex` management and panel switching must be handled by JavaScript.

---

## 8. JavaScript Hook Pattern

```html
<!-- Mark tab group with data attribute for JS targeting -->
<div id="tabs-main" data-tabs>
  <div class="tab-list tab-list--h" role="tablist" aria-label="...">
    ...
  </div>
  <div class="tab-panel" role="tabpanel" ...>...</div>
</div>
```

Minimal JavaScript requirements:
1. Arrow key listener on `role="tablist"`.
2. On focus move: set `tabindex="-1"` on current tab, `tabindex="0"` on new tab, call `.focus()`.
3. On activation: set `aria-selected="true"` on active tab, `aria-selected="false"` on others. Show active panel, hide others.

---

## 9. Prohibited Patterns

```html
<!-- Tab list without aria-label — INVALID -->
<div class="tab-list tab-list--h" role="tablist">...</div>

<!-- Tab without role="tab" — INVALID -->
<button class="tab tab--h" aria-selected="true">...</button>

<!-- Tab without aria-selected — INVALID -->
<button class="tab tab--h" role="tab" aria-controls="p-1" id="t-1">...</button>

<!-- Tab without aria-controls — INVALID -->
<button class="tab tab--h" role="tab" aria-selected="true" id="t-1">...</button>

<!-- Tab using <div> or <a> — INVALID -->
<div class="tab tab--h" role="tab">...</div>

<!-- Panel without role="tabpanel" — INVALID -->
<div id="panel-1" aria-labelledby="tab-1">...</div>

<!-- Panel missing aria-labelledby — INVALID -->
<div class="tab-panel" role="tabpanel" id="panel-1">...</div>

<!-- Multiple tabs with aria-selected="true" — INVALID -->
<button role="tab" aria-selected="true">One</button>
<button role="tab" aria-selected="true">Two</button>

<!-- Combining horizontal and vertical orientation modifiers — INVALID -->
<button class="tab tab--h tab--v">...</button>
```

---

## 10. Content Rules

1. **Tab labels**: Short, distinct labels. 1–3 words. Avoid duplicates within the same tab group.
2. **Arabic support**: `IBM Plex Sans Arabic` via `--tab-font-family`. Set `dir="rtl"` on ancestor.
3. **Language matching**: Tab label language should match document language context.
4. **Icon + text**: Icon is decorative — always include `.tab__text`. Do not use icon-only tabs.

---

## 11. Token Dependencies

- `--space-*` — spacing primitives
- `--radius-sm`, `--radius-full` — radius primitives
- `--fs-text-sm`, `--lh-text-sm`, `--fs-text-md`, `--lh-text-md` — typography
- `--font-weight-body`, `--font-weight-medium`, `--font-weight-semibold`, `--font-weight-heading` — weights
- `--font-sans` — font family
- `--gray-*`, `--sa-600` — color primitives

**Missing primitives** (must be added to token.css):
- `--space-6: 6px` (used for vertical tab sm/md padding)
- `--tab-text-active: #161616` (Figma `--Text-text-default` has no exact token.css match)
- All `--tab-*` component tokens
