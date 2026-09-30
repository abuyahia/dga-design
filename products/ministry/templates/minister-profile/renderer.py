"""Validate and render the Ministry-owned Minister Profile capability."""
from datetime import date
import html
from pathlib import Path, PurePosixPath
import re
from urllib.parse import urlsplit

try:
    from scripts.page_intro_markup import render_page_intro
except ImportError:
    from page_intro_markup import render_page_intro


TEMPLATE = 'products/ministry/templates/minister-profile/template.html'
REQUIRED_FIELDS = {
    'title', 'description', 'name', 'official_title', 'portrait',
    'portrait_alt', 'biography', 'updated',
}
OPTIONAL_FIELDS = {
    'message', 'appointment_date', 'qualifications', 'experience',
    'role_information', 'related_links',
}
INFRASTRUCTURE_FIELDS = {'path', 'sections'}
ASSET_SEGMENT = re.compile(r'[a-z0-9][a-z0-9._-]*')
INTERNAL_HREF = re.compile(r'[a-z][a-z0-9-]*\.html(?:#[a-z][a-z0-9-]*)?')
PORTRAIT_EXTENSIONS = {'.svg', '.png', '.jpg', '.jpeg', '.webp'}


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _date(value, label):
    if not _text(value):
        raise ValueError(f'Minister Profile requires {label}')
    try:
        date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f'Minister Profile {label} must use YYYY-MM-DD') from error


def _portrait_path(asset_root, value):
    if not _text(value):
        raise ValueError('Minister Profile requires portrait')
    relative = PurePosixPath(value)
    if (
        relative.is_absolute()
        or value != relative.as_posix()
        or any(part in ('', '.', '..') or not ASSET_SEGMENT.fullmatch(part) for part in relative.parts)
        or relative.suffix.lower() not in PORTRAIT_EXTENSIONS
    ):
        raise ValueError('Minister portrait must be a safe product image reference')
    asset_root = Path(asset_root).resolve()
    path = (asset_root / Path(*relative.parts)).resolve()
    if asset_root not in path.parents or not path.is_file():
        raise ValueError(f'Minister portrait asset does not exist: {value}')
    return relative.as_posix()


def _safe_href(value):
    if (
        not _text(value)
        or value != value.strip()
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
        or '\\' in value
    ):
        return False
    if INTERNAL_HREF.fullmatch(value):
        return True
    url = urlsplit(value)
    return url.scheme == 'https' and bool(url.hostname) and not url.username and not url.password


def _text_list(value, label):
    if not isinstance(value, list) or not value or any(not _text(item) for item in value):
        raise ValueError(f'Minister Profile {label} must be a nonempty text list')


def validate(page, asset_root):
    """Validate the V1 Minister record and its optional fields."""
    missing = REQUIRED_FIELDS - set(page)
    if missing:
        raise ValueError('Minister Profile missing required fields: ' + ', '.join(sorted(missing)))
    unknown = set(page) - REQUIRED_FIELDS - OPTIONAL_FIELDS - INFRASTRUCTURE_FIELDS
    if unknown:
        raise ValueError('Minister Profile contains unsupported fields: ' + ', '.join(sorted(unknown)))
    for field in REQUIRED_FIELDS - {'portrait', 'updated'}:
        if not _text(page[field]):
            raise ValueError(f'Minister Profile requires {field}')
    _date(page['updated'], 'updated date')
    _portrait_path(asset_root, page['portrait'])

    if 'message' in page and not _text(page['message']):
        raise ValueError('Minister Profile message must be nonempty text')
    if 'role_information' in page and not _text(page['role_information']):
        raise ValueError('Minister Profile role information must be nonempty text')
    if 'appointment_date' in page:
        _date(page['appointment_date'], 'appointment date')
    for field in ('qualifications', 'experience'):
        if field in page:
            _text_list(page[field], field)
    if 'related_links' in page:
        links = page['related_links']
        if not isinstance(links, list) or not links:
            raise ValueError('Minister Profile links must be a nonempty list')
        for link in links:
            if (
                not isinstance(link, dict)
                or set(link) != {'label', 'href'}
                or not _text(link['label'])
                or not _safe_href(link['href'])
            ):
                raise ValueError('Minister Profile links require a label and safe internal or HTTPS destination')


def _list_markup(items):
    return '<ul class="list list--unordered list--primary" role="list">{}</ul>'.format(
        ''.join(
            '<li class="list__item list__item--level-one"><span class="list__text">{}</span></li>'.format(
                html.escape(item)
            )
            for item in items
        )
    )


def _list_section(identifier, title, items):
    if not items:
        return ''
    return (
        '<section class="minister-profile__section" aria-labelledby="{0}">'
        '<h2 id="{0}">{1}</h2>{2}</section>'
    ).format(identifier, title, _list_markup(items))


def _links_section(links):
    if not links:
        return ''
    items = ''.join(
        '<li class="list__item list__item--level-one">'
        '<a class="link link--primary link--md" href="{0}">{1}</a></li>'.format(
            html.escape(link['href'], quote=True), html.escape(link['label'])
        )
        for link in links
    )
    return (
        '<section class="minister-profile__section" aria-labelledby="minister-links">'
        '<h2 id="minister-links">روابط مؤسسية ذات صلة</h2>'
        '<ul class="list list--unordered list--primary" role="list">{}</ul></section>'
    ).format(items)


def _role_section(page):
    if not page.get('appointment_date') and not page.get('role_information'):
        return ''
    appointment_markup = ''
    if page.get('appointment_date'):
        appointment_markup = (
            '<p class="minister-profile__appointment">'
            '<span>تاريخ التعيين التجريبي</span> '
            '<time datetime="{0}">{0}</time></p>'
        ).format(html.escape(page['appointment_date'], quote=True))
    role_markup = ''
    if page.get('role_information'):
        role_markup = '<p class="minister-profile__role">{}</p>'.format(
            html.escape(page['role_information'])
        )
    return (
        '<section class="minister-profile__section" aria-labelledby="minister-role">'
        '<h2 id="minister-role">معلومات التعيين والدور القيادي</h2>{}{}</section>'
    ).format(appointment_markup, role_markup)


def render(page, render_markup, asset_root, asset_prefix):
    """Render one validated Ministry Minister Profile."""
    validate(page, asset_root)
    portrait = _portrait_path(asset_root, page['portrait'])
    page_intro = render_page_intro(page, render_markup)
    message_markup = ''
    if page.get('message'):
        message_markup = (
            '<section class="minister-profile__section" aria-labelledby="minister-message">'
            '<h2 id="minister-message">كلمة الوزير التجريبية</h2>'
            '<blockquote class="minister-profile__message"><p>{}</p></blockquote></section>'
        ).format(html.escape(page['message']))

    return render_markup(TEMPLATE, {
        'page_intro': page_intro,
        'portrait': asset_prefix + portrait,
        'portrait_alt': page['portrait_alt'],
        'name': page['name'],
        'official_title': page['official_title'],
        'biography_markup': '<p>{}</p>'.format(html.escape(page['biography'])),
        'message_markup': message_markup,
        'qualifications_markup': _list_section(
            'minister-qualifications', 'المؤهلات التجريبية', page.get('qualifications')
        ),
        'experience_markup': _list_section(
            'minister-experience', 'الخبرات التجريبية', page.get('experience')
        ),
        'role_markup': _role_section(page),
        'links_markup': _links_section(page.get('related_links')),
    }, (
        'page_intro', 'biography_markup', 'message_markup', 'qualifications_markup',
        'experience_markup', 'role_markup', 'links_markup',
    ))
