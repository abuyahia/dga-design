# Component Analysis

- **Manifest path:** `components/code-snippet/mainifest.json`
- **Component name:** Code Snippet

---

## Source

Figma plugin export. COMPONENT_SET with 2 variants: `Type=Multi-Line` and `Type=Single-Line`.

---

## Detected Anatomy

### Multi-Line

```
.code-snippet (root — column flex, border, bg-white, radius-lg)
├── .code-snippet__tab-bar (Horizontal Tab List instance)
│   ├── .code-snippet__tab-divider (Divider — absolute, bottom, full-width)
│   └── .code-snippet__tabs (Tabs frame)
│       └── .code-snippet__tab (Horizontal Tab instance × N)
│           ├── .code-snippet__tab-title (Tab title)
│           │   └── .code-snippet__tab-text (Text)
│           └── .code-snippet__tab-indicator (Selection indicator — active tab only)
│               └── .code-snippet__tab-selector (Selector rectangle)
└── .code-snippet__body (row flex)
    ├── .code-snippet__gutter (Sidebar — line numbers column)
    │   └── .code-snippet__line-numbers (Line numbers text)
    └── .code-snippet__content (Content — column flex)
        ├── .code-snippet__code-row (code text + copy button row)
        │   ├── .code-snippet__code (Code text)
        │   └── .code-snippet__copy (Button instance — copy icon)
        └── .code-snippet__show-more (Button instance — Show More)
```

### Single-Line

```
.code-snippet.code-snippet--single (root — row flex, border, bg-white, radius-lg)
├── .code-snippet__inline (inline content row)
│   ├── .code-snippet__prompt (prompt keyword text — amber)
│   └── .code-snippet__inline-code (command text — green)
└── .code-snippet__copy (Button instance — copy icon, 32×32)
```

---

## Detected Axes

| Axis | Values |
|------|--------|
| Type | Multi-Line, Single-Line |

---

## Detected Variants

| Variant Name | Description |
|---|---|
| Type=Multi-Line | Multi-line code block with language tabs, line numbers, copy button, and show-more |
| Type=Single-Line | Single-line inline command with prompt keyword and copy button |

Total meaningful variants: 2

---

## Detected States

| State | Source | Implementation |
|---|---|---|
| Tab Default | Non-active tab: font-weight 500, secondary text color | `.code-snippet__tab` base |
| Tab Active | First tab (Java): font-weight 700, default text color + bottom indicator | `.code-snippet__tab[aria-selected="true"]` |
| Tab Hover | Not in manifest; inferred from platform standards | `:hover` CSS |
| Tab Focus | Not explicit in manifest | `:focus-visible` CSS |
| Copy Hover/Press/Focus | Delegated to Button component | Button component handles |
| Show More Toggle | Not a Figma state; inferred from "Show More" button label | JS toggle + `aria-expanded` |
| Expanded | Not explicit; assumed truncated by default | `.code-snippet--expanded` modifier |

---

## Detected Sizes

No size axis detected. Code Snippet does not vary by size in the manifest.

---

## Architecture Findings

1. **Composite component.** Code Snippet wraps Button (copy, show more) and Horizontal Tab instances. These child components keep their own CSS and contracts.
2. **Tab bar is an INSTANCE** of a `Horizontal Tab List` component in Figma. For implementation, the tab bar is rendered inline as native `<button role="tab">` elements inside a `role="tablist"` since there is no separate standalone tab-bar component file confirmed yet. This matches Platform Code accessibility standards.
3. **Line numbers** are a presentation-only block (Roboto Mono, `counter` or static text). They are `aria-hidden="true"`.
4. **Copy button** is a ghost icon-only button (delegated). Its visual spec (40×40 for multi-line, 32×32 for single-line) is controlled by Button modifiers.
5. **Show More** is a button that expands the code block. No Figma expanded state exists; behavior is assumed.
6. **Single-line prompt word** (`npm`) uses amber color `--Text-text-secondary: #DBA102`. This is semantically a "prompt keyword" text, distinct from the command text which uses green `--Text-text-primary: #1B8354`. Both are inline, not a true two-part syntax — just two styled spans.

---

## Token Findings

### Tokens referenced in manifest (with proposed component-level semantic mapping):

| Raw Figma Token | Proposed Component Token | Value |
|---|---|---|
| `--Radius-radius-lg` | `--code-snippet-border-radius` | `16px` |
| `--Border-border-neutral-secondary` | `--code-snippet-border-color` | `#E5E7EB` |
| `--Background-background-white` | `--code-snippet-bg` | `#FFF` |
| `--Background-background-neutral-50` | `--code-snippet-gutter-bg` | `#F9FAFB` |
| `--Border-border-neutral-primary` | `--code-snippet-tab-divider-color` | `#D2D6DB` |
| `--Border-border-primary` | `--code-snippet-tab-active-indicator-color` | `#1B8354` |
| `--Text-text-default` | `--code-snippet-code-color` | `#161616` |
| `--Text-text-default` | `--code-snippet-tab-active-text-color` | `#161616` |
| `--Text-text-primary-paragraph` | `--code-snippet-tab-inactive-text-color` | `#384250` |
| `--colors-text-text-quarterary-500` | `--code-snippet-line-numbers-color` | `#667085` |
| `--Text-text-secondary` | `--code-snippet-prompt-color` | `#DBA102` |
| `--Text-text-primary` | `--code-snippet-inline-code-color` | `#1B8354` |
| `--spacing-3xl` | `--code-snippet-padding` | `24px` |
| `--spacing-4xl` | `--code-snippet-content-pb` | `32px` |
| `--Tab-horizontal-tab-md-button-h-padding` | `--code-snippet-tab-button-padding` | `16px` |
| `--Tab-tab-button-gap` | `--code-snippet-tab-button-gap` | `4px` |
| `--radius-radius-full` | `--code-snippet-tab-indicator-radius` | `9999px` |
| `--Radius-radius-sm` | `--code-snippet-tab-button-radius` | `4px` |

---

## Accessibility Findings

1. **Tab bar** must use `role="tablist"` with `role="tab"` buttons and `aria-selected` state.
2. **Code panels** must use `role="tabpanel"` and `aria-labelledby` pointing to the active tab.
3. **Line numbers** must be `aria-hidden="true"` — they are presentational.
4. **Copy button** must have `aria-label="Copy code"` (icon-only button).
5. **Show More button** must have `aria-expanded` attribute toggled by JS.
6. **Code text** should be inside `<pre><code>` for semantic correctness and screen reader compatibility.
7. **Single-line prompt** (`npm`) has no semantic meaning beyond visual grouping — it can be a `<span>` inside the inline code.

---

## Compliance Findings

- No official compliance claims made.
- Token mapping is internal.
- Accessibility rules are aligned with Platform Code standards (WCAG 2.1 AA intent).

---

## Implementation Decisions

1. **Tab bar is rendered natively** using `role="tablist"` / `role="tab"` pattern. No dependency on a separate Tab component HTML since the tab bar is an INSTANCE in Figma and no standalone tab-bar HTML file was confirmed.
2. **Active tab** is controlled via `aria-selected="true"` and `.code-snippet__tab--active` modifier.
3. **Tab indicator** (green bottom bar) is implemented as `::after` pseudo-element on active tab — not as standalone HTML.
4. **Tab divider** (gray bottom line across full tab bar) is implemented as `::after` pseudo-element on the tab bar container — not as a real div.
5. **Line numbers** are generated dynamically by JS or rendered as static content. In template.html, a static block of 20 lines is used.
6. **Code is inside** `<pre><code>` for semantic correctness.
7. **Show More** uses JS toggle with `aria-expanded`. Expanded state removes line-clamp.
8. **Copy button** uses the Button component markup with icon-only modifier. Icon is an inline SVG `copy-01`.
9. **Single-line type** uses `--single` modifier on root.
10. **Focus strategy:** `:focus-visible` used for tab buttons and copy button per platform standards.

---

## Intentional Deviations From Figma

| Deviation | Reason |
|---|---|
| Tab bar Divider is `::after` pseudo-element | Figma shows a RECTANGLE layer; pseudo-element avoids extra DOM |
| Tab Selection Indicator is `::after` on active tab | Figma shows a positioned FRAME; pseudo-element is cleaner and avoids aria issues |
| Line numbers are `aria-hidden` | Purely presentational; screen readers should not read numbers |
| Code is wrapped in `<pre><code>` | Figma shows plain text; `<pre><code>` is required for semantics |
| Copy button uses `aria-label` | Figma shows icon-only — label is not visible but required for accessibility |

---

## Risks

- Tab bar behavior (keyboard nav between tabs) requires JS. No JS is provided by the CSS-only component. Showcase JS handles this.
- Show More behavior requires JS toggle. Showcase and component JS handle this.
- Syntax highlighting is NOT included — code text is plain monospace. This is intentional; syntax highlighting is outside the component scope.
- The `--code-snippet-*` token namespace does not yet exist in `token.css`. All tokens are proposed mappings.

---

## Assumptions

- The active tab (first tab, Java) is the default selected state.
- The copy button copies the text content of `.code-snippet__code`.
- "Show More" expands from a 20-line clamp to full content.
- Single-line variant does not have line numbers or a tab bar.
- The Button component is available and provides `.btn`, `.btn--icon`, `.btn--ghost`, `.btn--md`, `.btn--lg` modifiers.
- Dependency on Button component confirmed implicitly (Figma INSTANCE named "Button").

---

## Component Classification

**Composite Component**

The Code Snippet has its own visual identity (surface, border, radius, gutter) and wraps Button and Tab child instances.

---

## Component Dependencies

Required:
- `button` component (copy icon button, show more button)

Optional:
- `tab` / `horizontal-tab-list` component (the tab bar is currently rendered natively for independence)

---

## Dependency Confirmation

Dependency confirmation was not explicitly required from user per skill rules for default "generate" command. Assumption documented here.

---

## Layer Classification

| Layer | Figma Name | Role | Implementation |
|---|---|---|---|
| Root | Code Snippet | Structural | `.code-snippet` root element |
| Tab bar | Horizontal Tab List | Structural | `role="tablist"` |
| Divider | Divider | Interaction / Visual | `::after` on `.code-snippet__tab-bar` |
| Tabs | Tabs | Structural | `div.code-snippet__tabs` |
| Tab | Horizontal Tab | Structural | `button role="tab"` |
| Tab title | Tab title | Structural | span inside tab |
| Selection indicator | Selection indicator | Focus / Active state | `::after` on active tab |
| Selector | Selector | Focus / Active state | Part of `::after` |
| Body | Frame 1 | Structural | `.code-snippet__body` |
| Gutter | Sidebar | Structural | `.code-snippet__gutter` |
| Line numbers | Line numbers | Presentational | `aria-hidden="true"` |
| Content | Content | Structural | `.code-snippet__content` |
| Code row | Frame 669 | Structural | `.code-snippet__code-row` |
| Code text | Code | Structural | `<pre><code>` |
| Copy button | Button (copy-01) | Structural | Button component instance |
| Show more | Button (Show More) | Structural | Button component instance |
| Inline content | Frame 668 | Structural | `.code-snippet__inline` |
| Prompt | npm (text) | Structural | `.code-snippet__prompt` |
| Inline code | command text | Structural | `.code-snippet__inline-code` |

---

## State Delta Matrix

| State | vs Default | Implementation |
|---|---|---|
| Tab inactive | font-weight 500, `--code-snippet-tab-inactive-text-color` | base `.code-snippet__tab` |
| Tab active | font-weight 700, `--code-snippet-tab-active-text-color`, green `::after` indicator | `.code-snippet__tab[aria-selected="true"]` |
| Tab hover | platform default (background tint) | `.code-snippet__tab:hover` |
| Tab focus | `:focus-visible` ring | `.code-snippet__tab:focus-visible` |
| Expanded | no line-clamp, Show More label changes | `.code-snippet--expanded .code-snippet__code` |

---

## Pseudo-Element Decisions

| Element | Pseudo | Purpose |
|---|---|---|
| `.code-snippet__tab-bar::after` | `::after` | Full-width gray divider line at bottom of tab bar |
| `.code-snippet__tab[aria-selected="true"]::after` | `::after` | Green bottom indicator on active tab |
| `.code-snippet__tab:focus-visible::before` | `::before` | Focus ring (or use outline) |

---

## Interaction Layer Decisions

No explicit Figma interaction (ripple/overlay) layers detected on the Code Snippet root. Child Button component handles its own interaction states.

---

## Focus Layer Decisions

Focus implemented via `:focus-visible` outline on tab buttons and copy/show-more buttons.
Strategy: `:focus-visible` (keyboard-only) — preferred for interactive controls per Platform Code accessibility standards.

---

## Z-Index / Layering Decisions

Tab bar:
- `.code-snippet__tab-bar` → `position: relative`
- `::after` (divider) → `z-index: 0`, `position: absolute`, `bottom: 0`
- `.code-snippet__tab[aria-selected="true"]::after` (indicator) → `z-index: 1`, `position: absolute`, `bottom: 0`

This ensures the active indicator sits above the divider line.

---

## Severity Classification

### High
- None at generation time.

### Medium
- All `--code-snippet-*` tokens are proposed; they do not exist in `token.css` yet.

### Low
- `mainifest.json` (typo in source file name — "mainifest" vs "manifest"). Noted; not corrected since the skill must not modify the raw export file.

### Advisory
- Consider adding a "Copied!" feedback state to the copy button (aria-live announcement).
- Consider adding syntax highlighting support as a future enhancement.
- Consider a dark theme variant for the code block.

---

## Assembly Awareness

Code Snippet may participate in documentation page assemblies or tutorial assemblies. It is self-contained and does not expose slots for external assembly injection.

---

## Missing Tokens

All `--code-snippet-*` tokens listed in Token Findings are missing from `token.css`.

Proposed additions to `token.css`:
```css
--code-snippet-border-radius: var(--Radius-radius-lg, 16px);
--code-snippet-border-color: var(--Border-border-neutral-secondary, #E5E7EB);
--code-snippet-bg: var(--Background-background-white, #FFF);
--code-snippet-gutter-bg: var(--Background-background-neutral-50, #F9FAFB);
--code-snippet-tab-divider-color: var(--Border-border-neutral-primary, #D2D6DB);
--code-snippet-tab-active-indicator-color: var(--Border-border-primary, #1B8354);
--code-snippet-code-color: var(--Text-text-default, #161616);
--code-snippet-tab-active-text-color: var(--Text-text-default, #161616);
--code-snippet-tab-inactive-text-color: var(--Text-text-primary-paragraph, #384250);
--code-snippet-line-numbers-color: var(--colors-text-text-quarterary-500, #667085);
--code-snippet-prompt-color: var(--Text-text-secondary, #DBA102);
--code-snippet-inline-code-color: var(--Text-text-primary, #1B8354);
--code-snippet-padding: var(--spacing-3xl, 24px);
--code-snippet-content-pb: var(--spacing-4xl, 32px);
--code-snippet-tab-button-padding: var(--Tab-horizontal-tab-md-button-h-padding, 16px);
--code-snippet-tab-button-gap: var(--Tab-tab-button-gap, 4px);
--code-snippet-tab-indicator-radius: var(--radius-radius-full, 9999px);
--code-snippet-tab-button-radius: var(--Radius-radius-sm, 4px);
--code-snippet-gutter-border-color: var(--Border-border-neutral-secondary, #E5E7EB);
--code-snippet-inline-gap: 12px;
--code-snippet-font-family-mono: "Roboto Mono", monospace;
--code-snippet-font-size-code: 16px;
--code-snippet-font-size-tab: var(--Size-Text-typo-size-text-sm, 14px);
--code-snippet-line-height-tab: var(--Line-Height-Text-line-heights-text-sm, 20px);
--code-snippet-tab-font-family: var(--Font-Family-font-family-text, "IBM Plex Sans Arabic");
```

---

## Missing Standards

- No `--code-snippet-*` token namespace exists in `token.css`.
- No Platform Code standard for "code snippet" component registered yet.

---

## Known Issues

- Source file named `mainifest.json` (typo). Does not affect generation.
- Line clamp is implemented as `-webkit-line-clamp` (standard in modern browsers but prefixed).

---

## TODO

- [ ] Add `--code-snippet-*` token definitions to `token.css` (global file update — requires explicit user request).
- [ ] Confirm if a standalone `horizontal-tab-list` component CSS exists.
- [ ] Add "Copied!" aria-live feedback state for copy action.
- [ ] Consider dark theme modifier (`.code-snippet--dark`).
- [ ] Validate with axe or similar tool for full WCAG 2.1 AA compliance.
