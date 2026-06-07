# Chip — Component Contract

```
contract_version: 1.0.0
component_id:     chip
status:           pending_audit
category:         display
last_reviewed:    2026-06-06
```

---

## 1. Purpose

A Chip is a **compact interactive label** used for filtering, tagging, or categorizing content.

It represents a **toggle or selection state** — it is not a navigation element and not a form submission trigger.

> AI Rule: If the user is selecting a filter or toggling a category, use a Chip. If the user is submitting an action, use a Button. If the user is navigating, use a Link.

---

## 2. When to Use / When NOT to Use

| Situation | Use Chip? |
|---|---|
| Filter a list by category | Yes |
| Tag content with a label | Yes — display-only (`<span>`) |
| Toggle a persistent on/off state | Yes — with `aria-pressed` |
| Select from a set of options | Yes — with `aria-selected` in `role="group"` |
| Submit a form | No — use Button |
| Navigate to another page | No — use Link |
| Represent a single primary action | No — use Button |

---

## 3. Anatomy

```
.chip                     ← root element (<button> or <span>)
  .chip__label            ← visible label text (always required)
  ::after                 ← focus outline (injected by CSS in focused state only)
```

**Slot rules:**

| Slot | Required | Notes |
|---|---|---|
| `.chip__label` | Always | Visible text label. No icon slot exists in this component version. |
| `::after` | CSS-injected | Present only in `:focus` / `:focus-visible`. Not in the HTML. |

**Note:** This component has no icon slot. The Figma manifest contains no icon child nodes across all 288 variants. Icon support requires a future contract revision.

---

## 4. HTML Contract

### Interactive chip (toggle / filter)
```html
<button class="chip chip--primary" type="button">
  <span class="chip__label">تقنية</span>
</button>
```

### Interactive chip — selected state
```html
<button class="chip chip--primary chip--selected" type="button" aria-pressed="true">
  <span class="chip__label">تقنية</span>
</button>
```

### Interactive chip — disabled
```html
<button class="chip chip--neutral" type="button" disabled>
  <span class="chip__label">غير متاح</span>
</button>
```

### Display-only chip (non-interactive tag)
```html
<span class="chip chip--neutral">
  <span class="chip__label">تصنيف</span>
</span>
```

### Filter chip group
```html
<div role="group" aria-label="تصفية حسب الفئة">
  <button class="chip chip--neutral" type="button" aria-pressed="true">
    <span class="chip__label">الكل</span>
  </button>
  <button class="chip chip--neutral" type="button" aria-pressed="false">
    <span class="chip__label">تقنية</span>
  </button>
  <button class="chip chip--neutral" type="button" aria-pressed="false">
    <span class="chip__label">تصميم</span>
  </button>
</div>
```

---

## 5. CSS Modifier Map

| Modifier | Controls | Notes |
|---|---|---|
| `.chip--primary` | Style: SA-brand surface | Default off-color surface |
| `.chip--neutral` | Style: Gray surface | Default off-color surface |
| `.chip--on-color` | Surface switch | Add to either style when on colored/dark background |
| `.chip--rounded` | Border-radius: full | Pill shape (`--chip-radius-rounded`) |
| `.chip--sm` | Size: Small (20px) | Below 24px minimum — see Compliance |
| `.chip--md` | Size: Medium (24px) | |
| *(none)* | Size: Large (32px) | Default |
| `.chip--selected` / `[aria-pressed="true"]` / `[aria-selected="true"]` | Selected state | CSS targets all three |
| `.chip--disabled` / `[disabled]` / `[aria-disabled="true"]` | Disabled state | CSS targets all three |
| `.is-pressed` | Pressed state | JS class alternative to `:active` |
| `.is-focused` | Focused state | JS class alternative to `:focus-visible` |

---

## 6. Aria Contract

### Selected vs Pressed semantics

| Intent | Attribute | When |
|---|---|---|
| Persistent toggle (standalone) | `aria-pressed="true"` | Chip acts as on/off switch independently |
| Selection within a group | `aria-selected="true"` | Chip is inside `role="group"` or `role="listbox"` |
| Transient interaction | none (CSS `:active` only) | Pressed state during click — not a persistent state |

**Rule:** Never use both `aria-pressed` and `aria-selected` on the same chip.

### Disabled semantics

| Mechanism | Keyboard access | Use when |
|---|---|---|
| `disabled` attribute | Removed from tab order | Standard disabled — user cannot interact |
| `aria-disabled="true"` | Stays in tab order | Discoverable disabled — user can discover the unavailable action (e.g. with tooltip) |

---

## 7. Focus Behavior

### Implementation deviation from Figma

The Figma manifest models the focus outline as a fixed-size `RECTANGLE` node with hardcoded pixel dimensions:
- Small: `55 × 28px`
- Medium: `59 × 32px`
- Large: `68 × 40px`

**These values assume the label is always "Item".** They will break when labels are longer or shorter.

**Implementation uses `inset: -4px` instead:**
```css
.chip--primary:focus::after {
  content: "";
  position: absolute;
  inset: -4px;
  border-radius: var(--chip-radius-default);
  border: var(--chip-focus-outline-width) solid var(--chip-focus-outline-color);
  pointer-events: none;
}
```

**Reason:** `inset: -4px` grows with the chip's natural width and height, supporting dynamic label length and responsive layouts. The visual result is identical to Figma for the "Item" label, and correct for all other labels.

This deviation is intentional and documented. It does not affect the focus ring's visual prominence or color.

---

## 8. Group Pattern

The Chip component does not define a group container component. When used in filter groups:

- Wrap chips in `<div role="group" aria-label="[group purpose]">`
- Each chip manages its own toggle state via `aria-pressed`
- Keyboard navigation within the group (arrow keys) is not provided by chip.css — implement via JavaScript if required
- Single-select groups should consider `role="listbox"` with `aria-selected` on each chip

**This section is a placeholder.** A formal chip group pattern has not been designed. Do not ship a production chip group without defining the selection model and keyboard contract.

---

## 9. Implementation Notes

The following properties are added by chip.css but are not present in the Figma manifest:

| Property | Value | Reason |
|---|---|---|
| `cursor: pointer` | On all interactive chips | Platform interaction standard |
| `white-space: nowrap` | Base | Prevents label wrapping in fixed-height container |
| `user-select: none` | Base | Standard for interactive labels |
| `transition` | `background` | Motion standard — consistent with button |
| `box-sizing: border-box` | Base | Layout integrity |

**Padding invariance:** All three sizes use the same `padding-inline: var(--chip-padding-inline)` (12px). This is as-designed in Figma. Only height changes per size. Design team should confirm this is intentional at Large size.

**Font-weight progression:** Small uses `--font-weight-semibold` (600), while Medium and Large use `--font-weight-medium` (500). This reversed progression (heavier at smaller size) is atypical. Preserved as-is from Figma; design team to confirm.

---

## 10. Token Notes

### Missing chip-scoped tokens
No `--chip-*` tokens exist in token.css. All chip.css declarations reference pending tokens. The component is non-functional until these tokens are added to token.css. See `analysis.md §Token Findings` for the full list with recommended primitive mappings.

### `#161616` — missing primitive
The color `#161616` (used for Neutral text and focus outline) has no primitive token in token.css. `--gray-950: #0d121c` is the nearest available but differs visually. A `--near-black` or `--gray-925` primitive must be proposed to the token team before `--chip-text-neutral` and `--chip-focus-outline-color` can be resolved.

### Figma typo — on-color disabled background
The Figma source token name is `--Chip-chip-background-on-color-diabled` (missing 's'). The generated files use the corrected name `--chip-on-color-bg-disabled`.

### Cross-component token leak — Primary/Pressed text
The Figma manifest uses `--Button-button-background-primary-pressed` as the text color for Primary/Pressed chips. This is a Button-namespaced background token repurposed as text — a cross-component token leak. `--chip-text-primary-pressed: var(--sa-900)` is the correct chip-scoped replacement.

### Small font-size gap
10px (Small chip font-size) has no `--fs-text-2xs` primitive in token.css. The design token team must add a new step to the type scale, or the design team must confirm that 12px (`--fs-text-xs`) is an acceptable visual substitute.

---

## 11. Out of Scope

The following are not covered by this component version:

- Icon slot / icon+label chip variant
- Loading / busy chip state
- Chip group component (selection model, keyboard navigation)
- Chip removal / dismissible chips (×-button pattern)
- Chip input (chips as form input values)
