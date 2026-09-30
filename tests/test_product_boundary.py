import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('build_site', ROOT / 'scripts/build_site.py')
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class ProductBoundaryTests(unittest.TestCase):
    def load_registry(self, pages, content_files=None):
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        page_root = root / 'pages'
        content_root = root / 'content'
        page_root.mkdir()
        content_root.mkdir()
        for name, value in (content_files or {}).items():
            path = content_root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value))
        page_references = []
        for index, page in enumerate(pages):
            reference = f'page-{index}.json'
            (page_root / reference).write_text(json.dumps(page))
            page_references.append(reference)
        registry = page_root / 'index.json'
        registry.write_text(json.dumps({'schema_version': 1, 'pages': page_references}))
        return directory, registry, content_root

    def test_ministry_manifest_and_configuration_resolve(self):
        product = BUILDER.load_product('ministry')
        product_root = ROOT / 'products/ministry'
        navigation = json.loads((product_root / 'navigation.json').read_text())
        footer = json.loads((product_root / 'footer.json').read_text())

        self.assertEqual(product['manifest']['id'], 'ministry')
        self.assertEqual(product['root'], product_root)
        self.assertEqual(product['source_config'], ROOT / 'site/government.json')
        self.assertEqual(product['output'], ROOT / 'dist/products/ministry')
        self.assertEqual(product['data']['navigation'], navigation['navigation'])
        self.assertEqual(product['data']['navigation_label'], navigation['navigation_label'])
        for key, value in footer.items():
            self.assertEqual(product['data'][key], value)
        for path in product['paths'].values():
            self.assertTrue(path == product_root or product_root in path.parents)

    def test_empty_registry_is_deterministic_and_unregistered_routes_remain_transitional(self):
        directory, registry, content_root = self.load_registry([])
        with directory:
            self.assertEqual(BUILDER.load_page_registry(registry, content_root), [])

        product = BUILDER.load_product('ministry')
        transitional = json.loads((ROOT / 'site/government.json').read_text())
        registered_paths = {page['path'] for page in product['registered_pages']}
        transitional_remaining = [
            page for page in transitional['pages'] if page['path'] not in registered_paths
        ]
        remaining_paths = {page['path'] for page in transitional_remaining}
        product_remaining = [
            page for page in product['data']['pages'] if page['path'] in remaining_paths
        ]

        self.assertEqual(product['paths']['pages'], ROOT / 'products/ministry/pages/index.json')
        self.assertIn('about.html', registered_paths)
        self.assertEqual(product_remaining, transitional_remaining)

    def test_registered_renderer_controls_the_page_sections(self):
        page = {
            'id': 'example',
            'route': 'example.html',
            'renderer': 'page-intro',
            'content': 'example.json',
        }
        directory, registry, content_root = self.load_registry(
            [page],
            {'example.json': {'title': 'Example', 'description': 'Example summary'}},
        )
        with directory:
            pages = BUILDER.load_page_registry(registry, content_root)

        self.assertEqual(
            pages,
            [{
                'title': 'Example',
                'description': 'Example summary',
                'path': 'example.html',
                'sections': ['page-intro', 'feedback'],
            }],
        )

    def test_registered_route_replaces_its_transitional_source(self):
        transitional = [
            {'path': 'example.html', 'title': 'Transitional'},
            {'path': 'remaining.html', 'title': 'Remaining'},
        ]
        registered = [{'path': 'example.html', 'title': 'Product'}]

        self.assertEqual(
            BUILDER._merge_registered_pages(transitional, registered),
            [registered[0], transitional[1]],
        )

    def test_unknown_renderer_id_fails_clearly(self):
        page = {
            'id': 'example',
            'route': 'example.html',
            'renderer': 'unknown',
            'content': 'example.json',
        }
        directory, registry, content_root = self.load_registry([page])
        with directory, self.assertRaisesRegex(ValueError, 'Unknown product page renderer: unknown'):
            BUILDER.load_page_registry(registry, content_root)

    def test_duplicate_route_fails_clearly(self):
        pages = [
            {
                'id': 'first',
                'route': 'duplicate.html',
                'renderer': 'page-intro',
                'content': 'first.json',
            },
            {
                'id': 'second',
                'route': 'duplicate.html',
                'renderer': 'page-intro',
                'content': 'second.json',
            },
        ]
        directory, registry, content_root = self.load_registry(
            pages,
            {'first.json': {}, 'second.json': {}},
        )
        with directory, self.assertRaisesRegex(ValueError, 'Duplicate product page route: duplicate.html'):
            BUILDER.load_page_registry(registry, content_root)

    def test_missing_content_reference_fails_clearly(self):
        page = {
            'id': 'example',
            'route': 'example.html',
            'renderer': 'page-intro',
            'content': 'missing.json',
        }
        directory, registry, content_root = self.load_registry([page])
        with directory, self.assertRaisesRegex(ValueError, 'content reference does not exist: missing.json'):
            BUILDER.load_page_registry(registry, content_root)

    def test_unsafe_content_reference_fails_clearly(self):
        page = {
            'id': 'example',
            'route': 'example.html',
            'renderer': 'page-intro',
            'content': '../outside.json',
        }
        directory, registry, content_root = self.load_registry([page])
        with directory:
            (content_root.parent / 'outside.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'content reference must stay inside demo_content'):
                BUILDER.load_page_registry(registry, content_root)

    def test_unsafe_route_fails_clearly(self):
        page = {
            'id': 'example',
            'route': '../example.html',
            'renderer': 'page-intro',
            'content': 'example.json',
        }
        directory, registry, content_root = self.load_registry([page])
        with directory, self.assertRaisesRegex(ValueError, 'route must be a safe flat HTML filename'):
            BUILDER.load_page_registry(registry, content_root)

    def test_content_cannot_select_sections_or_renderer(self):
        page = {
            'id': 'example',
            'route': 'example.html',
            'renderer': 'page-intro',
            'content': 'example.json',
        }
        directory, registry, content_root = self.load_registry(
            [page],
            {'example.json': {'sections': ['contact']}},
        )
        with directory, self.assertRaisesRegex(ValueError, 'cannot define execution fields: sections'):
            BUILDER.load_page_registry(registry, content_root)

    def test_unsafe_page_reference_fails_clearly(self):
        directory, registry, content_root = self.load_registry([])
        with directory:
            outside = registry.parent.parent / 'outside.json'
            outside.write_text('{}')
            registry.write_text(json.dumps({'schema_version': 1, 'pages': ['../outside.json']}))
            with self.assertRaisesRegex(ValueError, 'page reference must stay inside the pages directory'):
                BUILDER.load_page_registry(registry, content_root)

    def test_product_build_reuses_foundation_and_legacy_build_still_works(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            product_pages = BUILDER.build_product('ministry', root / 'product')
            legacy_pages = BUILDER.build(ROOT / 'site/government.json', root / 'legacy')

            self.assertTrue(set(legacy_pages).issubset(product_pages))
            self.assertTrue((root / 'product/token.css').is_file())
            self.assertTrue((root / 'product/components/navigation-header/navigation-header.css').is_file())
            self.assertFalse((ROOT / 'products/ministry/token.css').exists())
            self.assertFalse((ROOT / 'products/ministry/components').exists())
            self.assertFalse((ROOT / 'products/ministry/sections').exists())
            self.assertFalse((ROOT / 'products/ministry/partials').exists())
            self.assertFalse((ROOT / 'products/ministry/styles').exists())
            self.assertFalse((ROOT / 'products/ministry/scripts').exists())

    def test_invalid_product_id_fails_clearly(self):
        for product_id in ('../ministry', 'Ministry', 'ministry/example'):
            with self.subTest(product_id=product_id):
                with self.assertRaisesRegex(ValueError, 'Invalid product id'):
                    BUILDER.load_product(product_id)

        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts/build_site.py'), '--product', '../ministry'],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn('Invalid product id', result.stderr)

        with self.assertRaisesRegex(ValueError, 'Unknown product: university'):
            BUILDER.load_product('university')

    def test_product_cli_selects_ministry(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'ministry'
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / 'scripts/build_site.py'),
                    '--product',
                    'ministry',
                    '--output',
                    str(output),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Built: index.html', result.stdout)
            self.assertTrue((output / 'index.html').is_file())

    def test_config_cli_remains_supported(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'configured'
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / 'scripts/build_site.py'),
                    '--config',
                    str(ROOT / 'site/government.json'),
                    '--output',
                    str(output),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Built: index.html', result.stdout)
            self.assertTrue((output / 'index.html').is_file())

    def test_authority_manifest_applies_owned_overlay_without_ministry_dependency(self):
        product = BUILDER.load_product('authority')
        authority_root = ROOT / 'products/authority'

        self.assertEqual(product['root'], authority_root)
        self.assertEqual(product['source_config'], ROOT / 'site/government.json')
        self.assertEqual(product['output'], ROOT / 'dist/products/authority')
        self.assertEqual(
            product['paths']['config_overlay'],
            authority_root / 'content/demo/product-overlay.json',
        )
        self.assertEqual(product['paths']['assets'], authority_root / 'assets')
        self.assertNotEqual(product['paths']['assets'], ROOT / 'products/ministry/assets')
        self.assertEqual(product['data']['site_name'], 'الهيئة الوطنية لتنمية المنظومات والخدمات')
        self.assertEqual(product['data']['brand_initial'], 'ن')
        self.assertEqual(product['data']['services'][0]['id'], 'journey-readiness')
        registered_paths = [page['path'] for page in product['registered_pages']]
        self.assertEqual(len(registered_paths), len(set(registered_paths)))
        self.assertIn('about.html', registered_paths)

        runtime_files = [
            authority_root / 'product.json',
            authority_root / 'navigation.json',
            authority_root / 'footer.json',
            authority_root / 'pages/index.json',
            authority_root / 'content/demo/product-overlay.json',
        ]
        authority_text = '\n'.join(path.read_text() for path in runtime_files)
        self.assertNotIn('products/ministry/', authority_text)
        self.assertNotIn('../ministry', authority_text)
        for copied_root in ('components', 'sections', 'partials', 'styles', 'scripts'):
            self.assertFalse((authority_root / copied_root).exists())

    def test_authority_build_uses_shared_foundation_and_owned_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'authority'
            pages = BUILDER.build_product('authority', output)
            index = (output / 'index.html').read_text()

            self.assertIn('index.html', pages)
            self.assertIn('services.html', pages)
            self.assertIn('service-journey-readiness.html', pages)
            self.assertIn('الهيئة الوطنية لتنمية المنظومات والخدمات', index)
            self.assertIn('لا تمثل جهة حكومية فعلية', index)
            self.assertNotIn('الجهة النموذجية', index)
            self.assertTrue((output / 'token.css').is_file())
            self.assertTrue((output / 'components/navigation-header/navigation-header.css').is_file())
            self.assertFalse((output / 'assets/products/ministry').exists())

    def test_product_overlay_rejects_unknown_and_execution_fields(self):
        source = json.loads(
            (ROOT / 'products/authority/content/demo/product-overlay.json').read_text()
        )
        for field, value in (
            ('renderer', 'authority'),
            ('module', 'renderer.py'),
            ('sections', ['hero']),
            ('path', '../outside.json'),
        ):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                invalid = dict(source)
                invalid[field] = value
                path = Path(directory) / 'overlay.json'
                path.write_text(json.dumps(invalid))
                with self.assertRaisesRegex(ValueError, 'must define only'):
                    BUILDER.load_product_overlay(path)

    def test_product_overlay_path_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            product_root = Path(directory) / 'authority'
            product_root.mkdir()
            outside = product_root.parent / 'outside.json'
            outside.write_text('{}')
            with self.assertRaisesRegex(ValueError, 'must stay inside the product directory'):
                BUILDER._resolve_product_path(
                    product_root, '../outside.json', 'config_overlay', 'file'
                )


if __name__ == '__main__':
    unittest.main()
