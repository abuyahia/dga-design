# Rating Component Contract

**Component**: Rating  
**Version**: 1.0.0  
**Status**: pending_audit  
**Source**: `components/rating/mainifest.json`, `components/rating/mainifest-items.json`

---

## 1. Purpose

Displays a 5-star rating indicator. Supports full, half, and empty star states. Available in three sizes and two color styles (default gold / brand green). Intended as a read-only display component; see §10 for interactive usage guidance.

---

## 2. Anatomy

```
.rating                        Root container
└── .rating__star              Individual star item (× 5 by default)
    ├── .rating__star-icon     SVG star — used in filled and empty states
    ├── .rating__star-base     SVG star base — used in half state only (gray)
    └── .rating__star-fill     SVG star fill overlay — used in half state only (colored, clipped)
```

The `.rating__star::before` pseudo-element is the interaction ring layer (pressed state). It is not a DOM element.

---

## 3. CSS Class API

### Root modifiers

| Class              | Description                                          |
|--------------------|------------------------------------------------------|
| `.rating`          | Required. Root element.                              |
| `.rating--lg`      | Large size: 48px stars.                              |
| `.rating--md`      | Medium size: 32px stars.                             |
| `.rating--sm`      | Small size: 24px stars.                              |
| `.rating--brand`   | Brand color variant: green stars instead of gold.    |
| `.rating--interactive` | Interactive mode: adds cursor and hover styles.  |
| `.rating--disabled`| Disabled state: 40% opacity, pointer-events none.    |

One size modifier is required. Default is large if none applied.

### Star state modifiers

| Class                     | Description                             |
|---------------------------|-----------------------------------------|
| `.rating__star--filled`   | Full colored star.                      |
| `.rating__star--half`     | Half-colored star (left 50% filled).    |
| `.rating__star--empty`    | Empty/unselected star.                  |

---

## 4. HTML Structure

### Display rating (read-only)

```html
<div class="rating rating--lg" role="img" aria-label="4 out of 5 stars">
  <span class="rating__star rating__star--filled" aria-hidden="true">
    <svg class="rating__star-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26Z"/>
    </svg>
  </span>
  <span class="rating__star rating__star--filled" aria-hidden="true">
    <svg class="rating__star-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26Z"/>
    </svg>
  </span>
  <span class="rating__star rating__star--filled" aria-hidden="true">
    <svg class="rating__star-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26Z"/>
    </svg>
  </span>
  <span class="rating__star rating__star--half" aria-hidden="true">
    <svg class="rating__star-icon rating__star-base" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26Z"/>
    </svg>
    <svg class="rating__star-fill" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26Z"/>
    </svg>
  </span>
  <span class="rating__star rating__star--empty" aria-hidden="true">
    <svg class="rating__star-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26Z"/>
    </svg>
  </span>
</div>
```

### Half star structure (detail)

The `.rating__star--half` requires two SVGs:
- `.rating__star-base` — the gray background star (shows the full star shape in neutral color)  
- `.rating__star-fill` — the colored fill star, positioned absolute, clipped to left 50%

Do not use `.rating__star-icon` for the base star inside `.rating__star--half`. Use `.rating__star-base` instead.

---

## 5. Valid Root Elements

| Element | Valid | Notes                                      |
|---------|-------|--------------------------------------------|
| `<div>` | Yes   | Default. Use `role="img"` for display.     |
| `<span>`| Yes   | Inline context.                            |
| `<fieldset>` | Yes | Interactive rating pattern (see §10). |

---

## 6. Size Axis

| Modifier     | Star size | Ring size (pressed) |
|--------------|-----------|---------------------|
| `.rating--lg`| 48 × 48px | 54 × 54px           |
| `.rating--md`| 32 × 32px | 46 × 46px           |
| `.rating--sm`| 24 × 24px | 38 × 38px           |

Star gap is always 4px (`--rating-gap`).

---

## 7. Brand Axis

| Modifier        | Star fill color         | Token                        |
|-----------------|-------------------------|------------------------------|
| (none / default)| Gold: `#DBA102`         | `--rating-star-fill-default` |
| `.rating--brand`| Green: `#1B8354`        | `--rating-star-fill-brand`   |

Apply `.rating--brand` to the `.rating` root. It cascades to all star states automatically.

---

## 8. Token Surface

All visual values must reference these tokens. Do not use primitive Figma variable references in consuming CSS.

| Token                              | Role                      | Fallback          |
|------------------------------------|---------------------------|-------------------|
| `--rating-star-fill-default`       | Filled star, default      | `#DBA102`         |
| `--rating-star-fill-brand`         | Filled star, brand        | `#1B8354`         |
| `--rating-star-empty-fill`         | Empty star                | `#E5E7EB`         |
| `--rating-star-half-base-fill`     | Half star base (gray)     | `#D2D6DB`         |
| `--rating-star-pressed-ring-bg`    | Pressed ring background   | `#F3F4F6`         |
| `--rating-gap`                     | Gap between stars         | `4px`             |
| `--rating-star-size-lg`            | Large star size           | `48px`            |
| `--rating-star-size-md`            | Medium star size          | `32px`            |
| `--rating-star-size-sm`            | Small star size           | `24px`            |
| `--rating-star-ring-size-lg`       | Pressed ring size, large  | `54px`            |
| `--rating-star-ring-size-md`       | Pressed ring size, medium | `46px`            |
| `--rating-star-ring-size-sm`       | Pressed ring size, small  | `38px`            |
| `--rating-star-ring-radius`        | Ring border-radius        | `50%`             |
| `--rating-disabled-opacity`        | Disabled state opacity    | `0.4`             |

All `--rating-*` tokens are proposed and must be added to `token.css` before production deployment.

---

## 9. Accessibility Rules

### Display rating (mandatory)

- Root element must have `role="img"`.
- Root element must have `aria-label` with the rating value, e.g. `aria-label="3.5 out of 5 stars"` or the Arabic equivalent.
- All `.rating__star` elements must have `aria-hidden="true"`.
- All SVG elements must have `aria-hidden="true"` and `focusable="false"`.

### Interactive rating (separate pattern — not in this manifest)

Use a `<fieldset>` with `<legend>` and five `<input type="radio">` elements styled to appear as stars. This provides native keyboard access and screen reader announcements. Do not use `role="radiogroup"` with `<div>` unless native radio inputs are not feasible.

---

## 10. Interactive Usage Guidance

The Figma manifest defines a display-only component. If used as a rating input:

1. Replace the root `<div role="img">` with a `<fieldset>`.
2. Add a `<legend>` as the label.
3. Use one `<input type="radio" name="rating" value="N">` per star slot.
4. Style the labels using `.rating__star` classes.
5. Use JavaScript to update star states on change.
6. The `.rating--interactive` modifier provides hover styles.

---

## 11. Disabled State

Apply `.rating--disabled` to the root `.rating` element.

- Reduces all stars to 40% opacity.
- Removes pointer events.
- Does not add `aria-disabled`. The consuming application must set `aria-disabled="true"` or the `disabled` attribute if needed.

---

## 12. RTL Support

The component gap uses `gap` (direction-agnostic in flex). The half-star `clip-path` currently fills the left 50% (LTR behavior).

**RTL note**: Under `[dir="rtl"]`, the half-star fill direction is reversed to `clip-path: inset(0 0 0 50%)`. Pending design team confirmation. See TODO in `analysis.md`.

---

## 13. Star Count

The default is 5 stars. The template shows 3.5/5 matching the manifest. Star count is a consumer concern — the component does not enforce 5 stars. `aria-label` must reflect the actual value and max.

---

## 14. Content Rules

- The `aria-label` must state the rating value in a human-readable form.
- The label language must match the document language context.
- Do not omit the `aria-label`. An unlabeled rating image provides no accessible information.
- For Arabic contexts: `aria-label="التقييم: 3.5 من 5 نجوم"`.

---

## 15. Assembly Notes

This component may be composed into:
- Product card assemblies
- Review list items
- Form fields for rating input

When composed, the rating inherits the surrounding container's text direction. Ensure `dir` is set correctly on the nearest ancestor or `<html>`.
