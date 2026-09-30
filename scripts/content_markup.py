"""Validate and render the reusable heavy-content template."""
import html
import re
try:
    from scripts.page_intro_markup import render_page_intro
except ImportError:
    from page_intro_markup import render_page_intro


SLUG = re.compile(r'[a-z][a-z0-9-]*')
BLOCK_TYPES = {'paragraph', 'ordered-list', 'unordered-list', 'metadata-list', 'link', 'media'}


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _safe_href(value, paths):
    if not _text(value):
        return False
    if value.startswith('https://'):
        return True
    target = value.partition('#')[0]
    return target in paths


def _validate_blocks(blocks, paths):
    if not isinstance(blocks, list) or not blocks:
        raise ValueError('Content sections require blocks')
    for block in blocks:
        if not isinstance(block, dict) or block.get('type') not in BLOCK_TYPES:
            raise ValueError('Unsupported content block')
        kind = block['type']
        if kind == 'paragraph' and not _text(block.get('text')):
            raise ValueError('Paragraph blocks require text')
        if kind in ('ordered-list', 'unordered-list') and (not isinstance(block.get('items'), list) or not block['items'] or any(not _text(item) for item in block['items'])):
            raise ValueError('List blocks require text items')
        if kind == 'metadata-list':
            items = block.get('items')
            if (
                not isinstance(items, list) or not items
                or any(
                    not isinstance(item, dict)
                    or set(item) != {'label', 'value'}
                    or not _text(item['label']) or not _text(item['value'])
                    for item in items
                )
            ):
                raise ValueError('Metadata lists require label and value text')
        if kind == 'link':
            planned_route = block.get('planned_route')
            if planned_route is not None:
                if (
                    set(block) != {'type', 'label', 'planned_route'}
                    or not _text(block.get('label'))
                    or not _text(planned_route)
                    or not re.fullmatch(r'[a-z][a-z0-9-]*\.html', planned_route)
                    or planned_route in paths
                ):
                    raise ValueError('Planned link blocks require one safe, not-yet-generated route')
            elif not _text(block.get('label')) or not _safe_href(block.get('href'), paths):
                raise ValueError('Link blocks require a safe destination')
        if kind == 'media' and not _text(block.get('alt')):
            raise ValueError('Media blocks require alternative text')
        if kind == 'media' and block.get('caption') is not None and not _text(block['caption']):
            raise ValueError('Media captions must be nonempty text')


def validate_heavy_content(page, paths):
    content = page.get('heavy_content')
    if not isinstance(content, dict) or not _text(content.get('overview')):
        raise ValueError('Heavy content requires an overview')
    sections = content.get('sections')
    if not isinstance(sections, list) or not sections:
        raise ValueError('Heavy content requires sections')
    ids = []
    for section in sections:
        if not isinstance(section, dict) or not SLUG.fullmatch(section.get('id', '')) or not _text(section.get('title')):
            raise ValueError('Content sections require a slug and title')
        ids.append(section['id'])
        _validate_blocks(section.get('blocks'), paths)
        subsections = section.get('subsections', [])
        if not isinstance(subsections, list):
            raise ValueError('Subsections must be a list')
        for subsection in subsections:
            if not isinstance(subsection, dict) or not SLUG.fullmatch(subsection.get('id', '')) or not _text(subsection.get('title')):
                raise ValueError('Content subsections require a slug and title')
            ids.append(subsection['id'])
            _validate_blocks(subsection.get('blocks'), paths)
    if len(ids) != len(set(ids)):
        raise ValueError('Content section IDs must be unique')


def _render_list(block):
    ordered = block['type'] == 'ordered-list'
    tag = 'ol' if ordered else 'ul'
    kind = 'ordered' if ordered else 'unordered'
    items = ''.join('<li class="list__item list__item--level-one"><span class="list__text">{}</span></li>'.format(html.escape(item)) for item in block['items'])
    return '<{0} class="list list--{1} list--primary" role="list">{2}</{0}>'.format(tag, kind, items)


def _render_block(block):
    kind = block['type']
    if kind == 'paragraph':
        return '<p>{}</p>'.format(html.escape(block['text']))
    if kind in ('ordered-list', 'unordered-list'):
        return _render_list(block)
    if kind == 'metadata-list':
        items = ''.join(
            '<div class="heavy-content__metadata-item"><dt>{}</dt><dd><bdi>{}</bdi></dd></div>'.format(
                html.escape(item['label']), html.escape(item['value'])
            )
            for item in block['items']
        )
        return '<dl class="heavy-content__metadata">{}</dl>'.format(items)
    if kind == 'link':
        if block.get('planned_route'):
            return '<p><a class="link link--primary link--md" role="link" aria-disabled="true">{}<span class="sr-only"> — صفحة مخطط تنفيذها لاحقًا</span></a></p>'.format(html.escape(block['label']))
        return '<p><a class="link link--primary link--md" href="{}">{}</a></p>'.format(html.escape(block['href'], quote=True), html.escape(block['label']))
    caption = '<figcaption>{}</figcaption>'.format(html.escape(block['caption'])) if block.get('caption') else ''
    return '<figure class="heavy-content__media"><div class="heavy-content__media-placeholder" role="img" aria-label="{}"></div>{}</figure>'.format(html.escape(block['alt'], quote=True), caption)


def validate_content_blocks(blocks, paths=()):
    """Public shared block-contract entry point for composed detail renderers."""
    _validate_blocks(blocks, set(paths))


def render_content_blocks(blocks):
    """Render already validated Heavy Content blocks without its page shell."""
    return ''.join(_render_block(block) for block in blocks)


def render_heavy_content(page, render):
    content = page['heavy_content']
    toc_items = []
    rendered_sections = []
    first = True
    for section in content['sections']:
        toc_items.append(render('components/table-of-contents/item.html', {
            'id': section['id'], 'label': section['title'], 'nested_class': '',
            'current': ' aria-current="location"' if first else '',
        }, ('nested_class', 'current')))
        first = False
        rendered_subsections = []
        for subsection in section.get('subsections', []):
            toc_items.append(render('components/table-of-contents/item.html', {
                'id': subsection['id'], 'label': subsection['title'],
                'nested_class': ' table-of-contents__list-item--nested', 'current': '',
            }, ('nested_class', 'current')))
            rendered_subsections.append(render('sections/heavy-content/subsection.html', {
                **subsection, 'blocks': ''.join(_render_block(block) for block in subsection['blocks'])
            }, ('blocks',)))
        rendered_sections.append(render('sections/heavy-content/section.html', {
            **section,
            'blocks': ''.join(_render_block(block) for block in section['blocks']),
            'subsections': ''.join(rendered_subsections),
        }, ('blocks', 'subsections')))

    description_markup = render('sections/page-intro/description-group.html', {
        'description': page['description'], 'supplement': content['overview'],
    })
    page_intro = render_page_intro(page, render, description_markup=description_markup)
    toc = render('components/table-of-contents/template.html', {
        'page_title': page['title'], 'items': ''.join(toc_items),
    }, ('items',))
    return render('sections/heavy-content/template.html', {
        **page, 'overview': content['overview'], 'page_intro': page_intro,
        'toc': toc, 'sections': ''.join(rendered_sections),
    }, ('page_intro', 'toc', 'sections'))
