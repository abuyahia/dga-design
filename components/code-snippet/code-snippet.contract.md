# Code Snippet Contract

## Component Type

Composite

---

## Dependencies

Required:

- `button` — used for copy icon button and show-more button
- `tab` — tab bar uses `.tab-list--h` and `.tab--h` from `tab/tab.css`

---

## Anatomy

### Multi-Line

| Element | Class | Role |
|---|---|---|
| Root | `.code-snippet` | Container, surface, border |
| Tab bar wrapper | `.tab-list.tab-list--h` (from `tab.css`) | `role="tablist"`, holds tabs + divider `::after` |
| Tab button | `.tab.tab--h` (from `tab.css`) | `role="tab"`, language selector |
| Tab text | `.tab__text` (from `tab.css`) | Label inside tab |
| Body | `.code-snippet__body` | Flex row: gutter + content |
| Gutter | `.code-snippet__gutter` | Line numbers sidebar |
| Line numbers | `.code-snippet__line-numbers` | `aria-hidden="true"`, presentational |
| Content | `.code-snippet__content` | Code + actions column |
| Code row | `.code-snippet__code-row` | Code text + copy button row |
| Code | `.code-snippet__code` | `<pre><code>`, clamped to 20 lines by default |
| Copy button | `.code-snippet__copy` | Icon-only Button, `aria-label="Copy code"` |
| Show more | `.code-snippet__show-more` | Button, `aria-expanded`, toggles expanded state |

### Single-Line

| Element | Class | Role |
|---|---|---|
| Root | `.code-snippet.code-snippet--single` | Container, surface, border |
| Inline row | `.code-snippet__inline` | Flex row: prompt + command |
| Prompt | `.code-snippet__prompt` | Keyword prefix (e.g. `npm`) |
| Inline code | `.code-snippet__inline-code` | Command text |
| Copy button | `.code-snippet__copy` | Icon-only Button, `aria-label="Copy code"` |

---

## Variants

| Variant | CSS Modifier | Description |
|---|---|---|
| Multi-Line | (default, no modifier) | Language tabs, gutter, multi-line code block |
| Single-Line | `.code-snippet--single` | Inline command row, no tabs or line numbers |

---

## States

| State | Selector | Description |
|---|---|---|
| Tab default | `.code-snippet__tab` | Inactive tab: medium weight, secondary text |
| Tab active | `.code-snippet__tab[aria-selected="true"]` | Bold weight, default text, green indicator |
| Tab hover | `.code-snippet__tab:hover` | Hover background tint |
| Tab focus | `.code-snippet__tab:focus-visible` | Focus ring outline |
| Expanded | `.code-snippet--expanded .code-snippet__code` | No line clamp |

---

## ARIA Requirements

| Element | Attribute | Value |
|---|---|---|
| Tab bar | `role` | `tablist` |
| Tab bar | `aria-label` | Language selector label |
| Tab button | `role` | `tab` |
| Tab button | `aria-selected` | `true` / `false` |
| Tab button | `aria-controls` | ID of associated `tabpanel` |
| Code panel | `role` | `tabpanel` |
| Code panel | `aria-labelledby` | ID of associated tab |
| Line numbers | `aria-hidden` | `true` |
| Copy button | `aria-label` | `"Copy code"` |
| Show more | `aria-expanded` | `true` / `false` |

---

## Token API

All tokens are component-level semantic tokens. All are currently proposed (not yet in `token.css`).

```css
--code-snippet-border-radius
--code-snippet-border-color
--code-snippet-bg
--code-snippet-gutter-bg
--code-snippet-gutter-border-color
--code-snippet-tab-divider-color
--code-snippet-tab-active-indicator-color
--code-snippet-code-color
--code-snippet-tab-active-text-color
--code-snippet-tab-inactive-text-color
--code-snippet-line-numbers-color
--code-snippet-prompt-color
--code-snippet-inline-code-color
--code-snippet-padding
--code-snippet-content-pb
--code-snippet-tab-button-padding
--code-snippet-tab-button-gap
--code-snippet-tab-indicator-radius
--code-snippet-tab-button-radius
--code-snippet-inline-gap
--code-snippet-font-family-mono
--code-snippet-font-size-code
--code-snippet-font-size-tab
--code-snippet-line-height-tab
--code-snippet-tab-font-family
```

---

## Keyboard Behavior

| Key | Context | Action |
|---|---|---|
| `Tab` | Code snippet | Move focus to tab bar, then copy button, then show more |
| `ArrowLeft` / `ArrowRight` | Inside `role="tablist"` | Move focus between language tabs |
| `Enter` / `Space` | On a `role="tab"` | Activate the tab |
| `Enter` / `Space` | On copy button | Copy code to clipboard |
| `Enter` / `Space` | On show more button | Toggle expanded state |

---

## JS Responsibilities

The following behaviors require JavaScript:

1. Tab switching — update `aria-selected`, show/hide panels, move focus between tabs with arrow keys.
2. Copy to clipboard — `navigator.clipboard.writeText()`, optionally announce "Copied!" via `aria-live`.
3. Show More toggle — toggle `.code-snippet--expanded`, toggle `aria-expanded` on the button.
4. Line number generation — optionally count lines in `<code>` and generate `<span>` elements in gutter.

---

## Pseudo-Element Specification

| Selector | Pseudo | CSS property | Purpose |
|---|---|---|---|
| `.code-snippet__tab-bar` | `::after` | `height: 3px; background: var(--code-snippet-tab-divider-color); bottom: 0` | Full-width divider line |
| `.code-snippet__tab[aria-selected="true"]` | `::after` | `height: 3px; background: var(--code-snippet-tab-active-indicator-color); bottom: 0` | Active tab green indicator |

---

## Usage Example — Multi-Line

```html
<div class="code-snippet" data-code-snippet>
  <div class="code-snippet__tab-bar" role="tablist" aria-label="Select language">
    <div class="code-snippet__tabs">
      <button class="code-snippet__tab" role="tab" aria-selected="true" aria-controls="panel-java" id="tab-java">
        <span class="code-snippet__tab-text">Java</span>
      </button>
      <button class="code-snippet__tab" role="tab" aria-selected="false" aria-controls="panel-python" id="tab-python" tabindex="-1">
        <span class="code-snippet__tab-text">Python</span>
      </button>
    </div>
  </div>
  <div class="code-snippet__body">
    <div class="code-snippet__gutter" aria-hidden="true">
      <span class="code-snippet__line-numbers">1&#10;2&#10;3</span>
    </div>
    <div class="code-snippet__content" role="tabpanel" id="panel-java" aria-labelledby="tab-java">
      <div class="code-snippet__code-row">
        <pre class="code-snippet__code"><code>// your code here</code></pre>
        <button class="code-snippet__copy btn btn--ghost btn--icon btn--lg" type="button" aria-label="Copy code">
          <svg width="24" height="24" aria-hidden="true"><!-- copy icon --></svg>
        </button>
      </div>
      <button class="code-snippet__show-more btn btn--ghost btn--md" type="button" aria-expanded="false">
        <span>Show More</span>
        <svg width="20" height="20" aria-hidden="true"><!-- chevron icon --></svg>
      </button>
    </div>
  </div>
</div>
```

---

## Usage Example — Single-Line

```html
<div class="code-snippet code-snippet--single" data-code-snippet>
  <div class="code-snippet__inline">
    <span class="code-snippet__prompt">npm</span>
    <span class="code-snippet__inline-code">npm install nds-design-system@^0.0.1</span>
  </div>
  <button class="code-snippet__copy btn btn--ghost btn--icon btn--md" type="button" aria-label="Copy code">
    <svg width="20" height="20" aria-hidden="true"><!-- copy icon --></svg>
  </button>
</div>
```

---

## Out of Scope

- Syntax highlighting (not in manifest; future enhancement)
- Dark theme variant (not in manifest; future enhancement)
- Line number auto-generation from code content (JS enhancement; template uses static)
- RTL layout variation (IBM Plex Sans Arabic is referenced but no RTL CSS delta in manifest)
