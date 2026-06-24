# Component Analysis

- **Manifest path:** `components/avatar/avatar.json`, `components/avatar/avatar-group.json`
- **Component name:** Avatar / Avatar Group

---

## Source

- Primary source: `avatar.json` (COMPONENT_SET: "Avatar") — 42 component variants
- Secondary source: `avatar-group.json` (COMPONENT_SET: "Avatar Group") — 2 variants
- Figma subfolders: `_figma/group/`, `_figma/shape/`, `_figma/sizes/`, `_figma/types/`
- Note: Source files are named `avatar.json` / `avatar-group.json`, not `manifest.json` — deviation from skill standard.

---

## Detected Anatomy

**Avatar (single):**
- Root COMPONENT: fixed-size circle or square container
- `bg` (RECTANGLE): visual surface layer — border-radius, border, and fill color
- `Placeholder` (FRAME): centering container — `display:flex`, `align-items:center`, zero padding
  - Icon variant: `user` (INSTANCE) → user silhouette SVG icon
  - Initials variant: `Text` (TEXT) → 1–2 character initials string (e.g. "AB")
- Image variant: `Image` (RECTANGLE) → `background: url() lightgray 50%/cover no-repeat`

**Avatar Group:**
- Root COMPONENT: `display: inline-flex`, `align-items: flex-start`
- Children: Avatar INSTANCE × N + optional overflow Avatar (Initials type, text = "+99")
- Stacked mode: `gap: -4px` (overlap)
- Flat mode: `gap: var(--Global-spacing-xs, 4px)`

---

## Detected Axes

| Axis   | Values                                    |
|--------|-------------------------------------------|
| Type   | Icon \| Initials \| Image                 |
| Square | False (circle) \| True (square)           |
| Size   | 24 \| 32 \| 40 \| 48 \| 64 \| 80 \| 120 |

Avatar Group:

| Axis    | Values          |
|---------|-----------------|
| Stacked | True \| False   |

---

## Detected Variants

- Avatar: 3 types × 2 shapes × 7 sizes = **42 variants**
- Avatar Group: **2 variants** (Stacked=True, Stacked=False)

---

## Detected States

No interactive states detected in manifest. Avatar is a **display-only** component.

States: **Default only** — no hover, pressed, focused, or disabled variants in Figma.

---

## Detected Sizes

| Size  | Dimensions | Icon slot | Initials font            | Font weight | Border |
|-------|-----------|-----------|--------------------------|-------------|--------|
| 24px  | 24×24     | 16×16     | typo-size-text-2xs (10px)| 700         | 2px    |
| 32px  | 32×32     | 24×24     | typo-size-text-xs (12px) | 600         | 2px    |
| 40px  | 40×40     | 32×32     | typo-size-text-sm (14px) | 600         | 2px    |
| 48px  | 48×48     | 32×32     | typo-size-text-md (16px) | 500         | 2px    |
| 64px  | 64×64     | 40×40     | typo-size-text-xl (20px) | 500         | 2px    |
| 80px  | 80×80     | 56×56     | typo-size-display-sm (30px) | 500      | 2px    |
| 120px | 120×120   | 80×80     | typo-size-display-md (36px) | 500      | **4px** |

Note: 80px and 120px initials switch from `font-family-text` to `font-family-display`.
Note: 120px uses 4px border (all smaller sizes use 2px).
Note: Square 120px uses `--radius-8` (8px) instead of `--radius-4` (4px).

---

## Architecture Findings

1. The `bg` RECTANGLE is a purely visual surface layer in Figma. In HTML, the `.avatar` root element serves as both container and visual surface. No separate `bg` element needed — collapsed into root.
2. The `Placeholder` FRAME is a centering container with zero padding. Collapsed into CSS `display: flex; align-items: center; justify-content: center` on the `.avatar` root.
3. The Image type uses a Figma RECTANGLE with CSS `background: url()`. In HTML, this is mapped to a semantic `<img>` element with `object-fit: cover` for alt text support and accessibility.
4. Avatar Group stacked mode: `gap: -4px` achieved with `margin-inline-start: -4px` on sibling `.avatar` elements to support LTR/RTL.
5. The overflow counter is an Avatar with Initials type — reuses `.avatar--overflow` modifier.

---

## Token Findings

| Figma Token Used                           | Source Namespace | Proposed Avatar Token    | Status                     |
|--------------------------------------------|------------------|--------------------------|----------------------------|
| `--Button-button-background-neutral-default` | Button           | `--avatar-bg-default`    | Missing — cross-namespace leak |
| `--Border-border-white`                    | Border           | `--avatar-border-color`  | Missing                    |
| `--Text-text-default`                      | Text             | `--avatar-text-color`    | Missing                    |
| `--Background-background-white`            | Background       | `--avatar-bg-image`      | Missing                    |
| `--radius-round`                           | Global shape     | `--avatar-radius-circle` | Missing                    |
| `--radius-4`                               | Global shape     | `--avatar-radius-square-sm` | Missing               |
| `--radius-8`                               | Global shape     | `--avatar-radius-square-lg` | Missing               |
| `--Global-spacing-xs`                      | Spacing          | `--avatar-group-gap`     | Missing                    |
| `--Font-Family-font-family-text`           | Typography       | (acceptable global ref)  | OK                         |
| `--Font-Family-font-family-display`        | Typography       | (acceptable global ref)  | OK                         |
| `--Size-Text-typo-size-text-*`             | Typography       | (acceptable global ref)  | OK                         |
| `--Size-Display-typo-size-display-*`       | Typography       | (acceptable global ref)  | OK                         |

Critical finding: `--Button-button-background-neutral-default` is a button-namespace token used for the avatar background fill. This is a cross-component token leak that could break if the button token is renamed.

---

## Accessibility Findings

1. Avatar conveys identity — requires `role="img"` and `aria-label` with the person's name on the root element.
2. Icon type: inner SVG must be `aria-hidden="true"` (decorative icon, label is on root).
3. Initials type: `.avatar__initials` span must be `aria-hidden="true"` (text is decorative, label is on root).
4. Image type: `<img>` requires a meaningful `alt` attribute (alt text on the img replaces the need for role/aria-label on root).
5. Overflow counter: must be `aria-hidden="true"` — it is visual-only; the group's `aria-label` conveys the full count semantically.
6. Avatar Group: requires `role="group"` and `aria-label` (e.g. "5 team members and 99 more").

---

## Compliance Findings

- Avatar is display-only → no keyboard interaction compliance concerns.
- ARIA pattern is implementation-defined (not declared in Figma manifest).
- No focus states in manifest → `:focus-visible` not required for avatar itself.
- If avatar is used inside an interactive element (link/button), focus ring belongs to the wrapper, not avatar.

---

## Implementation Decisions

1. `bg` RECTANGLE → collapsed into `.avatar` root styling. Decision: avoids unnecessary DOM nesting.
2. `Placeholder` FRAME → collapsed into CSS flex on root. Decision: Figma-specific layout detail, no semantic value.
3. Icon content → `<span class="avatar__icon" aria-hidden="true">` + raw SVG.
4. Initials content → `<span class="avatar__initials" aria-hidden="true">`.
5. Image content → `<img class="avatar__image" src="..." alt="...">` — semantic `<img>` preferred over CSS background for accessibility.
6. Avatar Group stacked gap → `margin-inline-start: -4px` on sibling avatars (not CSS `gap: -4px` which is not valid in flex).
7. Overflow counter → `.avatar--overflow` modifier on same `.avatar` base element.

---

## Intentional Deviations From Figma

1. **`bg` RECTANGLE collapsed:** The Figma layout uses a separate RECTANGLE stacked behind content. In HTML this is folded into the root `.avatar` element. Visual result is identical.
2. **`Placeholder` FRAME collapsed:** The centering FRAME wrapper is folded into root CSS. No extra wrapper element needed.
3. **`Image` RECTANGLE → `<img>`:** Figma uses a CSS background on a RECTANGLE. HTML uses `<img>` for semantic correctness and alt text support.
4. **Stacked gap implementation:** Figma uses a negative `gap` CSS property. Implemented with `margin-inline-start: -4px` since negative `gap` is not valid CSS.

---

## Risks

1. `--Button-button-background-neutral-default` is a cross-component token — renaming the button token will silently break avatar background.
2. Avatar Group source (`avatar-group.json`) is a separate file from `avatar.json` — a split source of truth.
3. No manifest.json naming — skill standard not followed for source file naming.

---

## Assumptions

1. Avatar is display-only (no interactive states required).
2. Avatar Group overflow counter is always an Initials-type avatar.
3. Both `avatar.json` and `avatar-group.json` form a single component package.
4. The icon content is always a user-silhouette SVG.
5. Image type always uses `<img>` not CSS background in HTML implementation.

---

## Known Issues

1. Source files named `avatar.json` / `avatar-group.json` (not `manifest.json`) — non-standard.
2. `--Button-button-background-neutral-default` used as avatar fill — cross-namespace token leak.

---

## Missing Tokens

- `--avatar-bg-default` — proposed mapping: `var(--Button-button-background-neutral-default, #F3F4F6)`
- `--avatar-border-color` — proposed mapping: `var(--Border-border-white, #FFF)`
- `--avatar-text-color` — proposed mapping: `var(--Text-text-default, #161616)`
- `--avatar-bg-image` — proposed mapping: `var(--Background-background-white, #FFF)`
- `--avatar-radius-circle` — proposed mapping: `var(--radius-round, 9999px)`
- `--avatar-radius-square-sm` — proposed mapping: `var(--radius-4, 4px)`
- `--avatar-radius-square-lg` — proposed mapping: `var(--radius-8, 8px)`
- `--avatar-group-gap` — proposed mapping: `var(--Global-spacing-xs, 4px)`

---

## Missing Standards

- No component-level CSS tokens exist for Avatar in `token.css`.
- All current token references point to other component namespaces or global primitives.

---

## TODO

- [ ] Define `--avatar-bg-default`, `--avatar-border-color`, `--avatar-text-color`, `--avatar-bg-image` in `token.css`
- [ ] Define shape tokens `--avatar-radius-circle`, `--avatar-radius-square-sm`, `--avatar-radius-square-lg` in `token.css`
- [ ] Define `--avatar-group-gap` in `token.css`
- [ ] Replace `--Button-button-background-neutral-default` with `--avatar-bg-default` once defined
- [ ] Normalize source file name: rename `avatar.json` → `manifest.json` if aligning to skill standard

---

## Component Classification

**Primitive Component**

Reason: Avatar is self-contained with no required external child component dependencies. It manages its own surface, content slots (icon/initials/image), and sizing. Avatar Group is a companion layout wrapper — it groups Avatar instances without introducing new component boundaries.

---

## Component Dependencies

None. Avatar is a Primitive Component.

Avatar Group uses Avatar instances internally — not a composite dependency relationship.

---

## Dependency Confirmation

Not applicable for Primitive Component.

---

## Layer Classification

| Layer Name     | Figma Type | Implementation Role | HTML Treatment               |
|----------------|------------|---------------------|------------------------------|
| Root COMPONENT | COMPONENT  | Structural Layer    | `.avatar` — root element     |
| `bg`           | RECTANGLE  | Structural Layer    | Collapsed into `.avatar` styling |
| `Placeholder`  | FRAME      | Layout Layer        | Collapsed into `.avatar` CSS flex |
| `user`         | INSTANCE   | Icon Layer          | `<span class="avatar__icon"><svg>` |
| `Text`         | TEXT       | Structural Layer    | `<span class="avatar__initials">` |
| `Image`        | RECTANGLE  | Structural Layer    | `<img class="avatar__image">` |

---

## State Delta Matrix

| State   | Delta from Default          |
|---------|-----------------------------|
| Default | Base anatomy — all variants |

No other states detected. Avatar is display-only.

---

## Pseudo-Element Decisions

No pseudo-elements required.

No interaction layers (Hover Overlay, Ripple, State Layer, Focus Ring) detected in manifest. Avatar has no interactive states.

---

## Interaction Layer Decisions

No interaction layers detected. Avatar is display-only. No pseudo-element treatment needed for interaction states.

---

## Focus Layer Decisions

No focus states in manifest. No focus ring required on Avatar itself.

Strategy: If avatar is placed inside a link or button, focus styling belongs to the wrapper element. Avatar does not define its own focus ring.

---

## Z-Index / Layering Decisions

Not applicable. No overlapping layers requiring z-index management.

---

## Severity Classification

**High:**
- Cross-component token `--Button-button-background-neutral-default` used as avatar background fill — token namespace leak, potential future breakage.

**Medium:**
- All 8 component-level avatar tokens are missing (see Missing Tokens section).
- Source file naming deviates from skill standard (`avatar.json` vs `manifest.json`).

**Low:**
- Avatar Group defined in a separate source file (`avatar-group.json`) — split source of truth.
- Initials text `line-height: 1` deviation from Figma `line-height` tokens (acceptable for centered single-line initials).

**Advisory:**
- When Avatar is used inside interactive elements, focus ring should be applied to the wrapper, not the avatar root.
- Consider defining a maximum character count for initials (1–2 chars) in the contract.
- Avatar Group with many members should convey the full count in the group's `aria-label`.

---

## Assembly Awareness

Avatar participates as a leaf component in assemblies:

```
avatar
  ↓
avatar-group
  ↓
profile-card / user-list / comment-thread (future assemblies)
```

Avatar boundaries must remain independent. Avatar Group CSS must not reach into `.avatar` styles.
