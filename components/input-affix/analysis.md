# Component Analysis

- Manifest path: `components/input-affix/manifest.json`
- Component name: `input-affix`

---

## Source

Figma component set: `_Input Prefix-Suffix`
Total Figma components in manifest: 64 (32 LTR + 32 RTL mirrors)

---

## Detected Anatomy

```
.input-affix                      ← root container (button or div)
  .input-affix__icon              ← optional decorative SVG icon (Dropdown type only)
  .input-affix__text              ← text label wrapper (both types)
  .input-affix__arrow             ← chevron icon (Dropdown type only)
```

---

## Detected Axes

| Axis | Values | CSS Strategy |
|---|---|---|
| RTL | False / True | Discarded. `[dir="rtl"]` on page ancestor handles layout reversal via flex direction. |
| Type | Text / Dropdown | `.input-affix--text` / `.input-affix--dropdown` modifier |
| Style | Solid / Subtle | `.input-affix--solid` / `.input-affix--subtle` modifier |
| Size | Large / Medium | Default = Large (no modifier). `.input-affix--md` for Medium. |
| State | Default, Hovered, Pressed, Focused, Selected, Disabled | CSS pseudo-classes and ARIA attributes |

---

## Detected Variants

Meaningful CSS variants (RTL discarded):
- **Dropdown**: 6 states × 2 styles × 2 sizes = 24
- **Text**: 2 states (Default, Disabled only) × 2 styles × 2 sizes = 8
- **Total**: 32

---

## Detected States

| State | Type applicability | CSS expression |
|---|---|---|
| Default | Both | base selector |
| Hovered | Dropdown only | `:hover` |
| Pressed | Dropdown only | `:active` |
| Focused | Dropdown only | `:focus-visible` |
| Selected | Dropdown only | `[aria-selected="true"]` |
| Disabled | Both | `[disabled]` (button) / `[aria-disabled="true"]` (div) |

---

## Detected Sizes

| Size | Height | Padding-inline | Padding-block | Gap | Font-size | Line-height | Icon | Arrow |
|---|---|---|---|---|---|---|---|---|
| Large (default) | 40px | 16px | 2px | 4px | 16px | 24px | 24px | 20px |
| Medium (.input-affix--md) | 32px | 12px | 2px | 4px | 14px | 20px | 20px | 16px |

---

## Architecture Findings

1. **RTL duplication**: RTL=True and RTL=False produce 64 total components in the manifest, but the only difference is child order (icon and arrow positions are reversed). CSS `direction: rtl` or `[dir="rtl"]` on the page ancestor handles this without a separate CSS modifier.

2. **Type split**: `Type=Text` is a read-only static label — it shows a secondary/placeholder-colored text with no interactivity beyond Disabled. It must render as `<div>`, not `<button>`. `Type=Dropdown` is interactive, must render as `<button type="button">`.

3. **Style difference**: Solid has a background fill on Default; Subtle has no background on Default. Both share the same hovered, pressed, and selected background tokens. This is a two-axis surface: one for Default-only, one for all interactive states.

4. **State coverage asymmetry**: Text type only has Default and Disabled. No Hovered, Pressed, Focused, or Selected states exist for Text type in the manifest. This is correct — Text affixes are non-interactive.

5. **Focus implementation**: Figma uses `border: 4px solid` for focus. This inset approach causes box-model layout shift. Implementation uses `outline: 4px solid` with `outline-offset: 0` to preserve layout integrity.

6. **Selected state semantics**: The Selected state uses an inverted (dark) background with white text. This represents an active/chosen value state on the Dropdown trigger. It requires parent ARIA context (`role="listbox"` or similar) to be meaningful to assistive technology — context provided by the text-input assembly.

---

## Token Findings

All background tokens in the manifest reference the `--Button-button-background-*` namespace (Button component tokens). These are wrong for input-affix. Remapping to `--input-affix-*` tokens is required.

No `--input-affix-*` tokens currently exist in `token.css`.

**Proposed token mapping:**

| Figma token (as-is) | Proposed component token | Fallback value |
|---|---|---|
| `--Button-button-background-neutral-default` | `--input-affix-bg-solid-default` | `#F3F4F6` |
| `--Button-button-background-neutral-hovered` | `--input-affix-bg-hovered` | `#F3F4F6` |
| `--Button-button-background-neutral-pressed` | `--input-affix-bg-pressed` | `#E5E7EB` |
| `--Button-button-background-neutral-focused` | `--input-affix-bg-focused` | `#F3F4F6` |
| `--Button-button-background-black-selected` | `--input-affix-bg-selected` | `#384250` |
| `--Global-background-disabled` | `--input-affix-bg-disabled` | `#E5E7EB` |
| `--Text-text-default` | `--input-affix-text-default` | `#161616` |
| `--Text-text-secondary-paragraph` | `--input-affix-text-placeholder` | `#6C737F` |
| `--Text-text-oncolor-primary` | `--input-affix-text-selected` | `#FFF` |
| `--Global-text-default-disabled` | `--input-affix-text-disabled` | `#9DA4AE` |
| `--Border-border-black` | `--input-affix-focus-ring-color` | `#161616` |
| `--Font-Family-font-family-text` | `--input-affix-font-family` | `"IBM Plex Sans Arabic"` |

**Size tokens (all missing):**
- `--input-affix-lg-height` (40px)
- `--input-affix-lg-padding-inline` (16px)
- `--input-affix-lg-padding-block` (2px)
- `--input-affix-lg-gap` (4px)
- `--input-affix-lg-font-size` (16px)
- `--input-affix-lg-line-height` (24px)
- `--input-affix-lg-icon-size` (24px)
- `--input-affix-lg-arrow-size` (20px)
- `--input-affix-md-height` (32px)
- `--input-affix-md-padding-inline` (12px)
- `--input-affix-md-padding-block` (2px)
- `--input-affix-md-gap` (4px)
- `--input-affix-md-font-size` (14px)
- `--input-affix-md-line-height` (20px)
- `--input-affix-md-icon-size` (20px)
- `--input-affix-md-arrow-size` (16px)
- `--input-affix-radius` (0px)
- `--input-affix-focus-ring-width` (4px)

---

## Accessibility Findings

1. **Dropdown type**: Must be `<button type="button">`. Requires `aria-expanded` when it controls a dropdown panel. Default value is `false`.
2. **Text type**: Must be `<div>` or `<span>`. Non-interactive. No role override needed.
3. **Selected state**: `[aria-selected="true"]` communicates selection. Requires parent `role="listbox"` or `role="combobox"` context — deferred to text-input assembly.
4. **Disabled**: `[disabled]` on `<button>`. `[aria-disabled="true"]` on `<div>` (since HTML `disabled` is invalid on div).
5. **Icons**: All icons (`__icon`, `__arrow`) must carry `aria-hidden="true"` — they are decorative.
6. **Focus ring**: 4px black outline. Implemented as CSS `outline` not `border` to avoid layout shift.
7. **Keyboard**: Dropdown type (`<button>`) is natively keyboard operable. Text type (`<div>`) has no keyboard interaction.

---

## Compliance Findings

1. All `--input-affix-*` tokens are absent from `token.css`. CSS uses fallback values. Theming will not work until tokens are registered.
2. Focus ring deviates from Figma (`outline` vs `border: 4px solid`) — intentional, documented.
3. Selected state ARIA semantics require assembly-level context not available in this component alone.

---

## Implementation Decisions

1. RTL axis discarded — `[dir="rtl"]` on page ancestor handles layout reversal.
2. `Type=Dropdown` → `<button type="button">` (native keyboard access, implicit role=button).
3. `Type=Text` → `<div>` (non-interactive, no interactivity affordance).
4. Focus ring implemented as `outline` with `outline-offset: 0`, not `border`, to avoid layout shift.
5. Size Large = default (no modifier). Size Medium = `.input-affix--md`.
6. Both Style=Solid and Style=Subtle use explicit class modifiers.
7. Hovered, Pressed, Focused states resolved via CSS pseudo-classes (not JS classes) for Dropdown type.

---

## Intentional Deviations From Figma

1. **Focus ring**: Figma specifies `border: 4px solid var(--Border-border-black)`. Implementation uses `outline: var(--input-affix-focus-ring-width) solid var(--input-affix-focus-ring-color)` to avoid layout shift.
2. **RTL**: Figma duplicates components for RTL. CSS handles via `[dir="rtl"]` on ancestor.
3. **Subtle Default background**: Figma has no `background` property for Subtle Default (implicit transparent). CSS explicitly sets `background: transparent` for clarity.

---

## Risks

1. All component tokens are missing from `token.css`. Fallback hex values are used — theming is non-functional until tokens are added.
2. Selected state ARIA semantics depend on the text-input assembly context. Using the component in isolation will produce incomplete ARIA announcements.
3. Subtle Hovered background in the manifest uses the same token as Solid Hovered (`--Button-button-background-neutral-hovered` → same hex `#F3F4F6`). This may appear visually identical to the Solid Default on hover — verify with design.

---

## Assumptions

1. RTL=True and RTL=False in the manifest produce identical visual output except for icon/arrow order. CSS direction handles this correctly.
2. Text type affixes are non-interactive in all platform contexts.
3. Selected state is used only when the Dropdown affix has an active/chosen value in the parent assembly.
4. Both Icon and Arrow slots are always decorative (`aria-hidden="true"`).
5. Hovered background for Subtle is intentionally the same value as Solid Default (`#F3F4F6`).

---

## Known Issues

None at generation time.

---

## Missing Tokens

All `--input-affix-*` tokens listed in Token Findings are missing from `token.css`.

---

## Missing Standards

1. `--input-affix-focus-ring-width` not in `token.css`
2. `--input-affix-focus-ring-color` not in `token.css`
3. No documented ARIA pattern for Selected state semantics in component-scope isolation

---

## TODO

- [ ] Add all `--input-affix-*` tokens to `token.css`
- [ ] Confirm Subtle Hovered background value with design (currently identical to Solid Default)
- [ ] Define `aria-expanded` behavior contract in text-input assembly
- [ ] Define `role` and ARIA pattern for Selected state in text-input assembly
- [ ] Confirm focus-ring approach (outline vs border) with accessibility team
