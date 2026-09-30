"""Shared validation and semantic rendering for organization hierarchies."""
import html
import re

try:
    from scripts.page_intro_markup import render_page_intro
except ImportError:
    from page_intro_markup import render_page_intro


SLUG = re.compile(r'[a-z][a-z0-9-]*')


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def validate_organization(page):
    data = page.get('organization')
    if not isinstance(data, dict) or set(data) != {'summary', 'nodes'} or not _text(data['summary']):
        raise ValueError('Organization requires summary and nodes')
    nodes = data['nodes']
    if not isinstance(nodes, list) or not nodes:
        raise ValueError('Organization nodes must be a nonempty list')
    ids = []
    by_id = {}
    for node in nodes:
        if (
            not isinstance(node, dict) or set(node) != {'id', 'parent_id', 'label', 'description'}
            or not SLUG.fullmatch(node.get('id', ''))
            or node.get('parent_id') is not None and not SLUG.fullmatch(node.get('parent_id', ''))
            or not _text(node.get('label')) or not _text(node.get('description'))
        ):
            raise ValueError('Organization nodes require id, parent_id, label and description')
        ids.append(node['id'])
        by_id[node['id']] = node
    if len(ids) != len(set(ids)):
        raise ValueError('Organization node ids must be unique')
    roots = [node for node in nodes if node['parent_id'] is None]
    if len(roots) != 1:
        raise ValueError('Organization requires exactly one root')
    if any(node['parent_id'] is not None and node['parent_id'] not in by_id for node in nodes):
        raise ValueError('Organization contains an orphan node')
    for node in nodes:
        visited = set()
        current = node
        while current['parent_id'] is not None:
            if current['id'] in visited:
                raise ValueError('Organization contains a cycle')
            visited.add(current['id'])
            current = by_id[current['parent_id']]


def render_organization(page, render):
    validate_organization(page)
    nodes = page['organization']['nodes']
    children = {node['id']: [] for node in nodes}
    roots = []
    for node in nodes:
        if node['parent_id'] is None:
            roots.append(node)
        else:
            children[node['parent_id']].append(node)

    def branch(node):
        nested = ''
        if children[node['id']]:
            nested = '<ul class="organization-tree__level">{}</ul>'.format(
                ''.join(branch(child) for child in children[node['id']])
            )
        return (
            '<li class="organization-tree__node"><div class="card organization-tree__card">'
            '<strong>{}</strong><p>{}</p></div>{}</li>'
        ).format(html.escape(node['label']), html.escape(node['description']), nested)

    tree = '<ul class="organization-tree__level organization-tree__level--root">{}</ul>'.format(
        ''.join(branch(root) for root in roots)
    )
    return render('sections/organization/template.html', {
        'page_intro': render_page_intro(page, render),
        'summary': page['organization']['summary'],
        'tree': tree,
    }, ('page_intro', 'tree'))
