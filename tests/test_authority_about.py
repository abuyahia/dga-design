import copy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / 'products/authority'
SPEC = importlib.util.spec_from_file_location('build_site', ROOT / 'scripts/build_site.py')
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class AboutDocument(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1_count = 0
        self.h1_text = []
        self.in_h1 = False
        self.ids = []
        self.toc_targets = []
        self.page_intro_count = 0
        self.heavy_content_count = 0
        self.breadcrumb_items = 0
        self.current_breadcrumbs = 0
        self.disabled_relationships = []

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
        if tag == 'article' and 'heavy-content' in classes:
            self.heavy_content_count += 1
        if tag == 'li' and 'breadcrumb__item' in classes:
            self.breadcrumb_items += 1
            if attributes.get('aria-current') == 'page':
                self.current_breadcrumbs += 1
        if tag == 'a' and 'table-of-contents__link' in classes:
            self.toc_targets.append(attributes.get('href'))
        if tag == 'a' and 'link' in classes and attributes.get('aria-disabled') == 'true':
            self.disabled_relationships.append(attributes)

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_h1:
            self.h1_text.append(data)


class AuthorityAboutTests(unittest.TestCase):
    def test_about_registration_uses_authority_content_and_shared_renderer(self):
        registry = json.loads((PRODUCT / 'pages/index.json').read_text())
        definition = json.loads((PRODUCT / 'pages/about.json').read_text())
        content = json.loads((PRODUCT / 'content/demo/about.json').read_text())
        product = BUILDER.load_product('authority')
        about = next(page for page in product['data']['pages'] if page['path'] == 'about.html')

        self.assertEqual(registry['schema_version'], 1)
        self.assertIn('about.json', registry['pages'])
        self.assertEqual(definition, {
            'id': 'about',
            'route': 'about.html',
            'renderer': 'heavy-content',
            'content': 'about.json',
        })
        self.assertEqual(about['title'], content['title'])
        self.assertEqual(about['description'], content['description'])
        self.assertEqual(about['updated'], content['updated'])
        self.assertEqual(about['heavy_content'], content['heavy_content'])
        self.assertEqual(about['sections'], ['heavy-content', 'feedback'])
        self.assertEqual(
            next(page for page in product['registered_pages'] if page['path'] == 'about.html'),
            about,
        )

        relationships = content['heavy_content']['sections'][-1]['blocks'][1:]
        self.assertEqual(
            [relationship['href'] for relationship in relationships],
            ['mandate.html', 'strategy.html'],
        )

    def test_about_build_satisfies_page_specification_structure(self):
        content = json.loads((PRODUCT / 'content/demo/about.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            pages = BUILDER.build_product('authority', output)
            markup = (output / 'about.html').read_text()

            self.assertIn('about.html', pages)
            self.assertTrue((output / 'sections/heavy-content/heavy-content.css').is_file())
            self.assertTrue((output / 'components/table-of-contents/table-of-contents.css').is_file())

        document = AboutDocument()
        document.feed(markup)
        expected_targets = [
            '#about-authority', '#establishment', '#mandate-summary',
            '#responsibilities', '#principles', '#related-pages',
        ]
        self.assertEqual(document.h1_count, 1)
        self.assertEqual(''.join(document.h1_text), 'عن الهيئة')
        self.assertEqual(document.page_intro_count, 1)
        self.assertEqual(document.heavy_content_count, 1)
        self.assertEqual(document.breadcrumb_items, 2)
        self.assertEqual(document.current_breadcrumbs, 1)
        self.assertEqual(document.toc_targets, expected_targets)
        self.assertTrue(all(target[1:] in document.ids for target in document.toc_targets))
        self.assertEqual(len(document.ids), len(set(document.ids)))
        self.assertEqual(len(document.disabled_relationships), 0)
        self.assertIn('href="mandate.html"', markup)
        self.assertIn('href="strategy.html"', markup)
        self.assertIn('<html lang="ar" dir="rtl">', markup)
        self.assertIn('<a href="index.html" class="breadcrumb__link">الرئيسية</a>', markup)
        self.assertIn('<span class="breadcrumb__link">عن الهيئة</span>', markup)
        self.assertIn('الهيئة الوطنية لتنمية المنظومات والخدمات', markup)
        self.assertIn('قرار إنشاء تجريبي رقم (ن-01/1448)', markup)
        self.assertIn('إعداد أدلة غير ملزمة لتحسين تصميم الخدمات العامة.', markup)
        self.assertIn('الوضوح: نشر المتطلبات والنتائج بلغة يمكن فهمها.', markup)
        self.assertIn('<time datetime="2026-09-14">2026-09-14</time>', markup)
        self.assertNotIn('الجهة النموذجية', markup)
        self.assertNotIn('الوزارة التجريبية', markup)
        self.assertEqual(content['description'] in markup, True)

    def test_planned_relationships_reject_unsafe_or_existing_routes(self):
        product = BUILDER.load_product('authority')
        for route in ('../mandate.html', 'javascript:alert(1)', 'about.html', 7):
            with self.subTest(route=route):
                invalid = copy.deepcopy(product['data'])
                about = next(page for page in invalid['pages'] if page['path'] == 'about.html')
                about['heavy_content']['sections'][-1]['blocks'][1]['planned_route'] = route
                with self.assertRaisesRegex(
                    ValueError, 'Planned link blocks require one safe, not-yet-generated route'
                ):
                    BUILDER.validate(invalid)

    def test_about_adds_no_product_template_css_or_ministry_dependency(self):
        self.assertFalse((PRODUCT / 'templates/about').exists())
        self.assertFalse((PRODUCT / 'assets/about.css').exists())
        for name in ('components', 'sections', 'partials', 'styles', 'scripts', 'token.css'):
            self.assertFalse((PRODUCT / name).exists())

        runtime_files = [
            PRODUCT / 'product.json',
            PRODUCT / 'pages/index.json',
            PRODUCT / 'pages/about.json',
            PRODUCT / 'content/demo/about.json',
        ]
        source = '\n'.join(path.read_text() for path in runtime_files)
        self.assertNotIn('products/ministry/', source)
        self.assertNotIn('../ministry', source)


if __name__ == '__main__':
    unittest.main()
