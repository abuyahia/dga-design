import copy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / 'products/ministry'
SPEC = importlib.util.spec_from_file_location('build_site', ROOT / 'scripts/build_site.py')
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class MinisterDocument(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1_count = 0
        self.h1_text = []
        self.in_h1 = False
        self.ids = []
        self.page_intro_count = 0
        self.profile_count = 0
        self.breadcrumb_items = 0
        self.current_breadcrumbs = 0
        self.portraits = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get('class', '').split())
        if tag == 'h1':
            self.h1_count += 1
            self.in_h1 = True
        if 'id' in attributes:
            self.ids.append(attributes['id'])
        if tag == 'section' and 'page-intro' in classes:
            self.page_intro_count += 1
        if tag == 'article' and 'minister-profile' in classes:
            self.profile_count += 1
        if tag == 'li' and 'breadcrumb__item' in classes:
            self.breadcrumb_items += 1
            if attributes.get('aria-current') == 'page':
                self.current_breadcrumbs += 1
        if tag == 'img' and 'avatar__image' in classes:
            self.portraits.append(attributes)

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_h1:
            self.h1_text.append(data)


class MinistryMinisterTests(unittest.TestCase):
    def product_and_handlers(self):
        product = BUILDER.load_product('ministry')
        handlers = BUILDER._load_product_renderer_handlers('ministry', product['paths'])
        return product, handlers

    def test_minister_registration_and_record_contract_are_product_owned(self):
        registry = json.loads((PRODUCT / 'pages/index.json').read_text())
        definition = json.loads((PRODUCT / 'pages/minister.json').read_text())
        content = json.loads((PRODUCT / 'content/demo/minister.json').read_text())
        product, handlers = self.product_and_handlers()
        minister = next(page for page in product['registered_pages'] if page['path'] == 'minister.html')

        self.assertEqual(registry, {
            'schema_version': 1,
            'pages': ['about.json', 'strategy.json', 'minister.json'],
        })
        self.assertEqual(set(definition), {'id', 'route', 'renderer', 'content'})
        self.assertEqual(definition['renderer'], 'minister-profile')
        self.assertEqual(minister['sections'], ['minister-profile', 'feedback'])
        for field, value in content.items():
            self.assertEqual(minister[field], value)
        self.assertIn('minister-profile', handlers)
        self.assertNotIn('minister-profile', BUILDER.REGISTERED_PAGE_RENDERERS)
        self.assertIn('minister-profile', BUILDER.PRODUCT_RENDERER_REGISTRY['ministry'])
        self.assertTrue((PRODUCT / 'templates/minister-profile/template.html').is_file())
        self.assertTrue((PRODUCT / 'templates/minister-profile/renderer.py').is_file())

    def test_minister_build_uses_canonical_intro_avatar_and_product_assets(self):
        content = json.loads((PRODUCT / 'content/demo/minister.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            pages = BUILDER.build_product('ministry', output)
            markup = (output / 'minister.html').read_text()
            about_markup = (output / 'about.html').read_text()
            strategy_markup = (output / 'strategy.html').read_text()

            self.assertIn('minister.html', pages)
            self.assertIn('about.html', pages)
            self.assertIn('strategy.html', pages)
            self.assertTrue((output / 'components/avatar/avatar.css').is_file())
            self.assertTrue((output / 'assets/products/ministry/minister-profile/minister-profile.css').is_file())
            self.assertTrue((output / 'assets/products/ministry/minister-profile/portrait-placeholder.svg').is_file())
            self.assertTrue((output / 'assets/products/ministry/minister-profile/SOURCES.md').is_file())
            for existing_markup in (about_markup, strategy_markup):
                self.assertNotIn('components/avatar/avatar.css', existing_markup)
                self.assertNotIn('minister-profile/minister-profile.css', existing_markup)

        document = MinisterDocument()
        document.feed(markup)
        self.assertEqual(document.h1_count, 1)
        self.assertEqual(''.join(document.h1_text), content['title'])
        self.assertEqual(document.page_intro_count, 1)
        self.assertEqual(document.profile_count, 1)
        self.assertEqual(document.breadcrumb_items, 2)
        self.assertEqual(document.current_breadcrumbs, 1)
        self.assertEqual(len(document.ids), len(set(document.ids)))
        self.assertEqual(len(document.portraits), 1)
        self.assertEqual(document.portraits[0]['alt'], content['portrait_alt'])
        self.assertEqual(
            document.portraits[0]['src'],
            'assets/products/ministry/minister-profile/portrait-placeholder.svg',
        )
        self.assertIn('<html lang="ar" dir="rtl">', markup)
        self.assertIn('<a href="index.html" class="breadcrumb__link">الرئيسية</a>', markup)
        self.assertIn(f'<span class="breadcrumb__link">{content["title"]}</span>', markup)
        self.assertIn('<title>معالي الوزير | ', markup)
        self.assertIn(
            '<meta name="description" content="{}">'.format(content['description']),
            markup,
        )
        self.assertIn(content['name'], markup)
        self.assertIn(content['official_title'], markup)
        self.assertIn(content['role_information'], markup)
        self.assertIn('&lt;شخص حقيقي&gt;', markup)
        self.assertNotIn('<شخص حقيقي>', markup)
        self.assertIn('href="about.html#mandate"', markup)
        self.assertIn('href="strategy.html"', markup)
        self.assertIn('id="mandate"', about_markup)
        self.assertNotIn('application/ld+json', markup)
        self.assertIn('<time datetime="2026-09-14">2026-09-14</time>', markup)
        heading_order = [
            markup.index('id="minister-message"'),
            markup.index('id="minister-biography"'),
            markup.index('id="minister-qualifications"'),
            markup.index('id="minister-experience"'),
            markup.index('id="minister-role"'),
            markup.index('id="minister-links"'),
        ]
        self.assertEqual(heading_order, sorted(heading_order))

    def test_optional_fields_omit_cleanly_and_text_is_escaped(self):
        product, handlers = self.product_and_handlers()
        minister = copy.deepcopy(next(
            page for page in product['registered_pages'] if page['path'] == 'minister.html'
        ))
        for field in (
            'message', 'appointment_date', 'qualifications', 'experience',
            'role_information', 'related_links',
        ):
            minister.pop(field)
        minister['name'] = '<اسم تجريبي>'
        minister['official_title'] = '<منصب تجريبي>'
        minister['biography'] = '<سيرة تجريبية>'

        markup = handlers['minister-profile']['render'](minister, BUILDER.render)

        for identifier in (
            'minister-message', 'minister-qualifications', 'minister-experience',
            'minister-role', 'minister-links', 'minister-profile__appointment',
        ):
            self.assertNotIn(identifier, markup)
        for escaped in (
            '&lt;اسم تجريبي&gt;', '&lt;منصب تجريبي&gt;', '&lt;سيرة تجريبية&gt;',
        ):
            self.assertIn(escaped, markup)
        self.assertNotIn('{{', markup)

    def test_portrait_alt_unsafe_assets_and_links_are_rejected(self):
        product, handlers = self.product_and_handlers()
        minister = next(page for page in product['registered_pages'] if page['path'] == 'minister.html')
        validator = handlers['minister-profile']['validate']

        missing_alt = copy.deepcopy(minister)
        missing_alt.pop('portrait_alt')
        with self.assertRaisesRegex(ValueError, 'missing required fields: portrait_alt'):
            validator(missing_alt)

        unsafe_asset = copy.deepcopy(minister)
        unsafe_asset['portrait'] = '../portrait.svg'
        with self.assertRaisesRegex(ValueError, 'safe product image reference'):
            validator(unsafe_asset)

        missing_asset = copy.deepcopy(minister)
        missing_asset['portrait'] = 'minister-profile/missing.svg'
        with self.assertRaisesRegex(ValueError, 'portrait asset does not exist'):
            validator(missing_asset)

        unsafe_link = copy.deepcopy(minister)
        unsafe_link['related_links'][0]['href'] = 'javascript:alert(1)'
        with self.assertRaisesRegex(ValueError, 'safe internal or HTTPS destination'):
            validator(unsafe_link)

    def test_minister_css_is_logical_and_foundation_is_not_copied(self):
        css = (PRODUCT / 'templates/minister-profile/minister-profile.css').read_text()
        self.assertIn('padding-inline-start', css)
        self.assertIn('border-inline-start', css)
        self.assertIn('@media (max-width: 767px)', css)
        self.assertIn('grid-template-columns: minmax(0, 1fr)', css)
        self.assertIsNone(re.search(r'\b(?:left|right)\b', css))
        for name in ('components', 'sections', 'partials', 'styles', 'scripts', 'token.css'):
            self.assertFalse((PRODUCT / name).exists())


if __name__ == '__main__':
    unittest.main()
