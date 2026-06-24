# Component Analysis — Quote

- **Manifest path:** `components/quote/mainifest.json` (note: filename typo preserved as-is)
- **Component name:** Quote

---

## Source

Figma export: `COMPONENT_SET` named `"Quote"`. Contains 8 `COMPONENT` children.

---

## Detected Anatomy

```
.quote                    ← root element (<blockquote>), position: relative
  ::before                ← opening decorative quotation mark " (pseudo-element, not HTML)
  ::after                 ← closing decorative quotation mark " (pseudo-element, not HTML)
  .quote__body            ← content area with horizontal inset padding
    .quote__title         ← optional heading text for the quote
    .quote__text          ← main quote body text
  .quote__author-details  ← <footer> attribution container
    .quote__author-info   ← column stack: name + description
      .quote__author-name ← <cite> for author attribution
      .quote__author-description ← <span> for brief/role/description
```

---

## Detected Axes

| Axis | Values | Implementation |
|---|---|---|
| Direction | RTL, LTR | `[dir="rtl"]` CSS selector |
| Size | Large, Small | `.quote--sm` modifier |
| White Background | Yes, No | `.quote--white-bg` modifier |

---

## Detected Variants

| Figma Name | Direction | Size | Background | CSS Expression |
|---|---|---|---|---|
| RTL=Yes, Size=Large, White Background=Yes | RTL | Large | White | `[dir="rtl"] .quote.quote--white-bg` |
| RTL=No, Size=Large, White Background=Yes | LTR | Large | White | `.quote.quote--white-bg` |
| RTL=No, Size=Large, White Background=No | LTR | Large | None | `.quote` |
| RTL=Yes, Size=Small, White Background=Yes | RTL | Small | White | `[dir="rtl"] .quote.quote--sm.quote--white-bg` |
| RTL=Yes, Size=Small, White Background=No | RTL | Small | None | `[dir="rtl"] .quote.quote--sm` |
| RTL=Yes, Size=Large, White Background=No | RTL | Large | None | `[dir="rtl"] .quote` |
| RTL=No, Size=Small, White Background=Yes | LTR | Small | White | `.quote.quote--sm.quote--white-bg` |
| RTL=No, Size=Small, White Background=No | LTR | Small | None | `.quote.quote--sm` |

Total: 8 variants. All 8 produce distinct CSS output.

---

## Detected States

No interactive states detected. The Quote component is purely presentational.
No hover, focus, pressed, disabled, or active states exist in the manifest.

---

## Detected Sizes

| Size | Width | Notes |
|---|---|---|
| Large | 846px | Hardcoded in Figma. No width variable found. Missing token: `--quote-width-lg`. |
| Small | `var(--Width-width-lg, 640px)` | Uses `--widths-widthwidth-lg` Figma variable. Token name 'width-lg' for the 'Small' component variant is an inconsistency in upstream token naming. |

Both sizes share the same padding, gap, radius, and typography — only the width differs.

---

## Architecture Findings

1. **No interactive states.** This component requires only layout and typography CSS. No state machine.
2. **Decorative quote marks are absolute-positioned text layers.** Both `"` (U+201C) and `"` (U+201D) have no semantic meaning. They are implemented as `::before`/`::after` pseudo-elements.
3. **RTL axis does produce CSS differences.** `align-items` on root, body, and author-info changes between `flex-start` (LTR) and `flex-end` (RTL). Quote mark positions are mirrored. Unlike text-only components, this component requires explicit RTL CSS overrides.
4. **`justify-content: flex-end` on Author Details is consistent across LTR and RTL.** In LTR this right-aligns the author attribution (intentional design decision). In RTL, flex-end in a row is also physical right, which aligns with logical start in RTL. No override needed.
5. **Author name and description are always `text-align: right`** even in LTR variants per Figma. This is intentional — preserved as-is.
6. **Body text (title, quote text) in LTR has no explicit text-align** — inherits from context. In RTL it is set to `text-align: right`.
7. **Large size width (846px) is hardcoded in Figma.** No Figma variable maps to it. A missing token `--quote-width-lg` is proposed.

---

## Token Findings

All listed tokens are missing from `token.css`. Component-level semantic token names are proposed for each:

| Proposed Token | Source (Figma Raw) | Fallback Value |
|---|---|---|
| `--quote-padding` | `--spacing-globalspacing-2xl` | 20px |
| `--quote-gap` | `--spacing-globalspacing-6xl` | 48px |
| `--quote-radius` | `--radius-radiusradius-lg` | 16px |
| `--quote-bg` | `--Background-background-neutral-50` | #F9FAFB |
| `--quote-body-padding-x` | `--spacing-globalspacing-7xl` | 64px |
| `--quote-body-gap` | `--spacing-globalspacing-xl` | 16px |
| `--quote-author-gap` | `--spacing-globalspacing-xl` | 16px |
| `--quote-author-info-gap` | `--spacing-globalspacing-md` | 8px |
| `--quote-title-color` | `--Text-text-default` | #161616 |
| `--quote-title-font-family` | `--Font-Family-font-family-display` | "IBM Plex Sans Arabic" |
| `--quote-title-font-size` | `--Size-Display-typo-size-display-xs` | 24px |
| `--quote-title-line-height` | `--Line-Height-Display-line-heights-display-xs` | 32px |
| `--quote-text-color` | `--Text-text-primary-paragraph` | #384250 |
| `--quote-text-font-family` | `--Font-Family-font-family-text` | "IBM Plex Sans Arabic" |
| `--quote-text-font-size` | `--Size-Text-typo-size-text-xl` | 20px |
| `--quote-text-line-height` | `--Line-Height-Text-line-heights-text-xl` | 30px |
| `--quote-author-name-font-size` | `--Size-Text-typo-size-text-xl` | 20px |
| `--quote-author-name-line-height` | `--Line-Height-Text-line-heights-text-xl` | 30px |
| `--quote-author-description-font-size` | `--Size-Text-typo-size-text-Ig` | 18px |
| `--quote-author-description-line-height` | `--Line-Height-Text-line-heights-text-Ig` | 28px |
| `--quote-mark-color` | `--Text-text-primary-sa-flag` | #14573A |
| `--quote-mark-font-size` | *(no Figma variable — 128px hardcoded)* | 128px |
| `--quote-width-lg` | *(no Figma variable — 846px hardcoded)* | 846px |
| `--quote-width-sm` | `--widths-widthwidth-lg` | 640px |

---

## Accessibility Findings

1. **Semantic root element:** `<blockquote>` is the correct semantic element for attributed quotations.
2. **Author attribution:** `<cite>` wraps the author name. `<footer>` contains the author attribution section inside the blockquote.
3. **Decorative quote marks:** `"` and `"` are decorative. Using `::before`/`::after` pseudo-elements with `content: "\201C" / ""` (CSS alt text empty string) suppresses them from modern screen readers.
4. **No interactive elements:** No keyboard focus or ARIA state management required.
5. **`dir` attribute:** The `dir="rtl"` / `dir="ltr"` attribute on the root element must be set correctly for proper text direction. The component does not set direction internally.
6. **Quote title element:** `.quote__title` uses `<p>`. If the quote appears as a section heading in the document hierarchy, the implementer may use an `<h*>` element at the appropriate level. The contract documents this.

---

## Compliance Findings

No official compliance audit has been performed. All compliance claims are internal and pending external review.

---

## Implementation Decisions

1. **Root element: `<blockquote>`** — Correct semantic HTML for attributed quotations.
2. **Author footer: `<footer>` inside `<blockquote>`** — Valid HTML5 pattern for attribution inside a blockquote.
3. **Author name: `<cite>`** — Semantic element for citation. `font-style: normal` overrides browser default italic for `<cite>`.
4. **Quote title: `<p class="quote__title">`** — Neutral element. Documented in contract. Implementer may use heading if appropriate.
5. **Quote marks as pseudo-elements** — Eliminates semantic noise; positions are controlled purely by CSS.
6. **`margin: 0` on `<blockquote>`** — Browsers apply default margin to blockquote. Reset to match Figma layout.
7. **`box-sizing: border-box`** — Width values include padding, matching Figma behavior.
8. **RTL via `[dir="rtl"]` attribute selector** — Not a modifier class. Direction is a document/context concern, not a component modifier.

---

## Intentional Deviations From Figma

| Deviation | Reason |
|---|---|
| Decorative quote marks rendered as CSS pseudo-elements, not HTML text nodes | HTML text nodes would be announced by screen readers as quoted text, confusing SR users. Pseudo-elements with empty alt text (`/ ""`) are decorative. |
| Author name wrapped in `<cite>` instead of plain `<span>` | `<cite>` is the semantic HTML element for citing a source. |
| `font-style: normal` applied to `<cite>` | Browsers default `<cite>` to italic. Figma shows upright text. |
| Author attribution wrapped in `<footer>` | `<footer>` inside `<blockquote>` is valid HTML5 and correctly scopes the attribution. |
| Author name/description `text-align: right` preserved for LTR | Figma explicitly sets `text-align: right` on author elements even in LTR variants. Preserved as intentional design decision. |
| Large width uses `--quote-width-lg` with 846px fallback | Figma has no variable for this width. Token proposed and documented. |

---

## Risks

1. **Width tokens missing.** Both `--quote-width-lg` and `--quote-width-sm` are missing. The 846px fallback is hardcoded and will not respond to theme changes until tokens are defined.
2. **All component-level tokens missing.** All 24 proposed tokens are absent from `token.css`. Fallbacks use raw Figma tokens, which themselves may not be defined in all environments.
3. **`--Size-Text-typo-size-text-Ig` token name.** The Figma token uses `Ig` (likely `lg` with a typo). If the token is renamed in the design system, the fallback will break.
4. **`box-sizing` assumption.** If the page does not use a global `box-sizing: border-box` reset, the width behavior may be inconsistent. The component sets `box-sizing: border-box` on the root.

---

## Assumptions

1. The `dir` attribute is set on the `.quote` root or an ancestor by the implementer.
2. `token.css` is loaded before `quote.css`.
3. IBM Plex Sans Arabic or an equivalent fallback is loaded by the application.
4. The Large size width (846px) is an absolute pixel value intended for wide content areas. A container query or max-width approach is not required by the Figma spec.
5. Author name always has `text-align: right` in both LTR and RTL is an intentional design decision (per Figma).

---

## Known Issues

1. **Figma manifest filename typo:** `mainifest.json` (not `manifest.json`). Preserved as-is per platform policy.
2. **Token name inconsistency:** `--Width-width-lg` (a "large" width token) is used for the "Small" size variant. This is an upstream Figma token naming issue — not corrected in implementation.

---

## Missing Tokens

All 24 component-level tokens listed in the Token Findings section are missing.
Global update required in `token.css` — documented here as TODO, not applied automatically.

**TODO:** Add to `token.css`:
```css
/* Quote component tokens */
--quote-padding: var(--Global-spacing-2xl, 20px);
--quote-gap: var(--Global-spacing-6xl, 48px);
--quote-radius: var(--Radius-radius-lg, 16px);
--quote-bg: var(--Background-background-neutral-50, #F9FAFB);
--quote-body-padding-x: var(--Global-spacing-7xl, 64px);
--quote-body-gap: var(--Global-spacing-xl, 16px);
--quote-author-gap: var(--Global-spacing-xl, 16px);
--quote-author-info-gap: var(--Global-spacing-md, 8px);
--quote-title-color: var(--Text-text-default, #161616);
--quote-title-font-family: var(--Font-Family-font-family-display, "IBM Plex Sans Arabic", sans-serif);
--quote-title-font-size: var(--Size-Display-typo-size-display-xs, 24px);
--quote-title-line-height: var(--Line-Height-Display-line-heights-display-xs, 32px);
--quote-text-color: var(--Text-text-primary-paragraph, #384250);
--quote-text-font-family: var(--Font-Family-font-family-text, "IBM Plex Sans Arabic", sans-serif);
--quote-text-font-size: var(--Size-Text-typo-size-text-xl, 20px);
--quote-text-line-height: var(--Line-Height-Text-line-heights-text-xl, 30px);
--quote-author-name-font-size: var(--Size-Text-typo-size-text-xl, 20px);
--quote-author-name-line-height: var(--Line-Height-Text-line-heights-text-xl, 30px);
--quote-author-description-font-size: var(--Size-Text-typo-size-text-Ig, 18px);
--quote-author-description-line-height: var(--Line-Height-Text-line-heights-text-Ig, 28px);
--quote-mark-color: var(--Text-text-primary-sa-flag, #14573A);
--quote-mark-font-size: 128px;
--quote-width-lg: 846px;
--quote-width-sm: var(--Width-width-lg, 640px);
```

---

## Missing Standards

- No `PLATFORM-CODE-QUOTE-*` standard IDs exist yet. Internal IDs used in audit-rules.json.

---

## TODO

- [ ] Define `--quote-*` tokens in `token.css`
- [ ] Confirm `846px` for Large width with design team — consider using a width token
- [ ] Confirm `text-align: right` on author elements in LTR is intentional
- [ ] Confirm whether `.quote__title` should allow `<h*>` elements in the contract
- [ ] Register `{ id: 'quote', label: 'Quote' }` in `components/_showcase/showcase.js` COMPONENTS array
- [ ] External accessibility audit for `<blockquote>` + `<cite>` + `<footer>` combination

---

## Component Classification

**Primitive Component**

Self-contained display component. No required child component dependencies. No interactive states.

---

## Component Dependencies

- None

---

## Dependency Confirmation

Not applicable. Primitive component.

---

## Layer Classification

| Figma Layer | Role | Implementation |
|---|---|---|
| Root COMPONENT frame | Structural Layer | `.quote` (`<blockquote>`) |
| `body` FRAME | Structural Layer | `.quote__body` (`<div>`) |
| `عنوان الاقتباس` / `Title of quote` TEXT | Structural Layer | `.quote__title` (`<p>`) |
| `تُوضع هنا...` / `The quote is placed here...` TEXT | Structural Layer | `.quote__text` (`<p>`) |
| `Author Details` FRAME | Structural Layer | `.quote__author-details` (`<footer>`) |
| `Author Info` FRAME | Structural Layer | `.quote__author-info` (`<div>`) |
| `اسم المؤلف` / `Author's name` TEXT | Structural Layer | `.quote__author-name` (`<cite>`) |
| `نبذة أو وصف` / `brief or description.` TEXT | Structural Layer | `.quote__author-description` (`<span>`) |
| `"` TEXT (absolute, top) | Decorative Layer | `::before` pseudo-element |
| `"` TEXT (absolute, bottom) | Decorative Layer | `::after` pseudo-element |

---

## State Delta Matrix

No interactive states. All variants are layout/direction/surface deltas, not state transitions.

| Axis | Base (LTR Large No-BG) | Delta |
|---|---|---|
| + White Background | no background | `background: var(--_quote-bg)` |
| + Small | width: 846px | width: 640px; `::before` left:13px; `::after` right:13px, bottom:36px |
| + RTL | `align-items: flex-start` on root/body/author-info; `::before` left:14px; `::after` right:19px | `align-items: flex-end`; `::before` right:7px left:unset; `::after` left:23px right:unset bottom:23px; body/title/text `text-align: right` |

---

## Pseudo-Element Decisions

| Layer | Decision | Reason |
|---|---|---|
| Opening `"` (top) | `::before` on `.quote` | Decorative, absolute-positioned, no semantic meaning. Mirrored by RTL. |
| Closing `"` (bottom) | `::after` on `.quote` | Same reasoning. Position differs between LTR Large, LTR Small, and RTL. |

CSS alt text syntax `content: "\201C" / ""` used to suppress from screen readers in supporting browsers.

---

## Interaction Layer Decisions

No interaction layers exist in the manifest. Component has no hover, pressed, or focus visual states.

---

## Focus Layer Decisions

No focus layer exists in the manifest. Component is not interactive and requires no focus styling.

---

## Z-Index / Layering Decisions

The decorative quote marks are `position: absolute`. The content (body, author) is in normal flow. Quote marks are visually behind the text content due to natural stacking order. No explicit `z-index` is required since there is no overlap between the pseudo-elements and the structural content at the default font sizes.

If the mark font size or positioning causes overlap with content, `z-index: 0` on `::before`/`::after` and `position: relative; z-index: 1` on `.quote__body` and `.quote__author-details` would resolve it.

---

## Severity Classification

**High:** None

**Medium:**
- All 24 component-level tokens are missing (PLATFORM-CODE-TOKEN-001)
- Width token for Large size hardcoded at 846px

**Low:**
- `--Size-Text-typo-size-text-Ig` token name may be a typo (`Ig` vs `lg`)
- Manifest filename typo (`mainifest.json`)

**Advisory:**
- Consider whether Large width (846px) should use a semantic width token from the widths collection
- `text-align: right` on author elements in LTR context may surprise developers — document clearly

---

## Assembly Awareness

The Quote component may participate in content page assemblies:

| Assembly | Role |
|---|---|
| Article / Editorial | Pull quote or featured quotation |
| Landing page | Hero testimonial block |
| Profile section | Featured statement |

The component is self-contained and does not define any slot API for child components.
