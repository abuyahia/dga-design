# Component Analysis

- Manifest path: `components/checkbox/manifest.json`
- Component name: Checkbox

---

## Source

Figma plugin export. 5042-line JSON array. 108 COMPONENT entries.

---

## Detected Anatomy

| Part | Figma name | CSS class | Role |
|------|-----------|-----------|------|
| Root | COMPONENT root | `.checkbox` | Outer container; carries size, style, state modifiers |
| Control | `_CheckboxBase1` | `.checkbox__control` | Visual box; receives border (unchecked) or background (checked/indeterminate) |
| Checkmark container | `checkmark` | `.checkbox__checkmark` | overflow-hidden frame; visible when checked + not indeterminate |
| Indeterminate mark container | `Indeterminate mark` | `.checkbox__indeterminate-mark` | overflow-hidden frame; visible when indeterminate |
| Icon vector | `Icon` | `.checkbox__icon` | SVG shape; fill: `--checkbox-icon-oncolor` |
| Focus ring | `Focus Ring` | `.checkbox__focus-ring` | Absolute overlay; visible on Focused state only |

---

## Detected Axes

| Axis | Values |
|------|--------|
| Checked | `True`, `False` |
| Indeterminate | `True` (only when Checked=True), `False` |
| State | `Default`, `Hovered`, `Pressed`, `Focused`, `Read-only`, `Disabled` |
| Size | `Medium` (24px), `Small` (20px), `x Small` (16px) |
| Style | `Primary`, `Neutral` |

---

## Detected Variants

**3 check-states × 6 interaction-states × 3 sizes × 2 styles = 108 Figma components.**

Check-states:
- **Unchecked** — Checked=False, Indeterminate=False
- **Checked** — Checked=True, Indeterminate=False
- **Indeterminate** — Checked=True, Indeterminate=True

Note: `Checked=False, Indeterminate=True` does not appear in the manifest. This combination is architecturally invalid.

---

## Detected States

| State | Figma visual delta | CSS implementation |
|-------|-------------------|-------------------|
| Default | Base styles | `.checkbox` base |
| Hovered | **Identical to Default** in Figma CSS | `:hover` + `--checkbox-bg-hover` (missing token) |
| Pressed | **Identical to Default** in Figma CSS | `:active` + `--checkbox-bg-pressed` (missing token) |
| Focused | Adds absolute focus ring −4px offset, 2px inset shadow | `.checkbox--focused` + `input:focus-visible` |
| Read-only | `opacity: 0.7` on root | `.checkbox--readonly` |
| Disabled | `opacity: 0.5` on root | `.checkbox--disabled` |

---

## Detected Sizes

| Modifier | Dimension | Focus ring outer size |
|----------|-----------|-----------------------|
| `.checkbox--md` | 24×24px | 32×32px (−4px offset) |
| `.checkbox--sm` | 20×20px | 28×28px (−4px offset) |
| `.checkbox--xs` | 16×16px | 24×24px (−4px offset) |

Icon dimensions:

| Size | Checkmark W×H | Indeterminate W×H |
|------|--------------|-------------------|
| Medium | 12×9.116px | 12×3px |
| Small | 10×7.596px | 10×2.5px |
| x Small | 8×6.077px | 8×2px |

---

## Architecture Findings

1. **Standalone control only.** This is the checkbox box, not a labeled checkbox. Labels belong at the form-field assembly level.
2. **Hover and Pressed are visually undifferentiated in Figma.** Interaction feedback must be added via CSS pseudo-classes using missing tokens.
3. **Focus ring uses `mix-blend-mode: multiply`.** Absolute sibling of `.checkbox__control`, extending 4px outside all edges, 2px inset box-shadow.
4. **Indeterminate background matches checked.** Figma shows the same `background-selected` for both checked and indeterminate. The indeterminate icon (horizontal bar) is the only visual differentiator.
5. **Style axis affects selected background only.** Primary = green `#1B8354`. Neutral = dark `#161616`. Border, icon color, and opacity states are identical.

---

## Token Findings

| Figma token | Fallback | Mapped component token |
|-------------|---------|----------------------|
| `--Checkbox-checkbox-border-unselected` | `#161616` | `--checkbox-border-unselected` |
| `--Checkbox-checkbox-background-selected` | `#1B8354` | `--checkbox-bg-selected-primary` |
| `--Checkbox-checkbox-background-selected-neutral` | `#161616` | `--checkbox-bg-selected-neutral` |
| `--Checkbox-checkbox-icon-oncolor` | `#FFF` | `--checkbox-icon-oncolor` |
| `--Checkbox-checkbox-focus-ring` | `#161616` | `--checkbox-focus-ring-color` |
| `--Radius-radius-xs` | `2px` | `--checkbox-border-radius` (maps to global) |

---

## Accessibility Findings

1. Must use native `<input type="checkbox">` (visually hidden) with a custom visual overlay for full accessibility compliance.
2. Focus ring satisfies WCAG 2.4.7 pending contrast ratio audit against adjacent backgrounds.
3. Indeterminate state must expose `aria-checked="mixed"`.
4. Disabled must use `disabled` attribute. `aria-disabled="true"` is an acceptable alternative when the element must remain discoverable.
5. Read-only must expose `aria-readonly="true"` and suppress interaction without removing from tab order.
6. Checkmark and indeterminate mark SVGs must carry `aria-hidden="true"` — state is communicated by native input semantics.

---

## Compliance Findings

- Focused state: focus ring present. WCAG 2.4.7 supportable.
- Disabled (opacity 0.5): WCAG 1.4.3 exemption applies for inactive UI components.
- Read-only (opacity 0.7): NOT exempt. Contrast requires verification in deployment context.
- **Error/invalid state absent from manifest** — required for government form validation (WCAG 3.3.1).

---

## Implementation Decisions

1. Visually hidden native `<input type="checkbox">` paired with custom `.checkbox` span. JS syncs check/indeterminate state and adds modifier classes.
2. Focus ring: `.checkbox__focus-ring` child span, absolute, −4px offset. Also activated via `input:focus-visible ~ .checkbox .checkbox__focus-ring`.
3. Icon SVGs: inline SVGs embedded in template. Figma vector paths not exported in manifest — standard checkmark and dash shapes used as proxies. Confirm before production.
4. State modifiers: `.checkbox--checked`, `.checkbox--indeterminate`, `.checkbox--focused`, `.checkbox--readonly`, `.checkbox--disabled`.
5. Hover/active also respond to `:hover`/`:active` pseudo-classes in addition to explicit modifier classes.

---

## Intentional Deviations From Figma

1. **Hover/pressed visual feedback added.** Figma shows no visual delta. `--checkbox-bg-hover` applied as subtle background on unchecked hover. Token flagged as missing.
2. **Visually hidden native input included.** Figma has no equivalent; required for accessibility.
3. **Focus ring fires on `:focus-visible` only**, suppressing it for pointer clicks. Figma represents focus as a static variant.

---

## Risks

1. No error/invalid state — required for government forms.
2. Hover/pressed tokens undefined — consuming teams must define them.
3. Read-only opacity 0.7 may fail WCAG 1.4.3 on light backgrounds.
4. SVG paths approximate — confirm actual Figma paths before production release.

---

## Assumptions

1. Label text is out of scope for this component.
2. `--Radius-radius-xs` is globally defined at 2px.
3. Indeterminate state is only valid in a parent/children selection context (checked + partially selected children).

---

## Known Issues

None at generation time.

---

## Missing Tokens

```
--checkbox-bg-hover
--checkbox-bg-pressed
--checkbox-opacity-readonly
--checkbox-opacity-disabled
--checkbox-focus-ring-offset
--checkbox-focus-ring-width
--checkbox-transition-duration
--checkbox-transition-easing
```

---

## Missing Standards

- Error/invalid state (WCAG 3.3.1, government forms).

---

## TODO

- [ ] Define `--checkbox-bg-hover` and `--checkbox-bg-pressed` in token.css
- [ ] Define `--checkbox-opacity-readonly` (0.7) and `--checkbox-opacity-disabled` (0.5) in token.css
- [ ] Define `--checkbox-focus-ring-offset` (4px) and `--checkbox-focus-ring-width` (2px) in token.css
- [ ] Define `--checkbox-transition-duration` and `--checkbox-transition-easing` in token.css
- [ ] Add error/invalid state to manifest and regenerate
- [ ] Confirm checkmark and indeterminate SVG paths from Figma source
- [ ] Audit focus ring contrast (WCAG 2.4.11)
- [ ] Audit read-only opacity 0.7 against WCAG 1.4.3 for deployment backgrounds
