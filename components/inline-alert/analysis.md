# Component Analysis

- **Manifest path:** `components/inline-alert/mainifest.json`
- **Component name:** Inline Alert

---

## Source

Figma plugin export. Single COMPONENT_SET containing 40 COMPONENT children.
File size: ~752 KB. Read in sections (offset/limit) due to size constraints.

---

## Component Classification

**Composite**

The inline-alert contains Button INSTANCE nodes in its Actions slot (Figma type: INSTANCE, name: "Button"). These are reusable action triggers embedded within the component.

## Component Dependencies

Required:
- None (inline-alert can be rendered standalone without external component CSS)

Optional:
- Button component — for action buttons using `.btn` classes instead of inline-alert-scoped action styles

## Dependency Confirmation

Proceeding with autonomous generation. Action buttons implemented as inline-alert-scoped styles (`inline-alert__action`), not using `.btn` classes. This avoids a hard dependency while preserving layout compatibility. Assumption documented here.

---

## Detected Anatomy

```
.inline-alert                      ← root (div, role="alert")
├── ::before                       ← vertical accent bar (decorative, type-colored)
├── .inline-alert__header          ← Title frame (flex row desktop / flex col mobile)
│   ├── .inline-alert__icon-wrap   ← Featured icon circle (40×40, border-radius: full)
│   │   └── .inline-alert__icon    ← SVG icon (20×20, aria-hidden)
│   ├── .inline-alert__content     ← Text and supporting text (flex col)
│   │   ├── .inline-alert__title   ← Lead Text (p, 16px/600/text-display)
│   │   └── .inline-alert__body    ← Helper Text (p, 14px/400/text-primary-paragraph)
│   └── .inline-alert__close       ← Button-Close (button, 32×32, aria-label)
│       └── SVG × (multiplication-sign, aria-hidden)
└── .inline-alert__actions         ← Actions frame (optional)
    ├── .inline-alert__action.inline-alert__action--primary
    └── .inline-alert__action.inline-alert__action--secondary
```

---

## Detected Axes

| Axis | Values | CSS Strategy |
|---|---|---|
| type | neutral, info, destructive, warning, success | `.inline-alert--[type]` modifier |
| background | white, color | `.inline-alert--color-bg` modifier |
| mobile | false, true | `.inline-alert--mobile` modifier + `@media (max-width: 768px)` |
| rtl | false, true | `[dir="rtl"]` attribute selectors |

---

## Detected Variants

40 Figma COMPONENT children = 2 RTL × 5 Type × 2 Background × 2 Mobile.

After deduplication and CSS strategy:
- RTL → `[dir="rtl"]` attribute selector (no standalone modifier class)
- Mobile → `.inline-alert--mobile` modifier + responsive `@media`
- Type → 5 modifier classes
- Background → 1 additional modifier class (`.inline-alert--color-bg`)

Meaningful CSS variant groups: **10** (5 types × 2 backgrounds)

---

## Detected States

The inline-alert root has no interactive states (hover/pressed/focused). Interactive states exist on the embedded close button and action buttons.

| State | Implementation |
|---|---|
| Visible | Default — no modifier needed |
| Dismissed | JavaScript sets `hidden` attribute or `display: none` on root |
| Close button :focus-visible | `:focus-visible` selector on `.inline-alert__close` |
| Action button :focus-visible | `:focus-visible` selector on `.inline-alert__action` |

---

## Detected Sizes

- Desktop: `width: 100%` fluid (Figma canvas: 1024px — treated as container width)
- Mobile: Full-width stacked column layout, buttons stretch to full width

---

## Architecture Findings

1. **Vertical accent bar — absolute child:** Figma renders a FRAME named "Vertical line" as a direct child of the root with `position: absolute; width: 8px; height: 132px; opacity: 0.7`. The fixed 132px height is a Figma canvas artifact. Converted to `::before` pseudo-element with `inset: 0; height: 100%` for fluid layout.

2. **Two-frame mobile structure:** Mobile=True uses two separate "Title" FRAMEs in Figma — one for (icon + absolute close button) and one for (text content). Desktop uses one "Title" FRAME for all three elements side by side. Single HTML markup is used; CSS flex-direction change on `.inline-alert__header` in mobile achieves the visual split.

3. **Mobile close button absolute position:** Figma shows `position: absolute; right: -8px` on the close button inside the mobile header. Implemented as `position: absolute; inset-inline-end: -8px; top: 0` within `.inline-alert__header` (which gets `position: relative` in mobile mode).

4. **Action buttons — md vs lg size:** Desktop actions use height 32px (md size). Mobile actions use height 40px (lg size), `align-self: stretch` (full-width). Separate mobile modifier CSS handles this.

5. **Icon instances:** "Featured icon" and embedded icon (e.g., "help-circle") are Figma INSTANCE types. In implementation, the icon is a slot accepting any inline SVG or `<img>`. The icon circle (`inline-alert__icon-wrap`) provides the colored circular background.

---

## Token Findings

### Spacing and Layout Token Mappings

| Figma token | Proposed component token | Fallback |
|---|---|---|
| `--Notification-notification-padding` | `--inline-alert-padding-block` | `16px` |
| `--Notification-notification-h-padding` | `--inline-alert-padding-inline` | `24px` |
| `--Notification-notification-gap` | `--inline-alert-gap` | `16px` |
| `--Radius-radius-md` | `--inline-alert-border-radius` | `8px` |
| `--Global-spacing-lg` | `--inline-alert-header-gap` | `12px` |
| `--Text-text-content-gap` | `--inline-alert-content-gap` | `8px` |
| `--Button-buttons-group-gap` | `--inline-alert-actions-gap` | `8px` |
| `--Global-spacing-5xl` | `--inline-alert-actions-padding-inline` | `40px` |
| `--radius-full` | `--inline-alert-icon-radius` | `9999px` |
| `--Radius-radius-sm` | `--inline-alert-close-radius` | `4px` |

### Per-Type Token Delta

| Type | Icon circle bg | Accent bar bg | Root bg (White) | Root bg (Color) | Border (White) | Border (Color) |
|---|---|---|---|---|---|---|
| Neutral | `--Background-background-neutral-50` | `--Background-background-neutral-200` | `--Background-background-notification-white` | `--Background-background-neutral-25` | `--Border-border-neutral-primary` | `--Border-border-neutral-primary` |
| Info | `--Icon-background-info-light` | `--Background-background-info` | `--Background-background-notification-white` | `--Background-background-info-25` | `--Border-border-neutral-primary` | `--Border-border-info-light` |
| Destructive | `--Icon-background-error-light` | `--Background-background-error` | `--Background-background-notification-white` | `--Background-background-error-25` | `--Border-border-neutral-primary` | `--Border-border-error-light` |
| Warning | `--Icon-background-warning-light` | `--Background-background-warning` | `--Background-background-notification-white` | `--Background-background-warning-25` | `--Border-border-neutral-primary` | `--Border-border-warning-light` |
| Success | `--Icon-background-success-light` | `--Background-background-success` | `--Background-background-notification-white` | `--Background-background-success-25` | `--Border-border-neutral-primary` | `--Border-border-success-light` |

---

## Accessibility Findings

1. Root must carry `role="alert"` and `aria-live="polite"`. For Destructive type, `aria-live="assertive"` is appropriate.
2. Close button must have `aria-label="Dismiss notification"` (no visible text label).
3. Icon SVG must have `aria-hidden="true"` — icon is decorative; type meaning is conveyed by title text.
4. Action buttons have visible text labels (per manifest). No additional ARIA needed for simple buttons.
5. Color is not the sole differentiator — each type also changes icon shape and label text.
6. Focus ring required on close button and action buttons. Implemented via `:focus-visible`.

---

## Compliance Findings

No official compliance claim. Status: `pending_audit`.
All criteria are internally mapped only. See `compliance.json`.

---

## Implementation Decisions

1. **Vertical accent bar → `::before`:** The "Vertical line" FRAME is a decorative, non-semantic overlay. Converted to `::before`. Fixed 132px height replaced with `inset: 0; height: 100%`. Border-radius applied to match component corners.

2. **RTL → `[dir="rtl"]`:** RTL in Figma only changes `align-items: flex-end` on root and reverses horizontal flow. CSS logical properties (`inset-inline-start`, `inset-inline-end`) handle this natively without needing an explicit modifier class.

3. **Mobile → `.inline-alert--mobile` + `@media`:** Mobile=True changes flex direction of the header, repositions the close button, stacks actions vertically, and enlarges action buttons. Both a modifier class and a responsive media query implement this.

4. **Action buttons scoped within inline-alert:** Action buttons use `.inline-alert__action` classes with local sizing tokens rather than `.btn` classes. This avoids an explicit dependency on the button component CSS. The optional dependency is documented.

5. **Icon slot:** The icon is an implementation slot. Showcase uses inline SVGs. Production use should use the design system icon component.

---

## Intentional Deviations From Figma

| Figma Value | Implementation Value | Reason |
|---|---|---|
| `width: 1024px` (root) | `width: 100%` | Fluid layout for responsive use |
| `height: 132px` (accent bar) | `height: 100%` via `inset: 0` | Fluid with content height |
| `right: -8px` (mobile close) | `inset-inline-end: -8px` | Logical property for RTL support |
| `gap: 4px` (mobile text container) | `4px` with TODO comment | Token missing — preserved as hardcoded |

---

## Layer Classification

| Layer | Figma Name | Implementation Role | HTML Element |
|---|---|---|---|
| Root container | COMPONENT_SET / COMPONENT | Structural | `div.inline-alert` |
| Vertical line | FRAME (absolute) | Decorative | `::before` pseudo-element |
| Title frame | FRAME | Structural | `div.inline-alert__header` |
| Featured icon | INSTANCE | Structural | `div.inline-alert__icon-wrap` |
| help-circle / alert-02 / tick-02 | INSTANCE | Icon (decorative) | SVG with `aria-hidden` |
| Text and supporting text | FRAME | Structural | `div.inline-alert__content` |
| Lead Text | TEXT | Structural | `p.inline-alert__title` |
| Helper Text | TEXT | Structural | `p.inline-alert__body` |
| Button-Close | INSTANCE | Structural (interaction) | `button.inline-alert__close` |
| multiplication-sign | INSTANCE | Icon (decorative) | SVG with `aria-hidden` |
| Actions | FRAME | Structural (optional) | `div.inline-alert__actions` |
| Button (primary) | INSTANCE | Structural (interaction) | `button.inline-alert__action--primary` |
| Button (secondary) | INSTANCE | Structural (interaction) | `button.inline-alert__action--secondary` |

---

## State Delta Matrix

| State | Root bg | Border | Icon circle bg | Accent bar bg | Close position | Actions height |
|---|---|---|---|---|---|---|
| Default (White) | notification-white | neutral-primary | type-specific | type-specific | row end | 32px |
| Default (Color) | type-25 | type-light | type-specific | type-specific | row end | 32px |
| Mobile (White) | notification-white | neutral-primary | type-specific | type-specific | absolute -8px | 40px stretch |
| Mobile (Color) | type-25 | type-light | type-specific | type-specific | absolute -8px | 40px stretch |

---

## Pseudo-Element Decisions

| Pseudo | Attached to | Purpose | Trigger |
|---|---|---|---|
| `::before` | `.inline-alert` | Vertical accent bar (colored left border indicator) | Always visible |

No `::after` pseudo-elements needed. Focus rings use `:focus-visible` with `outline`.

---

## Interaction Layer Decisions

No interaction layers detected (no hover overlay, ripple, or state layer). The inline-alert is a notification — it is not interactive on the root level.

---

## Focus Layer Decisions

Focus implemented via `:focus-visible` with `outline` on interactive children (close button, action buttons). No `::after` ring needed. Strategy: `:focus-visible` chosen over `:focus` because the component is primarily navigated by keyboard in assistive technology contexts.

---

## Z-Index / Layering Decisions

| Element | z-index | Reason |
|---|---|---|
| `.inline-alert` | auto | Root stacking context |
| `.inline-alert::before` (accent bar) | 0 | Below all content |
| `.inline-alert__header`, `.inline-alert__content`, `.inline-alert__actions` | 1 | Above accent bar |
| `.inline-alert__close` (mobile, absolute) | 2 | Above header content |

---

## Assembly Awareness

The inline-alert may participate in assemblies such as:
- Notification tray / notification panel
- Toast stack (as a persistent variant)
- Form validation summary

It must remain a self-contained component and must not absorb layout from parent assemblies into its own CSS.

---

## Severity Classification

### High
- Missing component-level tokens (`--inline-alert-*`) — currently using primitive tokens as fallbacks via CSS custom property defaults. Risk: token renaming breaks component silently.

### Medium
- `gap: 4px` in mobile text container is not tokenized in Figma. Hardcoded fallback used.
- Icon color tokens for SVG fill/stroke are not specified in the manifest. Icon color inherits from the icon component.

### Low
- Destructive type uses `help-circle` icon (same as Neutral/Info) — semantically ambiguous.
- `height: 132px` for accent bar is a Figma canvas artifact — deviated intentionally.

### Advisory
- Add dismiss animation (CSS height/opacity transition) in a future iteration.
- Confirm whether action buttons should consume `.btn` classes for full behavioral parity.

---

## Risks

1. Missing component-level tokens — fallbacks use primitive references that may drift if primitives are renamed.
2. Close button absolute positioning in mobile may overlap content if the title text is very short and the icon area is small.
3. The `inset-inline-end: -8px` close position in mobile is a Figma exact value — may need design confirmation in production.

---

## Assumptions

1. The inline-alert is a dismissible notification. Dismiss behavior is JavaScript-controlled and out of scope for CSS.
2. Action buttons are implemented as inline-alert-scoped styles, not consuming `.btn` classes.
3. Destructive type uses `help-circle` icon per manifest — preserved as-is; flagged for design review.
4. `opacity: 0.7` on the accent bar is preserved from the Figma FRAME property.
5. RTL produces functionally identical CSS with only layout direction changes — confirmed by comparing LTR and RTL variants in the manifest.
6. `aria-live="polite"` used as default for all types; caller may upgrade to `assertive` for Destructive.

---

## Known Issues

1. Destructive type uses `help-circle` icon — semantically mismatched with error/destructive intent.
2. `gap: 4px` in mobile text container is not tokenized in Figma — using hardcoded 4px.
3. No icon color tokens detected. SVG icon color is implementation-defined.

---

## Missing Tokens

All component-level tokens below are undefined and require addition to `token.css`:

- `--inline-alert-bg`
- `--inline-alert-border-color`
- `--inline-alert-border-radius`
- `--inline-alert-padding-block`
- `--inline-alert-padding-inline`
- `--inline-alert-gap`
- `--inline-alert-header-gap`
- `--inline-alert-content-gap`
- `--inline-alert-actions-gap`
- `--inline-alert-actions-padding-inline`
- `--inline-alert-icon-bg`
- `--inline-alert-icon-radius`
- `--inline-alert-accent-bg`
- `--inline-alert-accent-opacity`
- `--inline-alert-accent-width`
- `--inline-alert-title-color`
- `--inline-alert-title-font-size`
- `--inline-alert-title-font-weight`
- `--inline-alert-title-line-height`
- `--inline-alert-body-color`
- `--inline-alert-body-font-size`
- `--inline-alert-body-font-weight`
- `--inline-alert-body-line-height`
- `--inline-alert-close-size`
- `--inline-alert-close-radius`
- `--inline-alert-mobile-content-gap` (gap: 4px in Figma mobile — not tokenized)

---

## Missing Standards

- No icon color tokens for SVG fill/stroke per type. Must be sourced from icon component or design tokens.
- No aria-live level guidance per type in Figma. Documented assumption: `polite` by default.

---

## TODO

- [ ] Add `--inline-alert-*` component tokens to `token.css`
- [ ] Confirm icon color (SVG fill/stroke) per type with design team
- [ ] Design review: Destructive type icon (`help-circle`) should be reviewed — consider `alert-02` or error-specific icon
- [ ] Request tokenized value for mobile text container gap (currently `4px`)
- [ ] Confirm whether action buttons should use `.btn` component classes
- [ ] Add dismiss transition animation in v2 (height + opacity collapse)
- [ ] Validate `aria-live` level guidance per alert type with accessibility team
