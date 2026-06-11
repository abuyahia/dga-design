# Slider — Component Contract

```
contract_version: 1.0.0
component_id:     slider
status:           draft
category:         form-input
last_reviewed:    2026-06-12
```

---

## Component Type

- Primitive

## Dependencies

- None

---

## 1. Purpose

A Slider lets the user select a numeric value (or range of values) by dragging one or two thumbs along a track. Use it when the exact value matters less than exploring a continuous range — for example, volume, opacity, or budget filters.

---

## 2. When to Use / When NOT to Use

| Situation | Use Slider? |
|---|---|
| User selects from a continuous numeric range | Yes |
| User selects a bounded min–max range | Yes — Range mode |
| Exact numeric input is required | No — use a text input with numeric validation |
| Discrete set of choices (3–5 options) | No — use radio buttons or a select |
| Binary toggle | No — use a toggle/switch |

---

## 3. Anatomy

```
.slider                          ← root (div)
  .slider__label-text            ← label (label, optional)
  .slider__track-row             ← track + value row (div)
    .slider__value               ← start/current value display (output, optional)
    .slider__control-wrap        ← positioning wrapper (div)
      .slider__track             ← full-width background bar (div, aria-hidden)
        .slider__fill            ← filled portion (div, aria-hidden)
      .slider__input             ← range input (input[type="range"])
      .slider__input--end        ← end range input (input[type="range"], Range only)
    .slider__value--end          ← end value display (output, Range only)
  .slider__helper                ← helper text row (div, optional)
    .slider__helper-icon         ← icon slot (span)
    .slider__helper-text         ← helper text (span)
```

---

## 4. HTML Contract

### Single-value slider (minimum)

```html
<div class="slider" data-component="slider">
  <label class="slider__label-text" for="slider-1">Label</label>
  <div class="slider__track-row">
    <div class="slider__control-wrap">
      <div class="slider__track" aria-hidden="true">
        <div class="slider__fill" style="--fill: 20%"></div>
      </div>
      <input type="range" class="slider__input" id="slider-1"
             min="0" max="100" value="20"
             aria-describedby="slider-1-helper">
    </div>
    <output class="slider__value" for="slider-1" aria-hidden="true">20</output>
  </div>
  <div class="slider__helper" id="slider-1-helper">
    <span class="slider__helper-icon" aria-hidden="true"><!-- icon --></span>
    <span class="slider__helper-text">Help Text</span>
  </div>
</div>
```

### Range slider

```html
<div class="slider slider--range" data-component="slider">
  <label class="slider__label-text" id="range-lbl">Price Range</label>
  <div class="slider__track-row">
    <output class="slider__value" aria-hidden="true">20</output>
    <div class="slider__control-wrap">
      <div class="slider__track" aria-hidden="true">
        <div class="slider__fill" style="--fill-start: 20%; --fill-end: 70%"></div>
      </div>
      <input type="range" class="slider__input" min="0" max="100" value="20"
             aria-label="Minimum value" aria-labelledby="range-lbl"
             aria-describedby="range-helper">
      <input type="range" class="slider__input slider__input--end"
             min="0" max="100" value="70"
             aria-label="Maximum value" aria-labelledby="range-lbl"
             aria-describedby="range-helper">
    </div>
    <output class="slider__value slider__value--end" aria-hidden="true">70</output>
  </div>
  <div class="slider__helper" id="range-helper">
    <span class="slider__helper-icon" aria-hidden="true"><!-- icon --></span>
    <span class="slider__helper-text">Help Text</span>
  </div>
</div>
```

### Size modifier

```html
<!-- Small (default) -->
<div class="slider">...</div>

<!-- Medium -->
<div class="slider slider--md">...</div>
```

### RTL

```html
<div class="slider" dir="rtl">...</div>
<!-- or set dir="rtl" on a parent element -->
```

### Disabled

```html
<div class="slider" aria-disabled="true">
  ...
  <input type="range" class="slider__input" disabled>
  ...
</div>
```

---

## 5. CSS Modifier Reference

| Class | Description |
|---|---|
| `.slider` | Root element. Default = Small size, LTR, single value |
| `.slider--md` | Medium size modifier |
| `.slider--range` | Range (dual-thumb) mode |
| `.slider__input--end` | End thumb input in Range mode |
| `.slider__value--end` | End value display in Range mode |

---

## 6. State Reference

| State | Selector | Visual change |
|---|---|---|
| Default | `.slider` | Base styles |
| Thumb hovered | `.slider__input:hover` | Thumb scale 1.1 |
| Thumb focused | `.slider__input:focus-visible` | Focus outline ring |
| Disabled | `.slider[aria-disabled="true"]` | Opacity 0.4, not-allowed cursor |
| RTL | `[dir="rtl"] .slider` | Fill and layout mirrored |

---

## 7. ARIA Contract

| Attribute | Element | Required | Notes |
|---|---|---|---|
| `type="range"` | `input` | Always | Semantic slider element |
| `min`, `max`, `value` | `input` | Always | Numeric bounds and current value |
| `aria-describedby` | `input` | Recommended | Points to helper text id |
| `aria-label` | Each `input` | Range mode | "Minimum value" / "Maximum value" (localize for Arabic) |
| `aria-labelledby` | Each `input` | Range mode | Points to shared label id |
| `aria-hidden="true"` | `.slider__track`, `.slider__fill`, `.output` | Required | Decorative elements hidden from AT |
| `for` | `label.slider__label-text` | Recommended | Associates label with input id |
| `disabled` | `input` | Disabled state | Native disabled attribute |

---

## 8. Token Reference

All `--slider-*` tokens are pending addition to `token.css`. Fallback values are sourced from the manifest.

| Token | Fallback | Usage |
|---|---|---|
| `--slider-track-bg` | `#F3F4F6` | Track background |
| `--slider-fill-bg` | `#1B8354` | Fill / thumb color |
| `--slider-thumb-fill` | `#1B8354` | Thumb circle fill |
| `--slider-thumb-stroke` | `#067647` | Thumb circle border |
| `--slider-label-color` | `#161616` | Label text |
| `--slider-value-color` | `#384250` | Value/percentage text |
| `--slider-helper-color` | `#384250` | Helper text |
| `--slider-track-radius` | `4px` | Track and fill radius |
| `--slider-sm-track-height` | `4px` | Small track height |
| `--slider-md-track-height` | `8px` | Medium track height |
| `--slider-sm-thumb-size` | `12px` | Small thumb diameter |
| `--slider-md-thumb-size` | `16px` | Medium thumb diameter |
| `--slider-disabled-opacity` | `0.4` | Disabled state opacity |
| `--slider-focus-ring-color` | `#1B8354` | Focus ring color |
| `--slider-focus-ring-width` | `2px` | Focus ring width |
| `--slider-focus-ring-offset` | `2px` | Focus ring offset |

---

## 9. Focus Behavior

Focus strategy: `:focus-visible` (keyboard-only focus indicator).

The focus ring renders as an outline on the `input[type="range"]` element using:
```css
.slider__input:focus-visible {
  outline: var(--slider-focus-ring-width, 2px) solid var(--slider-focus-ring-color, #1B8354);
  outline-offset: var(--slider-focus-ring-offset, 2px);
}
```

Rationale: no explicit Focus Ring layer in the Figma manifest. Platform accessibility standard requires visible keyboard focus. `:focus-visible` is used (not `:focus`) to suppress focus rings on mouse interaction.

---

## 10. JavaScript Contract

The `.slider__fill` element's `--fill` CSS custom property must be updated by JavaScript as the input value changes:

```js
const input = slider.querySelector('.slider__input');
const fill  = slider.querySelector('.slider__fill');
function updateFill() {
  const pct = ((input.value - input.min) / (input.max - input.min)) * 100;
  fill.style.setProperty('--fill', pct + '%');
}
input.addEventListener('input', updateFill);
updateFill(); // initialise on load
```

For Range mode, `--fill-start` and `--fill-end` must both be updated, and the z-index of overlapping thumbs must be managed:

```js
/* Range fill positioning */
const startInput = slider.querySelector('.slider__input');
const endInput   = slider.querySelector('.slider__input--end');
function updateRangeFill() {
  const min  = +startInput.min;
  const max  = +startInput.max;
  const s    = ((startInput.value - min) / (max - min)) * 100;
  const e    = ((endInput.value   - min) / (max - min)) * 100;
  fill.style.setProperty('--fill-start', Math.min(s, e) + '%');
  fill.style.setProperty('--fill-end',   (100 - Math.max(s, e)) + '%');
  /* z-index swap when thumbs are close */
  endInput.style.zIndex = (s > e) ? '3' : '';
}
[startInput, endInput].forEach(i => i.addEventListener('input', updateRangeFill));
updateRangeFill();
```

For RTL: multiply fill percentage by `-1` and use `right` instead of `left` — or apply `transform: scaleX(-1)` to the track wrapper and `scaleX(-1)` to the input.

---

## 11. RTL Behavior

When `dir="rtl"` is set on the slider root or any ancestor:

- Fill grows from right to left.
- Thumb starts at the right end (value = min).
- Value text position is reversed (start value on right, end value on left in Range mode).
- Label and helper text align to the right.
- `input[type="range"]` direction is set to `rtl` via CSS.

---

## 12. Known Limitations

- Range slider thumb z-index management requires JavaScript.
- No native cross-browser solution for styling both thumbs independently without JS.
- All `--slider-*` tokens are pending `token.css` update.
