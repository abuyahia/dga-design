import copy
from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / 'products/authority'
SPEC = importlib.util.spec_from_file_location('build_site', ROOT / 'scripts/build_site.py')
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class Outline(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.nested_lists = 0
        self.images = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get('class', '').split())
        if tag == 'h1':
            self.h1 += 1
        if tag == 'ul' and 'organization-tree__level' in classes:
            self.nested_lists += 1
        if tag == 'img':
            self.images.append(attributes)


class AuthorityProfileTests(unittest.TestCase):
    def test_a05_executive_profile_is_authority_owned_and_accessible(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            pages = BUILDER.build_product('authority', output)
            markup = (output / 'leadership.html').read_text()

        document = Outline()
        document.feed(markup)
        portrait = next(image for image in document.images if 'portrait-placeholder.svg' in image.get('src', ''))
        self.assertIn('leadership.html', pages)
        self.assertEqual(document.h1, 1)
        self.assertTrue(portrait.get('alt'))
        self.assertIn('د. ريم بنت خالد السَّنامي', markup)
        self.assertIn('الرئيس التنفيذي لهيئة نماء التجريبية', markup)
        self.assertIn('assets/products/authority/executive-profile/executive-profile.css', markup)
        self.assertNotIn('minister-profile', markup)

    def test_a06_organization_is_semantic_and_rejects_invalid_graphs(self):
        product = BUILDER.load_product('authority')
        organization = next(page for page in product['data']['pages'] if page['path'] == 'organization.html')
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            BUILDER.build_product('authority', output)
            markup = (output / 'organization.html').read_text()

        document = Outline()
        document.feed(markup)
        self.assertEqual(document.h1, 1)
        self.assertGreater(document.nested_lists, 1)
        self.assertIn('مجلس الإدارة التجريبي', markup)
        self.assertIn('إدارة التواصل والدعم', markup)
        self.assertNotIn('<canvas', markup)

        for mutation, message in (
            (lambda nodes: nodes.append(copy.deepcopy(nodes[0])), 'ids must be unique'),
            (lambda nodes: nodes.__setitem__(1, {**nodes[1], 'parent_id': 'missing'}), 'orphan'),
            (lambda nodes: nodes.__setitem__(1, {**nodes[1], 'parent_id': nodes[1]['id']}), 'cycle'),
        ):
            invalid = copy.deepcopy(organization)
            mutation(invalid['organization']['nodes'])
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                BUILDER.validate_organization(invalid)

    def test_shared_organization_validator_accepts_a_second_sector_shape(self):
        second_consumer = {
            'organization': {
                'summary': 'A neutral second-sector hierarchy fixture.',
                'nodes': [
                    {'id': 'root', 'parent_id': None, 'label': 'Root', 'description': 'Root responsibility.'},
                    {'id': 'unit', 'parent_id': 'root', 'label': 'Unit', 'description': 'Unit responsibility.'},
                ],
            }
        }
        BUILDER.validate_organization(second_consumer)

    def test_profiles_do_not_import_ministry_assets_or_templates(self):
        files = [
            PRODUCT / 'templates/executive-profile/renderer.py',
            PRODUCT / 'templates/executive-profile/template.html',
            PRODUCT / 'content/demo/leadership.json',
            PRODUCT / 'content/demo/organization.json',
        ]
        source = '\n'.join(path.read_text() for path in files)
        self.assertNotIn('products/ministry/', source)
        self.assertNotIn('../ministry', source)


if __name__ == '__main__':
    unittest.main()
