# Breadcrumb composition contract

Use `render_breadcrumb(items, render, navigation_label='مسار التنقل')` from
`scripts/breadcrumb_markup.py` with the project's escaping fragment renderer.

```python
render_breadcrumb([
    {'label': 'Home', 'href': 'index.html'},
    {'label': 'Services', 'href': 'services.html'},
    {'label': 'Current service', 'current': True},
], render)
```

- Accepts an ordered, nonempty list/tuple of 1..N items.
- Each label must be nonempty text. The renderer escapes labels, navigation labels
  and href attributes through the existing `render` function.
- Ancestors require a local relative/root-relative/fragment URL or an HTTPS URL.
  Protocol-relative URLs, credentials, other schemes, backslashes and control
  characters are rejected. Destinations need not exist at render time; the caller
  owns route existence checks.
- The final item is always a non-navigable span inside an li carrying
  `aria-current="page"`. `current: true` is optional there. Explicit current flags
  must agree with position. An optional final href is validated but not emitted.
- A one-item trail has one current item and no separator.
- Root label/destination come entirely from the list; there is no root default in
  the canonical renderer. The navigation label is independently configurable.
- `template.html`, `item.html`, `link.html`, `current.html` and `separator.html`
  are fragments of the existing Breadcrumb component, not new components.
- Presentation remains in `breadcrumb.css`: the same wrapping list, link/current
  styles and RTL separator flip apply at every depth. No JavaScript is required.

## Compatibility and consumers

The site builder still accepts
`render('components/breadcrumb/two-level.html', {root_href, root_label, current_label})`.
Its compatibility adapter calls `render_two_level`, which delegates to
`render_breadcrumb`; `two-level.html` only inserts the resulting trusted markup.
Page Intro and Heavy Content keep their existing calls. Service Detail and Contact
call the list renderer directly and insert its output as a trusted section slot.
A different build integration should call `render_two_level` explicitly rather
than treating the compatibility fragment as a standalone text-substitution API.

Consumers own page placement and breadcrumb data. They do not construct nav/li or
separator markup. This change adopts the existing canonical separator for Contact
and Service Detail; their former template-asset arrow rules are no longer needed.
It does not claim pixel identity with those previous independent implementations.
