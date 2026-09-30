"""Canonical ordered breadcrumb composition; text and URLs are escaped by render."""
from urllib.parse import urlsplit


def _validate_href(href):
    if not isinstance(href, str) or not href.strip() or href != href.strip():
        raise ValueError('Breadcrumb links require a nonempty destination')
    if any(ord(c) < 32 or ord(c) == 127 for c in href) or "\\" in href:
        raise ValueError('Invalid breadcrumb destination')
    url = urlsplit(href)
    if url.scheme:
        if url.scheme != 'https' or not url.hostname or url.username or url.password:
            raise ValueError('Breadcrumb external destinations must use HTTPS')
    elif url.netloc or href.startswith('//'):
        raise ValueError('Breadcrumb destinations must be local or HTTPS')


def render_breadcrumb(items, render, *, navigation_label='مسار التنقل'):
    """Render 1..N items; the final item is always current and non-navigable.

    Ancestors require label/href. Only the final item may set current=True.
    An optional final href is validated but deliberately not rendered.
    """
    if not isinstance(items, (list, tuple)) or not items:
        raise ValueError('Breadcrumb requires at least one item')
    if not isinstance(navigation_label, str) or not navigation_label.strip():
        raise ValueError('Breadcrumb requires a navigation label')
    rendered = []
    for index, item in enumerate(items):
        if not isinstance(item, dict) or not isinstance(item.get('label'), str) or not item['label'].strip():
            raise ValueError('Breadcrumb items require nonempty labels')
        current = index == len(items) - 1
        if 'current' in item and (not isinstance(item['current'], bool) or item['current'] != current):
            raise ValueError('Only the final breadcrumb item can be current')
        if not current or item.get('href') is not None:
            _validate_href(item.get('href'))
        content = render('components/breadcrumb/current.html' if current else 'components/breadcrumb/link.html', item)
        rendered.append(render('components/breadcrumb/item.html', {
            'modifier': (' breadcrumb__item--root' if index == 0 else '') + (' breadcrumb__item--current' if current else ''),
            'current_attribute': ' aria-current="page"' if current else '',
            'separator': render('components/breadcrumb/separator.html', {}) if index else '',
            'content': content,
        }, ('current_attribute', 'separator', 'content')))
    return render('components/breadcrumb/template.html', {
        'navigation_label': navigation_label, 'items': ''.join(rendered),
    }, ('items',))


def render_two_level(values, render):
    """Compatibility for existing root_href/root_label/current_label callers."""
    return render_breadcrumb([
        {'label': values['root_label'], 'href': values['root_href']},
        {'label': values['current_label'], 'current': True},
    ], render)
