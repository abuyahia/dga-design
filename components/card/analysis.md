# Component Analysis — Card

- **Manifest path:** `components/card/manifest-3.json`
- **Component name:** Card
- **Generated:** 2026-06-22
- **Schema version:** 2.0.0

---

## Source

Figma export — `COMPONENT_SET` named `Card`. Total Figma variants: 34. Meaningful CSS variants after axis reduction: 17.

---

## Detected Anatomy

```
.card                        ← root surface (border, bg, radius, padding, gap)
  .avatar.avatar--40         ← Avatar component (icon type, 40px) — styles owned by Avatar
  .card__content             ← title + body text column
    .card__title             ← h-level heading text
    .card__body              ← paragraph body text
  .card__actions             ← action area (varies per Type)
    [Default type]
      btn.btn--secondary-outline  ← outline action button (child component)
      btn.btn--primary            ← primary action button (child component)
    [Expandable type]
      .card__toggle               ← icon-only expand/collapse button
        .card__toggle-icon        ← SVG chevron (rotates 180° when expanded)
    [Selectable type]
      .card__checkbox-wrapper     ← checkbox slot (child component boundary)
  .card__expandable-content  ← hidden slot; visible only when Expanded=True (Expandable type)
```

---

## Detected Axes

| Axis | Figma values | CSS treatment |
|---|---|---|
| Type | Default, Expandable, Selectable | `.card--expandable`, `.card--selectable` (no modifier for Default) |
| State | Default, Hover, Focused, Disabled | `:hover`, `:focus-within`, `[aria-disabled]`, `.card--disabled` |
| Expanded | False, True | `.card--expanded` + `aria-expanded` on toggle button |
| Selected | False, True | `.card--selected` + checkbox checked state |
| RTL | yes, no | **Discarded** — see RTL section |
| Effect | Stroke | **Discarded** — single value, always present |

---

## Detected Variants

| # | Type | State | Expanded | Selected |
|---|---|---|---|---|
| 1 | Default | Default | — | — |
| 2 | Expandable | Default | False | — |
| 3 | Expandable | Default | True | — |
| 4 | Expandable | Hover | False | — |
| 5 | Expandable | Hover | True | — |
| 6 | Expandable | Focused | False | — |
| 7 | Expandable | Focused | True | — |
| 8 | Expandable | Disabled | False | — |
| 9 | Expandable | Disabled | True | — |
| 10 | Selectable | Default | — | False |
| 11 | Selectable | Default | — | True |
| 12 | Selectable | Hover | — | False |
| 13 | Selectable | Hover | — | True |
| 14 | Selectable | Focused | — | False |
| 15 | Selectable | Focused | — | True |
| 16 | Selectable | Disabled | — | False |
| 17 | Selectable | Disabled | — | True |

---

## Detected States

| State | Trigger | Notes |
|---|---|---|
| Default | (none) | Baseline |
| Hover | `:hover` | Expandable and Selectable types only. Default type has no hover state in Figma. |
| Focused | `:focus-within` | Card receives focus through child interactive element (toggle button or checkbox) |
| Disabled | `aria-disabled="true"` or `.card--disabled` | Applies to Expandable and Selectable types |

---

## Detected Sizes

Single size only. No size axis.

---

## Component Classification

**Composite**

The Card owns its surface, border, radius, spacing, layout, and slots. Child components (Button, Checkbox) maintain their own contracts and CSS. The Card does not own or duplicate their styles.

---

## Component Dependencies

| Dependency | Role | Required by |
|---|---|---|
| Avatar (avatar--40, icon type) | Card icon slot | All types |
| Button (outline) | Secondary action slot | Default type |
| Button (primary) | Primary action slot | Default type |
| Button (icon-only toggle, custom) | Expand/collapse trigger | Expandable type |
| Checkbox | Selection control slot | Selectable type |

---

## Dependency Confirmation

Confirmed by user 2026-06-22. All child components remain independent. Card CSS does not duplicate Button or Checkbox styles.

---

## Layer Classification

| Layer | Role | Implementation |
|---|---|---|
| Card root | Structural | `.card` element |
| Avatar | Child component | `.avatar.avatar--40` — Avatar component (icon type). Card does not own Avatar internals. |
| Content frame | Structural | `.card__content` |
| Card Title text | Structural | `.card__title` |
| Card body text | Structural | `.card__body` |
| Actions frame | Structural | `.card__actions` |
| Button (Default type) | Child component | Composed — not owned by Card |
| Toggle button (Expandable) | Structural (card-owned) | `.card__toggle` + `.card__toggle-icon` |
| Checkbox (Selectable) | Child component | Composed — not owned by Card |
| Expandable content | Structural | `.card__expandable-content` |

No interaction layers (ripple, overlay) detected in Figma. No focus ring layer detected as a standalone element — focus is implemented via `border-width` + `border-color` change on root. Avatar disabled appearance is governed by avatar.css — card.css does not override Avatar internals in the disabled state.

---

## State Delta Matrix

**Baseline: Default type, State=Default**
- bg: `var(--card-bg-default, #FFF)`
- border: `1px solid var(--card-border-default, #D2D6DB)`
- icon-wrapper bg: `var(--card-icon-bg-default, #F3FCF6)`
- title/body color: `var(--card-text-default, #1F2A37)`

**Hover (Expandable + Selectable only):**
- bg: → `var(--card-bg-hover, #F9FAFB)` ← changed
- border: unchanged
- text colors: unchanged

**Focused — Expandable:**
- bg: unchanged (#FFF)
- border-width: → `2px` ← changed
- border-color: → `var(--card-border-focused, #161616)` ← changed

**Focused — Selectable:**
- bg: → `var(--card-bg-hover, #F9FAFB)` ← changed
- border-width: → `2px` ← changed
- border-color: → `var(--card-border-focused, #161616)` ← changed

**Disabled (both types):**
- bg: → `var(--card-bg-disabled, #E5E7EB)` ← changed
- border-color: → `var(--card-border-disabled, #9DA4AE)` ← changed
- title/body color: → `var(--card-text-disabled, #9DA4AE)` ← changed
- Avatar disabled appearance: governed by `avatar.css` — card does not override

**Expanded (Expandable type):**
- `.card--expanded` modifier added
- toggle icon rotates 180°
- `.card__expandable-content[hidden]` becomes visible

**Selected (Selectable type):**
- `.card--selected` modifier added
- Visual indicator on Checkbox child (checked state — card does not own it)

---

## Architecture Findings

1. **Default type has no interactive states.** Only one state in Figma (Default). It is a static content card. Hover/focus/disabled do not apply.
2. **Expandable focused bg stays white.** Unlike Selectable focused (which adds hover bg), Expandable focused only changes the border. This is a deliberate design distinction.
3. **Toggle button is card-owned.** The expand trigger is not a reusable Button component — it is a minimal icon-only button owned by Card, with no text and no border. Implemented as `.card__toggle`.
4. **Selectable card has two interactive sub-states.** The card can be both `hover+selected`, `focused+selected`, `disabled+selected`. CSS handles these as combinations of `.card--selectable.is-hover` + `.card--selected`.
5. **Card width is fixed at 360px in Figma.** This is likely design canvas sizing, not a production constraint. Implemented as `var(--card-width, 360px)` to allow override.

---

## Token Findings

All `--card-*` tokens listed below are missing from `token.css`. They are used in `card.css` with fallback values. Mapping proposals are documented.

---

## Accessibility Findings

1. **Default type:** Card root is a presentational container `<div>`. No role required.
2. **Expandable type:** Toggle button needs `aria-expanded` and `aria-controls`. Card root may carry `aria-labelledby` pointing to the title.
3. **Selectable type:** Checkbox must have an accessible label. Card may act as a group container with `role="group"` and `aria-labelledby`.
4. **Disabled state:** `aria-disabled="true"` on the card root communicates state to assistive technology. `pointer-events: none` prevents mouse interaction. Child interactive elements should also carry `disabled` or `aria-disabled`.
5. **Focus indicator:** Focus is communicated via border change (border-width 1px → 2px, border-color → black). This border change is the sole focus indicator on the card root. Sufficient contrast (black on white/light) is maintained.

---

## Compliance Findings

1. All color values use `--card-*` component-level tokens with fallback values.
2. No primitive tokens (`--sa-600`, `--gray-200`, etc.) used in component selectors.
3. No hardcoded hex values used as primary values (all are CSS custom property fallbacks).
4. RTL support via `dir="rtl"` on ancestor — no physical CSS properties used.
5. No official compliance claim made (`official_compliance_claim: false`).

---

## Implementation Decisions

1. **`:focus-within` chosen over `:focus`.** The card root is not itself focusable. Focus enters through child interactive elements (toggle button, checkbox). `:focus-within` correctly applies card-level focus styles when any child receives focus.
2. **Showcase-only `.is-hover` and `.is-focused` modifiers added.** These allow static state display in the showcase without requiring real interaction.
3. **Toggle button owned by Card.** Not delegated to a separate Button component because the toggle in Figma has no visible label, no border/background, and no standard button behavior — it is purely a card-internal control.
4. **Selectable card uses `role="group"`.** The card groups the content and the selection control. The checkbox itself provides the interactive control and accessible name for the selection action.
5. **Expandable content slot uses `[hidden]` attribute.** Native `hidden` attribute is toggled by JS. CSS provides `display: none` for `.card__expandable-content[hidden]` as a safety fallback.
6. **`.card--selected` modifier tracks selection visual state at card level.** The actual checked state is on the Checkbox component. The card modifier allows card-level styling hooks if needed (e.g., border color change for selected state) without coupling to the checkbox internals.

---

## Intentional Deviations From Figma

1. **RTL axis discarded.** Figma RTL=yes variants use `align-items: flex-end` (physical). In code, `dir="rtl"` on an ancestor element handles bidirectional layout correctly. No separate CSS class is needed or appropriate.
2. **Effect=Stroke discarded.** Only one value present. The stroke (border) is always applied as the base style.
3. **Card width made flexible.** Figma shows 360px fixed. Production use requires responsive behavior. `var(--card-width, 360px)` allows override.
4. **Toggle button simplified.** Figma shows a Button instance with arrow icon. In code this is a minimal `<button>` without the full Button component structure, since it carries no text, no standard size tokens, and no variant-specific behavior.

---

## Pseudo-Element Decisions

No pseudo-elements used. No interaction layers (ripple, state overlay) were detected in the Figma variants. Focus state is handled via border property changes on the root element, not via `::after`.

---

## Interaction Layer Decisions

No interaction layers detected. No `::before` pseudo-elements needed.

---

## Focus Layer Decisions

Focus is indicated by:
- `border-width: 2px` (up from 1px)
- `border-color: var(--card-border-focused, #161616)`

Applied via `:focus-within` on `.card--expandable` and `.card--selectable`.
No separate focus ring element exists in Figma.
Strategy: `:focus-within` (not `:focus-visible`) — the card root is not focusable; it receives styles when a child is focused, regardless of input device.

---

## Z-Index / Layering Decisions

No z-index required. No overlapping layers. Card is flat.

---

## RTL Behavior

RTL axis discarded. No separate CSS class generated.

**Why:** Figma uses physical CSS properties in RTL variants (`align-items: flex-end`). In web implementation:
- `flex-direction: column` is direction-neutral
- `align-items: flex-start` combined with `dir="rtl"` on an ancestor handles text alignment correctly
- Content (title, body) inherits text direction from the document

**Consequence:** The card renders correctly in both LTR and RTL contexts without any additional CSS.

---

## Severity Classification

### High (none identified)

### Medium
- All `--card-*` tokens are missing from `token.css` (PLATFORM-CODE-TOKEN-001)
- No automated contrast rule covers WCAG 1.4.3 (disabled text #9DA4AE on #E5E7EB)

### Low
- Card width fixed at 360px may need responsive override in production
- Expandable focused bg (white) vs Selectable focused bg (neutral-50) is a subtle design inconsistency that may confuse implementors

### Advisory
- Consider a `--card-selected-border-color` token if selected state border styling is needed in future
- Avatar disabled appearance inside a disabled card is inherited from avatar.css. If a specific disabled tint is required for the Avatar slot within the card, a scoped override rule may be needed — coordinate with Avatar component owner.

---

## Assembly Awareness

Card is designed to participate in assemblies:

```
Card
  ↓ (composed into)
Card Grid / Card List / Dashboard Layout
  ↓
Page Assembly
```

Card must remain independently reusable. Do not merge card behavior into layout assemblies.

---

## Known Issues

1. `--card-*` token suite does not exist in `token.css`. Fallback values are used. Token definition PR needed.
2. No automated WCAG 1.4.3 contrast check for disabled state (text: #9DA4AE on bg: #E5E7EB = ~2.1:1 — exempt per WCAG inactive UI exemption).
3. Selectable card selection behavior (click-card → toggle-checkbox) requires JavaScript not provided by this component. Implementors must wire this behavior.

---

## Missing Tokens

All `--card-*` tokens are missing from `token.css`:

| Token | Proposed source token | Fallback |
|---|---|---|
| `--card-width` | — | `360px` |
| `--card-padding` | `var(--Global-spacing-xl)` | `16px` |
| `--card-gap` | `var(--Card-card-lg-gap)` | `24px` |
| `--card-radius` | `var(--radius-lg)` | `16px` |
| `--card-border-default` | `var(--Border-border-neutral-primary)` | `#D2D6DB` |
| `--card-bg-default` | `var(--Background-background-card)` | `#FFF` |
| `--card-bg-hover` | `var(--Background-background-neutral-50)` | `#F9FAFB` |
| `--card-border-focused` | `var(--Border-border-black)` | `#161616` |
| `--card-bg-disabled` | `var(--Global-background-disabled)` | `#E5E7EB` |
| `--card-border-disabled` | `var(--Global-border-disabled)` | `#9DA4AE` |
| `--card-text-default` | `var(--Text-text-display)` | `#1F2A37` |
| `--card-text-disabled` | `var(--Global-text-default-disabled)` | `#9DA4AE` |
| `--card-content-gap` | `var(--Global-spacing-md)` | `8px` |
| `--card-actions-gap` | `var(--Global-spacing-xl)` | `16px` |
| `--card-font-family` | `var(--Font-Family-font-family-text)` | `"IBM Plex Sans Arabic"` |
| `--card-title-font-size` | `var(--Size-Text-typo-size-text-Ig)` | `18px` |
| `--card-title-line-height` | `var(--Line-Height-Text-line-heights-text-Ig)` | `28px` |
| `--card-body-font-size` | `var(--Size-Text-typo-size-text-md)` | `16px` |
| `--card-body-line-height` | `var(--Line-Height-Text-line-heights-text-md)` | `24px` |
| `--card-toggle-radius` | `var(--Radius-radius-sm)` | `4px` |
| `--card-toggle-icon-color` | `var(--Text-text-display)` | `#1F2A37` |
| `--card-toggle-transition-duration` | `var(--transition-fast)` | `0.2s` |

---

## Missing Standards

- No `PLATFORM-CODE-CARD-*` standard IDs yet. Internal IDs proposed in `compliance.json`.

---

## Assumptions

1. The Featured Icon instance in Figma maps to the Avatar component (`avatar--40`, icon type). Card composes Avatar as a child component and does not own Avatar internals.
2. The `--card-*` token suite will be defined in a future `token.css` update.
3. Selectable card click-to-select behavior will be implemented by the consuming team via JavaScript.
4. The toggle button in Expandable cards does not reuse the Button component — it is a card-internal control.
5. Default type card has no interactive states — this is correct per Figma (no hover, focused, or disabled variants exist for Default type).

---

## TODO

- [ ] Define `--card-*` token suite in `token.css`
- [ ] Write PLATFORM-CODE-CARD-* standard IDs in `standards/platform-code.standards.json`
- [ ] Add JS behavior for Selectable card click-to-select
- [ ] Add JS behavior for Expandable card toggle
- [ ] Add audit rule for WCAG 2.4.7 focus indicator on card
- [ ] Confirm Avatar disabled appearance inside a disabled Card is acceptable — coordinate with Avatar component owner if a card-scoped override is needed
- [ ] Verify IBM Plex Sans Arabic renders correctly in production environment
