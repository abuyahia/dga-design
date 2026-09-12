"""Build the government example using trusted HTML fragments and escaped JSON text."""
import argparse
import html
import json
from pathlib import Path
import re
import shutil
try:
    from scripts.contact_markup import contact_page, validate_contact
    from scripts.feedback_markup import render_feedback
    from scripts.footer_markup import render_footer
    from scripts.digital_stamp_markup import render_stamp, validate_stamp
    from scripts.service_markup import validate_services, service_card, catalogue, overview, detail_url
    from scripts.content_markup import validate_heavy_content, render_heavy_content
    from scripts.form_markup import validate_form_template, render_form_template
    from scripts.page_intro_markup import validate_page_intro, render_page_intro
    from scripts.error_state_markup import validate_error_state, render_error_state
except ImportError:
    from contact_markup import contact_page, validate_contact
    from feedback_markup import render_feedback
    from footer_markup import render_footer
    from digital_stamp_markup import render_stamp, validate_stamp
    from service_markup import validate_services, service_card, catalogue, overview, detail_url
    from content_markup import validate_heavy_content, render_heavy_content
    from form_markup import validate_form_template, render_form_template
    from page_intro_markup import validate_page_intro, render_page_intro
    from error_state_markup import validate_error_state, render_error_state

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ['components/accordion-new/accordion-new.css', 'components/select/select.css', 'components/textarea/textarea.css', 'components/file-upload/file-upload.css', 'templates/contact/contact.css', 'components/radio/radio.css', 'components/checkbox/checkbox-2.css', 'styles/composites/feedback.css', 'components/page-feedback/page-feedback.css', 'components/service-rating/service-rating.css', 'components/rating/rating.css', 'token.css', 'styles/base/global.css', 'styles/base/layout.css',
          'styles/base/accessibility.css', 'components/card/card.css',
          'components/navigation-header/navigation-header.css', 'components/footer/footer.css', 'components/digital-stamp/digital-stamp.css', 'components/service-card/service-card.css', 'components/tab/tab.css', 'components/breadcrumb/breadcrumb.css', 'components/divider/divider.css', 'components/list/list.css', 'components/table-of-contents/table-of-contents.css', 'templates/service/service.css', 'components/link/link.css', 'components/button/button.css', 'components/tag/tag.css',
          'components/label/label.css', 'components/text-input/text-input.css', 'components/input-affix/input-affix.css', 'components/progress-indicator/progress-indicator.css',
          'assets/fonts/fonts.css', 'templates/government/tokens.css', 'templates/government/composition.css', 'templates/faq/faq.css', 'templates/content/content.css', 'templates/form/form.css', 'templates/error/error.css']
SUPPORT_ASSETS = ['templates/faq/faq.js', 'templates/faq/assets/contact.svg', 'templates/content/content.js', 'templates/form/form.js', 'templates/contact/contact.js', 'components/select/select.css', 'components/textarea/textarea.css', 'components/file-upload/file-upload.css', 'templates/contact/contact.css', 'components/radio/radio.css', 'components/checkbox/checkbox-2.css', 'styles/composites/feedback.js', 'styles/composites/feedback.css', 'components/page-feedback/page-feedback.css', 'components/service-rating/service-rating.css', 'components/rating/rating.css', 'assets/fonts/OFL.txt', 'assets/fonts/SOURCES.md', 'assets/templates/home/SOURCES.md', 'components/navigation-header/navigation-header.js', 'components/digital-stamp/digital-stamp.js', 'templates/government/home.js', 'templates/service/service.js', 'assets/templates/home/news.png'] + [f'assets/fonts/ibm-plex-arabic-{weight}.woff2' for weight in [400, 500, 600, 700]]


def render(name, values, slots=()):
    source = (ROOT / name).read_text()
    def replace(match):
        key = match[1]
        value = str(values[key])
        return value if key in slots else html.escape(value, quote=True)
    return re.sub(r'\{\{([a-z_]+)\}\}', replace, source)


def validate(data):
    validate_stamp(data.get('digital_stamp', {}))
    if data['dir'] not in ('rtl', 'ltr') or not re.fullmatch(r'[a-z]{2,3}(?:-[A-Za-z0-9]+)*', data['lang']):
        raise ValueError('Invalid language or direction')
    paths = [page['path'] for page in data['pages']]
    if len(set(paths)) != len(paths) or any(not re.fullmatch(r'[a-z][a-z0-9-]*\.html', p) for p in paths):
        raise ValueError('Page paths must be unique flat HTML filenames')
    if not {'index.html', 'services.html'}.issubset(paths):
        raise ValueError('This archetype requires index.html and services.html')
    validate_services(data['services'])
    if any('contact' in p['sections'] for p in data['pages']): validate_contact(data.get('contact'))
    ids = [service['id'] for service in data['services']]
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r'[a-z][a-z0-9-]*', i) for i in ids):
        raise ValueError('Service IDs must be unique slugs')
    generated = [detail_url(service) for service in data['services']]
    if set(generated) & set(paths):
        raise ValueError('Service paths collide with configured pages')
    if any(item['href'].partition('#')[0] not in paths for item in data['navigation'] + [child for item in data['navigation'] for child in item.get('children', [])] + [link for group in data['footer_groups'] + data.get('footer_tools', []) for link in group['links']]):
        raise ValueError('Navigation must target generated pages')
    for page in data['pages']:
        sections = page['sections']
        if 'faq' in sections:
            questions = page.get('questions')
            if not isinstance(questions, list) or not questions:
                raise ValueError('FAQ requires questions')
            ids = [q.get('id', '') for q in questions]
            if len(ids) != len(set(ids)) or any(not re.fullmatch(r'[a-z][a-z0-9-]*', i) for i in ids):
                raise ValueError('FAQ question IDs must be unique slugs')
            if any(not isinstance(q.get(k), str) or not q[k].strip() for q in questions for k in ('question', 'answer')):
                raise ValueError('FAQ requires nonempty question and answer text')
        if 'contact-cta' in sections and page.get('contact_cta', {}).get('href') not in paths:
            raise ValueError('Contact CTA must target a generated page')
        if 'heavy-content' in sections:
            validate_heavy_content(page, paths)
        if 'form-template' in sections:
            validate_form_template(page)
        if 'page-intro' in sections:
            validate_page_intro(page)
        if 'error-state' in sections:
            validate_error_state(page, paths)
        if sum(sections.count(name) for name in ('page-intro', 'hero', 'contact', 'heavy-content', 'form-template', 'error-state')) != 1 or len(set(sections)) != len(sections):
            raise ValueError('Exactly one intro and no duplicate sections are allowed')
        if 'services' in sections and 'home-services' in sections:
            raise ValueError('Only one services presentation is allowed per page')
        if set(sections) - {'page-intro', 'services', 'service-details', 'hero', 'about', 'home-services', 'news', 'partners', 'feedback', 'content', 'service-catalog', 'contact', 'faq', 'contact-cta', 'heavy-content', 'form-template', 'error-state'}:
            raise ValueError('Unknown section')


def build(config, output):
    data = json.loads(Path(config).read_text())
    validate(data)
    output = Path(output)
    pages = {}
    service_pages = [dict(path=detail_url(service), title=service['title'], description=service['description'], sections=['service-overview','feedback'], service_id=service['id'], feedback_statistics=service.get('feedback_statistics')) for service in data['services']]
    for page in data['pages'] + service_pages:
        current_path = 'services.html' if page.get('service_id') else page['path']
        navigation_items = []
        for index, item in enumerate(data['navigation']):
            if item.get('children'):
                children = [dict(label=item['label'], href=item['href']), *item['children']]
                submenu = ''.join(render('components/navigation-header/submenu-item.html', {**child, 'current': ' aria-current="page"' if child['href'] == page['path'] else ''}, ('current',)) for child in children)
                navigation_items.append(render('components/navigation-header/dropdown.html', {'label': item['label'], 'panel_id': f'primary-submenu-{index}', 'current_section': str(any(child['href'].partition('#')[0] == current_path for child in children)).lower(), 'items': submenu, 'chevron': render('components/navigation-header/icon.html', {'class_name': 'nav-header__chevron', 'asset_prefix': 'components/navigation-header/assets/', 'default_asset': 'menu-imgElements7.svg', 'white_asset': 'menu-imgElements1.svg', 'disabled_asset': 'menu-imgElements4.svg'})}, ('items', 'chevron')))
            else:
                navigation_items.append(render('components/navigation-header/item.html', {**item, 'current': ' aria-current="page"' if item['href'] == page['path'] else ''}, ('current',)))
        navigation = '\n'.join(navigation_items)
        search_links = ''.join('<li><a class="link link--inline" href="{}">{}</a></li>'.format(html.escape(detail_url(service)), html.escape(service['title'])) for service in data['services'])
        footer_component = render_footer({
            'theme': 'dark', 'groups': data['footer_groups'],
            'tools': data.get('footer_tools', []),
            'legal_links': [{'label': 'الخصوصية وشروط الاستخدام', 'href': 'about.html#privacy'}, {'label': 'إمكانية الوصول', 'href': 'about.html#accessibility'}],
            'copyright': data['footer_note'], 'updated': 'آخر تحديث للقالب: ' + data['updated'],
            'logos': [{'label': data['site_name']}],
        }, render)
        common = {**data, 'navigation': navigation, 'search_links': search_links, 'footer_component': footer_component}
        sections = []
        for section in page['sections']:
            if section == 'contact':
                sections.append(contact_page(data['contact'], render))
            elif section == 'service-catalog':
                sections.append(catalogue(data['services'], render))
            elif section == 'service-overview':
                service = next(s for s in data['services'] if s['id'] == page['service_id'])
                sections.append(overview(service, data['services'], render, 'contact.html' if any(p['path']=='contact.html' for p in data['pages']) else None))
            elif section == 'heavy-content':
                sections.append(render_heavy_content(page, render))
            elif section == 'form-template':
                sections.append(render_form_template(page, render))
            elif section == 'error-state':
                sections.append(render_error_state(page, render))
            elif section == 'page-intro':
                sections.append(render_page_intro(page, render))
            elif section == 'faq':
                items = ''.join(render('components/accordion-new/item.html', item) for item in page['questions'])
                sections.append(render('sections/faq/template.html', {'items': items}, ('items',)))
            elif section == 'contact-cta':
                sections.append(render('sections/contact-cta/template.html', page['contact_cta']))
            elif section == 'services':
                cards = ''.join(render('sections/services/card.html', {**service, 'href': 'services.html#' + service['id']}) for service in data['services'])
                sections.append(render('sections/services/template.html', {'heading': data['services_heading'], 'description': data['services_description'], 'cards': cards}, ('cards',)))
            elif section == 'service-details':
                items = ''.join(render('sections/service-details/item.html', service) for service in data['services'])
                sections.append(render('sections/service-details/template.html', {'heading': data['details_heading'], 'items': items}, ('items',)))
            elif section == 'hero':
                dots = ''.join('<button class="hero-dot" type="button" aria-label="الشريحة {}" aria-pressed="{}" data-title="{}" data-description="{}"></button>'.format(i + 1, str(i == 0).lower(), html.escape(slide['title'], quote=True), html.escape(slide['description'], quote=True)) for i, slide in enumerate(data['home']['slides']))
                sections.append(render('sections/hero/template.html', {**page, 'dots': dots}, ('dots',)))
            elif section == 'about':
                statistics = ''.join('<div><span class="home-feature-icon" aria-hidden="true">{}</span><dt>{}</dt><dd dir="ltr">{}</dd></div>'.format(icon, html.escape(stat['label']), html.escape(stat['value'])) for icon, stat in zip(['◎', '+', '☆', '♡'], data['home']['statistics']))
                sections.append(render('sections/about/template.html', {'heading': data['home']['about_heading'], 'description': data['home']['about_description'], 'statistics': statistics}, ('statistics',)))
            elif section == 'home-services':
                cards = ''.join(service_card(service, render, 'home-') for service in data['services'])
                sections.append(render('sections/home-services/template.html', {'heading': data['services_heading'], 'description': data['services_description'], 'cards': cards}, ('cards',)))
            elif section == 'news':
                cards = ''.join(render('sections/news/card.html', article) for article in data['news'][:3])
                sections.append(render('sections/news/template.html', {'heading': data['home']['news_heading'], 'description': data['home']['news_description'], 'cards': cards}, ('cards',)))
            elif section == 'partners':
                partners = ''.join('<div class="card"><span class="home-feature-icon" aria-hidden="true">◇</span><span>{}</span></div>'.format(html.escape(name)) for name in data['home']['partners'])
                sections.append(render('sections/partners/template.html', {'heading': data['home']['partners_heading'], 'partners': partners}, ('partners',)))
            elif section == 'feedback':
                sections.append(render('sections/feedback/template.html', {'updated': data['updated'], 'component': render_feedback('service' if page.get('service_id') else 'page', page.get('service_id', page['path']), render, page.get('feedback_statistics'))}, ('component',)))
            elif section == 'content':
                items = ''.join(render('sections/content/item.html', item) for item in page['items'])
                sections.append(render('sections/content/template.html', {'items': items}, ('items',)))
        values = {**data, **page,
                  'digital_stamp': render_stamp(data.get('digital_stamp', {}), render, data['dir']),
                  'header': render('partials/site-header/template.html', common, ('navigation', 'search_links', 'footer_groups')),
                  'footer': render('partials/site-footer/template.html', common, ('footer_component',)),
                  'content': '\n'.join(sections),
                  'styles': '\n'.join(f'  <link rel="stylesheet" href="{asset}">' for asset in ASSETS)}
        pages[page['path']] = render('templates/government/page.html', values, ('digital_stamp', 'header', 'footer', 'content', 'styles'))
    output.mkdir(parents=True, exist_ok=True)
    for asset in ASSETS + SUPPORT_ASSETS + [str(p.relative_to(ROOT)) for component in ('navigation-header', 'footer', 'digital-stamp', 'service-card', 'service-rating', 'page-feedback', 'select') for p in (ROOT / 'components' / component / 'assets').glob('*.svg')] + [str(p.relative_to(ROOT)) for folder in ('service', 'contact', 'error') for p in (ROOT / 'templates' / folder / 'assets').glob('*') if p.suffix in ('.svg', '.png')]:
        target = output / asset
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / asset, target)
    core = (ROOT / 'scripts/core/index.js').read_text().replace('export function initCore', 'function initCore')
    (output / 'templates/faq/core.js').write_text('(function () {\n' + core + '\n' + (ROOT / 'templates/faq/faq.js').read_text() + '\n})();\n')
    # ES module source remains canonical; this generated IIFE supports file:// previews.
    for component, initializer in [('navigation-header', 'initNavigationHeaders'), ('digital-stamp', 'initDigitalStamps')]:
        source = (ROOT / 'components' / component / (component + '.js')).read_text()
        runtime = '(function () {\n' + source.replace('export function ' + initializer, 'function ' + initializer) + '\n' + initializer + '();\n})();\n'
        (output / 'components' / component / (component + '.runtime.js')).write_text(runtime)
    for name, content in pages.items():
        (output / name).write_text(content)
    return list(pages)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT / 'site/government.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/government')
    args = parser.parse_args()
    print('Built: ' + ', '.join(build(args.config, args.output)))
