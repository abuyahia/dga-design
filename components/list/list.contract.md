# List Component Contract

**Component**: `list`
**Version**: 1.0.0
**Status**: pending_audit

---

## Overview

The List component renders ordered, unordered, or icon-annotated lists. It supports two nesting levels (Level One and Level Two) and three visual styles (Primary, Neutral, On-Color). Fully bilingual: LTR and RTL via the `dir` attribute.

The component consists of two reusable parts:
- **List** — the container (`<ol>` or `<ul>`)
- **List item** — the atomic row (`<li>`)

---

## HTML Structure

**Markers are CSS-generated. There is no marker element in the HTML.**

Ordered and unordered list markers (numbers, letters, dash, bullet) are produced by CSS counters and `::before` / `::after` pseudo-elements. The `<li>` contains only the text content.

### Ordered list (LTR and RTL)

```html
<!-- LTR: CSS ::before generates "1-", "a-", etc. on the left -->
<ol class="list list--ordered list--primary" role="list">
  <li class="list__item list__item--level-one">
    <span class="list__text">Item text</span>
  </li>
  <li class="list__item list__item--level-two">
    <span class="list__text">Sub-item text</span>
  </li>
</ol>

<!-- RTL: same DOM. CSS ::after generates "-1", "أ-" etc. on the left.
     dir="rtl" on this element or any ancestor activates RTL markers. -->
<ol class="list list--ordered list--primary" role="list" dir="rtl">
  <li class="list__item list__item--level-one">
    <span class="list__text">عنصر قائمة</span>
  </li>
  <li class="list__item list__item--level-two">
    <span class="list__text">عنصر قائمة</span>
  </li>
</ol>
```

### Unordered list (LTR and RTL)

```html
<!-- LTR: CSS ::before generates "-" (level one) and "•" (level two) -->
<ul class="list list--unordered list--neutral" role="list">
  <li class="list__item list__item--level-one">
    <span class="list__text">Item text</span>
  </li>
  <li class="list__item list__item--level-two">
    <span class="list__text">Nested item text</span>
  </li>
</ul>

<!-- RTL: same DOM. CSS ::after generates the same characters on the left. -->
<ul class="list list--unordered list--neutral" role="list" dir="rtl">
  <li class="list__item list__item--level-one">
    <span class="list__text">عنصر قائمة</span>
  </li>
  <li class="list__item list__item--level-two">
    <span class="list__text">عنصر قائمة</span>
  </li>
</ul>
```

### With Icon list

```html
<!-- LTR and RTL: same DOM order [.list__icon][.list__text].
     CSS `order: 1` on .list__icon in RTL pushes it to the visual LEFT.
     No DOM change needed between LTR and RTL. -->
<ul class="list list--with-icon list--primary" role="list">
  <li class="list__item list__item--level-one">
    <span class="list__icon" aria-hidden="true">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true" focusable="false">
        <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1"/>
        <path d="M5 8.5L7 10.5L11 6" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </span>
    <span class="list__text">Item text</span>
  </li>
  <li class="list__item list__item--level-two">
    <span class="list__icon" aria-hidden="true">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true" focusable="false">
        <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1"/>
        <path d="M5 8.5L7 10.5L11 6" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </span>
    <span class="list__text">Nested item text</span>
  </li>
</ul>
```

---

## CSS Modifiers

### Container modifiers (applied to `<ol>` or `<ul>`)

| Modifier           | Effect                                    |
|--------------------|-------------------------------------------|
| `.list--ordered`   | Ordered list (pair with `<ol>`)           |
| `.list--unordered` | Unordered list (pair with `<ul>`)         |
| `.list--with-icon` | Icon-annotated list (pair with `<ul>`)    |
| `.list--primary`   | Brand green text (`--list-text-primary`)  |
| `.list--neutral`   | Default dark text (`--list-text-neutral`) |
| `.list--on-color`  | White text (`--list-text-oncolor`)        |

### Item modifiers (applied to `<li>`)

| Modifier                    | Effect                                             |
|-----------------------------|----------------------------------------------------|
| `.list__item--level-one`    | No indent (default)                                |
| `.list__item--level-two`    | 24px inline-start indent (`--list-item-indent`)    |

---

## Anatomy

| Element             | Tag    | Class              | Notes                                              |
|---------------------|--------|--------------------|----------------------------------------------------|
| List container      | ol/ul  | `.list`            | `role="list"` required                             |
| List item row       | li     | `.list__item`      | —                                                  |
| Marker (ordered)    | —      | `::before` / `::after` | CSS-generated. No HTML element. LTR=`::before`, RTL=`::after` |
| Marker (unordered)  | —      | `::before` / `::after` | CSS-generated. No HTML element.                |
| Icon wrapper        | span   | `.list__icon`      | With Icon type only. `aria-hidden="true"` required |
| Item text           | span   | `.list__text`      | —                                                  |

---

## Tokens

All `--list-*` tokens are proposed and must be added to `token.css`.

| Token                        | Proposed value                           |
|------------------------------|------------------------------------------|
| `--list-text-primary`        | `var(--Text-text-primary)`               |
| `--list-text-neutral`        | `var(--Text-text-default)`               |
| `--list-text-oncolor`        | `var(--Text-text-oncolor-primary)`       |
| `--list-item-gap`            | `var(--Global-spacing-md)` = 8px         |
| `--list-item-indent`         | `var(--Global-spacing-3xl)` = 24px       |
| `--list-item-font-family`    | `var(--Font-Family-font-family-text)`    |
| `--list-item-font-size`      | `var(--Size-Text-typo-size-text-md)`     |
| `--list-item-line-height`    | `var(--Line-Height-Text-line-heights-text-md)` |
| `--list-item-icon-size`      | `16px`                                   |
| `--list-item-font-weight`    | `400`                                    |

---

## Accessibility Requirements

| Requirement                            | Implementation                                                    |
|----------------------------------------|-------------------------------------------------------------------|
| List role preserved with Safari        | `role="list"` on container                                        |
| Icon accessible label suppressed       | `aria-hidden="true"` on `.list__icon`                             |
| Accessible text always present         | `.list__text` provides readable label for every item              |
| No interactive focus behavior          | List items are non-interactive; no `tabindex` or role needed      |
| Bidirectional text                     | `dir="rtl"` on container or parent `<html>` for RTL layouts       |

---

## States

None. This component has no interactive states.

---

## RTL Behavior

### Ordered and Unordered markers

In LTR flex layout, `::before` is the first flex item and appears on the **LEFT**.
In RTL flex layout, `::before` (first item) would appear on the **RIGHT** — incorrect for a list marker.

Solution: in RTL contexts, `::before` is cleared (`content: none`) and `::after` is used instead. `::after` is the last flex item, which in RTL flex appears on the **LEFT**. ✓

This is activated automatically by `[dir="rtl"]` on the `.list` or any ancestor — no extra classes needed.

### With Icon position

DOM order is always `[.list__icon][.list__text]`. In RTL, CSS `order: 1` on `.list__icon` pushes the icon to the visual end (LEFT). No DOM change is needed between LTR and RTL.

### Level Two indent

`padding-inline-start` is a CSS logical property: resolves to `padding-left` in LTR and `padding-right` in RTL automatically.

| Element              | LTR                            | RTL                            |
|----------------------|--------------------------------|--------------------------------|
| Ordered marker       | `::before` → LEFT              | `::after` → LEFT               |
| Unordered marker     | `::before` → LEFT              | `::after` → LEFT               |
| With Icon position   | `[icon][text]` → natural       | `order:1` → icon visual LEFT   |
| Level Two indent     | `padding-left: 24px`           | `padding-right: 24px`          |

---

## Marker Reference

| Type      | Level | LTR (::before)        | RTL (::after)           |
|-----------|----|----------------------|------------------------|
| Ordered   | One   | `counter() + "-"`  = `1-` | `"-" + counter()` = `-1` |
| Ordered   | Two   | `lower-alpha + "-"` = `a-` | `arabic-alpha + "-"` = `أ-` |
| Unordered | One   | `"-"`               | `"-"`                  |
| Unordered | Two   | `"•"`               | `"•"`                  |
| With Icon | —     | — (icon via HTML)   | — (icon via HTML, `order:1`) |

---

## On-Color Usage

The `--on-color` style variant renders white text. The consuming layout **must** provide a dark or brand-color background. This component does not define its own background.

```html
<section style="background: var(--sa-600);">
  <ul class="list list--unordered list--on-color" role="list">
    ...
  </ul>
</section>
```

---

## Do Not

- Do not apply `.list--on-color` on a white or light background — text will be invisible.
- Do not omit `role="list"` when using `list-style: none` — VoiceOver/Safari will lose list semantics.
- Do not omit `aria-hidden="true"` on `.list__icon` — the SVG will create redundant AT output.
- Do not nest a `.list` inside another `.list` without using the Level Two modifier on items — indent will be missing.
