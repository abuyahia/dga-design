import copy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / 'products/ministry'
SPEC = importlib.util.spec_from_file_location('build_site', ROOT / 'scripts/build_site.py')
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class StrategyDocument(HTMLParser):
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
        self.ordered_lists = 0

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
        if tag == 'ol' and {'list', 'list--ordered'} <= classes:
            self.ordered_lists += 1

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_h1:
            self.h1_text.append(data)


class MinistryStrategyTests(unittest.TestCase):
    def test_strategy_registration_uses_m02_heavy_content_pattern(self):
        registry = json.loads((PRODUCT / 'pages/index.json').read_text())
        definition = json.loads((PRODUCT / 'pages/strategy.json').read_text())
        content = json.loads((PRODUCT / 'content/demo/strategy.json').read_text())
        product = BUILDER.load_product('ministry')
        strategy = next(page for page in product['data']['pages'] if page['path'] == 'strategy.html')

        self.assertEqual(registry['schema_version'], 1)
        self.assertIn('strategy.json', registry['pages'])
        self.assertEqual(set(definition), {'id', 'route', 'renderer', 'content'})
        self.assertEqual(definition, {
            'id': 'strategy',
            'route': 'strategy.html',
            'renderer': 'heavy-content',
            'content': 'strategy.json',
        })
        self.assertEqual(strategy['title'], content['title'])
        self.assertEqual(strategy['description'], content['description'])
        self.assertEqual(strategy['updated'], content['updated'])
        self.assertEqual(strategy['heavy_content'], content['heavy_content'])
        self.assertEqual(strategy['sections'], ['heavy-content', 'feedback'])

    def test_strategy_build_renders_objectives_and_canonical_navigation(self):
        content = json.loads((PRODUCT / 'content/demo/strategy.json').read_text())
        objectives = content['heavy_content']['sections'][2]['blocks'][1]['items']
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            pages = BUILDER.build_product('ministry', output)
            markup = (output / 'strategy.html').read_text()
            about_markup = (output / 'about.html').read_text()

            self.assertIn('strategy.html', pages)
            self.assertIn('about.html', pages)
            self.assertTrue((output / 'sections/heavy-content/heavy-content.css').is_file())
            self.assertTrue((output / 'components/table-of-contents/table-of-contents.css').is_file())

        document = StrategyDocument()
        document.feed(markup)
        self.assertEqual(document.h1_count, 1)
        self.assertEqual(''.join(document.h1_text), content['title'])
        self.assertEqual(document.page_intro_count, 1)
        self.assertEqual(document.heavy_content_count, 1)
        self.assertEqual(document.breadcrumb_items, 2)
        self.assertEqual(document.current_breadcrumbs, 1)
        self.assertEqual(document.ordered_lists, 1)
        self.assertEqual(len(document.ids), len(set(document.ids)))
        self.assertEqual(document.toc_targets, ['#vision', '#mission', '#objectives'])
        self.assertTrue(all(target[1:] in document.ids for target in document.toc_targets))
        self.assertIn('<html lang="ar" dir="rtl">', markup)
        self.assertIn('<a href="index.html" class="breadcrumb__link">الرئيسية</a>', markup)
        self.assertIn(f'<span class="breadcrumb__link">{content["title"]}</span>', markup)
        self.assertIn('href="about.html#mandate"', markup)
        for objective in objectives:
            self.assertIn(f'<span class="list__text">{objective}</span>', markup)
        self.assertIn('&lt;مؤشرات حقيقية&gt;', markup)
        self.assertNotIn('<مؤشرات حقيقية>', markup)
        self.assertIn('<time datetime="2026-09-14">2026-09-14</time>', markup)
        self.assertIn('عن الوزارة التجريبية للخدمات المجتمعية', about_markup)

    def test_strategy_rejects_unsafe_content_links(self):
        product = BUILDER.load_product('ministry')
        invalid = copy.deepcopy(product['data'])
        strategy = next(page for page in invalid['pages'] if page['path'] == 'strategy.html')
        strategy['heavy_content']['sections'][1]['blocks'][1]['href'] = 'javascript:alert(1)'

        with self.assertRaisesRegex(ValueError, 'Link blocks require a safe destination'):
            BUILDER.validate(invalid)

    def test_strategy_introduces_no_template_or_foundation_copy(self):
        self.assertFalse((PRODUCT / 'templates/strategy').exists())
        for name in ('components', 'sections', 'partials', 'styles', 'scripts', 'token.css'):
            self.assertFalse((PRODUCT / name).exists())


if __name__ == '__main__':
    unittest.main()
