# Component Analysis

- **Manifest path**: `components/divider/mainifest.json` ⚠️ filename typo — `mainifest` not `manifest`. Do not rename; treat as source of truth.
- **Component name**: Divider
- **Analysis date**: 2026-06-12
- **Analyst**: Platform Component Builder (automated)

---

## Source

- `mainifest.json` — Figma plugin export, `COMPONENT_SET` containing 8 `COMPONENT` nodes.
- Manifest file size: ~3.9 KB.
- Variants: 4 colors × 2 line types = 8 total.

---

## Component Classification

**Primitive Component**

The Divider has no required or optional child component dependencies. It is a self-contained visual and semantic element with no interactive states.

---

## Component Dependencies

**Required:** None

**Optional:** None

---

## Dependency Confirmation

Not applicable — Primitive component. Proceeding without confirmation step.

---

## Detected Anatomy

```
.divider           ← root element (<hr> or <div role="separator">)
                     — the element IS its own visual representation
```

Figma child elements:

| Figma element | Figma type | Implementation |
|---|---|---|
| `Divider` (in Horizontal variants) | RECTANGLE | The root element itself. No child HTML needed. |
| `Line 1` (in Vertical variants) | LINE | The root element itself. No child HTML needed. |

Both the RECTANGLE and LINE are the visual element — they carry only `background` and dimensional CSS. The root element absorbs both with no child elements in HTML.

---

## Detected Axes

| Axis | Values | CSS mapping |
|---|---|---|
| Color | Neutral, Primary, Alpha-white, White | modifier classes |
| Line Type | Horizontal, Vertical | modifier class `.divider--vertical` |

No RTL axis present. Dividers are direction-neutral — horizontal/vertical orientation does not change with reading direction.

---

## Detected Variants

Total Figma variants: **8** (4 colors × 2 line types)

| ID | Color | Line Type |
|---|---|---|
| neutral-horizontal | Neutral | Horizontal |
| primary-horizontal | Primary | Horizontal |
| alpha-white-horizontal | Alpha-white | Horizontal |
| white-horizontal | White | Horizontal |
| neutral-vertical | Neutral | Vertical |
| primary-vertical | Primary | Vertical |
| alpha-white-vertical | Alpha-white | Vertical |
| white-vertical | White | Vertical |

---

## Detected States

**None.** The Divider is a static, non-interactive element. It has no hover, focus, pressed, active, disabled, or read-only states.

---

## Detected Sizes

**No size axis in manifest.** All variants use 1px thickness. The Figma dimensions (192px width/height) are layout preview values, not component constraints. The component expands to fill its container.

---

## Architecture Findings

1. **Root element is the line** — Unlike most components that have a container plus inner elements, the Divider root element IS the visual line. No child HTML elements needed.

2. **`<hr>` as semantic element** — HTML `<hr>` has implicit `role="separator"`, maps to a thematic break in HTML5, and is the correct semantic choice for a divider. CSS resets (`border: none`, `margin: 0`) convert it to a fully token-driven element.

3. **Vertical via CSS only** — Figma uses `width: 0; height: 192px` for vertical variants with a LINE child of `width: 1px`. In CSS, `.divider--vertical` flips the dimensions: `height: 100%; width: 1px`. No structural change needed.

4. **Decorative vs. semantic** — The Divider may be used either semantically (as a thematic break) or decoratively (purely visual). Contract documents both use cases with appropriate ARIA guidance.

5. **No fixed width/height** — Figma preview uses 192px as a canvas constraint. The component should be 100% width (horizontal) or `align-self: stretch` (vertical) to fit its container.

6. **`<hr>` resets required** — Browsers add default `margin` and render `<hr>` as a border-based element. All browser defaults must be reset in CSS.

---

## Layer Classification

| Layer | Figma name | Role | HTML mapping |
|---|---|---|---|
| `Divider` (RECTANGLE) | Horizontal line element | Structural | Root `<hr>` element |
| `Line 1` (LINE) | Vertical line element | Structural | Root `<hr>` element |

No Interaction Layer, Focus Layer, or Icon Layer detected.

No pseudo-elements required.

---

## State Delta Matrix

No interactive states. No delta analysis required.

The Divider has one visual configuration per variant: color × direction. These are fully expressed as modifier classes.

---

## Pseudo-Element Decisions

**None required.** The element itself is the visual. No overlays, ripples, focus rings, or interaction layers exist in any variant.

---

## Interaction Layer Decisions

**None.** The Divider has no interaction layers.

---

## Focus Layer Decisions

**No focus indicator implemented.** The Divider is a non-interactive element. It does not receive keyboard focus. No `:focus`, `:focus-visible`, or `::after` focus ring is needed.

If used inside an interactive container that receives focus, focus management is the container's responsibility.

---

## Z-Index / Layering Decisions

**No z-index required.** Single-element component with no overlapping layers.

---

## Token Findings

All tokens below are **missing from token.css**. Inline fallbacks are active.

| Component token | Proposed mapping | Fallback |
|---|---|---|
| `--divider-color-neutral` | `var(--Border-border-neutral-primary)` | `#D2D6DB` |
| `--divider-color-primary` | `var(--Border-border-primary)` | `#1B8354` |
| `--divider-color-alpha-white` | `var(--Alpha-alpha-white-30)` | `rgba(255, 255, 255, 0.30)` |
| `--divider-color-white` | `var(--Border-border-white)` | `#FFF` |
| `--divider-thickness` | `1px` (fixed, no Figma variable) | `1px` |

---

## Accessibility Findings

1. **`<hr>` implicit semantics** — `<hr>` maps to `role="separator"` with `aria-orientation="horizontal"` by default. No additional ARIA needed for horizontal dividers.
2. **Vertical dividers** — `aria-orientation="vertical"` must be added to `<hr>` for vertical variants.
3. **Decorative dividers** — When a divider is purely decorative (e.g., repeated visual styling not representing a content boundary), use `role="none"` and `aria-hidden="true"`.
4. **No keyboard interaction** — Dividers are not focusable. `tabindex` must not be added.
5. **Color-only information** — If `--primary` or `--white` color is used to convey meaning (e.g., green = active section), this violates WCAG 1.4.1. Color must not be the only means of conveying information.

---

## Compliance Findings

- WCAG 1.4.1 risk: Using color variants to convey meaning without another indicator. Consumer responsibility.
- WCAG 4.1.2: `<hr>` provides role/name via implicit semantics. Passes for semantic use.
- Decorative use: `aria-hidden="true"` should be applied when the divider is purely visual.

---

## Implementation Decisions

1. **`<hr>` as root element** — Selected for semantic correctness. CSS resets applied to neutralize all browser defaults.
2. **Neutral is the default color** — Neutral is the first variant in Figma. `.divider` base class uses neutral color. Other colors are modifier classes.
3. **Horizontal is the default direction** — No modifier needed. `.divider--vertical` for vertical orientation.
4. **100% width by default** — Horizontal divider spans its container. Vertical uses `align-self: stretch` to fill container height.
5. **No fixed pixel dimensions** — 192px in Figma is a preview canvas value. All dimensional CSS is percentage/stretch-based.

---

## Intentional Deviations From Figma

| Deviation | Reason |
|---|---|
| 192px width/height not applied | Figma preview canvas value. Component must be responsive and fill its container. |
| Vertical `width: 0` not applied | Figma uses `width: 0` for the vertical container. CSS uses `width: 1px` on the element itself (correct). |
| `<hr>` not mirroring Figma RECTANGLE/LINE types | Figma structural types do not map to HTML. `<hr>` is the semantic equivalent. |

---

## Risks

1. **`<hr>` browser default styles** — Must be fully reset. Missing resets cause inconsistent rendering across browsers.
2. **Vertical height** — `.divider--vertical` with `height: 100%` requires a parent with a defined height. If the parent is `height: auto`, the vertical divider will collapse. Contract documents this limitation.
3. **Color-only meaning risk** — Consumers may use color variants to convey state/meaning without a non-color indicator. WCAG 1.4.1 violation risk.

---

## Assumptions

1. The 192px dimension in Figma is a preview canvas value, not a required fixed size.
2. Neutral is the default/base color.
3. Horizontal is the default/base orientation.
4. `--divider-thickness` is always 1px (no size axis in manifest).
5. The component is used both decoratively and semantically; both cases are documented.

---

## Known Issues

1. **Filename typo** — Source file is `mainifest.json` (not `manifest.json`). Do not rename; treat as canonical.
2. **Missing tokens in token.css** — All `--divider-*` tokens are undefined globally. Inline fallbacks active.

---

## Missing Tokens

Add to `token.css` under `/* Divider tokens */`:

```css
--divider-thickness: 1px;
--divider-color-neutral: var(--Border-border-neutral-primary, #D2D6DB);
--divider-color-primary: var(--Border-border-primary, #1B8354);
--divider-color-alpha-white: var(--Alpha-alpha-white-30, rgba(255, 255, 255, 0.30));
--divider-color-white: var(--Border-border-white, #FFF);
```

---

## Missing Standards

- No Platform Code standard documented for decorative vs. semantic divider usage. Consumer guidance added to contract.

---

## TODO

- [ ] Add `--divider-*` token block to `token.css` under `/* Divider tokens */`.
- [ ] Add `divider` entry to `components/_showcase/showcase.js` COMPONENTS registry.
- [ ] Confirm with design team whether additional thickness variants (e.g., 2px) are planned.
- [ ] Confirm whether a dashed/dotted style variant is planned.
- [ ] Run WCAG audit to verify color contrast for `--divider-color-neutral` (#D2D6DB on white = ~1.4:1) against WCAG 1.4.11.
