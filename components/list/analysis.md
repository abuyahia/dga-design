# Component Analysis

- **Manifest path**: `components/list/manifest.json` (List container) + `components/list/mainifest-2.json` (List item atom)
- **Component name**: List / List item

---

## Source

- `manifest.json`: `COMPONENT_SET` named **List** — 18 variants (2 RTL × 3 Style × 3 Type)
- `mainifest-2.json`: `COMPONENT_SET` named **List item** — 36 variants (2 RTL × 3 Type × 2 Level × 3 Style)

Both manifests live in the same `components/list/` folder and describe a two-tier structure:
- **List item** is the reusable atomic sub-component.
- **List** is the composite container that holds List item instances.

---

## Detected Anatomy

### List container

```
.list                         (ol | ul — column flex, no padding, no gap)
  .list__item                 (li — row flex, gap=8px)
    .list__marker             (span — marker text: "1-", "a-", "-", "•")
    .list__text               (span — item label text)
    .list__icon               (span — icon wrapper, With Icon type only)
```

### Nesting (Level Two)

Level Two items carry `padding-inline-start: 24px` (logical, covers LTR and RTL).

---

## Detected Axes

| Axis  | Values                               | Source         |
|-------|--------------------------------------|----------------|
| RTL   | yes / no                             | Both manifests |
| Style | Primary / Neutral / On-Color         | Both manifests |
| Type  | Ordered List / Unordered / With Icon | Both manifests |
| Level | One / Two                            | mainifest-2.json only |

The **List container** (`manifest.json`) exposes Style, Type, RTL.
The **List item** (`mainifest-2.json`) additionally exposes Level.

---

## Detected Variants

### List container (manifest.json): 18 variants

| RTL | Style     | Type          |
|-----|-----------|---------------|
| no  | Primary   | Ordered List  |
| no  | Primary   | Unordered     |
| no  | Primary   | With Icon     |
| yes | Primary   | Ordered List  |
| yes | Primary   | Unordered     |
| yes | Primary   | With Icon     |
| no  | Neutral   | Ordered List  |
| no  | Neutral   | Unordered     |
| no  | Neutral   | With Icon     |
| yes | Neutral   | Ordered List  |
| yes | Neutral   | Unordered     |
| yes | Neutral   | With Icon     |
| no  | On-Color  | Ordered List  |
| no  | On-Color  | Unordered     |
| no  | On-Color  | With Icon     |
| yes | On-Color  | Ordered List  |
| yes | On-Color  | Unordered     |
| yes | On-Color  | With Icon     |

### List item (mainifest-2.json): 36 variants

Axes: 2 RTL × 3 Type × 2 Level × 3 Style = 36.

---

## Detected States

No interactive states. The List component is purely typographic/content. No Hovered, Pressed, Focused, Disabled, or Selected states are present in either manifest.

---

## Detected Sizes

No size axis. A single size is defined: font-size 16px, line-height 24px.

---

## Architecture Findings

1. **Two-tier structure**: `List item` is a standalone reusable atom. `List` is a composite container. Kept as a single component package under `components/list/` with unified CSS and template.
2. **No gap between list items**: The container uses `gap: 0`. Vertical rhythm comes only from line-height of the text.
3. **No outer padding**: Container has `padding: 0` on all sides — consuming layout must provide spacing.
4. **inline-flex on container**: Figma uses `display: inline-flex` on the container. Converted to block-level `display: flex` for HTML because `inline-flex` is unusual for block list semantics. Documented as intentional deviation.
5. **RTL**: The RTL axis produces different padding direction for Level Two indent (left vs right). Implemented via `padding-inline-start` (CSS logical property) which automatically handles both directions. No separate RTL selector required for indent.
6. **RTL marker order**: In RTL ordered lists, the number appears after the Arabic text (text-first, number-second). This is natural flex RTL behavior when `dir="rtl"` is set on the container or parent. No extra CSS needed — the flex row reverses naturally.
7. **Level axis**: Only present in `mainifest-2.json`. The List container in `manifest.json` shows levels implicitly via indented instances but names them as sub-instances, not as separate variants.

---

## Token Findings

### Global tokens used in manifest (source tokens)

| Token variable                             | Fallback value                 | Role              |
|--------------------------------------------|--------------------------------|-------------------|
| `--Text-text-primary`                      | `#1B8354`                      | Primary style text color |
| `--Text-text-default`                      | `#161616`                      | Neutral style text color |
| `--Text-text-oncolor-primary`              | `#FFF`                         | On-Color style text color |
| `--Font-Family-font-family-text`           | `"IBM Plex Sans Arabic"`       | Font family       |
| `--Size-Text-typo-size-text-md`            | `16px`                         | Font size         |
| `--Line-Height-Text-line-heights-text-md`  | `24px`                         | Line height       |
| `--Global-spacing-none`                    | `0`                            | No spacing        |
| `--Global-spacing-md`                      | `8px`                          | Item gap          |
| `--Global-spacing-3xl`                     | `24px`                         | Level Two indent  |

### Required component-level tokens (proposed, missing from token.css)

All component CSS uses component-level tokens per policy. Each has a TODO comment.

| Component token                    | Proposed mapping                              |
|------------------------------------|-----------------------------------------------|
| `--list-text-primary`              | `var(--Text-text-primary)`                    |
| `--list-text-neutral`              | `var(--Text-text-default)`                    |
| `--list-text-oncolor`              | `var(--Text-text-oncolor-primary)`            |
| `--list-item-gap`                  | `var(--Global-spacing-md)`                    |
| `--list-item-indent`               | `var(--Global-spacing-3xl)`                   |
| `--list-item-font-family`          | `var(--Font-Family-font-family-text)`         |
| `--list-item-font-size`            | `var(--Size-Text-typo-size-text-md)`          |
| `--list-item-line-height`          | `var(--Line-Height-Text-line-heights-text-md)`|
| `--list-item-icon-size`            | `16px` (no global token found)                |
| `--list-item-font-weight`          | `400` (no token found — hardcoded normal)     |

---

## Accessibility Findings

1. **Native list elements**: Using `<ol>` for ordered, `<ul>` for unordered and with-icon types. `list-style: none` suppresses browser default markers. Explicit marker `<span class="list__marker">` is used.
2. **NVDA/VoiceOver quirk**: Setting `list-style: none` on `<ul>/<ol>` causes VoiceOver (Safari) to stop announcing the element as a list. Mitigation: add `role="list"` to the container element in template.html.
3. **Icon accessibility**: The icon `<svg>` inside `.list__icon` must carry `aria-hidden="true"` to suppress redundant AT announcements. The text content `.list__text` provides the accessible label.
4. **No focusable elements**: List items are not interactive and receive no focus. No focus indicator is needed.
5. **No keyboard interaction**: No keyboard pattern required. List is a content-only component.
6. **RTL semantics**: The `dir="rtl"` attribute on the `<html>` element or on `.list` provides semantic bidirectionality to AT.

---

## Compliance Findings

No external compliance claims. `overall_status: pending_audit`.

---

## Implementation Decisions

1. **Markers via CSS pseudo-elements, NOT HTML elements**: The Figma renders markers as TEXT children inside List item instances. However, explicit marker `<span>` elements are incorrect — markers are a CSS concern. CSS counters + `::before` (LTR) / `::after` (RTL) generate markers with no extra HTML. `<li>` contains only `.list__text` for ordered/unordered types.
2. **LTR `::before` / RTL `::after` for marker position**: In LTR flex, `::before` (first item) is on the LEFT — correct. In RTL flex, `::before` (first item) would be on the RIGHT — incorrect. Solution: RTL contexts clear `::before` (`content: none`) and use `::after` (last item → LEFT in RTL). Activated automatically by `[dir="rtl"]` on any ancestor.
3. **CSS counters for ordered lists**: `counter-reset` on `.list--ordered`, `counter-increment` on each level item. LTR Level One uses `counter()` (decimal). LTR Level Two uses `counter(, lower-alpha)`. RTL Level Two uses `@counter-style arabic-alpha` (requires Safari 17+ — see TODO).
4. **With Icon: CSS `order: 1` for RTL position**: DOM order is always `[.list__icon][.list__text]`. In RTL, `order: 1` on `.list__icon` pushes it to the visual LEFT without changing markup. Accessible — `aria-hidden="true"` means screen readers skip the icon regardless of visual order.
5. **`padding-inline-start` for Level Two**: Logical CSS property handles LTR (padding-left) and RTL (padding-right) automatically. No `[dir="rtl"]` selector needed for indentation.
6. **`role="list"` on container**: Required to restore VoiceOver/Safari list semantics when `list-style: none` is applied.
7. **`display: flex` on container** (not `inline-flex`): Converted from Figma's `inline-flex` to block `flex` for standard block-level list usage. Deviation documented.
8. **Style modifier on the container**: `.list--primary`, `.list--neutral`, `.list--on-color` applied to the `<ol>/<ul>` root. Color cascades to `::before`, `::after`, `.list__text`, and `.list__icon` via compound selectors.

---

## Intentional Deviations From Figma

| Deviation | Reason |
|-----------|--------|
| Container uses `display: flex` instead of `inline-flex` | Block layout is standard for list components; inline-flex creates unexpected inline flow in documents |
| `role="list"` added to container | VoiceOver (Safari) strips list semantics when `list-style: none` is set — must restore via role attribute |
| Markers generated by CSS (::before / ::after), not HTML span elements | Markers are a CSS concern, not content. Explicit `<span>` marker elements are semantically incorrect. CSS counters provide auto-incrementing behavior and clean markup |
| RTL marker uses `::after` not `::before` | In RTL flex layout, `::before` (first item) appears on the RIGHT. `::after` (last item) appears on the LEFT, which is the correct marker position in RTL |
| With Icon icon position in RTL uses CSS `order: 1` | DOM order stays uniform `[icon][text]` for both LTR and RTL; `order` handles visual flip without duplicating markup |

---

## Layer Classification

| Layer             | Type       | Classification |
|-------------------|------------|----------------|
| List container    | COMPONENT  | Structural Layer |
| List item row     | INSTANCE   | Structural Layer |
| Marker text ("1-", "-") | TEXT  | Structural Layer (content marker) |
| Icon instance     | INSTANCE   | Icon Layer (semantic content marker) |
| Item text         | TEXT       | Structural Layer |

No interaction layers. No focus ring layers. No ripple/overlay layers.

---

## State Delta Matrix

No states. Baseline is the only state.

---

## Pseudo-Element Decisions

No pseudo-elements needed. The manifest contains no interaction overlays, ripple layers, or focus ring layers.

---

## Interaction Layer Decisions

Not applicable. No interaction layers present.

---

## Focus Layer Decisions

No focus indicators required. List items are not focusable elements.

---

## Z-Index / Layering Decisions

No z-index layering needed. The list is a flat content component with no overlapping layers.

---

## Risks

1. **VoiceOver list semantics loss**: Resolved by `role="list"` but requires QA verification on Safari + VoiceOver.
2. **Arabic counter markers**: The Figma uses "أ-", "ب-" alphabetic Arabic for RTL ordered sub-items. The current template uses a static "أ-" placeholder. Dynamic counter requires JavaScript or server-side rendering for multi-item Arabic lists.
3. **On-Color context**: The `--list--on-color` variant requires a dark/colored background. No background is defined by this component — consuming context must provide it.

---

## Assumptions

1. The List container in `manifest.json` is assumed to also support Neutral and On-Color styles, even though only Primary appears in the first visible group. Confirmed by reading line ~1533 which shows `RTL=no, Style=Neutral, Type=Ordered List`.
2. The "With Icon" type uses an icon component instance (16×16). The actual SVG path is not specified in the manifest — treated as a slot.
3. No size variants exist — the single size (16px/24px) is the only size.
4. Unordered Level Two uses "•" (bullet) as confirmed by both manifests. Level One uses "-" (dash).

---

## Known Issues

1. **Marker discrepancy**: `manifest.json` (List container) shows Level Two unordered items with "•" marker, while the early reading of `mainifest-2.json` appeared to use "-" for Level Two. On full reading of `mainifest-2.json`, Level Two unordered items (lines ~1696-1832) also use "•" — confirmed consistent.
2. **`mainifest-2.json` filename typo**: The secondary manifest file is named `mainifest-2.json` (typo: "main" vs "mani"). Not corrected — preserving original filename.

---

## Missing Tokens

All component-level tokens (`--list-*`) are missing from token.css and need to be added. See Token Findings table above.

- `--list-text-primary`
- `--list-text-neutral`
- `--list-text-oncolor`
- `--list-item-gap`
- `--list-item-indent`
- `--list-item-font-family`
- `--list-item-font-size`
- `--list-item-line-height`
- `--list-item-icon-size`
- `--list-item-font-weight`

---

## Missing Standards

No formal Platform Code standard IDs were found for the List component. IDs follow internal naming convention: `PLATFORM-CODE-LIST-001`, etc.

---

## TODO

- [ ] Add `--list-*` component tokens to `token.css`
- [ ] QA test with VoiceOver (Safari) to verify `role="list"` restores list announcement
- [ ] Verify Arabic counter rendering ("أ-") with multi-item RTL ordered sub-lists in production
- [ ] Confirm icon slot API (icon component name, aria-label strategy) with design team
- [ ] Formal WCAG 2.1 audit of contrast ratios for all three Style variants
