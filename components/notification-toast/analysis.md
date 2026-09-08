# Component Analysis

- **Manifest path:** `components/notification-toast/mainifest.json`
- **Component name:** Notification Toast

---

## Source

Figma plugin export — COMPONENT_SET with 20 component variants.

---

## Component Classification

**Type:** Composite Component

**Reason:** The Notification Toast contains `Button` INSTANCE nodes inside the Actions slot (two action buttons) and a `Button-Close` INSTANCE in the Title header. Both are reusable child components with their own contracts and CSS. The notification-toast owns only layout, spacing, surface, slots, and type-level visual states.

---

## Component Dependencies

**Required:**
- `button` — used for action buttons in `.notification-toast__actions` and for the close button in `.notification-toast__title`

**Optional:**
- None

---

## Dependency Confirmation

`components/button/reference.json` — EXISTS. Button is a Primitive component with axes: shape, size, state. Files treated as frozen. No button files were regenerated or modified during this component generation.

The `Button-Close` in the manifest is an icon-only button instance. It is implemented using the existing `.btn.btn--subtle.btn--icon-only.btn--md` class pattern from the button component.

The two `Button` instances in the `Actions` frame are implemented as `.btn.btn--secondary-solid.btn--md` (primary action) and `.btn.btn--subtle.btn--md` (secondary/dismiss action). Actual shape selection is left to the consumer per the button contract.

---

## Detected Anatomy

```
.notification-toast                    ← root container (white card, drop shadow)
  .notification-toast__title           ← header row (desktop: flex-row; mobile: flex-col)
    .notification-toast__icon-wrap     ← 40×40 full-radius circle, type-specific background
      <svg>                            ← type-specific icon (Icon Layer)
    .notification-toast__text          ← text column (flex=1)
      .notification-toast__lead        ← title text (font-weight 600, text-md)
      .notification-toast__helper      ← description text (font-weight 400, text-sm)
    .notification-toast__close         ← 32×32 icon-only dismiss button (Structural Layer)
      <svg>                            ← multiplication-sign icon
  .notification-toast__actions         ← actions row (desktop: flex-row; mobile: flex-column)
    .btn (slot)                        ← primary action button — consumer-provided shape
    .btn (slot)                        ← secondary/dismiss button — consumer-provided shape
```

---

## Detected Axes

| Axis    | Values                                          | CSS Implementation         |
|---------|--------------------------------------------------|----------------------------|
| Type    | neutral, info, critical-error, warning, success  | `.notification-toast--[type]` modifier |
| RTL     | false, true                                      | CSS logical properties + `[dir="rtl"]` |
| Mobile  | false (484px), true (343px)                      | `@media (max-width: 767px)` |

---

## Detected Variants

20 variants = 5 types × 2 RTL × 2 Mobile

| Type           | RTL=False Desktop | RTL=True Desktop | RTL=False Mobile | RTL=True Mobile |
|----------------|:-----------------:|:----------------:|:----------------:|:---------------:|
| Neutral        | ✓                 | ✓                | ✓                | ✓               |
| Info           | ✓                 | ✓                | ✓                | ✓               |
| Critical/Error | ✓                 | ✓                | ✓                | ✓               |
| Warning        | ✓                 | ✓                | ✓                | ✓               |
| Success        | ✓                 | ✓                | ✓                | ✓               |

---

## Detected States

The Notification Toast has no interactive states of its own (no hover, focus, pressed, disabled axes in manifest). It is a display component, not an interactive control.

Internal interactive elements (close button, action buttons) inherit states from the button component.

---

## Detected Sizes

| Viewport | Width  | H-Padding Token                                  |
|----------|--------|--------------------------------------------------|
| Desktop  | 484px  | `--notification-toast-desktop-h-padding` (24px)  |
| Mobile   | 343px  | `--notification-toast-mobile-h-padding` (16px)   |

Common:
- V-padding: `--notification-toast-v-padding` (16px)
- Gap between sections: `--notification-toast-gap` (16px)
- Border radius: `--notification-toast-radius` (8px)

---

## Architecture Findings

1. **Mobile layout restructure:** In desktop, the icon, text, and close button are in a single row. In mobile, the close button becomes `position: absolute` at `inset-inline-end: -8px` and the text wraps to a second line below the icon. This is implemented using `flex-wrap: wrap` on the title container in mobile.

2. **Actions layout differs per viewport:** Desktop actions are a horizontal flex row with `padding-inline: 40px` indentation. Mobile actions are a vertical flex column with full-width (stretch) buttons at 40px height each.

3. **Icon layer — pure visual, content-driven:** The icon inside `.notification-toast__icon-wrap` changes per type (icon name and background color). It is an Icon Layer in semantic terms — it signals meaning (neutral/info/warning/error/success). It must carry `aria-hidden="true"` since the type meaning is also conveyed via `.notification-toast--[type]` which can be announced via the role/live region.

4. **Button-Close is a structural slot:** Although it renders as an icon-only button, it belongs to the notification-toast's anatomy. The notification-toast owns its 32×32 container dimensions; the visual appearance delegates to `.btn.btn--subtle.btn--icon-only.btn--md`.

---

## Token Findings

**Component-level tokens required (all must exist in token.css or be proposed):**

| Token | Fallback | Source |
|-------|----------|--------|
| `--notification-toast-bg` | `#FFF` | `--Background-background-notification-white` |
| `--notification-toast-v-padding` | `16px` | `--Notification-notification-toast-v-padding` |
| `--notification-toast-desktop-h-padding` | `24px` | `--Notification-notification-toast-desktop-h-padding` |
| `--notification-toast-mobile-h-padding` | `16px` | `--Notification-notification-toast-mobile-h-padding` |
| `--notification-toast-gap` | `16px` | `--Notification-notification-gap` |
| `--notification-toast-radius` | `8px` | `--radius-md` |
| `--notification-toast-shadow` | `0 32px 64px -12px rgba(16,24,40,0.14)` | hardcoded in manifest — token missing |
| `--notification-toast-title-gap` | `12px` | `--Global-spacing-lg` |
| `--notification-toast-icon-size` | `40px` | derived from layout |
| `--notification-toast-icon-radius` | `9999px` | `--radius-full` |
| `--notification-toast-icon-bg-neutral` | `#F9FAFB` | `--Background-background-neutral-50` |
| `--notification-toast-icon-bg-info` | `#EFF8FF` | `--Icon-background-info-light` |
| `--notification-toast-icon-bg-critical-error` | `#FEF3F2` | `--Icon-background-error-light` |
| `--notification-toast-icon-bg-warning` | `#FFFAEB` | `--Icon-background-warning-light` |
| `--notification-toast-icon-bg-success` | `#ECFDF3` | `--Icon-background-success-light` |
| `--notification-toast-text-gap` | `4px` | `--Global-spacing-xs` |
| `--notification-toast-title-color` | `#1F2A37` | `--Text-text-display` |
| `--notification-toast-title-font-size` | `16px` | `--Size-Text-typo-size-text-md` |
| `--notification-toast-title-font-weight` | `600` | manifest |
| `--notification-toast-title-line-height` | `24px` | `--Line-Height-Text-line-heights-text-md` |
| `--notification-toast-helper-color` | `#384250` | `--Text-text-primary-paragraph` |
| `--notification-toast-helper-font-size` | `14px` | `--Size-Text-typo-size-text-sm` |
| `--notification-toast-helper-font-weight` | `400` | manifest |
| `--notification-toast-helper-line-height` | `20px` | `--Line-Height-Text-line-heights-text-sm` |
| `--notification-toast-font-family` | `"IBM Plex Sans Arabic"` | `--Font-Family-font-family-text` |
| `--notification-toast-actions-indent` | `40px` | `--Global-spacing-5xl` |
| `--notification-toast-actions-gap` | `8px` | `--Button-button-menu-gap` |
| `--notification-toast-close-size` | `32px` | manifest |
| `--notification-toast-close-mobile-offset` | `8px` | derived from `right: -8px` in manifest |
| `--notification-toast-desktop-width` | `484px` | manifest |
| `--notification-toast-mobile-width` | `343px` | manifest |

---

## Accessibility Findings

1. **role="alert" / aria-live:** Notification toasts are live regions. The root should carry `role="alert"` (implies `aria-live="assertive"`) for critical/error types and `role="status"` (implies `aria-live="polite"`) for neutral/info/warning/success. Implementation decision: use `role="alert"` by default and let consumers override. Document in contract.

2. **Close button:** Must carry `aria-label` describing the dismiss action (e.g., "إغلاق الإشعار" / "Dismiss notification"). Implemented as icon-only `.btn.btn--subtle.btn--icon-only.btn--md` per button contract.

3. **Icon is decorative:** The type icon (`information-circle`, `alert-02`, etc.) carries semantic meaning visually but is redundant with the text content and `--[type]` modifier. Marked `aria-hidden="true"`.

4. **No interactive state on root:** The root element must NOT be focusable or interactive. All interactivity is delegated to child buttons.

5. **Lead text:** Should be an actual heading (`<h3>` or appropriate heading level) or plain text — left as `<p>` for flexibility since toast headings are not always in a page hierarchy. Document as advisory.

---

## Compliance Findings

- No claim of official compliance.
- Mapped to internal PLATFORM-CODE identifiers only.
- `overall_status: pending_audit`

---

## Implementation Decisions

1. **RTL via CSS logical properties:** Use `padding-inline`, `inset-inline-end`, `gap` throughout. The `[dir="rtl"]` ancestor selector handles any non-logical properties.

2. **Mobile via media query:** `@media (max-width: 767px)` breakpoint — not a CSS modifier class, because the mobile vs desktop distinction is viewport-driven, not content-driven.

3. **Type via CSS modifier class:** `.notification-toast--[type]` on the root element. Only the icon background changes per type. The icon SVG itself changes — this is managed via `data-type` attribute rendering or by including all icons with `hidden` toggling. Chosen approach: single data-type-driven slot — consumer renders the correct icon SVG.

4. **Actions slot:** The notification-toast does NOT dictate button shapes. It provides the layout container. Consumers choose which `.btn--*` variant fits the context. The template shows the expected pattern only.

5. **Close button:** Uses existing `.btn.btn--subtle.btn--icon-only.btn--md` pattern. The notification-toast's `.notification-toast__close` class adds only positioning overrides (mobile: absolute; desktop: none).

6. **Shadow token missing:** The manifest shows a hardcoded shadow `0 32px 64px -12px rgba(16,24,40,0.14)`. A component-level token `--notification-toast-shadow` is defined in the CSS with this fallback, pending a token.css entry.

7. **Focus policy:** No `:focus-visible` on the notification root. The button component's own focus styles handle close/action buttons.

---

## Intentional Deviations From Figma

1. **Two "Title" frames collapsed into one container:** Figma's mobile variant uses two sibling frames both named "Title" (one for icon+close header, one for text). In code these are collapsed into `.notification-toast__title` with responsive CSS. This avoids redundant HTML while preserving visual fidelity.

2. **Actions indentation on desktop:** Figma shows `padding-inline: 40px` on the Actions frame. This is preserved via `padding-inline: var(--notification-toast-actions-indent)`. On mobile the indent is removed (Actions frame in mobile has no horizontal padding).

---

## Layer Classification

| Layer | Figma Name | Role | HTML Output |
|-------|-----------|------|-------------|
| Root container | COMPONENT | Structural | `.notification-toast` div |
| Title row | Title (FRAME) | Structural | `.notification-toast__title` div |
| Icon circle | Featured icon (INSTANCE) | Icon Layer | `.notification-toast__icon-wrap` div + svg |
| Status icon | information-circle / alert-02 / etc. | Icon Layer | `<svg aria-hidden="true">` inside icon-wrap |
| Text container | Text and supporting text (FRAME) | Structural | `.notification-toast__text` div |
| Lead text | Lead Text (TEXT) | Structural | `.notification-toast__lead` p |
| Helper text | Helper Text (TEXT) | Structural | `.notification-toast__helper` p |
| Close button | Button-Close (INSTANCE) | Structural | `.notification-toast__close .btn.btn--subtle.btn--icon-only.btn--md` button |
| Close icon | multiplication-sign (INSTANCE) | Icon Layer | `.btn__icon` span + svg (aria-hidden) |
| Actions row | Actions (FRAME) | Structural | `.notification-toast__actions` div |
| Action button 1 | Button (INSTANCE) | Slot | consumer-rendered `.btn` |
| Action button 2 | Button (INSTANCE) | Slot | consumer-rendered `.btn` |

No Interaction Layers detected (no ripple, hover overlay, or pressed overlay in manifest).
No Focus Layers detected in manifest (handled by button component's own :focus-visible styles).

---

## State Delta Matrix

The notification-toast has no interactive state axis. Type axis deltas:

| Axis Value | Delta from Neutral |
|------------|-------------------|
| neutral | Base — icon-bg: `--notification-toast-icon-bg-neutral`, icon: `information-circle` |
| info | icon-bg: `--notification-toast-icon-bg-info`, icon: `information-circle` (same icon, different bg) |
| critical-error | icon-bg: `--notification-toast-icon-bg-critical-error`, icon: `alert-02` |
| warning | icon-bg: `--notification-toast-icon-bg-warning`, icon: `alert-circle` |
| success | icon-bg: `--notification-toast-icon-bg-success`, icon: `checkmark-circle-02` |

Mobile deltas vs Desktop:

| Property | Desktop | Mobile |
|----------|---------|--------|
| Root width | 484px | 343px |
| Root h-padding | 24px | 16px |
| Title flex-direction | row | column (via flex-wrap: wrap) |
| Title gap | 12px | 0 |
| Close button | in-flow, end of title row | position: absolute, inset-inline-end: -8px |
| Actions flex-direction | row | column |
| Actions h-indent | 40px | 0 |
| Action button height | 32px (md) | 40px (lg, full-width) |

---

## Pseudo-Element Decisions

No pseudo-elements required for this component. No interaction layers or focus rings at the notification level were found in the manifest.

---

## Interaction Layer Decisions

None detected.

---

## Focus Layer Decisions

No focus layer on the notification root. Focus rings are handled by button component on `.notification-toast__close` and `.notification-toast__actions .btn`.

---

## Z-Index / Layering Decisions

The notification-toast card itself is a presentational surface. Z-index stacking context for toast positioning (e.g., fixed overlay) is out of scope for the component CSS — handled at the layout/page level.

---

## Risks

1. Shadow token does not exist in `token.css` — hardcoded fallback in use.
2. Icon SVGs for each type must be sourced from the icon library — not embedded in component CSS.
3. Mobile breakpoint (767px) is an assumption — no breakpoint token confirmed in manifest.
4. `role="alert"` vs `role="status"` distinction is implementation-level; the Figma does not specify ARIA roles.

---

## Assumptions

1. Mobile breakpoint is `max-width: 767px`.
2. The `Button-Close` is always an icon-only button using the existing button component.
3. The action buttons in the Actions slot are always medium (32px) on desktop and large (40px full-width) on mobile, per the manifest.
4. Icon SVG source paths are external — consumers import from the icon library.
5. The toast is always white background regardless of type — type only affects the icon container background.

---

## Known Issues

None at generation time.

---

## Missing Tokens

- `--notification-toast-shadow` — hardcoded value `0 32px 64px -12px rgba(16,24,40,0.14)` used as fallback
- `--notification-toast-desktop-width` — 484px, no token in manifest
- `--notification-toast-mobile-width` — 343px, no token in manifest
- `--notification-toast-close-mobile-offset` — 8px, no token in manifest

---

## Missing Standards

None identified beyond the general compliance gap (pending audit).

---

## Assembly Awareness

`notification-toast` may participate in a `notification-center` or `toast-stack` assembly in future.

---

## Severity Classification

**High:**
- None at this time.

**Medium:**
- `--notification-toast-shadow` token missing in `token.css` — CSS uses hardcoded fallback (PLATFORM-CODE-TOKEN-001)

**Low:**
- Icon SVGs must be externally sourced — no SVG path validation possible at component level
- `role="alert"` vs `role="status"` distinction not enforced by audit rule

**Advisory:**
- Consider adding `--notification-toast-shadow` to `token.css`
- Consider adding `--notification-toast-desktop-width` and `--notification-toast-mobile-width` to token.css
- Consider adding breakpoint token for the 767px mobile breakpoint

---

## TODO

- [ ] Add `--notification-toast-shadow` to `token.css` — proposed value: `0 32px 64px -12px rgba(16,24,40,0.14)`
- [ ] Add `--notification-toast-desktop-width` and `--notification-toast-mobile-width` to `token.css`
- [ ] Confirm mobile breakpoint token if available in design system
- [ ] Confirm ARIA live region strategy: `role="alert"` (assertive) vs `role="status"` (polite) per type
- [ ] Source icon SVGs from icon library and document expected icon names in contract
