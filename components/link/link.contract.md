# Link — Component Contract

```
contract_version: 1.0.0
component_id:     link
status:           stable
category:         navigation
last_reviewed:    2026-06-09
```

---

## 1. Purpose

A Link navigates the user to another page, URL, or anchor within the current page.

It is NOT an action trigger. Use `<button>` (or the Button component) when a click causes something to happen on the current page without navigation.

> AI Rule: If the intent is "go to X", render a Link. If the intent is "do X", render a Button.

---

## 2. When to Use / When NOT to Use

| Situation | Use Link? |
|---|---|
| Navigate to another page or URL | Yes |
| Navigate to an anchor on the current page | Yes |
| Open a new browser tab | Yes — add `target="_blank"` + accessible label |
| Submit a form | No — use Button |
| Open a modal or dialog | No — use Button |
| Toggle a state on the current page | No — use Button with `aria-pressed` |
| Represent a destructive action | No — use Button |

---

## 3. Anatomy

```
.link                     ← root element (<a>)
  [text content]          ← visible label (direct text or <span>)
```

**Slot rules:**

| Slot | Required | Notes |
|---|---|---|
| Text content | Always | The visible label. Screen readers read this as the link name. |

---

## 4. CSS Modifiers

| Modifier | Description | Required? |
|---|---|---|
| `.link--primary` | Green brand link color | Default style if omitted |
| `.link--neutral` | Grey neutral link color | Style modifier |
| `.link--on-color` | White link for dark/color backgrounds | Style modifier |
| `.link--md` | Medium size (16px / 24px line-height) | Default is Small (14px) |
| `.link--inline` | Persistent underline in all states | For links embedded in paragraph text |

---

## 5. HTML Contract

### Standard link (primary, small)
```html
<a class="link link--primary" href="/destination">Link Text</a>
```

### Neutral link
```html
<a class="link link--neutral" href="/destination">Link Text</a>
```

### On-color link (on dark background)
```html
<a class="link link--on-color" href="/destination">Link Text</a>
```

### Medium size
```html
<a class="link link--primary link--md" href="/destination">Link Text</a>
```

### Inline link (inside paragraph text)
```html
<p>
  Read the
  <a class="link link--primary link--inline" href="/policy">Privacy Policy</a>
  for details.
</p>
```

### Disabled link
```html
<a class="link link--primary" href="/destination" aria-disabled="true" tabindex="-1">Link Text</a>
```

> `tabindex="-1"` removes the link from the tab order. Add a JavaScript click guard to prevent navigation when `aria-disabled="true"` is present.

### External link (opens in new tab)
```html
<a class="link link--primary" href="https://example.com" target="_blank" rel="noopener noreferrer">
  External Resource
  <span class="sr-only">(opens in new tab)</span>
</a>
```

### RTL (Arabic)
```html
<a class="link link--primary" href="/destination" dir="rtl">رابط</a>
```

Or set `dir="rtl"` on a parent element.

---

## 6. States

| State | How triggered | CSS |
|---|---|---|
| Default | Initial render | `.link` base styles |
| Visited | After user has visited the href | `.link:visited` |
| Hovered | Mouse pointer over element | `.link:not([aria-disabled]):hover` |
| Pressed | Mouse/touch held down | `.link:not([aria-disabled]):active` |
| Focused | Keyboard focus | `.link:focus-visible` |
| Disabled | `aria-disabled="true"` on element | `.link[aria-disabled="true"]` |

---

## 7. Style × State Color Reference

### Primary

| State | Color token |
|---|---|
| Default | `--Link-link-primary` (#1B8354) |
| Visited | `--Link-link-primary-visited` (#14573A) |
| Hovered | `--Link-link-primary-hovered` (#54C08A) |
| Pressed | `--Link-link-primary-pressed` (#88D8AD) |
| Focused | Same as Default |
| Disabled | `--Global-text-default-disabled` (#9DA4AE) |

### Neutral

| State | Color token |
|---|---|
| Default | `--Link-link-neutral` (#384250) |
| Visited | `--Link-link-primary-visited` (#14573A) ¹ |
| Hovered | `--Link-link-neutral-hovered` (#6C737F) |
| Pressed | `--Link-link-neutral-pressed` (#9DA4AE) |
| Focused | Same as Default |
| Disabled | `--Global-text-default-disabled` (#9DA4AE) |

¹ Neutral Visited intentionally uses the primary-visited token per Figma design. No separate neutral-visited token exists.

### On-color

| State | Color token |
|---|---|
| Default | `--Link-link-oncolor` (#FFF) |
| Visited | `--Link-link-oncolor-visited` (rgba 255,255,255,0.90) |
| Hovered | `--Link-link-oncolor-hovered` (rgba 255,255,255,0.80) |
| Pressed | `--Link-link-oncolor-pressed` (rgba 255,255,255,0.60) |
| Focused | Same as Default |
| Disabled | `--Link-link-oncolor-disabled` (rgba 255,255,255,0.30) |

---

## 8. Focus Ring

| Style | Focus ring color | Source token |
|---|---|---|
| Primary, Neutral | Black, 2px solid | `--Border-border-black` (#161616) |
| On-color | White, 2px solid | `--Border-border-white` (#FFF) |

Offset: 2px. Radius: 2px.

**Implementation note:** Figma encodes focus as `border` on the root element. The CSS implementation uses `outline` to avoid layout shift. This is an intentional deviation.

---

## 9. Text Decoration Behavior

| State | Inline=False | Inline=True |
|---|---|---|
| Default | none | underline |
| Visited | none | underline |
| Hovered | underline | underline |
| Pressed | underline | underline |
| Focused | none | underline |
| Disabled | none | none |

`text-decoration-skip-ink: none` and `text-underline-position: from-font` are applied on all underlined states to ensure correct rendering with Arabic (and other) text.

---

## 10. Accessibility Requirements

| Requirement | Rule ID |
|---|---|
| `<a>` must have `href` for keyboard operability | LNK-A11Y-001 |
| Disabled link must have `aria-disabled="true"` | LNK-A11Y-002 |
| Disabled link must have `tabindex="-1"` | LNK-A11Y-003 |
| Disabled link must have JS click guard | LNK-A11Y-004 |
| External links must communicate `target="_blank"` to screen readers | LNK-A11Y-005 |
| Focus ring must not be suppressed by `outline: none` | LNK-A11Y-006 |

---

## 11. What NOT to Do

```html
<!-- WRONG: using button role for navigation -->
<a class="link link--primary" role="button" href="#">Go to page</a>

<!-- WRONG: link without href (not keyboard focusable) -->
<a class="link link--primary">Link Text</a>

<!-- WRONG: hardcoded color instead of token -->
<a class="link" style="color: #1B8354;">Link Text</a>

<!-- WRONG: using disabled attribute on <a> (invalid HTML) -->
<a class="link link--primary" disabled href="#">Link Text</a>

<!-- WRONG: outline: none on focused link -->
<a class="link link--primary" style="outline: none;">Link Text</a>
```

---

## 12. Assembly Awareness

The Link component may participate in the following assemblies:

| Assembly | Role |
|---|---|
| Breadcrumb | Individual navigation crumbs |
| Navigation | Menu items |
| Pagination | Page number links |
| Rich text / Body content | Inline `link--inline` variant |
| Footer | Footer navigation links |

Do not embed Button inside Link or Link inside Button.
