"""Validate and render the Authority-owned Executive Profile."""
from datetime import date
import html
from pathlib import Path, PurePosixPath
import re
from urllib.parse import urlsplit

try:
    from scripts.page_intro_markup import render_page_intro
except ImportError:
    from page_intro_markup import render_page_intro


TEMPLATE = 'products/authority/templates/executive-profile/template.html'
REQUIRED = {
    'title', 'description', 'name', 'role_label', 'portrait', 'portrait_alt',
    'biography', 'updated',
}
OPTIONAL = {'qualifications', 'experience', 'related_links'}
INFRASTRUCTURE = {'path', 'sections'}
SEGMENT = re.compile(r'[a-z0-9][a-z0-9._-]*')
INTERNAL_LINK = re.compile(r'[a-z][a-z0-9-]*\.html(?:#[a-z][a-z0-9-]*)?')


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _asset(asset_root, value):
    if not _text(value):
        raise ValueError('Executive Profile requires a portrait')
    relative = PurePosixPath(value)
    if (
        relative.is_absolute() or value != relative.as_posix()
        or any(part in ('', '.', '..') or not SEGMENT.fullmatch(part) for part in relative.parts)
        or relative.suffix.lower() not in {'.svg', '.png', '.jpg', '.jpeg', '.webp'}
    ):
        raise ValueError('Executive Profile portrait must be a safe product image')
    root = Path(asset_root).resolve()
    resolved = (root / Path(*relative.parts)).resolve()
    if root not in resolved.parents or not resolved.is_file():
        raise ValueError('Executive Profile portrait does not exist')
    return relative.as_posix()


def _href(value):
    if not _text(value) or '\\' in value:
        return False
    if INTERNAL_LINK.fullmatch(value):
        return True
    parsed = urlsplit(value)
    return parsed.scheme == 'https' and bool(parsed.hostname) and not parsed.username and not parsed.password


def validate(page, asset_root):
    missing = REQUIRED - set(page)
    unknown = set(page) - REQUIRED - OPTIONAL - INFRASTRUCTURE
    if missing or unknown:
        raise ValueError('Executive Profile fields do not match its contract')
    for field in REQUIRED - {'portrait', 'updated'}:
        if not _text(page[field]):
            raise ValueError(f'Executive Profile requires {field}')
    try:
        date.fromisoformat(page['updated'])
    except (TypeError, ValueError) as error:
        raise ValueError('Executive Profile updated must use YYYY-MM-DD') from error
    _asset(asset_root, page['portrait'])
    for field in ('qualifications', 'experience'):
        if field in page and (
            not isinstance(page[field], list) or not page[field]
            or any(not _text(item) for item in page[field])
        ):
            raise ValueError(f'Executive Profile {field} must be nonempty text items')
    for link in page.get('related_links', []):
        if (
            not isinstance(link, dict) or set(link) != {'label', 'href'}
            or not _text(link['label']) or not _href(link['href'])
        ):
            raise ValueError('Executive Profile links require safe destinations')


def _list_section(identifier, title, values):
    if not values:
        return ''
    items = ''.join(
        '<li class="list__item list__item--level-one"><span class="list__text">{}</span></li>'.format(html.escape(value))
        for value in values
    )
    return '<section aria-labelledby="{0}"><h2 id="{0}">{1}</h2><ul class="list list--unordered list--primary" role="list">{2}</ul></section>'.format(identifier, title, items)


def _links(values):
    if not values:
        return ''
    items = ''.join(
        '<li class="list__item list__item--level-one"><a class="link link--primary link--md" href="{}">{}</a></li>'.format(html.escape(value['href'], quote=True), html.escape(value['label']))
        for value in values
    )
    return '<section aria-labelledby="executive-links"><h2 id="executive-links">محتوى مؤسسي مرتبط</h2><ul class="list list--unordered list--primary" role="list">{}</ul></section>'.format(items)


def render(page, render_markup, asset_root, asset_prefix):
    validate(page, asset_root)
    return render_markup(TEMPLATE, {
        **page,
        'page_intro': render_page_intro(page, render_markup),
        'portrait': asset_prefix + _asset(asset_root, page['portrait']),
        'qualifications_markup': _list_section('executive-qualifications', 'المؤهلات التجريبية', page.get('qualifications')),
        'experience_markup': _list_section('executive-experience', 'الخبرة التجريبية', page.get('experience')),
        'links_markup': _links(page.get('related_links')),
    }, ('page_intro', 'qualifications_markup', 'experience_markup', 'links_markup'))
