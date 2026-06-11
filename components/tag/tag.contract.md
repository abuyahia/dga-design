# Tag + Status Tag — Component Contract

```
contract_version: 1.0.0
component_id:     tag
status:           stable
category:         feedback
last_reviewed:    2026-06-09
```

---

## 1. Purpose

**Tag** is a compact, display-only inline badge used to annotate content with categorical metadata, status labels, or descriptive attributes.

**Status Tag** is a pill-shaped display component combining a colored dot indicator and a text label. It communicates entity status or workflow state.

Both components are **non-interactive** in their base form. They carry information — they do not trigger actions.

> AI Rule: Use Tag when annotating an item with a category, type, or attribute label. Use Status Tag when expressing the current state or status of an entity with a visual dot indicator.

---

## 2. When to Use / When NOT to Use

### Tag

| Situation | Use Tag? |
|---|---|
| Label a record type (Document, Request, Draft) | Yes |
| Show a content category or filter chip | Yes |
| Indicate a feature flag or environment label | Yes |
| Trigger navigation or filtering | No — Tags are non-interactive. Use a FilterChip or Button. |
| Indicate live/workflow status with a dot | No — Use Status Tag |
| Replace a badge on a notification icon | No — Use Badge component |

### Status Tag

| Situation | Use Status Tag? |
|---|---|
| Show workflow state (Active, Pending, Failed) | Yes |
| Show connection/online status | Yes |
| Show a process status in a table | Yes |
| Show a boolean toggle state | No — Use a Toggle or Checkbox |
| Replace navigation breadcrumb | No |

---

## 3. Anatomy

### Tag

```
.tag                          ← root element (<span>)
  .tag__icon  [optional]      ← SVG icon wrapper, aria-hidden="true"
  .tag__text                  ← visible label text
```

**Slot rules:**

| Slot | Required | Notes |
|---|---|---|
| `.tag__text` | Conditionally | Required unless icon-only. In icon-only mode: use `.sr-only` text or `aria-label` on root. |
| `.tag__icon` | Optional | Decorative — wrap SVG, set `aria-hidden="true"` |

### Status Tag

```
.status-tag                   ← root element (<span>)
  .status-tag__dot            ← colored status circle, aria-hidden="true"
  .status-tag__text           ← visible label text
```

**Slot rules:**

| Slot | Required | Notes |
|---|---|---|
| `.status-tag__dot` | Required | Always present. `aria-hidden="true"`. The dot is decorative — the text communicates the state. |
| `.status-tag__text` | Required | Always present. The visible text is the primary accessible label. |

---

## 4. HTML Contract

### Tag — text only (default/neutral/medium)
```html
<span class="tag">
  <span class="tag__text">Label</span>
</span>
```

### Tag — with leading icon
```html
<span class="tag">
  <span class="tag__icon" aria-hidden="true">
    <svg>...</svg>
  </span>
  <span class="tag__text">Label</span>
</span>
```

### Tag — icon only (requires accessible label)
```html
<span class="tag tag--icon-only" aria-label="Category label">
  <span class="tag__icon" aria-hidden="true">
    <svg>...</svg>
  </span>
</span>
```

### Tag — rounded
```html
<span class="tag tag--rounded">
  <span class="tag__text">Label</span>
</span>
```

### Tag — x Small
```html
<span class="tag tag--xs">
  <span class="tag__text">Label</span>
</span>
```

### Tag — Small
```html
<span class="tag tag--sm">
  <span class="tag__text">Label</span>
</span>
```

### Tag — Error style
```html
<span class="tag tag--error">
  <span class="tag__text">Error</span>
</span>
```

### Tag — Outline modifier (combine with any style)
```html
<span class="tag tag--outline tag--success">
  <span class="tag__text">Verified</span>
</span>
```

### Tag — On-Color (on dark/colored backgrounds)
```html
<span class="tag tag--on-color">
  <span class="tag__text">Beta</span>
</span>
```

### Status Tag — default (neutral, subtle, medium)
```html
<span class="status-tag">
  <span class="status-tag__dot" aria-hidden="true"></span>
  <span class="status-tag__text">Active</span>
</span>
```

### Status Tag — Ghost
```html
<span class="status-tag status-tag--green status-tag--ghost">
  <span class="status-tag__dot" aria-hidden="true"></span>
  <span class="status-tag__text">Active</span>
</span>
```

### Status Tag — Inverted
```html
<span class="status-tag status-tag--red status-tag--inverted">
  <span class="status-tag__dot" aria-hidden="true"></span>
  <span class="status-tag__text">Failed</span>
</span>
```

---

## 5. Modifier Reference

### Tag — Size modifiers

| Modifier | Figma size | Height | Padding-inline | Font |
|---|---|---|---|---|
| `.tag--xs` | x Small | 20px | 8px | 10px / 14px / 600 |
| `.tag--sm` | Small | 24px | 8px | 12px / 18px / 500 |
| _(none)_ | Medium | 32px | 12px | 16px / 24px / 500 |

### Tag — Style modifiers

| Modifier | Figma style | Background | Border | Text |
|---|---|---|---|---|
| _(none)_ | Neutral | `--tag-neutral-bg` | `--tag-neutral-border` | `--tag-neutral-text` |
| `.tag--error` | Error | `--tag-error-bg` | `--tag-error-border` | `--tag-error-text` |
| `.tag--info` | Info | `--tag-info-bg` | `--tag-info-border` | `--tag-info-text` |
| `.tag--success` | Success | `--tag-success-bg` | `--tag-success-border` | `--tag-success-text` |
| `.tag--warning` | Warning | `--tag-warning-bg` | `--tag-warning-border` | `--tag-warning-text` |
| `.tag--on-color` | On-Color | `--tag-on-color-bg` | none | `--tag-on-color-text` |

### Tag — Other modifiers

| Modifier | Effect |
|---|---|
| `.tag--outline` | Removes background. Applies darker border. Combine with style. |
| `.tag--rounded` | Applies `border-radius: full` (pill shape). |
| `.tag--icon-only` | Square container. Text must be provided via `aria-label` on root. |

### Status Tag — Size modifiers

| Modifier | Figma size | Height | Padding-inline | Gap | Font |
|---|---|---|---|---|---|
| `.status-tag--xs` | x Small | 20px | 8px | 8px | 10px / 14px / 500 |
| `.status-tag--sm` | Small | 24px | 8px | 8px | 14px / 20px / 500 |
| _(none)_ | Medium | 32px | 16px | 8px | 16px / 24px / 500 |

### Status Tag — Style modifiers

| Modifier | Figma style | Subtle bg | Dot color | Text |
|---|---|---|---|---|
| _(none)_ | Neutral | `--status-tag-neutral-subtle-bg` | `--status-tag-neutral-subtle-dot` | `--status-tag-neutral-subtle-text` |
| `.status-tag--blue` | Blue | `--status-tag-blue-subtle-bg` | `--status-tag-blue-subtle-dot` | `--status-tag-blue-subtle-text` |
| `.status-tag--green` | Green | `--status-tag-green-subtle-bg` | `--status-tag-green-subtle-dot` | `--status-tag-green-subtle-text` |
| `.status-tag--red` | Red | `--status-tag-red-subtle-bg` | `--status-tag-red-subtle-dot` | `--status-tag-red-subtle-text` |
| `.status-tag--yellow` | Yellow | `--status-tag-yellow-subtle-bg` | `--status-tag-yellow-subtle-dot` | `--status-tag-yellow-subtle-text` |

### Status Tag — Status modifiers

| Modifier | Figma status | Effect |
|---|---|---|
| _(none)_ | Subtle | Style bg, style dot, style text |
| `.status-tag--ghost` | Ghost | No background. Style dot retained. Text → neutral. |
| `.status-tag--inverted` | Inverted | Dark style bg. Dot → semi-transparent white. Text → white. |

---

## 6. Class Composition Rules

**Tag:**
- Combine any one style modifier with any one size modifier and/or `--outline` and/or `--rounded`.
- Do NOT combine multiple style modifiers (e.g., `.tag--error.tag--success` is invalid).
- Do NOT combine `.tag--icon-only` without providing an `aria-label` on the root.

**Status Tag:**
- Combine any one style modifier with any one size modifier and/or one status modifier.
- Do NOT combine multiple style modifiers.
- Do NOT combine multiple status modifiers.
- Do NOT omit `.status-tag__text`. The dot alone is insufficient for accessibility.

---

## 7. Accessibility Contract

### 7.1 Tag — text visible

```html
<span class="tag tag--error">
  <span class="tag__text">Rejected</span>
</span>
```
Text is the accessible label. No additional ARIA needed.

### 7.2 Tag — icon only

```html
<!-- CORRECT -->
<span class="tag tag--icon-only" aria-label="Archived">
  <span class="tag__icon" aria-hidden="true"><svg>...</svg></span>
</span>

<!-- INCORRECT — no accessible label -->
<span class="tag tag--icon-only">
  <span class="tag__icon" aria-hidden="true"><svg>...</svg></span>
</span>
```

### 7.3 Tag — hidden text alternative

```html
<span class="tag tag--icon-only">
  <span class="tag__icon" aria-hidden="true"><svg>...</svg></span>
  <span class="sr-only">Archived</span>
</span>
```

### 7.4 Status Tag — dot must be aria-hidden

```html
<!-- CORRECT -->
<span class="status-tag status-tag--green">
  <span class="status-tag__dot" aria-hidden="true"></span>
  <span class="status-tag__text">Active</span>
</span>

<!-- INCORRECT — dot color conveys meaning without text -->
<span class="status-tag status-tag--green">
  <span class="status-tag__dot"></span>
</span>
```

### 7.5 Color-only status must have text

The dot in Status Tag uses color to convey state. The text label MUST communicate the same information. Never rely on dot color alone.

---

## 8. Prohibited Patterns

```html
<!-- Tag: multiple style modifiers — INVALID -->
<span class="tag tag--error tag--warning">...</span>

<!-- Tag: icon-only without label — INVALID -->
<span class="tag tag--icon-only">
  <span class="tag__icon" aria-hidden="true"><svg>...</svg></span>
</span>

<!-- Status Tag: missing text — INVALID -->
<span class="status-tag status-tag--red">
  <span class="status-tag__dot" aria-hidden="true"></span>
</span>

<!-- Status Tag: dot without aria-hidden — WARNING -->
<span class="status-tag">
  <span class="status-tag__dot"></span>
  <span class="status-tag__text">Active</span>
</span>

<!-- Tag as a navigation link — WRONG COMPONENT -->
<span class="tag" onclick="navigate()">Dashboard</span>
<!-- Use <a> or Button instead -->

<!-- Using Tag as interactive filter without JS handling — INVALID -->
<span class="tag" tabindex="0">Filter by Type</span>
```

---

## 9. Content Rules

1. **Tag text**: Short, concise labels. Typically 1–3 words. Avoid full sentences.
2. **Status Tag text**: Match the entity's actual state in the UI language context. Provide localized strings.
3. **Arabic support**: Both components use `IBM Plex Sans Arabic` via `--tag-font-family`. Arabic text renders correctly in RTL layouts. Ensure `dir="rtl"` is set on the appropriate ancestor.
4. **Language matching**: Tag label language should match the page language context. Do not mix languages within a single tag.

---

## 10. Token Dependencies

Both components depend on the following token.css primitives (via component token fallbacks):

- `--gray-*`, `--error-*`, `--info-*`, `--success-*`, `--warning-*` — color primitives
- `--space-*` — spacing primitives
- `--radius-sm`, `--radius-full` — radius primitives
- `--fs-text-*`, `--lh-text-*` — typography primitives
- `--font-weight-*` — font weight primitives
- `--font-sans` — font family

**Missing primitives** (must be added to token.css):
- `--fs-text-2xs` (10px)
- `--lh-text-2xs` (14px)
- Semi-transparent white tokens for on-color and inverted dot variants

See `analysis.md §Missing Tokens` for full list.
