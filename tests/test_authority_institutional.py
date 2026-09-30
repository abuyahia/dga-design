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


class InstitutionalDocument(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.toc = []
        self.ids = set()
        self.metadata_lists = 0
        self.ordered_lists = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get('class', '').split())
        if tag == 'h1':
            self.h1 += 1
        if attributes.get('id'):
            self.ids.add(attributes['id'])
        if tag == 'a' and 'table-of-contents__link' in classes:
            self.toc.append(attributes.get('href'))
        if tag == 'dl' and 'heavy-content__metadata' in classes:
            self.metadata_lists += 1
        if tag == 'ol' and 'list--ordered' in classes:
            self.ordered_lists += 1


class AuthorityInstitutionalTests(unittest.TestCase):
    def test_a03_and_a04_are_registered_with_shared_heavy_content(self):
        registry = json.loads((PRODUCT / 'pages/index.json').read_text())
        product = BUILDER.load_product('authority')
        registered = {page['path']: page for page in product['registered_pages']}

        self.assertIn('mandate.json', registry['pages'])
        self.assertIn('strategy.json', registry['pages'])
        self.assertEqual(registered['mandate.html']['sections'], ['heavy-content', 'feedback'])
        self.assertEqual(registered['strategy.html']['sections'], ['heavy-content', 'feedback'])
        self.assertEqual(registered['mandate.html']['updated'], '2026-09-14')
        self.assertEqual(registered['strategy.html']['updated'], '2026-09-14')

    def test_mandate_and_strategy_render_complete_accessible_structures(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            BUILDER.build_product('authority', output)
            mandate = (output / 'mandate.html').read_text()
            strategy = (output / 'strategy.html').read_text()

        mandate_doc = InstitutionalDocument()
        mandate_doc.feed(mandate)
        strategy_doc = InstitutionalDocument()
        strategy_doc.feed(strategy)

        self.assertEqual(mandate_doc.h1, 1)
        self.assertEqual(mandate_doc.metadata_lists, 1)
        self.assertEqual(mandate_doc.ordered_lists, 1)
        self.assertTrue(all(target[1:] in mandate_doc.ids for target in mandate_doc.toc))
        self.assertIn('وثيقة عرض غير نافذة', mandate)
        self.assertIn('mandate.html#legal-basis', mandate)
        self.assertIn('<bdi>قرار إنشاء تجريبي رقم (ن-01/1448)</bdi>', mandate)
        self.assertIn('<time datetime="2026-09-14">2026-09-14</time>', mandate)

        self.assertEqual(strategy_doc.h1, 1)
        self.assertTrue(all(target[1:] in strategy_doc.ids for target in strategy_doc.toc))
        self.assertIn('منظومات خدمات مترابطة تصنع أثرًا مستدامًا', strategy)
        self.assertIn('مشاركة مبكرة', strategy)
        self.assertIn('href="programs.html"', strategy)
        self.assertIn('<html lang="ar" dir="rtl">', strategy)

    def test_a03_a04_add_no_product_templates_or_ministry_references(self):
        for name in ('mandate', 'strategy'):
            self.assertFalse((PRODUCT / 'templates' / name).exists())
            self.assertFalse((PRODUCT / 'assets' / f'{name}.css').exists())
        source = '\n'.join(
            (PRODUCT / relative).read_text()
            for relative in (
                'pages/mandate.json', 'pages/strategy.json',
                'content/demo/mandate.json', 'content/demo/strategy.json',
            )
        )
        self.assertNotIn('products/ministry/', source)
        self.assertNotIn('../ministry', source)


if __name__ == '__main__':
    unittest.main()
