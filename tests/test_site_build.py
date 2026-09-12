import importlib.util
import json
import re
from pathlib import Path
import tempfile
import unittest
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_site', ROOT / 'scripts/build_site.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.assets, self.headings = [], [], [], []
        self.main = 0
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag == 'a': self.links.append(a['href'])
        if tag == 'link': self.assets.append(a['href'])
        if tag in ('img', 'script') and 'src' in a: self.assets.append(a['src'])
        if tag in ('h1', 'h2', 'h3'): self.headings.append(tag)
        if tag == 'main': self.main += 1

class SiteTests(unittest.TestCase):
    def test_build_links_structure_assets_and_escaping(self):
        data = json.loads((ROOT / 'site/government.json').read_text())
        data['site_name'] = '<script>alert("test")</script>'
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            config = folder / 'config.json'
            config.write_text(json.dumps(data))
            names = builder.build(config, folder / 'out')
            pages = {name: Page((folder / 'out' / name).read_text()) for name in names}
            for name, page in pages.items():
                self.assertEqual(page.main, 1)
                self.assertEqual(page.headings.count('h1'), 1)
                self.assertEqual(len(page.ids), len(set(page.ids)))
                self.assertNotIn('<script>', (folder / 'out' / name).read_text())
                for asset in page.assets:
                    if asset == 'templates/faq/core.js':
                        runtime = (folder / 'out' / asset).read_text()
                        self.assertIn((ROOT / 'scripts/core/index.js').read_text().replace('export function initCore', 'function initCore'), runtime)
                        self.assertIn((ROOT / 'templates/faq/faq.js').read_text(), runtime)
                    elif asset.endswith('.runtime.js'):
                        self.assertNotIn('export function', (folder / 'out' / asset).read_text())
                        self.assertIn('initDigitalStamps();' if 'digital-stamp' in asset else 'initNavigationHeaders();', (folder / 'out' / asset).read_text())
                    else:
                        self.assertEqual((folder / 'out' / asset).read_bytes(), (ROOT / asset).read_bytes())
                for href in page.links:
                    if href.startswith(('https://', 'mailto:', 'tel:')):
                        continue
                    target, _, fragment = href.partition('#')
                    self.assertIn(target or name, pages)
                    if fragment: self.assertIn(fragment, pages[target or name].ids)
    def test_reject_invalid_composition(self):
        data = json.loads((ROOT / 'site/government.json').read_text())
        for mutate in [lambda d: d['pages'][0].update(path='../escape.html'),
                       lambda d: d['navigation'][0].update(href='javascript:alert(1)'),
                       lambda d: d['pages'][0]['sections'].append(d['pages'][0]['sections'][0]),
                       lambda d: d['services'][1].update(id=d['services'][0]['id'])]:
            candidate = json.loads(json.dumps(data))
            mutate(candidate)
            with self.assertRaises(ValueError): builder.validate(candidate)

    def test_composition_token_references_resolve(self):
        definitions = set(re.findall(r'(--[\w-]+)\s*:', (ROOT / 'token.css').read_text() + (ROOT / 'templates/government/tokens.css').read_text()))
        references = set(re.findall(r'var\((--[\w-]+)', (ROOT / 'templates/government/composition.css').read_text() + (ROOT / 'templates/content/content.css').read_text() + (ROOT / 'components/table-of-contents/table-of-contents.css').read_text() + (ROOT / 'templates/form/form.css').read_text() + (ROOT / 'components/progress-indicator/progress-indicator.css').read_text() + (ROOT / 'templates/error/error.css').read_text()))
        self.assertFalse(references - definitions)

    def test_page_intro_variants_optional_content_and_existing_faq(self):
        base = {'title': 'عنوان داخلي'}
        default = builder.render_page_intro(base, builder.render)
        self.assertIn('<section class="page-intro"', default)
        self.assertNotIn('page-intro--', default)
        self.assertIn('class="breadcrumb"', default)
        self.assertNotIn('page-intro__description', default)
        self.assertNotIn('{{', default)

        compact = builder.render_page_intro({**base, 'intro_variant': 'compact'}, builder.render)
        self.assertIn('<section class="page-intro page-intro--compact"', compact)

        described = builder.render_page_intro({**base, 'description': '<وصف>'}, builder.render)
        self.assertIn('<section class="page-intro page-intro--description"', described)
        self.assertIn('&lt;وصف&gt;', described)

        featured = builder.render_page_intro({**base, 'intro_variant': 'featured', 'intro_extra': '<كتلة>'}, builder.render)
        self.assertIn('<section class="page-intro page-intro--featured"', featured)
        self.assertIn('page-intro__extra', featured)
        self.assertIn('&lt;كتلة&gt;', featured)

        decorative = builder.render_page_intro({**base, 'intro_variant': 'decorative'}, builder.render)
        self.assertIn('<section class="page-intro page-intro--decorative"', decorative)

        data = json.loads((ROOT / 'site/government.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'out'
            config = Path(directory) / 'config.json'
            config.write_text(json.dumps(data))
            builder.build(config, output)
            faq = (output / 'faq.html').read_text()
            self.assertIn('<section class="page-intro page-intro--compact"', faq)
            self.assertIn('class="breadcrumb"', faq)
            self.assertIn('page-intro__description', faq)
            self.assertNotIn('{{breadcrumb_markup}}', faq)

        candidate = json.loads(json.dumps(data))
        page = next(item for item in candidate['pages'] if 'page-intro' in item['sections'])
        page['intro_variant'] = 'unknown'
        with self.assertRaises(ValueError):
            builder.validate(candidate)

    def test_error_template_renders_reusable_state_and_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            pages = builder.build(ROOT / 'site/government.json', output)
            self.assertIn('error.html', pages)
            error_page = (output / 'error.html').read_text()
            self.assertIn('class="error-page"', error_page)
            self.assertIn('class="error-state"', error_page)
            self.assertIn('class="error-state__code" dir="ltr">404</span>', error_page)
            self.assertIn('<h1 id="error-title">حدث خطأ</h1>', error_page)
            self.assertIn('class="btn btn--primary" href="index.html"', error_page)
            self.assertNotIn('class="page-intro', error_page)
            self.assertTrue((output / 'templates/error/assets/alert-16.svg').is_file())
            self.assertTrue((output / 'templates/error/assets/search-remove-24.svg').is_file())

        data = json.loads((ROOT / 'site/government.json').read_text())
        error_page_data = next(page for page in data['pages'] if page['path'] == 'error.html')
        error_page_data['error_state']['action_href'] = 'missing.html'
        with self.assertRaises(ValueError):
            builder.validate(data)

    def test_heavy_content_validation_rendering_and_escaping(self):
        data = json.loads((ROOT / 'site/government.json').read_text())
        page = next(page for page in data['pages'] if page['path'] == 'content.html')
        page['heavy_content']['sections'][0]['blocks'][0]['text'] = '<script>alert("content")</script>'
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'out'
            config = Path(directory) / 'config.json'
            config.write_text(json.dumps(data))
            builder.build(config, output)
            content = (output / 'content.html').read_text()
            self.assertNotIn('<script>alert', content)
            self.assertIn('&lt;script&gt;alert', content)
            self.assertEqual(content.count('data-content-section'), 9)
            self.assertEqual(content.count('class="table-of-contents__link"'), 9)
            self.assertIn('templates/content/content.js', content)

        for mutate in [
            lambda item: item['heavy_content']['sections'][1].update(id='section-1'),
            lambda item: item['heavy_content']['sections'][0]['blocks'][0].update(type='unknown'),
            lambda item: item['heavy_content']['sections'][4]['blocks'][-1].update(href='javascript:alert(1)'),
            lambda item: item['heavy_content']['sections'][0].update(blocks=[]),
        ]:
            candidate = json.loads(json.dumps(data))
            item = next(page for page in candidate['pages'] if page['path'] == 'content.html')
            mutate(item)
            with self.assertRaises(ValueError):
                builder.validate(candidate)

    def test_form_template_validation_rendering_and_escaping(self):
        data = json.loads((ROOT / 'site/government.json').read_text())
        page = next(page for page in data['pages'] if page['path'] == 'form.html')
        page['form_template']['steps'][1]['title'] = '<script>alert("step")</script>'
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'out'
            config = Path(directory) / 'config.json'
            config.write_text(json.dumps(data))
            builder.build(config, output)
            content = (output / 'form.html').read_text()
            self.assertNotIn('<script>alert', content)
            self.assertIn('&lt;script&gt;alert', content)
            self.assertEqual(content.count('data-field-variant='), 7)
            self.assertEqual(content.count('data-progress-step='), 3)
            self.assertEqual(content.count('class="input-affix '), 4)
            self.assertIn('templates/form/form.js', content)
            self.assertIn('aria-current="step"', content)

        for mutate in [
            lambda item: item['form_template'].update(steps=item['form_template']['steps'][:1]),
            lambda item: item['form_template'].update(current_step=0),
            lambda item: item['form_template'].update(variants=['unknown']),
            lambda item: item['form_template'].update(variants=['default', 'default']),
            lambda item: item['form_template'].update(required_note=''),
        ]:
            candidate = json.loads(json.dumps(data))
            item = next(page for page in candidate['pages'] if page['path'] == 'form.html')
            mutate(item)
            with self.assertRaises(ValueError):
                builder.validate(candidate)

class DigitalStampDataTests(unittest.TestCase):
    def test_registered_stamp_requires_explicit_registry_data(self):
        for data in [dict(mode='registered'), dict(mode='registered', registration_number='20230103200', registration_url='javascript:alert(1)'), dict(mode='registered', registration_number='20230103200', registration_url='https://raqmi.dga.gov.sa.evil.example/license'), dict(extension='example.com')]:
            with self.assertRaises(ValueError): builder.validate_stamp(data)
        builder.validate_stamp(dict(mode='registered', registration_number='20230103200', registration_url='https://raqmi.dga.gov.sa/Platforms/example'))

    def test_preview_does_not_claim_registration(self):
        text=builder.render_stamp({},builder.render)
        self.assertIn('معاينة الختم الرقمي',text)
        self.assertNotIn('20230103200',text)
        self.assertNotIn('موقع حكومي مسجل',text)
        self.assertNotIn('class="link link--md link--inline"',text)

class ServiceTemplateTests(unittest.TestCase):
    def test_service_data_validation(self):
        data=json.loads((ROOT/'site/government.json').read_text())
        for field,value in [('start_url','javascript:alert(1)'),('guide_url','http://example.test/guide'),('video_url','data:text/html,example'),('steps',[]),('audiences',[])]:
            copy=json.loads(json.dumps(data));copy['services'][0][field]=value
            with self.assertRaises(ValueError):builder.validate(copy)

    def test_generated_service_paths_cannot_collide(self):
        data=json.loads((ROOT/'site/government.json').read_text())
        data['pages'][2]['path']='service-new-request.html'
        with self.assertRaises(ValueError):builder.validate(data)

    def test_service_template_escapes_content_and_uses_real_destinations(self):
        from scripts.service_markup import overview, service_card
        services=json.loads((ROOT/'site/government.json').read_text())['services']
        service=dict(services[0], title='<img src=x onerror=alert(1)>',start_url='https://example.test/start')
        card=service_card(service,builder.render)
        detail=overview(service,services,builder.render)
        self.assertNotIn('<img src=x',card+detail)
        self.assertIn('&lt;img',card+detail)
        self.assertIn('href="https://example.test/start"',card)
        self.assertIn('href="service-new-request.html"',card)
        self.assertNotIn('id="start"',detail)
