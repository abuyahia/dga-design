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

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_h1:
            self.h1_text.append(data)


class MinistryAboutTests(unittest.TestCase):
    def test_about_registration_uses_product_data_and_heavy_content(self):
        registry = json.loads((PRODUCT / 'pages/index.json').read_text())
        definition = json.loads((PRODUCT / 'pages/about.json').read_text())
        content = json.loads((PRODUCT / 'content/demo/about.json').read_text())
        product = BUILDER.load_product('ministry')
        about = next(page for page in product['data']['pages'] if page['path'] == 'about.html')

        self.assertEqual(registry['schema_version'], 1)
        self.assertIn('about.json', registry['pages'])
        self.assertEqual(set(definition), {'id', 'route', 'renderer', 'content'})
        self.assertEqual(definition['renderer'], 'heavy-content')
        self.assertEqual(
            next(page for page in product['registered_pages'] if page['path'] == 'about.html'),
            about,
        )
        self.assertEqual(about['title'], content['title'])
        self.assertEqual(about['description'], content['description'])
        self.assertEqual(about['heavy_content'], content['heavy_content'])
        self.assertEqual(about['updated'], content['updated'])
        self.assertEqual(about['sections'], ['heavy-content', 'feedback'])

    def test_about_build_has_canonical_intro_breadcrumb_and_resolved_toc(self):
        content = json.loads((PRODUCT / 'content/demo/about.json').read_text())
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            pages = BUILDER.build_product('ministry', output)
            markup = (output / 'about.html').read_text()

            self.assertIn('about.html', pages)
            self.assertTrue((output / 'sections/heavy-content/heavy-content.css').is_file())
            self.assertTrue((output / 'components/table-of-contents/table-of-contents.css').is_file())

        document = AboutDocument()
        document.feed(markup)
        self.assertEqual(document.h1_count, 1)
        self.assertEqual(''.join(document.h1_text), content['title'])
        self.assertEqual(document.page_intro_count, 1)
        self.assertEqual(document.heavy_content_count, 1)
        self.assertEqual(document.breadcrumb_items, 2)
        self.assertEqual(document.current_breadcrumbs, 1)
        self.assertIn('<html lang="ar" dir="rtl">', markup)
        self.assertIn('<a href="index.html" class="breadcrumb__link">الرئيسية</a>', markup)
        self.assertIn(f'<span class="breadcrumb__link">{content["title"]}</span>', markup)
        self.assertEqual(len(document.ids), len(set(document.ids)))
        self.assertEqual(document.toc_targets, ['#mandate', '#responsibilities', '#working-principles'])
        self.assertTrue(all(target[1:] in document.ids for target in document.toc_targets))
        self.assertIn('href="about.html#responsibilities"', markup)
        self.assertIn('&lt;جهة حقيقية&gt;', markup)
        self.assertNotIn('<جهة حقيقية>', markup)
        self.assertIn('<time datetime="2026-09-14">2026-09-14</time>', markup)

    def test_about_rejects_unsafe_content_links(self):
        product = BUILDER.load_product('ministry')
        invalid = copy.deepcopy(product['data'])
        about = next(page for page in invalid['pages'] if page['path'] == 'about.html')
        about['heavy_content']['sections'][0]['blocks'][1]['href'] = 'javascript:alert(1)'

        with self.assertRaisesRegex(ValueError, 'Link blocks require a safe destination'):
            BUILDER.validate(invalid)

    def test_about_introduces_no_product_template_or_foundation_copy(self):
        self.assertFalse((PRODUCT / 'templates/about').exists())
        for name in ('components', 'sections', 'partials', 'styles', 'scripts', 'token.css'):
            self.assertFalse((PRODUCT / name).exists())


if __name__ == '__main__':
    unittest.main()
