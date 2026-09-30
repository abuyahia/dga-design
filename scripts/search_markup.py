"""Shared static search-results validation and rendering."""
import html
import re

try:
    from scripts.page_intro_markup import render_page_intro
except ImportError:
    from page_intro_markup import render_page_intro


ROUTE = re.compile(r'[a-z][a-z0-9-]*\.html(?:#[a-z][a-z0-9-]*)?')


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def validate_search_results(page):
    search = page.get('search')
    if not isinstance(search, dict) or set(search) != {'empty_message', 'records'}:
        raise ValueError('Search Results requires empty_message and records')
    if not _text(search['empty_message']) or not isinstance(search['records'], list):
        raise ValueError('Search Results data is invalid')
    routes = set()
    for record in search['records']:
        if (
            not isinstance(record, dict)
            or set(record) - {'id', 'type', 'type_label', 'title', 'summary', 'route', 'date'}
            or {'id', 'type', 'type_label', 'title', 'summary', 'route'} - set(record)
            or any(not _text(record[field]) for field in ('id', 'type', 'type_label', 'title', 'summary', 'route'))
            or not ROUTE.fullmatch(record['route'])
            or record['route'] in routes
            or 'date' in record and not _text(record['date'])
        ):
            raise ValueError('Search Results records must use the safe shared contract')
        routes.add(record['route'])


def render_search_results(page, render):
    validate_search_results(page)
    records = page['search']['records']
    types = []
    for record in records:
        pair = (record['type'], record['type_label'])
        if pair not in types:
            types.append(pair)
    options = ''.join(
        '<option value="{}">{}</option>'.format(html.escape(value, quote=True), html.escape(label))
        for value, label in types
    )
    items = ''.join(
        '<li class="search-results__item" data-search-record data-type="{type}" data-search="{search}">'
        '<article><p class="search-results__type">{type_label}</p>'
        '<h2><a class="link link--primary link--md" href="{route}">{title}</a></h2>'
        '<p>{summary}</p>{date}</article></li>'.format(
            type=html.escape(record['type'], quote=True),
            search=html.escape((record['title'] + ' ' + record['summary']).casefold(), quote=True),
            type_label=html.escape(record['type_label']), route=html.escape(record['route'], quote=True),
            title=html.escape(record['title']), summary=html.escape(record['summary']),
            date='<time datetime="{0}">{0}</time>'.format(html.escape(record['date'], quote=True)) if record.get('date') else '',
        )
        for record in records
    )
    return render('sections/search-results/template.html', {
        'page_intro': render_page_intro(page, render, variant='compact'),
        'options': options,
        'count': str(len(records)),
        'items': items,
        'empty_message': page['search']['empty_message'],
    }, ('page_intro', 'options', 'items'))
