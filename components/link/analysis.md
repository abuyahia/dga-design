# Component Analysis

- **Manifest path:** `components/link/mainifest.json` (note: filename is a typo of "manifest" — preserved as-is)
- **Component name:** Link

---

## Source

Figma export from a `COMPONENT_SET` named `Link`. The file contains 144 `COMPONENT` nodes. Each node name encodes 5 axes in the format: `RTL=<v>, State=<v>, Style=<v>, Size=<v>, Inline=<v>`.

---

## Detected Anatomy

The Link is a minimal component. Every variant contains exactly one child layer:

| Layer name  | Figma type | Implementation role |
|-------------|-----------|---------------------|
| `Link Text` | TEXT       | Content/Structural — the visible anchor label |

The root COMPONENT node carries layout properties (`display: inline-flex`, `gap`, `padding: 0`). There are no icon layers, interaction overlay layers, or focus ring child layers in the manifest. Focus is applied as a `border` property directly on the root node in Focused variants.

---

## Detected Axes

| Axis    | Values                                             | Implementation |
|---------|----------------------------------------------------|---------------|
| RTL     | False, True                                        | See Layer Classification — discarded as a CSS axis |
| State   | Default, Visited, Disabled, Focused, Hovered, Pressed | CSS state selectors |
| Style   | Primary, Neutral, On-color                        | BEM modifier classes |
| Size    | Small, Medium                                      | BEM modifier classes |
| Inline  | False, True                                        | BEM modifier class |

---

## Detected Variants

Total variants in manifest: **144**
Formula: 6 states × 2 RTL × 3 styles × 2 sizes × 2 inline modes = 144

Meaningful CSS variants: **36 base** (3 styles × 6 states × 2 sizes), reduced to **24 unique CSS rule blocks** because Focused state text color equals Default text color in all styles (no separate CSS color needed).

The `Inline` axis adds one boolean modifier class (`.link--inline`) that does not multiply the state/style/size space.

---

## Detected States

| State    | CSS selector              | Delta vs Default |
|----------|---------------------------|-----------------|
| Default  | `.link`                   | base |
| Visited  | `.link:visited`           | different text color |
| Disabled | `.link[aria-disabled="true"]` | different text color, no pointer events |
| Focused  | `.link:focus-visible`     | focus ring (outline), text color same as Default |
| Hovered  | `.link:hover`             | different text color + underline |
| Pressed  | `.link:active`            | different text color + underline |

---

## Detected Sizes

| Size   | Font size token                           | Line-height token                           | Gap token               |
|--------|-------------------------------------------|---------------------------------------------|------------------------|
| Small  | `--Size-Text-typo-size-text-sm` (14px)    | `--Line-Height-Text-line-heights-text-sm` (20px) | `--Link-link-sm-gap` (4px) |
| Medium | `--Size-Text-typo-size-text-md` (16px)    | `--Line-Height-Text-line-heights-text-md` (24px) | `--Link-link-md-gap` (8px) |

Small is treated as the default (no modifier required). Medium requires `.link--md`.

---

## Architecture Findings

1. **Simple anatomy.** The Link component has no interaction overlay layers, no ripple, no focus ring child. It is purely text with color and underline state changes.
2. **Focus ring on root.** Figma encodes focus as `border: 2px solid` on the root COMPONENT node. In HTML, this is implemented as `outline` (not `border`) to avoid layout shift. See Intentional Deviations.
3. **Gap token is present but no icons exist.** The root has `gap` from Spacing tokens. This is preserved for future icon slot compatibility but produces no visible output currently.
4. **Visited state is a CSS pseudo-class.** The `:visited` selector has privacy restrictions in browsers — only color and text-decoration changes are respected; other properties (opacity, transform, border) are ignored per browser security model.
5. **Disabled state requires aria-disabled.** A link (`<a>`) cannot use the HTML `disabled` attribute. The disabled state must be communicated via `aria-disabled="true"` and `tabindex="-1"`. Click prevention must be added at the JavaScript level since CSS `pointer-events: none` does not prevent keyboard interaction.

---

## Token Findings

### Component-level tokens (from Figma, use directly):

| Token | Value | Purpose |
|-------|-------|---------|
| `--Link-link-primary` | #1B8354 | Primary default text color |
| `--Link-link-neutral` | #384250 | Neutral default text color |
| `--Link-link-oncolor` | #FFF | On-color default text color |
| `--Link-link-primary-visited` | #14573A | Primary + Neutral visited text color |
| `--Link-link-primary-focused` | #1B8354 | Primary focused text color (= default) |
| `--Link-link-neutral-focused` | #384250 | Neutral focused text color (= default) |
| `--Link-link-oncolor-focused` | #FFF | On-color focused text color (= default) |
| `--Link-link-primary-hovered` | #54C08A | Primary hovered text color |
| `--Link-link-neutral-hovered` | #6C737F | Neutral hovered text color |
| `--Link-link-oncolor-hovered` | rgba(255,255,255,0.80) | On-color hovered text color |
| `--Link-link-primary-pressed` | #88D8AD | Primary pressed text color |
| `--Link-link-neutral-pressed` | #9DA4AE | Neutral pressed text color |
| `--Link-link-oncolor-pressed` | rgba(255,255,255,0.60) | On-color pressed text color |
| `--Link-link-oncolor-visited` | rgba(255,255,255,0.90) | On-color visited text color |
| `--Link-link-oncolor-disabled` | rgba(255,255,255,0.30) | On-color disabled text color |
| `--Link-link-sm-gap` | 4px | Small size gap |
| `--Link-link-md-gap` | 8px | Medium size gap |

### Global semantic tokens (acceptable to reference directly):

| Token | Value | Purpose |
|-------|-------|---------|
| `--Global-text-default-disabled` | #9DA4AE | Primary + Neutral disabled text color |
| `--Border-border-black` | #161616 | Primary + Neutral focus ring color |
| `--Border-border-white` | #FFF | On-color focus ring color |

### Missing component-level tokens (typography):

The following tokens reference global typography collections and need component-level wrappers:

| Missing token | Proposed name | Current fallback |
|--------------|--------------|-----------------|
| `--link-font-family` | `--link-font-family` | `var(--Font-Family-font-family-text)` |
| `--link-font-size-sm` | `--link-font-size-sm` | `var(--Size-Text-typo-size-text-sm, 14px)` |
| `--link-font-size-md` | `--link-font-size-md` | `var(--Size-Text-typo-size-text-md, 16px)` |
| `--link-line-height-sm` | `--link-line-height-sm` | `var(--Line-Height-Text-line-heights-text-sm, 20px)` |
| `--link-line-height-md` | `--link-line-height-md` | `var(--Line-Height-Text-line-heights-text-md, 24px)` |
| `--link-focus-ring-width` | `--link-focus-ring-width` | 2px (hardcoded in Figma) |
| `--link-focus-ring-offset` | `--link-focus-ring-offset` | 2px (no Figma source, standard practice) |

---

## Accessibility Findings

1. **`<a>` is the correct semantic element.** Links navigate. No `role="button"` is needed.
2. **href is required for keyboard operability.** An `<a>` without `href` is not keyboard-focusable by default. All link instances must include a valid `href`.
3. **Disabled links require `aria-disabled="true"` + `tabindex="-1"`.** Without `tabindex="-1"`, disabled links remain in the tab order, which is confusing for screen reader users.
4. **`:visited` color contrast.** The Visited color `#14573A` on white background = ~8.5:1. Passes WCAG 1.4.3.
5. **Focus ring contrast.** `--Border-border-black` (#161616) outline on white = ~19.6:1. Passes WCAG 2.4.11 (focus appearance, 3:1 minimum).
6. **On-color focus ring contrast.** `--Border-border-white` (#FFF) on dark background: contrast depends on the background color at deployment site. Flag as context-dependent.
7. **`text-decoration-skip-ink: none`** is required on hover/pressed to ensure underlines are visible under characters with descenders (Arabic text).
8. **External links.** When `target="_blank"` is used, an `aria-label` or visually hidden text like "(opens in new tab)" should be added. This is a deployment concern, not a component concern.

---

## Compliance Findings

- No official compliance audit has been conducted.
- All WCAG 2.1 mappings in `compliance.json` are internal mappings (status: `mapped`).
- Disabled link pattern has a non-standard implementation risk (see Architecture Findings #5).
- `:visited` privacy restrictions mean some Figma Visited state properties cannot be implemented in CSS (limited to color and text-decoration).

---

## Implementation Decisions

1. **CSS cascade variable approach for style theming.** Each `.link--[style]` modifier redefines a set of internal CSS custom properties (`--_link-color`, `--_link-visited-color`, etc.). State selectors read these variables. This avoids N×M selector duplication and is maintainable when new styles are added.
2. **Default size = Small.** Small is more common in body text contexts. No size modifier is required for Small. `.link--md` applies Medium.
3. **Focus ring via `outline`, not `border`.** Figma encodes focus as `border`. In HTML, `border` shifts layout. `outline` is layout-neutral and is the correct accessibility approach.
4. **`outline-offset: 2px`** is added. Not present in Figma (which collapses focus padding into the element). Added per standard focus ring accessibility practice.
5. **Inline underline via modifier class.** `Inline=True` adds underline to all states. Implemented as `.link--inline`. The hover/active underline states apply regardless of inline mode.
6. **RTL discarded as a CSS axis.** See Intentional Deviations.
7. **Disabled via `aria-disabled="true"`** on the `<a>` element. `pointer-events: none` is added; `tabindex="-1"` is required in the template but enforced in the audit rule.

---

## Intentional Deviations From Figma

| Figma behavior | Implementation | Reason |
|---|---|---|
| Focus ring as `border: 2px solid` on root | `outline: 2px solid` with `outline-offset: 2px` | `border` shifts layout; `outline` does not. Standard browser focus ring pattern. |
| RTL axis produces separate LTR/RTL variants | RTL handled via `[dir="rtl"]` attribute; CSS produces no delta for text-only links | Text-only links have no layout difference in LTR vs RTL. `text-align` is not needed on inline-flex links without fixed width. RTL will matter when icon slots are added. |
| Focused text color = separate token (`--Link-link-primary-focused`) | Color not reapplied in focused state CSS | The focused color token is identical to the default color (#1B8354 = #1B8354). No delta to implement. |
| Neutral Visited uses `--Link-link-primary-visited` token | Preserved as-is | Confirmed intentional in Figma. Both Primary and Neutral visited states use the same green token. |

---

## Layer Classification

| Layer | Classification | CSS target |
|-------|---------------|-----------|
| Root COMPONENT | Structural Layer | `.link` (`<a>`) |
| Link Text (TEXT) | Content Layer | direct text content of `<a>` |
| Focus border (on root in Focused variants) | Focus Layer → `outline` | `.link:focus-visible` |

No Interaction Circle, Ripple, or Hover Overlay layers detected. No pseudo-element generation needed.

---

## State Delta Matrix

| State | Text color | Underline | Focus ring | Cursor |
|-------|-----------|-----------|-----------|--------|
| Default | `--_link-color` | none (or via `.link--inline`) | none | pointer |
| Visited | `--_link-visited-color` | none (or via `.link--inline`) | none | pointer |
| Hovered | `--_link-hovered-color` | always | none | pointer |
| Pressed | `--_link-pressed-color` | always | none | pointer |
| Focused | same as Default | none (or via `.link--inline`) | 2px solid `--_link-focus-ring` | pointer |
| Disabled | `--_link-disabled-color` | none | none | not-allowed |

---

## Pseudo-Element Decisions

No pseudo-elements required. The link has no interaction overlay layers and no focus ring children. Focus ring is implemented via CSS `outline` on the root element.

---

## Interaction Layer Decisions

No interaction layers detected in manifest. No `::before` or `::after` interaction overlays needed.

---

## Focus Layer Decisions

Focus ring is a `border` on the root element in Figma. Implemented as `outline: var(--link-focus-ring-width) solid var(--_link-focus-ring)` with `outline-offset: var(--link-focus-ring-offset)` on `.link:focus-visible`.

---

## Z-Index / Layering Decisions

Not applicable. The link has a flat anatomy (no layered pseudo-elements).

---

## Risks

1. **`:visited` privacy restrictions.** Only `color` and `text-decoration` can be changed via `:visited`. Any additional Figma Visited state properties would be silently ignored by browsers.
2. **Disabled link keyboard accessibility.** `pointer-events: none` does not prevent keyboard Tab focus or Enter activation. The template enforces `tabindex="-1"` but this can be omitted by implementors. Audit rule LNK-A11Y-004 catches this.
3. **On-color focus ring contrast.** `--Border-border-white` (#FFF) is the focus ring color for On-color links. Contrast against the actual page background depends on deployment context — cannot be guaranteed at component level.
4. **No href = not focusable.** An `<a>` without `href` is excluded from the tab order. Audit rule LNK-A11Y-005 catches links without href.

---

## Assumptions

1. The `gap` property on the root is preserved even though no icons exist in the current manifest. It is assumed that icon slots will be added in a future version.
2. `font-weight: 400` is consistent across all states and styles. No bold/strong variation was detected.
3. The Neutral Visited state intentionally uses `--Link-link-primary-visited` (a green token). This was confirmed as intentional by visual inspection of the manifest — there is no separate `--Link-link-neutral-visited` token.
4. `font-style: normal` is consistent across all variants. No italic variation.

---

## Known Issues

1. **Neutral Visited token ambiguity.** Neutral links in Visited state use `--Link-link-primary-visited` (#14573A, dark green). This may be unexpected for teams using Neutral links in non-green design contexts.
2. **Manifest filename typo.** The file is named `mainifest.json` instead of `manifest.json`. This is not corrected to avoid breaking any tooling that references the current filename.

---

## Missing Tokens

| Token | Proposed name | Proposed value | Notes |
|-------|--------------|----------------|-------|
| Link font family | `--link-font-family` | `var(--Font-Family-font-family-text)` | No component-scoped token in manifest |
| Link font size small | `--link-font-size-sm` | `var(--Size-Text-typo-size-text-sm, 14px)` | No component-scoped token in manifest |
| Link font size medium | `--link-font-size-md` | `var(--Size-Text-typo-size-text-md, 16px)` | No component-scoped token in manifest |
| Link line height small | `--link-line-height-sm` | `var(--Line-Height-Text-line-heights-text-sm, 20px)` | No component-scoped token in manifest |
| Link line height medium | `--link-line-height-md` | `var(--Line-Height-Text-line-heights-text-md, 24px)` | No component-scoped token in manifest |
| Link focus ring width | `--link-focus-ring-width` | `2px` | Hardcoded in Figma border, no token |
| Link focus ring offset | `--link-focus-ring-offset` | `2px` | Not in Figma (standard practice addition) |
| Link font weight | `--link-font-weight` | `400` | Not tokenized in manifest |

---

## Missing Standards

- No `--link-transition` token for hover/focus transitions. Figma has no transition defined; a smooth transition is added as an enhancement with a TODO.
- No component-level typography scale token (all font sizes reference the global typography collection directly).

---

## TODO

- [ ] Add component-level typography tokens to token.css: `--link-font-family`, `--link-font-size-sm/md`, `--link-line-height-sm/md`
- [ ] Add `--link-focus-ring-width` and `--link-focus-ring-offset` to token.css
- [ ] Add `--link-font-weight` to token.css
- [ ] Verify Neutral Visited token intent with design team — is `--Link-link-primary-visited` correct for Neutral visited links?
- [ ] Rename manifest file from `mainifest.json` to `manifest.json` in a coordinated update with all tooling
- [ ] Run color contrast audit for On-color focus ring in deployment contexts
- [ ] Define external link pattern (target="_blank" + accessible label)
- [ ] Consider icon slot design when icon variants are added to Figma
