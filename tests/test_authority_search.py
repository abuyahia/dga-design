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


class SearchDocument(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.forms = []
        self.results = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get('class', '').split())
        if tag == 'h1':
            self.h1 += 1
        if tag == 'form' and 'search-results__form' in classes:
            self.forms.append(attributes)
        if tag == 'li' and 'search-results__item' in classes:
            self.results += 1


class AuthoritySearchTests(unittest.TestCase):
    def test_a09_shared_contract_and_a10_adapter_derive_records(self):
        source = json.loads((PRODUCT / 'content/demo/search.json').read_text())
        product = BUILDER.load_product('authority')
        search = next(page for page in product['data']['pages'] if page['path'] == 'search.html')

        self.assertEqual(source['search']['records'], [])
        self.assertGreater(len(search['search']['records']), 6)
        self.assertEqual(search['robots'], 'noindex,follow')
        routes = [record['route'] for record in search['search']['records']]
        self.assertEqual(len(routes), len(set(routes)))
        self.assertIn('about.html', routes)
        self.assertIn('service-journey-readiness.html', routes)
        for record in search['search']['records']:
            self.assertTrue(set(record) <= {'id', 'type', 'type_label', 'title', 'summary', 'route', 'date'})

    def test_search_build_has_get_form_noindex_empty_state_and_header_route(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            BUILDER.build_product('authority', output)
            search_markup = (output / 'search.html').read_text()
            about_markup = (output / 'about.html').read_text()

        document = SearchDocument()
        document.feed(search_markup)
        self.assertEqual(document.h1, 1)
        self.assertEqual(len(document.forms), 1)
        self.assertEqual(document.forms[0].get('method'), 'get')
        self.assertEqual(document.forms[0].get('action'), 'search.html')
        self.assertGreater(document.results, 6)
        self.assertIn('<meta name="robots" content="noindex,follow">', search_markup)
        self.assertIn('data-search-empty hidden', search_markup)
        self.assertIn('sections/search-results/search-results.js', search_markup)
        self.assertIn('href="search.html" aria-label="البحث في الموقع"', about_markup)
        self.assertNotIn('class="site-search"', about_markup)

    def test_search_contract_rejects_unsafe_result_routes(self):
        product = BUILDER.load_product('authority')
        invalid = copy.deepcopy(product['data'])
        search = next(page for page in invalid['pages'] if page['path'] == 'search.html')
        search['search']['records'][0]['route'] = '../outside.html'
        with self.assertRaisesRegex(ValueError, 'safe shared contract'):
            BUILDER.validate_search_results(search)

    def test_search_adapter_is_code_owned_and_ministry_independent(self):
        manifest = json.loads((PRODUCT / 'product.json').read_text())
        page = json.loads((PRODUCT / 'pages/search.json').read_text())
        content = json.loads((PRODUCT / 'content/demo/search.json').read_text())
        self.assertNotIn('adapter', manifest)
        self.assertNotIn('module', page)
        self.assertNotIn('module', content)
        adapter = (PRODUCT / 'templates/search/adapter.py').read_text()
        self.assertNotIn('products/ministry/', adapter)
        self.assertNotIn('../ministry', adapter)


if __name__ == '__main__':
    unittest.main()
