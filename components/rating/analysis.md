# Component Analysis — Rating

**Manifest path**: `components/rating/mainifest.json`  
**Items manifest path**: `components/rating/mainifest-items.json`  
**Component name**: Rating  
**Sub-component name**: _RatingStar  
**Generated**: 2026-06-10  

---

## Source

Two manifest files exported from Figma:

- `mainifest.json` — the `Rating` composite COMPONENT_SET (5-star row)  
- `mainifest-items.json` — the `_RatingStar` individual item COMPONENT_SET

---

## Detected Anatomy

### Rating (composite)
```
.rating                         Root container — inline-flex row of stars
└── .rating__star × 5           Individual star wrapper
    ├── .rating__star-icon      SVG star element (filled or empty state)
    └── (half state only)
        ├── .rating__star-base  SVG base star (gray D2D6DB)
        └── .rating__star-fill  SVG fill star (clipped to 50% via clip-path)
```

### _RatingStar (sub-component)
```
.rating__star                   Container (position: relative)
├── ::before                    Interaction ring layer (Pressed state)
├── .rating__star-base          Base star SVG (half state only)
└── .rating__star-icon          Main star SVG
```

---

## Detected Axes

### Rating (composite)
| Axis  | Values                   | CSS mechanism         |
|-------|--------------------------|-----------------------|
| Size  | Large, Medium, Small     | `.rating--lg/md/sm`   |
| Brand | No (default), Yes (brand)| `.rating--brand`      |

### _RatingStar (sub-component)
| Axis  | Values                            | CSS mechanism              |
|-------|-----------------------------------|----------------------------|
| Size  | Large, Medium, Small              | Inherited from `.rating--*`|
| State | Normal, Half, Selected, Pressed   | Modifier classes + pseudo  |
| Style | Default (gold), Brand (green)     | `.rating--brand` on root   |

---

## Detected Variants

### Rating composite (mainifest.json): 6 variants
| Variant               | Size   | Brand |
|-----------------------|--------|-------|
| Size=Large, Brand=No  | Large  | No    |
| Size=Large, Brand=yes | Large  | Yes   |
| Size=Meduim, Brand=No | Medium | No    |  ← Note: "Meduim" typo in manifest
| Size=Meduim, Brand=yes| Medium | Yes   |
| Size=Small, Brand=No  | Small  | No    |
| Size=Small, Brand=yes | Small  | Yes   |

### _RatingStar (mainifest-items.json): 24 variants (3 sizes × 4 states × 2 styles)

---

## Detected States

### Composite (per star slot)
- **Filled** — full star, colored (secondary/primary fill)
- **Half** — left 50% colored, right 50% empty
- **Empty** — full star, neutral-200 fill

### _RatingStar item
- **Normal** — base state (empty: neutral fill implied by neutral-200)
- **Selected** — filled state
- **Half** — partial fill via rectangle overlay system
- **Pressed** — ring appears behind star (neutral-100, circular, oversized)

---

## Detected Sizes

| Size   | Star size | Ring size | Manifset name |
|--------|-----------|-----------|---------------|
| Large  | 48 × 48px | 54 × 54px | `Size=Large`  |
| Medium | 32 × 32px | 46 × 46px | `Size=Meduim` |
| Small  | 24 × 24px | 38 × 38px | `Size=Small`  |

Ring overhang: 3px on each side (ring = star + 6px).

Gap between stars: `var(--Global-spacing-xs, 4px)` = `--spacing-globalspacing-xs`.

---

## Architecture Findings

1. **Composite boundary preserved.** Rating and _RatingStar are separate Figma components. Rating is the consumer; _RatingStar is the item. Implementation treats them as a single integrated component with CSS-level sub-component classes.

2. **Half-star uses rectangle masking in Figma.** The Figma design implements the half state with three layers: a gray star base + a colored left-half rectangle + a neutral right-half rectangle. In HTML/CSS this is replaced with two overlapping SVGs using `clip-path: inset(0 50% 0 0)` on the fill layer. This is semantically equivalent and more maintainable.

3. **Pressed ring is an interaction layer.** The `ring` RECTANGLE in Pressed state variants is 54px/46px/38px with `border-radius: --radius-radius-full`. It sits behind the star. Implemented as `::before` pseudo-element. Never generates standalone HTML.

4. **No Focus layer in manifest.** The _RatingStar manifest does not show a focus/keyboard state. Focus behavior is determined by platform standards and documented as missing in this manifest.

5. **Star corner radius.** The manifest shows `cornerRadius-variable: --radius-radius-xs` on STAR shapes. Figma star corner radius controls the concave inner points. SVG polygon-based paths do not support this natively. Deviation documented. A future enhancement could use rounded SVG bezier paths.

6. **Normal vs Selected state ambiguity.** In mainifest-items.json, both Normal and Selected states show the same SVG structure without explicit fill values. The fill distinction comes from the composite manifest (mainifest.json) which shows: filled stars = secondary/primary color, empty star = neutral-200.

---

## Token Findings

### Used in manifest (Figma references → component token mapping)
| Figma variable                          | Hex fallback | Proposed component token                  |
|-----------------------------------------|--------------|-------------------------------------------|
| `--Background-background-secondary`     | `#DBA102`    | `--rating-star-fill-default`              |
| `--Background-background-primary`       | `#1B8354`    | `--rating-star-fill-brand`                |
| `--Background-background-neutral-200`   | `#E5E7EB`    | `--rating-star-empty-fill`                |
| `--Colors-Gray-neutral-300`             | `#D2D6DB`    | `--rating-star-half-base-fill`            |
| `--Background-background-neutral-100`   | `#F3F4F6`    | `--rating-star-pressed-ring-bg`           |
| `--spacing-globalspacing-xs`            | `4px`        | `--rating-gap`                            |
| `--radius-radius-xs`                    | —            | `--rating-star-radius` (star corner)      |
| `--radius-radius-full`                  | `50%`        | `--rating-star-ring-radius`               |

### Proposed size tokens (missing from token.css)
| Token                      | Value  |
|----------------------------|--------|
| `--rating-star-size-lg`    | 48px   |
| `--rating-star-size-md`    | 32px   |
| `--rating-star-size-sm`    | 24px   |
| `--rating-star-ring-size-lg` | 54px |
| `--rating-star-ring-size-md` | 46px |
| `--rating-star-ring-size-sm` | 38px |

### Proposed animation tokens (missing from token.css)
- `--rating-star-ring-transition-duration`
- `--rating-star-ring-transition-easing`
- `--rating-disabled-opacity`

---

## Accessibility Findings

1. **No accessible label on STAR shape in manifest.** Stars are visual-only. The composite must carry `role="img"` and `aria-label="X out of 5 stars"` or equivalent.

2. **No focus state in manifest.** The _RatingStar manifest does not define a focus variant. If the rating is used as an interactive input widget, focus indicators must be added that are not present in the Figma source.

3. **Interactive pattern not specified.** The composite manifest shows a static display-only rating. If used as an input, the ARIA pattern for star rating inputs (radiogroup / radio inputs) must be applied separately.

4. **Arabic language context.** This design system targets government platforms with Arabic language support. The rating label in `aria-label` must be provided in the appropriate language by the consuming application.

---

## Compliance Findings

1. **WCAG 1.4.3 Contrast — star fill colors:**
   - Default gold `#DBA102` on white `#FFF` — needs verification: luminance ~0.47, approximately 2.0:1. Below 4.5:1 for text, but stars are non-text content (icons). WCAG 1.4.11 applies (3:1 required for non-text).
   - `#DBA102` on `#FFF`: ~2.0:1 — **BELOW** 3:1 threshold. Non-compliant for non-text contrast. Design token value from manifest.
   - Brand green `#1B8354` on `#FFF`: ~4.58:1 — above 3:1. Compliant.
   - Empty `#E5E7EB` on `#FFF`: ~1.16:1 — below 3:1. This is intentional as empty stars represent absent content, not actionable UI.

2. **No hover or focus variant in manifest.** Interactive rating requires additional accessible states not captured in the Figma export.

---

## Implementation Decisions

1. **Half-star via clip-path, not rectangle overlay.** Figma's rectangle masking system is replaced with `clip-path: inset(0 50% 0 0)` on a positioned fill SVG. This is equivalent visually and avoids extra DOM.

2. **Pressed ring as `::before`** on `.rating__star`. Ring RECTANGLE in Figma maps to `::before` pseudo-element with `border-radius: 50%` and neutral-100 background. Triggered by `:active`.

3. **SVG star path.** Using `M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26Z` as 24×24 viewBox path. Scaled via CSS width/height.

4. **fill: currentColor on SVG.** Star SVGs use `fill="currentColor"`. Color is set via CSS `color` property on the SVG element, enabling clean state overrides.

5. **Size controlled on the root.** `.rating--lg/md/sm` modifiers control star dimensions. Stars inherit size from the parent modifier via descendant selectors.

6. **Brand axis as CSS modifier on root.** `.rating--brand` on the `.rating` root overrides fill tokens to brand green. No separate class per star needed.

7. **Interactive modifier.** `.rating--interactive` added for interactive rating input use cases. Not in manifest but needed for real-world usage. Documented as assumption.

---

## Layer Classification

| Figma layer    | Type       | Manifest context | Implementation         |
|----------------|------------|------------------|------------------------|
| Star 1 (STAR)  | Structural | Normal/Half      | SVG path in HTML       |
| Star 2 (RECT)  | Structural | Half fill        | SVG `rating__star-fill` with clip-path |
| Star 3 (RECT)  | Structural | Half empty mask  | Eliminated — clip-path handles this   |
| ring (RECT)    | Interaction| Pressed only     | `::before` pseudo-element             |

---

## State Delta Matrix

Base: empty star (`.rating__star--empty`)
| From base        | Delta                                              | CSS selector                              |
|------------------|----------------------------------------------------|-------------------------------------------|
| → Filled         | Star fill changes to secondary/primary color       | `.rating__star--filled .rating__star-icon`|
| → Half           | Left 50% of star filled, right 50% empty           | `.rating__star--half` + clip-path         |
| → Pressed (ring) | Ring appears behind star (neutral-100, circular)   | `.rating__star:active::before`            |
| → Brand modifier | Fill color changes from gold to green              | `.rating--brand .rating__star--filled`    |
| → Disabled       | All stars dimmed at 40% opacity                    | `.rating--disabled`                       |

---

## Pseudo-Element Decisions

| Figma layer   | Decision  | Reason                                                    |
|---------------|-----------|-----------------------------------------------------------|
| `ring` (RECT) | `::before`| Pure interaction/visual indicator, no semantic content    |

---

## Interaction Layer Decisions

- `ring` RECTANGLE → `.rating__star::before`
- Activated on `:active` (pressed) state
- Opacity transitions from 0 to 1 on press
- Sits at z-index 0 behind star at z-index 1

---

## Focus Layer Decisions

- No focus layer detected in manifest
- **Decision**: Use `:focus-visible` on `.rating__star` with `outline` for interactive rating
- Implemented as advisory/TODO since manifest does not define focus state
- Focus strategy: `:focus-visible` (keyboard-only visible focus per platform standard)

---

## Z-Index / Layering Decisions

```
z-index 0: .rating__star::before (ring — interaction layer)
z-index 1: .rating__star-icon, .rating__star-base (structural SVG)
z-index 2: .rating__star-fill (half fill overlay — only in half state)
```

`.rating__star` has `position: relative` as the stacking context.

---

## Intentional Deviations From Figma

1. **Half-star rectangle system replaced with clip-path.** Figma uses 3-layer (star base + 2 rectangles). HTML/CSS uses 2-layer (base SVG + fill SVG with clip-path). Visual output is equivalent.

2. **Star 3 (right-half neutral rectangle) eliminated.** In CSS, `clip-path: inset(0 50% 0 0)` limits the fill SVG to left 50% automatically. The empty base star (Star 1) shows through the right side without needing a masking rectangle.

3. **Star corner radius not reproduced.** Figma `cornerRadius-variable: --radius-radius-xs` on STAR shapes (rounded inner concave points) is not reproduced in SVG path. SVG polygon path has sharp inner corners. Deviation noted as low-severity visual difference.

4. **Pressed state ring uses opacity transition.** Figma shows a static pressed state. HTML/CSS adds `opacity: 0 → 1` transition for smooth interaction feedback. No negative visual impact.

---

## Risks

1. **WCAG 1.4.11 failure for default (gold) stars.** `#DBA102` on white does not meet 3:1 non-text contrast. Must be resolved with consumer/design before shipping to production.

2. **Interactive rating pattern not in manifest.** If this component is used as an input, the ARIA semantics must be added at consumption time. CSS only provides the visual layer.

3. **Half-star RTL direction.** `clip-path: inset(0 50% 0 0)` clips from the right side, showing the left half. In RTL contexts, the design intent is unclear. TODO added in CSS.

---

## Assumptions

1. "Normal" in _RatingStar items manifest = empty state (neutral-200 fill).
2. "Selected" in _RatingStar items = filled state (secondary/primary fill). Same visual structure as Normal.
3. The composite always renders exactly 5 stars. Template shows 3.5/5 as the example rating matching the manifest.
4. The `Brand=yes/No` distinction at the composite level corresponds to `Style=Brand/Default` at the item level.
5. The ring overhang of 3px on each side is intentional interaction affordance, not a layout artifact.
6. Disabled state is not shown in the manifest but is included as a standard platform requirement. Opacity 0.4 is a placeholder.

---

## Known Issues

1. **Typo in manifest:** `Size=Meduim` (should be `Size=Medium`) — recorded as-is. CSS uses `.rating--md` (corrected spelling).
2. **Missing fill on Normal/Selected in items manifest.** Fill colors are inferred from composite manifest and documented above.
3. **No hover state for the composite.** The Figma composite only shows static display. Hover state for interactive version is added as advisory.

---

## Missing Tokens

| Token                              | Proposed mapping                      |
|------------------------------------|---------------------------------------|
| `--rating-star-fill-default`       | `--Background-background-secondary`   |
| `--rating-star-fill-brand`         | `--Background-background-primary`     |
| `--rating-star-empty-fill`         | `--Background-background-neutral-200` |
| `--rating-star-half-base-fill`     | `--Colors-Gray-neutral-300`           |
| `--rating-star-pressed-ring-bg`    | `--Background-background-neutral-100` |
| `--rating-gap`                     | `--spacing-globalspacing-xs`          |
| `--rating-star-size-lg`            | 48px                                  |
| `--rating-star-size-md`            | 32px                                  |
| `--rating-star-size-sm`            | 24px                                  |
| `--rating-star-ring-size-lg`       | 54px                                  |
| `--rating-star-ring-size-md`       | 46px                                  |
| `--rating-star-ring-size-sm`       | 38px                                  |
| `--rating-star-ring-radius`        | `--radius-radius-full`                |
| `--rating-star-ring-transition-duration` | `--transition-fast` (proposed)  |
| `--rating-star-ring-transition-easing`   | `--ease-in-out` (proposed)      |
| `--rating-disabled-opacity`        | 0.4 (proposed)                        |

---

## Missing Standards

1. **Focus state definition for interactive rating.** No Figma variant exists. Must be added per platform focus standard before interactive usage.
2. **Hover state for interactive rating.** No Figma variant exists for the composite.
3. **Touch target guidance.** Stars at 24px (Small) meet the 24×24px minimum. No explicit touch target token or padding is defined.

---

## TODO

- [ ] Verify `#DBA102` (gold) star color against WCAG 1.4.11 (3:1 non-text contrast). Consider raising token to meet threshold.
- [ ] Add component-level tokens (`--rating-*`) to `token.css`.
- [ ] Confirm RTL half-star fill direction with design team.
- [ ] Define and add focus state for interactive rating usage.
- [ ] Verify whether `Normal` and `Selected` _RatingStar states have visual differences (fill colors not explicit in items manifest).
- [ ] Consider rounded star SVG path to match Figma corner radius on star inner points.
- [ ] Add disabled state variant to Figma manifest.
