# Divider — Component Contract

```
contract_version: 1.0.0
component_id:     divider
status:           stable
category:         layout
classification:   Primitive
last_reviewed:    2026-06-12
```

---

## Component Type

**Primitive** — self-contained, no child component dependencies, no interactive states.

---

## Dependencies

None.

---

## 1. Purpose

The Divider is a thin visual line used to separate content areas, list items, or sections. It communicates a visual boundary and may or may not carry semantic meaning depending on context.

Use it:
- Between sections of a page
- Between items in a list or menu
- Between panels in a layout
- As a decorative visual separator

Do not use it:
- To convey meaning through color alone (WCAG 1.4.1)
- To replace proper heading/section structure
- As a loading skeleton or placeholder
- With `tabindex` — it is not interactive

---

## 2. Anatomy

```
.divider     ← root element (<hr>)
             — the element IS the visual line. No child elements.
```

No slots. No child elements required or optional.

---

## 3. HTML Contract

### Horizontal / Neutral (default)
```html
<hr class="divider" />
```

### Horizontal / Primary
```html
<hr class="divider divider--primary" />
```

### Horizontal / Alpha White
```html
<hr class="divider divider--alpha-white" />
```

### Horizontal / White
```html
<hr class="divider divider--white" />
```

### Vertical / Neutral
```html
<hr class="divider divider--vertical" aria-orientation="vertical" />
```

### Vertical / Primary
```html
<hr class="divider divider--vertical divider--primary" aria-orientation="vertical" />
```

### Vertical / Alpha White
```html
<hr class="divider divider--vertical divider--alpha-white" aria-orientation="vertical" />
```

### Vertical / White
```html
<hr class="divider divider--vertical divider--white" aria-orientation="vertical" />
```

### Decorative (no semantic meaning)
```html
<hr class="divider" role="none" aria-hidden="true" />
```

---

## 4. Modifier Classes

| Class | Description |
|---|---|
| `.divider--vertical` | Vertical orientation (1px wide, 100% tall) |
| `.divider--primary` | Primary (green) color |
| `.divider--alpha-white` | Semi-transparent white (30% opacity) — for dark backgrounds |
| `.divider--white` | Solid white — for dark backgrounds |

**Default:** Horizontal orientation, Neutral (grey) color.

**Valid combinations:**

| Combination | Valid? |
|---|---|
| `.divider` | Yes — horizontal neutral |
| `.divider .divider--vertical` | Yes — vertical neutral |
| `.divider .divider--primary` | Yes — horizontal primary |
| `.divider .divider--vertical .divider--primary` | Yes — vertical primary |
| Any color modifier + `--vertical` | Yes |

---

## 5. Semantic vs. Decorative Usage

### Semantic (thematic break)
Use when the divider represents a meaningful content boundary:
```html
<hr class="divider" />
```
The `<hr>` element has implicit `role="separator"`. No additional ARIA needed.

### Decorative (visual only)
Use when the divider is purely visual and does not mark a content boundary:
```html
<hr class="divider" role="none" aria-hidden="true" />
```

### Alternative element (non-semantic contexts)
If `<hr>` is not appropriate (e.g., inside a `<dl>`, `<ul>`, or flex layout where `<hr>` is invalid):
```html
<div class="divider" role="separator" aria-hidden="true"></div>
```

---

## 6. Vertical Divider — Layout Requirement

The vertical divider uses `height: 100%; align-self: stretch`. This requires the parent container to have a defined height.

**Works:**
```html
<!-- Parent has defined height -->
<div style="display: flex; height: 64px; align-items: center; gap: 16px;">
  <span>Left content</span>
  <hr class="divider divider--vertical" aria-orientation="vertical" />
  <span>Right content</span>
</div>
```

**Does not work:**
```html
<!-- Parent height is auto — vertical divider will collapse to 0 -->
<div style="height: auto;">
  <hr class="divider divider--vertical" aria-orientation="vertical" />
</div>
```

---

## 7. Color Usage Guidance

| Color | Background | Use case |
|---|---|---|
| Neutral (#D2D6DB) | White / light | Default content separators |
| Primary (#1B8354) | White / light | Highlighted sections, branded separators |
| Alpha White (30%) | Dark / colored | On-color surfaces, header backgrounds |
| White | Dark / colored | Maximum contrast on dark surfaces |

> **Warning:** Do not use color as the sole means of conveying information. Pair color variants with context, labels, or structural hierarchy.

---

## 8. Accessibility

| Requirement | Implementation |
|---|---|
| Semantic divider | `<hr>` provides implicit `role="separator"` |
| Vertical semantic divider | `<hr aria-orientation="vertical">` |
| Decorative divider | `role="none" aria-hidden="true"` |
| Not focusable | Never add `tabindex` to a divider |
| Color contrast | Neutral (#D2D6DB on white) = ~1.4:1 — below WCAG 1.4.11. Acceptable for decorative separators; not for focus or informational indicators |

---

## 9. Token Dependencies

All `--divider-*` tokens must be defined in `token.css`. Until then, fallback values in `divider.css` are active. See `analysis.md` Missing Tokens section.

---

## 10. AI Generation Rules

```
AI rule: Divider root element is always <hr class="divider"> unless explicitly using a non-semantic context.
AI rule: Default variant needs no modifier classes beyond .divider.
AI rule: Vertical dividers require .divider--vertical AND aria-orientation="vertical".
AI rule: Decorative dividers require role="none" aria-hidden="true".
AI rule: Do not add child elements inside .divider.
AI rule: Do not add tabindex to .divider.
AI rule: Do not use color-only variants to convey meaning without additional context.
AI rule: The --alpha-white and --white modifiers are for dark/colored backgrounds only.
```
