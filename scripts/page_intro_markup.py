"""Compose the shared Page Intro with the existing Breadcrumb component."""
import html


PAGE_INTRO_SUFFIXES = {
    'default': '',
    'compact': ' page-intro--compact',
    'description': ' page-intro--description',
    'featured': ' page-intro--featured',
    'decorative': ' page-intro--decorative',
}


def validate_page_intro(page):
    variant = page.get('intro_variant')
    if variant is not None and variant not in PAGE_INTRO_SUFFIXES:
        raise ValueError('Unknown Page Intro variant')
    extra = page.get('intro_extra')
    if extra is not None and (not isinstance(extra, str) or not extra.strip()):
        raise ValueError('Page Intro extra content must be nonempty text')


def render_page_intro(page, render, *, variant=None, extra_content_markup=None):
    validate_page_intro(page)
    description = page.get('description')
    selected = variant or page.get('intro_variant') or ('description' if description else 'default')
    if selected not in PAGE_INTRO_SUFFIXES:
        raise ValueError('Unknown Page Intro variant')
    breadcrumb = render('components/breadcrumb/two-level.html', {
        'root_href': 'index.html',
        'root_label': 'الرئيسية',
        'current_label': page['title'],
    })
    if extra_content_markup is None:
        extra = page.get('intro_extra')
        extra_content_markup = '<div class="page-intro__extra"><p>{}</p></div>'.format(html.escape(extra)) if extra else ''
    eyebrow = page.get('eyebrow')
    return render('sections/page-intro/template.html', {
        'variant': PAGE_INTRO_SUFFIXES[selected],
        'breadcrumb_markup': breadcrumb,
        'eyebrow_markup': '<p class="page-intro__eyebrow">' + html.escape(eyebrow) + '</p>' if eyebrow else '',
        'title': page['title'],
        'description_markup': '<p class="page-intro__description ds-reading">' + html.escape(description) + '</p>' if description else '',
        'extra_content_markup': extra_content_markup,
    }, ('breadcrumb_markup', 'eyebrow_markup', 'description_markup', 'extra_content_markup'))
