# Button — Component Contract

```
contract_version: 1.0.0
component_id:     button
status:           stable
category:         action
last_reviewed:    2026-06-05
```

---

## 1. Purpose

A Button triggers an **action** — submit a form, open a dialog, execute a command.

It is NOT a navigation element. Use `<a>` (or the Link component) when the user navigates to another page or URL. Use `<button>` when the click causes something to happen on the current page.

> AI Rule: If the intent is "go to X", render a Link. If the intent is "do X", render a Button.

---

## 2. When to Use / When NOT to Use

| Situation | Use Button? |
|---|---|
| Submit a form | Yes |
| Open a modal or dialog | Yes |
| Toggle a panel (accordion, tab) | Yes — with `aria-expanded` |
| Toggle a persistent state (bookmark, like) | Yes — with `aria-pressed` |
| Navigate to another page | No — use Link |
| Navigate within a page (anchor) | No — use Link |
| Represent a destructive action (delete, cancel) | Yes — prefer `neutral` or `secondary-outline` shape |

---

## 3. Anatomy

```
.btn                          ← root element (button or a)
  .btn__icon  [optional]      ← SVG icon wrapper, aria-hidden="true"
  .btn__text                  ← visible label text (always present, even if visually hidden)
```

**Slot rules:**

| Slot | Required | Notes |
|---|---|---|
| `.btn__text` | Always | Even in icon-only mode: add text + `.sr-only` class, or use `aria-label` on root |
| `.btn__icon` | Optional | Decorative when text is also visible — wrap SVG, set `aria-hidden="true"` |

---

## 4. HTML Contract

### Standard button (text only)
```html
<button class="btn btn--primary" type="button">
  <span class="btn__text">Submit Application</span>
</button>
```

### Button with leading icon
```html
<button class="btn btn--primary" type="button">
  <span class="btn__icon" aria-hidden="true">
    <svg>...</svg>
  </span>
  <span class="btn__text">Save</span>
</button>
```

### Icon-only button
```html
<button class="btn btn--primary btn--icon-only" type="button" aria-label="Delete record">
  <span class="btn__icon" aria-hidden="true">
    <svg>...</svg>
  </span>
</button>
```

### Small size
```html
<button class="btn btn--primary btn--sm" type="button">
  <span class="btn__text">Filter</span>
</button>
```

### Disabled button
```html
<button class="btn btn--primary" type="button" disabled aria-disabled="true">
  <span class="btn__text">Submit</span>
</button>
```

### Toggle button (persistent state)
```html
<button class="btn btn--secondary-solid" type="button" aria-pressed="false">
  <span class="btn__text">Bookmark</span>
</button>
```

### Link that looks like a button (navigation)
```html
<a class="btn btn--primary" href="/apply" role="button">
  <span class="btn__text">Start Application</span>
</a>
```

---

## 5. Variant Selection Guide

All shapes are interchangeable at the CSS level. Choose based on **visual hierarchy and context**:

| Shape | Use when |
|---|---|
| `primary` | The single most important action on the page or section. Use once per visual group. |
| `primary-on-color` | Same as primary, but placed on a colored/dark background (hero, banner). |
| `neutral` | High-emphasis action in dark/brand contexts. Equivalent weight to primary. |
| `neutral-on-color` | Neutral on colored backgrounds. |
| `secondary-solid` | Secondary action alongside a primary. Lower visual weight. |
| `secondary-solid-on-color` | Secondary action on colored backgrounds. |
| `secondary-outline` | Alternative secondary with visible border. Use when background is white/light. |
| `secondary-outline-on-color` | Outline secondary on colored backgrounds. |
| `subtle` | Tertiary action — least prominent, no background. Use for cancel, dismiss. |
| `subtle-on-color` | Subtle on colored backgrounds. |
| `transparent` | Ghost button — no background, no border. Use sparingly inside tight layouts. |
| `transparent-on-color` | Ghost on colored backgrounds. |

**Hierarchy rule:** A page section should have at most one `primary`, one `secondary-*`, and optionally one `subtle`/`transparent`. Never render two `primary` buttons side by side.

---

## 6. Size Guide

| Size | CSS Modifier | Min touch target | Use when |
|---|---|---|---|
| `large` | (default, no modifier) | 40×40px | Default for all page-level actions |
| `medium` | `.btn--md` | 32×32px | Compact toolbars, inline actions, table rows |
| `small` | `.btn--sm` | 24×24px | Dense UI, tags, chips — avoid for primary actions |

---

## 7. Content Rules

**Label text:**
- Minimum 2 characters
- Maximum 40 characters (longer text wraps unpredictably and breaks fixed height)
- Use **sentence case**: "Submit application" not "Submit Application" or "SUBMIT"
- Arabic labels: right-to-left, font inherits IBM Plex Sans Arabic via token

**Icon:**
- Icon-only buttons MUST carry an `aria-label` on the root element
- Icon + text: icon is decorative, set `aria-hidden="true"` on `.btn__icon`
- Icon size is controlled by tokens — do not hardcode width/height in HTML

**Forbidden content inside button:**
- No `<a>` tags
- No `<button>` tags
- No `<input>` elements
- No headings (`<h1>`–`<h6>`)

---

## 8. CSS Class Contract

| Class | Purpose | Required |
|---|---|---|
| `.btn` | Base styles — always present | Yes |
| `.btn--[shape]` | Shape modifier (e.g., `.btn--primary`) | Yes |
| `.btn--sm` | Small size | No |
| `.btn--md` | Medium size | No |
| `.btn--icon-only` | Icon-only layout (square, no text) | Only for icon-only |
| `.btn__icon` | Icon wrapper | Only when icon present |
| `.btn__text` | Text wrapper | Yes |

---

## 9. State Management

| State | How to apply |
|---|---|
| `hovered` | CSS `:hover` — handled by stylesheet |
| `focused` | CSS `:focus-visible` — handled by stylesheet. Never remove outline. |
| `pressed` | CSS `:active` — handled by stylesheet |
| `disabled` | `disabled` attribute on `<button>` + `aria-disabled="true"` |
| `selected` (toggle) | `aria-pressed="true"` on root |
| `expanded` (trigger) | `aria-expanded="true"` on root + `aria-controls="[panel-id]"` |

The `is-focused` and `is-pressed` CSS classes are **showcase-only** — do not use in production HTML.

---

## 10. Accessibility Contract

| Requirement | Rule |
|---|---|
| Accessible name | Every button must have a non-empty accessible name: visible text, `aria-label`, or `aria-labelledby` |
| Role | Use `<button>` element (implicit `role="button"`). If using `<div>`, add `role="button"` and `tabindex="0"`. |
| Keyboard | Must be operable with `Enter` and `Space` keys |
| Focus visible | Focus ring must be visible — do not suppress `:focus-visible` styles |
| Disabled state | Use `disabled` attribute or `aria-disabled="true"`. When `aria-disabled`, keep in tab order. |
| Toggle state | `aria-pressed="true/false"` for toggle buttons |
| Loading state | Use `aria-busy="true"` and update `aria-label` to include "loading" |
| Icon-only | Must have `aria-label` describing the action |

---

## 11. RTL Behavior

The button layout mirrors automatically when `dir="rtl"` is set on a parent element.

- Icon order reverses (trailing icon becomes leading)
- Text alignment inherits from document direction
- Padding and gap are direction-neutral (use `padding-inline`, `gap`)
- No additional class or attribute needed on the button itself

---

## 12. Composition Patterns

**Button group (horizontal):**
```html
<div role="group" aria-label="Actions">
  <button class="btn btn--primary" type="button"><span class="btn__text">Save</span></button>
  <button class="btn btn--secondary-outline" type="button"><span class="btn__text">Cancel</span></button>
</div>
```

**Full-width button (form footer):**
```html
<button class="btn btn--primary" type="submit" style="width: 100%;">
  <span class="btn__text">Submit Application</span>
</button>
```

---

## 13. Forbidden Patterns

The following are invalid and will fail audit:

```html
<!-- WRONG: div as button without role -->
<div class="btn btn--primary" onclick="submit()">Submit</div>

<!-- WRONG: no accessible label -->
<button class="btn btn--primary btn--icon-only"><span class="btn__icon"><svg/></span></button>

<!-- WRONG: hardcoded color bypassing token -->
<button class="btn" style="background: #1B8354;">Submit</button>

<!-- WRONG: two primary buttons side by side -->
<button class="btn btn--primary">Save</button>
<button class="btn btn--primary">Publish</button>

<!-- WRONG: button inside button -->
<button class="btn btn--primary">
  <button class="btn btn--sm">Inner</button>
</button>
```

---

## 14. Token Surface (Compliance Anchor)

These are the tokens this component reads. Any override must go through these tokens — never hardcode values:

```
--button-lg-height           --button-md-height           --button-sm-height
--button-lg-padding-inline   --button-md-padding-inline   --button-sm-padding-inline
--button-radius
--button-label-font-family   --button-label-font-size     --button-label-font-weight
--button-focus-border-width  --button-focus-ring-outer-color  --button-focus-ring-inner-color
--button-primary-bg-default  --button-primary-bg-hover    --button-primary-bg-pressed
--button-primary-text        --button-disabled-bg         --button-disabled-text
```

Compliance checks verify that rendered CSS references these tokens, not raw hex values.

---

## 15. Compliance Mapping

This component is mapped to the following standards. Status `mapped` means the component has been reviewed against the criterion — it does not mean a formal audit has been run.

| Standard | Criterion | Status |
|---|---|---|
| WCAG 2.1 AA | 1.1.1 Non-text Content | mapped |
| WCAG 2.1 AA | 1.4.3 Contrast (Minimum) | mapped |
| WCAG 2.1 AA | 1.4.11 Non-text Contrast | mapped (conditional — see secondary-outline) |
| WCAG 2.1 AA | 2.1.1 Keyboard | mapped |
| WCAG 2.1 AA | 2.4.7 Focus Visible | mapped |
| WCAG 2.1 AA | 4.1.2 Name, Role, Value | mapped |
| PLATFORM-CODE-DS | PLATFORM-CODE-BTN-001 (tokens) | mapped |
| PLATFORM-CODE-DS | PLATFORM-CODE-BTN-002 (RTL) | mapped |
| PLATFORM-CODE-DS | PLATFORM-CODE-BTN-003 (hierarchy) | mapped |
| PLATFORM-CODE-DS | PLATFORM-CODE-BTN-004 (semantic HTML) | mapped |
| PLATFORM-CODE-DS | PLATFORM-CODE-BTN-005 (touch target) | mapped |
| PLATFORM-CODE-A11Y | PLATFORM-CODE-A11Y-001 (Arabic font) | mapped |
| PLATFORM-CODE-A11Y | PLATFORM-CODE-A11Y-002 (label language) | mapped — manual review required |

Full standard definitions: `standards/platform-code.standards.json`, `standards/accessibility.standards.json`.

**Important:** `PLATFORM-CODE-*` identifiers are internal mapping IDs. They are not official government or external standards. They will be updated when the real Platform Code standards document is released.

---

## 16. Audit Readiness

**Automated rules defined:** 11 rules in `audit-rules.json`
**Run context:**
- Static analysis (CSS source): BTN-TOKEN-001, BTN-STRUCT-001, BTN-STRUCT-002, BTN-RTL-001, BTN-A11Y-004
- DOM inspection (rendered HTML): BTN-A11Y-001, BTN-A11Y-002, BTN-A11Y-003, BTN-A11Y-005, BTN-USAGE-001, BTN-CONTENT-001
- Manual review required: PLATFORM-CODE-A11Y-002 (label language match)

**Current validation_status:** `not_run` on all rules. No audit has been executed yet.

**To run an audit:**
1. Execute static analysis rules against `button.css` and `token.css`
2. Render a showcase page and run DOM inspection rules against the output
3. Update each rule's `validation_status` in `audit-rules.json`
4. If all error-severity rules pass: update `overall_status` in `compliance.json` to `"audited_pass"`

**Known gap:** No automated rule covers WCAG 1.4.3 (contrast ratio) or 1.4.11 (non-text contrast). These require a dedicated color-contrast checker against the token values. Planned for audit engine v2.

---

## 17. AI Usage Notes

These notes guide AI assistants generating HTML that includes this component.

**Choosing shape:**
- Default to `btn--primary` for the main CTA on a page or section
- Default to `btn--secondary-outline` for cancel or secondary actions
- Default to `btn--subtle` for dismiss or low-importance tertiary actions
- Use `btn--neutral` only in brand-dark or colored-header contexts
- Use `*-on-color` variants only when the button sits on a colored background

**Choosing size:**
- Default to large (no modifier) unless the layout is explicitly compact
- Use `btn--md` inside toolbars, table rows, or sidebars
- Use `btn--sm` only for tags, chips, or highly dense data views — never as a primary action

**Generating accessible HTML:**
- Always wrap label text in `.btn__text`
- Always add `type="button"` unless the button submits a form (then `type="submit"`)
- Always add `aria-label` to icon-only buttons
- Always set `aria-hidden="true"` on `.btn__icon`
- Never omit `.btn__text` — even in icon-only mode it can hold visually hidden text

**Inferred intent → shape mapping:**

| User intent | Shape |
|---|---|
| "Submit", "Save", "Confirm", "Apply" | `btn--primary` |
| "Cancel", "Back", "Dismiss" | `btn--subtle` or `btn--secondary-outline` |
| "Delete", "Remove" | `btn--neutral` (high contrast, signals weight) |
| "Edit", "View", "Open" | `btn--secondary-solid` or `btn--secondary-outline` |
| Icon-only action in toolbar | `btn--subtle btn--icon-only` |

---

## 18. Template Composition Notes

These patterns are pre-approved for use in page templates.

**Form footer — submit + cancel:**
```html
<div role="group" aria-label="Form actions" style="display:flex; gap: var(--space-8);">
  <button class="btn btn--primary" type="submit">
    <span class="btn__text">Submit Application</span>
  </button>
  <button class="btn btn--subtle" type="button">
    <span class="btn__text">Cancel</span>
  </button>
</div>
```

**Confirmation dialog — confirm + dismiss:**
```html
<div role="group" aria-label="Confirm action" style="display:flex; gap: var(--space-8);">
  <button class="btn btn--neutral" type="button">
    <span class="btn__text">Delete</span>
  </button>
  <button class="btn btn--secondary-outline" type="button">
    <span class="btn__text">Keep</span>
  </button>
</div>
```

**Hero section CTA on brand background:**
```html
<button class="btn btn--primary-on-color" type="button">
  <span class="btn__text">Start Your Application</span>
</button>
```

**Toolbar with icon actions (medium, icon-only):**
```html
<div role="toolbar" aria-label="Document actions">
  <button class="btn btn--subtle btn--icon-only btn--md" type="button" aria-label="Print">
    <span class="btn__icon" aria-hidden="true"><svg>...</svg></span>
  </button>
  <button class="btn btn--subtle btn--icon-only btn--md" type="button" aria-label="Share">
    <span class="btn__icon" aria-hidden="true"><svg>...</svg></span>
  </button>
</div>
```

**RTL form footer (Arabic page):**
```html
<!-- No change to HTML — layout mirrors via dir="rtl" on ancestor -->
<div dir="rtl" role="group" aria-label="إجراءات النموذج" style="display:flex; gap: var(--space-8);">
  <button class="btn btn--primary" type="submit">
    <span class="btn__text">إرسال الطلب</span>
  </button>
  <button class="btn btn--subtle" type="button">
    <span class="btn__text">إلغاء</span>
  </button>
</div>
```

---

## 19. Known Limitations

| Limitation | Impact | Workaround |
|---|---|---|
| `secondary-outline` border contrast (1.6:1) fails WCAG 1.4.11 on white backgrounds | Compliance gap for outline variant | Use `secondary-solid` on white backgrounds until border token is upgraded |
| No automated contrast-ratio audit rule | WCAG 1.4.3 / 1.4.11 cannot be verified by the current audit engine | Run a manual contrast check using the token values documented in §14 |
| `btn--sm` (24px) may fall below WCAG 2.5.5 target size (44px) | Small buttons may be hard to tap on touch devices | Do not use `btn--sm` as a primary action; reserve for dense secondary UI |
| `aria-expanded` pattern not yet covered by an audit rule | Expandable-trigger buttons (e.g. dropdowns) have no automated state check | Use `data-toggle` attribute and manually verify `aria-expanded` is set correctly |
| Label language matching (PLATFORM-CODE-A11Y-002) requires manual review | AI or automated tools cannot verify Arabic vs English label appropriateness | Include language review in the QA checklist for all Arabic-language pages |

---

## 20. Common Violations

These are the most frequent errors found during design system audits. Listed in order of occurrence.

**1. Icon-only button missing aria-label** (BTN-A11Y-002 — error)
```html
<!-- WRONG -->
<button class="btn btn--subtle btn--icon-only btn--md">
  <span class="btn__icon"><svg>...</svg></span>
</button>

<!-- CORRECT -->
<button class="btn btn--subtle btn--icon-only btn--md" aria-label="Close menu">
  <span class="btn__icon" aria-hidden="true"><svg>...</svg></span>
</button>
```

**2. Two primary buttons in the same form** (BTN-USAGE-001 — warning)
```html
<!-- WRONG — two primary buttons -->
<button class="btn btn--primary">Save Draft</button>
<button class="btn btn--primary">Publish</button>

<!-- CORRECT — one primary, one secondary -->
<button class="btn btn--primary">Publish</button>
<button class="btn btn--secondary-outline">Save Draft</button>
```

**3. Hardcoded color bypassing token** (BTN-TOKEN-001 — error)
```html
<!-- WRONG -->
<button class="btn" style="background: #1B8354;">Submit</button>

<!-- CORRECT — token via CSS class -->
<button class="btn btn--primary">
  <span class="btn__text">Submit</span>
</button>
```

**4. Using a div as a button** (BTN-STRUCT-001 — error)
```html
<!-- WRONG -->
<div class="btn btn--primary" onclick="submit()">Submit</div>

<!-- CORRECT -->
<button class="btn btn--primary" type="button">
  <span class="btn__text">Submit</span>
</button>
```

**5. Missing .btn__text wrapper** (not caught by a rule — breaks token-driven layout)
```html
<!-- WRONG — text directly in button breaks icon alignment and font tokens -->
<button class="btn btn--primary">Submit</button>

<!-- CORRECT -->
<button class="btn btn--primary">
  <span class="btn__text">Submit</span>
</button>
```
