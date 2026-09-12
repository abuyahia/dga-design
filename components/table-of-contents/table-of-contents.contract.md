# Table of Contents — Component Contract

```
contract_version: 1.0.0
component_id: table-of-contents
status: stable
category: navigation
```

## Purpose

Provides an in-page outline for long content. Each item is an anchor whose fragment matches the `id` of a page section. Native links remain functional without JavaScript.

## Structure

- `.table-of-contents` is a `nav` with a descriptive accessible label.
- `.table-of-contents__header` contains the context label and page title.
- `.table-of-contents__list` is an ordered list whose visual numbering is removed.
- `.table-of-contents__link` targets one section in the current page.
- `.table-of-contents__list-item--nested` marks a subsection with a neutral logical-edge rule.

The active link uses `aria-current="location"`. The optional template script updates this state when a link is activated or the reader scrolls. The server-rendered first item provides a useful initial state.

## Accessibility and behavior

- Use native anchor links and valid, unique section IDs.
- Keep the navigation before the article sections in DOM order.
- Use `aria-current="location"` on one link at a time.
- Do not use tab roles: items navigate within the document and do not switch panels.
- Section targets use `tabindex="-1"` so fragment navigation can move programmatic focus when needed.
- The component uses logical properties and needs no separate RTL markup.

## Responsive use

The component owns its internal presentation only. Its parent decides whether it appears beside or above the content. In the heavy-content template it is a sticky 222px column on larger screens and a normal full-width block on mobile.
