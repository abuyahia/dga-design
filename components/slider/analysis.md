# Component Analysis

- **Manifest path:** `components/slider/mainifest.json`
- **Component name:** Slider

---

## Source

Figma COMPONENT_SET exported via Platform Code plugin. Contains 30+ component variants named using the pattern `Size=[Small|Medium], Persentage=[0|20|50|100|0 - 50|20 - 70], Range=[No|Yes], RTL=[No|Yes]`.

---

## Detected Anatomy

```
.slider                          ← root (inline-flex, column)
  .slider__label                 ← label container (flex, column)
    .slider__label-text          ← label text (Form-field-text-label color)
  .slider__track-row             ← track + value row (flex, row, gap: spacing-sm)
    .slider__value               ← single or start value text (optional, aria-hidden)
    .slider__control-wrap        ← relative positioning wrapper (width: 320px)
      .slider__track             ← full-width background bar (neutral-100)
        .slider__fill            ← filled portion (background-primary)
      .slider__input             ← <input type="range"> (transparent, full-width)
      .slider__input--end        ← [Range only] second range input
    .slider__value               ← current or end value text (aria-hidden)
  .slider__helper                ← helper text row (flex, row, gap: spacing-formicon)
    .slider__helper-icon         ← icon wrapper (16×16)
    .slider__helper-text         ← helper text (text-primary-paragraph)
```

---

## Detected Axes

| Axis | Values | CSS strategy |
|------|--------|-------------|
| Size | Small, Medium | `.slider--sm` (default) / `.slider--md` modifier |
| Range | No, Yes | `.slider--range` modifier |
| RTL | No, Yes | `[dir="rtl"]` selector — meaningful CSS differences confirmed |

---

## Detected Variants

| Figma axis | Axis type | CSS action |
|---|---|---|
| Size | Structural | Modifier class |
| Range | Structural | Modifier class |
| RTL | Layout | `[dir="rtl"]` selector |
| Persentage | **Data / runtime** | Discarded as structural variant — see §Discarded Axes |

Meaningful variant matrix: 2 sizes × 2 range modes × 2 directions = 8 structural variants.

---

## Detected States

No explicit Hover / Pressed / Focused / Disabled Figma frames were present in this export. Standard interactive states are implemented from platform accessibility standards:

| State | CSS selector |
|---|---|
| Default | `.slider` |
| Hovered (thumb) | `.slider__input:hover::-webkit-slider-thumb` |
| Focused (thumb) | `.slider__input:focus-visible` + `::after` ring |
| Disabled | `.slider[aria-disabled="true"]` / `.slider__input:disabled` |

---

## Detected Sizes

| Size | Track height | Thumb diameter | Label font | Helper font |
|------|-------------|----------------|------------|-------------|
| Small | 4px | 12px | 14px / 20px lh | 12px / 18px lh (typo-size-text-xs) |
| Medium | 8px | 16px | 16px / 24px lh | 14px / 20px lh (typo-size-text-sm) |

---

## Architecture Findings

1. **ELLIPSE "Control" is inside Progress fill in Figma.** In Figma, the thumb is a child of the fill frame, positioned at its trailing edge. In HTML, the thumb (`input[type="range"]`) must span the full track for correct pointer interaction. The thumb visual (via `::thumb` pseudo-element) floats over the fill via stacked positioning.

2. **Persentage is a Figma axis representing data state, not a component variant.** The Figma team created multiple frames (0, 20, 50, 100) to show different slider positions. These are all the same component with different values. A single template with a CSS custom property `--slider-fill-pct` driven by JavaScript covers all positions.

3. **Range slider uses two thumbs.** The Range=Yes variants show two Control ellipses inside one Progress fill. Implementation uses two `<input type="range">` elements overlaid on the same track, with z-index management.

4. **RTL produces meaningful CSS differences.** The component root alignment, label alignment, value text position (order), fill direction, and text-align all change for RTL. Confirmed as a real implementation axis (not discarded).

5. **Track width is 320px in Figma static frames.** In implementation, the track uses `width: 100%` on `.slider__control-wrap` to be responsive. The 320px is a Figma canvas constraint, not a design intent.

6. **Gap between Progress Bar elements in Figma is negative (-46px).** This is a Figma layout artifact for overlapping the thumb with the fill. Not replicated in HTML — thumb overlap achieved via absolute positioning.

---

## Token Findings

| Token used in CSS | Source in manifest | Status |
|---|---|---|
| `--slider-track-bg` | `--Background-background-neutral-100` | MISSING — pending |
| `--slider-fill-bg` | `--Background-background-primary` | MISSING — pending |
| `--slider-thumb-fill` | `--Background-background-primary` | MISSING — pending |
| `--slider-thumb-stroke` | `--Border-border-success` | MISSING — pending |
| `--slider-label-color` | `--Form-field-text-label` | MISSING — pending |
| `--slider-value-color` | `--Text-text-primary-paragraph` | MISSING — pending |
| `--slider-helper-color` | `--Text-text-primary-paragraph` | MISSING — pending |
| `--slider-track-radius` | `--Radius-radius-sm` | MISSING — pending |
| `--slider-gap` | `--Global-spacing-xs` | MISSING — pending |
| `--slider-track-row-gap` | `--Global-spacing-sm` | MISSING — pending |
| `--slider-helper-gap` | `--Form-icon-helpertext` | MISSING — pending |
| `--slider-label-gap` | `--Form-label-gap` | MISSING — pending |
| `--slider-sm-track-height` | 4px (Figma direct) | MISSING — pending |
| `--slider-md-track-height` | 8px (Figma direct) | MISSING — pending |
| `--slider-sm-thumb-size` | 12px (Figma direct) | MISSING — pending |
| `--slider-md-thumb-size` | 16px (Figma direct) | MISSING — pending |
| `--slider-sm-label-font-size` | 14px (Figma Small label) | MISSING — pending |
| `--slider-md-label-font-size` | 16px (Figma Medium label) | MISSING — pending |
| `--slider-sm-helper-font-size` | `--Size-Text-typo-size-text-xs` | MISSING — pending |
| `--slider-md-helper-font-size` | `--Size-Text-typo-size-text-sm` | MISSING — pending |
| `--slider-disabled-opacity` | Not in manifest | MISSING — assumed 0.4 |
| `--slider-focus-ring-color` | Not in manifest | MISSING — assumed primary |
| `--slider-focus-ring-width` | Not in manifest | MISSING — assumed 2px |

All `--slider-*` tokens are declared as CSS custom properties with fallback values in `slider.css`. No tokens exist in `token.css` at this time.

---

## Accessibility Findings

1. **Native `<input type="range">` required.** The ELLIPSE control in Figma is a visual metaphor for a native range input. Native `<input type="range">` provides keyboard navigation (arrow keys), screen reader announcements, and ARIA role automatically.

2. **Range slider ARIA.** For Range=Yes mode: two inputs must each have `aria-label` ("Minimum value" / "Maximum value") or be associated with a visible label via `aria-labelledby`.

3. **Focus ring.** The Figma manifest contains no explicit Focus Ring layer. Implementing via `input:focus-visible` outline in platform green. Documented as implementation decision.

4. **Value output.** The Figma "Persentage" text is rendered as an `<output>` element associated with the input via `for=` attribute for live announcements.

5. **Helper text.** Must be associated with the input via `aria-describedby` for screen reader support.

---

## Compliance Findings

- No `--slider-*` tokens exist in `token.css`. All token references use inline fallbacks.
- No Focus state in Figma — implemented from platform accessibility standards.
- No Disabled state in Figma — implemented from platform accessibility standards.
- `official_compliance_claim: false` — pending audit.

---

## Implementation Decisions

| Decision | Rationale |
|---|---|
| Use `<input type="range">` | Semantic HTML; keyboard + screen reader support built-in |
| Use CSS custom property `--slider-fill-pct` for fill width | Decoupled from JS update mechanism; single source |
| Two overlaid `<input type="range">` for Range mode | Standard dual-handle pattern; avoids custom ARIA complexity |
| `[dir="rtl"]` selector for RTL | Respects platform convention; consistent with other components |
| `input[type="range"]` transparent with styled `::thumb` | Matches Figma visual without duplicating semantic elements |
| Track width 100% (not 320px) | Figma 320px is canvas artifact; responsive is correct |
| Focus ring via `input:focus-visible` outline | No Focus Layer in Figma; platform standard used |
| Disabled via `aria-disabled="true"` + `pointer-events: none` | Matches other platform components |

---

## Intentional Deviations From Figma

1. **Track width:** 100% fluid, not fixed 320px.
2. **Negative gap (-46px):** Not replicated; absolute positioning used instead.
3. **Thumb inside fill:** Thumb positioned via CSS `::thumb`, not as child of fill div.
4. **Persentage axis discarded:** Runtime data, not structural variant.
5. **Focus ring added:** Not present in Figma; required for accessibility compliance.
6. **Disabled state added:** Not present in Figma; required for accessibility compliance.

---

## Risks

- Range slider thumb z-index management — when thumbs overlap, the top thumb must receive pointer events. Requires JS to swap z-index.
- RTL fill direction for range slider — both fill start and end positions must update.
- `input[type="range"]` thumb styling is cross-browser inconsistent (`::-webkit-slider-thumb`, `::-moz-range-thumb`). Both selectors are included.

---

## Assumptions

1. The "Persentage" Figma axis represents static preview states, not component variants.
2. Default size is Small (`.slider` without modifier = small).
3. Helper text with icon is optional (component should render without it).
4. Label is optional (component should render without it).
5. Disabled opacity fallback is 0.4 (platform convention assumed from button).
6. Focus ring color uses `--slider-fill-bg` (platform green) — same as fill.

---

## Known Issues

- No `--slider-*` tokens in `token.css`. All fallbacks are temporary.
- Range slider JavaScript (for z-index swap and fill positioning) is not included in `template.html`. A comment block documents the required JS.

---

## Missing Tokens

All `--slider-*` tokens listed in §Token Findings are missing from `token.css`. Required global update — not applied automatically. Proposed mappings:

```css
/* Add to token.css: */
--slider-track-bg:            var(--Background-background-neutral-100);
--slider-fill-bg:             var(--Background-background-primary);
--slider-thumb-fill:          var(--Background-background-primary);
--slider-thumb-stroke:        var(--Border-border-success);
--slider-label-color:         var(--Form-field-text-label);
--slider-value-color:         var(--Text-text-primary-paragraph);
--slider-helper-color:        var(--Text-text-primary-paragraph);
--slider-track-radius:        var(--Radius-radius-sm);
--slider-gap:                 var(--Global-spacing-xs);
--slider-track-row-gap:       var(--Global-spacing-sm);
--slider-helper-gap:          var(--Form-icon-helpertext);
--slider-label-gap:           var(--Form-label-gap);
--slider-sm-track-height:     4px;
--slider-md-track-height:     8px;
--slider-sm-thumb-size:       12px;
--slider-md-thumb-size:       16px;
--slider-sm-label-font-size:  14px;
--slider-sm-label-line-height: 20px;
--slider-md-label-font-size:  16px;
--slider-md-label-line-height: 24px;
--slider-sm-helper-font-size: var(--Size-Text-typo-size-text-xs);
--slider-sm-helper-line-height: var(--Line-Height-Text-line-heights-text-xs);
--slider-md-helper-font-size: var(--Size-Text-typo-size-text-sm);
--slider-md-helper-line-height: var(--Line-Height-Text-line-heights-text-sm);
--slider-disabled-opacity:    0.4;
--slider-focus-ring-color:    var(--Background-background-primary);
--slider-focus-ring-width:    2px;
--slider-focus-ring-offset:   2px;
```

---

## Missing Standards

- No explicit Focus layer or Disabled state in Figma manifest. These are implemented from platform accessibility standards as required.

---

## Component Classification

**Primitive Component** — self-contained form input with no required child component dependencies.

---

## Component Dependencies

- None.

---

## Dependency Confirmation

N/A — Primitive. No confirmation required.

---

## Layer Classification

| Layer name | Type | HTML/CSS implementation |
|---|---|---|
| Progress Bar (frame) | Structural | `.slider__track` |
| Progress (frame / fill) | Structural | `.slider__fill` |
| Control (ELLIPSE) | Structural | `input[type="range"]` + `::thumb` pseudo |
| Label (INSTANCE) | Structural | `<label class="slider__label-text">` |
| Persentage (TEXT) | Structural (data) | `<output class="slider__value">` |
| Helper text (FRAME) | Structural | `.slider__helper` |
| Feedback Icon (INSTANCE) | Icon | `.slider__helper-icon` (SVG) |
| Interaction Circle | Interaction | N/A — not present in manifest |
| Focus Ring | Focus | `input:focus-visible` outline / `::after` |

---

## State Delta Matrix

| Property | Default | Hovered | Focused | Disabled |
|---|---|---|---|---|
| Thumb fill | `--slider-thumb-fill` | same | same | opacity 0.4 |
| Thumb stroke | `--slider-thumb-stroke` | same | + focus ring | none |
| Fill bg | `--slider-fill-bg` | same | same | opacity 0.4 |
| Track bg | `--slider-track-bg` | same | same | opacity 0.4 |
| Thumb scale | 1 | 1.1 | 1 | 1 |
| Cursor | pointer | pointer | pointer | not-allowed |

---

## Pseudo-Element Decisions

| Pseudo | Usage |
|---|---|
| `::-webkit-slider-thumb` | Thumb visual (circle) on WebKit/Blink |
| `::-moz-range-thumb` | Thumb visual (circle) on Firefox |
| `::-webkit-slider-runnable-track` | Track reset on WebKit |
| `::-moz-range-track` | Track reset on Firefox |
| `input:focus-visible` outline | Focus ring |

No Interaction Circle or Ripple layer present in manifest. No `::before` interaction layer required.

---

## Interaction Layer Decisions

No interaction layers in manifest. Not applicable.

---

## Focus Layer Decisions

No Focus Ring layer in manifest. Implemented via native `input:focus-visible` outline using `--slider-focus-ring-color` and `--slider-focus-ring-width`. Focus strategy: `:focus-visible` (keyboard-only focus indicator per platform convention).

---

## Z-Index / Layering Decisions

```
.slider__control-wrap: position: relative
  .slider__track:        position: absolute, z-index: 0  (track bg)
  .slider__fill:         position: absolute, z-index: 1  (fill overlay)
  .slider__input:        position: relative, z-index: 2  (transparent, pointer events)
  .slider__input--end:   position: relative, z-index: 3  (range: top input)
```

Range slider: when thumbs overlap, z-index is swapped via JavaScript to ensure the "ahead" thumb receives pointer events.

---

## Severity Classification

### High
- Missing `--slider-*` tokens in `token.css` — all visual values are using fallbacks. Blocking for production.

### Medium
- Range slider requires JavaScript for fill positioning and thumb z-index management. Not included in static template.
- Cross-browser `::thumb` styling requires both WebKit and Firefox selectors.

### Low
- "Persentage" typo in Figma manifest preserved in analysis; corrected to "Percentage" in all generated files.
- Helper text icon (`help-circle`) uses a generic SVG placeholder — actual icon component integration required.

### Advisory
- Consider implementing slider as a Web Component for encapsulation of JS logic.
- Token.css update required before production use.
- Range slider ARIA labeling should be reviewed for localization (Arabic "القيمة الدنيا" / "القيمة القصوى").

---

## Assembly Awareness

Slider may participate in form assemblies:

```
slider → form-field → form
```

Reusable boundary preserved. No child components collapsed.

---

## TODO

- [ ] Add all `--slider-*` tokens to `token.css` (see §Missing Tokens)
- [ ] Integrate actual `help-circle` icon component into helper text slot
- [ ] Implement Range slider JavaScript in a `slider.js` companion file
- [ ] Review Range slider ARIA labeling for Arabic localization
- [ ] Audit focus ring color contrast against all background contexts
- [ ] Verify cross-browser thumb styling (Safari, Firefox, Chrome)
