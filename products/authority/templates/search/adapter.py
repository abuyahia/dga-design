"""Derive the Authority static search index from registered content."""
import re


SAFE_ROUTE = re.compile(r'[a-z][a-z0-9-]*\.html')
TYPE_LABELS = {
    'institutional': 'عن الهيئة',
    'leadership': 'القيادة',
    'interaction': 'المشاركة والتواصل',
    'services': 'الخدمات',
    'media': 'الأخبار',
    'portfolio': 'البرامج والمبادرات',
    'knowledge': 'المعرفة',
    'regulatory': 'التنظيمات',
}


def _kind(page):
    path = page['path']
    sections = set(page['sections'])
    if path in {'about.html', 'mandate.html', 'strategy.html', 'organization.html'}:
        return 'institutional'
    if path == 'leadership.html':
        return 'leadership'
    if path in {'contact.html', 'faq.html'}:
        return 'interaction'
    if 'editorial-listing' in sections or 'editorial-detail' in sections:
        return 'media'
    if 'portfolio-listing' in sections or 'portfolio-detail' in sections:
        return 'portfolio'
    if 'resource-listing' in sections or 'resource-detail' in sections:
        return 'knowledge'
    if 'regulatory-listing' in sections or 'regulatory-detail' in sections:
        return 'regulatory'
    return None


def apply(data, content_root=None):
    search_page = next((page for page in data['pages'] if page['path'] == 'search.html'), None)
    if search_page is None:
        return data
    records = []
    routes = set()
    for page in data['pages']:
        kind = _kind(page)
        if not kind or page['path'] in routes or not SAFE_ROUTE.fullmatch(page['path']):
            continue
        records.append({
            'id': page['path'][:-5], 'type': kind, 'type_label': TYPE_LABELS[kind],
            'title': page['title'], 'summary': page.get('description', page['title']),
            'route': page['path'], **({'date': page['updated']} if page.get('updated') else {}),
        })
        routes.add(page['path'])
    for service in data.get('services', []):
        route = 'service-' + service['id'] + '.html'
        if route in routes:
            continue
        records.append({
            'id': 'service-' + service['id'], 'type': 'services',
            'type_label': TYPE_LABELS['services'], 'title': service['title'],
            'summary': service['description'], 'route': route,
            **({'date': service['updated']} if service.get('updated') else {}),
        })
        routes.add(route)
    search_page['search']['records'] = records
    return data
