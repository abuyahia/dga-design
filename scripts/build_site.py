"""Build the government example or a selected product from trusted sources."""
import argparse
import html
import importlib.util
import json
from pathlib import Path
import re
import shutil
try:
    from scripts.breadcrumb_markup import render_two_level
    from scripts.contact_markup import contact_page, validate_contact
    from scripts.feedback_markup import render_feedback
    from scripts.footer_markup import render_footer
    from scripts.digital_stamp_markup import render_stamp, validate_stamp
    from scripts.service_markup import validate_services, service_card, catalogue, overview, detail_url
    from scripts.content_markup import validate_heavy_content, render_heavy_content
    from scripts.form_markup import validate_form_template, render_form_template
    from scripts.page_intro_markup import validate_page_intro, render_page_intro
    from scripts.error_state_markup import validate_error_state, render_error_state
    from scripts.organization_markup import validate_organization, render_organization
    from scripts.search_markup import validate_search_results, render_search_results
    from scripts.editorial_markup import validate_editorial_records, render_editorial_listing, render_editorial_detail
    from scripts.portfolio_markup import validate_portfolio_records, render_portfolio_listing, render_portfolio_detail
    from scripts.resource_markup import validate_resource_records, render_resource_listing, render_resource_detail
except ImportError:
    from breadcrumb_markup import render_two_level
    from contact_markup import contact_page, validate_contact
    from feedback_markup import render_feedback
    from footer_markup import render_footer
    from digital_stamp_markup import render_stamp, validate_stamp
    from service_markup import validate_services, service_card, catalogue, overview, detail_url
    from content_markup import validate_heavy_content, render_heavy_content
    from form_markup import validate_form_template, render_form_template
    from page_intro_markup import validate_page_intro, render_page_intro
    from error_state_markup import validate_error_state, render_error_state
    from organization_markup import validate_organization, render_organization
    from search_markup import validate_search_results, render_search_results
    from editorial_markup import validate_editorial_records, render_editorial_listing, render_editorial_detail
    from portfolio_markup import validate_portfolio_records, render_portfolio_listing, render_portfolio_detail
    from resource_markup import validate_resource_records, render_resource_listing, render_resource_detail

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_ROOT = ROOT / 'products'
PRODUCT_ID_PATTERN = re.compile(r'[a-z][a-z0-9-]*')
PRODUCT_PAGE_ID_PATTERN = re.compile(r'[a-z][a-z0-9-]*')
PRODUCT_PAGE_ROUTE_PATTERN = re.compile(r'[a-z][a-z0-9-]*\.html')
PRODUCT_PATHS = {
    'navigation': 'file',
    'footer': 'file',
    'pages': 'file',
    'templates': 'directory',
    'demo_content': 'directory',
    'assets': 'directory',
}
PRODUCT_MANIFEST_REQUIRED_FIELDS = {
    'schema_version', 'id', 'name', 'source_config', *PRODUCT_PATHS,
}
PRODUCT_MANIFEST_OPTIONAL_FIELDS = {'config_overlay'}
PRODUCT_OVERLAY_FIELDS = {'schema_version', 'identity', 'homepage', 'services'}
PRODUCT_IDENTITY_FIELDS = {'site_name', 'brand_initial', 'updated'}
PRODUCT_HOMEPAGE_FIELDS = {
    'title', 'eyebrow', 'description', 'slides', 'about_heading',
    'about_description', 'statistics', 'news_heading', 'news_description',
    'partners_heading', 'partners', 'news',
}
PRODUCT_SERVICES_FIELDS = {
    'page_title', 'page_eyebrow', 'page_description', 'heading', 'description',
    'details_heading', 'records',
}
PRODUCT_SERVICES_COLLECTION_FIELDS = (
    PRODUCT_SERVICES_FIELDS - {'records'}
) | {'collection'}
PRODUCT_SERVICE_RECORD_FIELDS = {
    'id', 'title', 'description', 'action', 'details', 'audiences', 'duration',
    'channels', 'cost', 'owner', 'languages', 'agreement', 'steps',
    'requirements', 'documents', 'faq', 'updated', 'category',
    'related_service_ids', 'program_ids', 'regulation_ids', 'resource_ids',
}
REGISTERED_PAGE_RENDERERS = {
    'page-intro': ('page-intro', 'feedback'),
    'heavy-content': ('heavy-content', 'feedback'),
    'contact': ('contact', 'feedback'),
    'faq': ('page-intro', 'faq', 'contact-cta', 'feedback'),
    'form-template': ('form-template', 'feedback'),
    'error-state': ('error-state',),
    'service-catalog': ('page-intro', 'service-catalog', 'feedback'),
    'organization': ('organization', 'feedback'),
    'search-results': ('search-results', 'feedback'),
    'editorial-listing': ('editorial-listing', 'feedback'),
    'editorial-detail': ('editorial-detail', 'feedback'),
    'portfolio-listing': ('portfolio-listing', 'feedback'),
    'portfolio-detail': ('portfolio-detail', 'feedback'),
    'resource-listing': ('resource-listing', 'feedback'),
    'resource-detail': ('resource-detail', 'feedback'),
}
PRODUCT_RENDERER_REGISTRY = {
    'ministry': {
        'minister-profile': {
            'sections': ('minister-profile', 'feedback'),
            'module': 'minister-profile/renderer.py',
            'styles': ('minister-profile/minister-profile.css',),
        },
    },
    'authority': {
        'executive-profile': {
            'sections': ('executive-profile', 'feedback'),
            'module': 'executive-profile/renderer.py',
            'styles': ('executive-profile/executive-profile.css',),
        },
        'regulatory-listing': {
            'sections': ('regulatory-listing', 'feedback'),
            'module': 'regulatory/listing_renderer.py',
            'styles': ('regulatory/regulatory.css',),
        },
        'regulatory-detail': {
            'sections': ('regulatory-detail', 'feedback'),
            'module': 'regulatory/detail_renderer.py',
            'styles': ('regulatory/regulatory.css',),
        },
        'authority-home': {
            'sections': ('authority-home', 'feedback'),
            'module': 'home/renderer.py',
            'styles': (),
        },
    },
}
PRODUCT_DATA_ADAPTER_REGISTRY = {
    'authority': ('editorial/adapter.py', 'portfolio/adapter.py', 'resources/adapter.py', 'regulatory/adapter.py', 'home/adapter.py', 'search/adapter.py'),
}
PRODUCT_EXCLUSIVE_PAGE_REGISTRY = {'authority'}
ASSETS = ['components/accordion-new/accordion-new.css', 'components/select/select.css', 'components/textarea/textarea.css', 'components/file-upload/file-upload.css', 'templates/contact/contact.css', 'components/radio/radio.css', 'components/checkbox/checkbox-2.css', 'styles/composites/feedback.css', 'components/page-feedback/page-feedback.css', 'components/service-rating/service-rating.css', 'components/rating/rating.css', 'token.css', 'styles/base/global.css', 'styles/base/layout.css',
          'styles/base/accessibility.css', 'components/card/card.css',
          'components/navigation-header/navigation-header.css', 'components/footer/footer.css', 'components/digital-stamp/digital-stamp.css', 'components/service-card/service-card.css', 'components/avatar/avatar.css', 'components/tab/tab.css', 'components/breadcrumb/breadcrumb.css', 'components/divider/divider.css', 'components/list/list.css', 'components/table-of-contents/table-of-contents.css', 'templates/service/service.css', 'components/link/link.css', 'components/button/button.css', 'components/tag/tag.css',
          'components/label/label.css', 'components/text-input/text-input.css', 'components/input-affix/input-affix.css', 'components/progress-indicator/progress-indicator.css',
          'assets/fonts/fonts.css', 'templates/government/tokens.css', 'templates/government/composition.css', 'sections/page-intro/page-intro.css', 'sections/faq/faq.css', 'sections/contact-cta/contact-cta.css', 'sections/heavy-content/heavy-content.css', 'sections/organization/organization.css', 'sections/search-results/search-results.css', 'styles/composites/content-collections.css', 'templates/content/content.css', 'templates/form/form.css', 'templates/error/error.css']
SUPPORT_ASSETS = ['sections/faq/faq.js', 'sections/search-results/search-results.js', 'styles/composites/content-collections.js', 'sections/contact-cta/assets/contact.svg', 'components/table-of-contents/table-of-contents.js', 'components/tab/tab.js', 'components/progress-indicator/progress-indicator.js', 'components/file-upload/file-upload.js', 'templates/form/form.js', 'templates/contact/contact.js', 'components/select/select.css', 'components/textarea/textarea.css', 'components/file-upload/file-upload.css', 'components/radio/radio.css', 'components/checkbox/checkbox-2.css', 'styles/composites/feedback.js', 'styles/composites/feedback.css', 'components/page-feedback/page-feedback.css', 'components/service-rating/service-rating.css', 'components/rating/rating.css', 'assets/fonts/OFL.txt', 'assets/fonts/SOURCES.md', 'assets/templates/home/SOURCES.md', 'components/navigation-header/navigation-header.js', 'components/digital-stamp/digital-stamp.js', 'templates/government/home.js', 'templates/service/service.js', 'assets/templates/home/news.png'] + [f'assets/fonts/ibm-plex-arabic-{weight}.woff2' for weight in [400, 500, 600, 700]]

ASSETS.append('components/inline-alert/inline-alert.css')

# Keep the established ordered asset list; select only relevant owned sections/pages.
# Section-specific styles are selected without cross-template presentation dependencies.
STYLE_SECTIONS = {
    'components/avatar/avatar.css': {'minister-profile'},
    'sections/page-intro/page-intro.css': {'page-intro', 'contact', 'heavy-content', 'form-template', 'service-overview'},
    'sections/faq/faq.css': {'faq'},
    'sections/contact-cta/contact-cta.css': {'contact-cta', 'authority-home'},
    'sections/heavy-content/heavy-content.css': {'heavy-content'},
    'templates/contact/contact.css': {'contact'},
    'templates/content/content.css': {'heavy-content'},
    'styles/composites/content-collections.css': {'editorial-listing', 'editorial-detail', 'portfolio-listing', 'portfolio-detail', 'resource-listing', 'resource-detail'},
    'templates/form/form.css': {'form-template'},
    'templates/service/service.css': {'service-catalog', 'service-overview'},
    'templates/error/error.css': {'error-state'},
    'sections/organization/organization.css': {'organization'},
    'sections/search-results/search-results.css': {'search-results'},
    'components/inline-alert/inline-alert.css': {'regulatory-listing', 'regulatory-detail'},
}


def _resolve_product_path(product_root, value, key, kind):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'Product manifest requires a nonempty {key} path')
    path = (product_root / value).resolve()
    if path != product_root and product_root not in path.parents:
        raise ValueError(f'Product {key} path must stay inside the product directory')
    if kind == 'file' and not path.is_file():
        raise ValueError(f'Product {key} file does not exist: {value}')
    if kind == 'directory' and not path.is_dir():
        raise ValueError(f'Product {key} directory does not exist: {value}')
    return path


def _load_json_object(path, label):
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f'{label} must be a JSON object')
    return value


def _require_exact_fields(value, fields, label):
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError(f'{label} must define only: ' + ', '.join(sorted(fields)))


def _require_nonempty_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{label} must be nonempty text')


def _validate_text_list(value, label, minimum=1):
    if (
        not isinstance(value, list) or len(value) < minimum
        or not all(isinstance(item, str) and item.strip() for item in value)
    ):
        raise ValueError(f'{label} must be a list of nonempty text values')


def load_product_overlay(path):
    """Load a declarative product overlay with no execution or routing fields."""
    overlay = _load_json_object(Path(path), 'Product config overlay')
    _require_exact_fields(overlay, PRODUCT_OVERLAY_FIELDS, 'Product config overlay')
    if overlay['schema_version'] != 1:
        raise ValueError('Product config overlay schema_version must be 1')

    identity = overlay['identity']
    _require_exact_fields(identity, PRODUCT_IDENTITY_FIELDS, 'Product overlay identity')
    for field in PRODUCT_IDENTITY_FIELDS:
        _require_nonempty_text(identity[field], f'Product overlay identity.{field}')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', identity['updated']):
        raise ValueError('Product overlay identity.updated must use YYYY-MM-DD')

    homepage = overlay['homepage']
    _require_exact_fields(homepage, PRODUCT_HOMEPAGE_FIELDS, 'Product overlay homepage')
    homepage_text_fields = PRODUCT_HOMEPAGE_FIELDS - {
        'slides', 'statistics', 'partners', 'news',
    }
    for field in homepage_text_fields:
        _require_nonempty_text(homepage[field], f'Product overlay homepage.{field}')

    if not isinstance(homepage['slides'], list) or not homepage['slides']:
        raise ValueError('Product overlay homepage.slides must be a nonempty list')
    for slide in homepage['slides']:
        _require_exact_fields(slide, {'title', 'description'}, 'Product overlay homepage slide')
        for field in ('title', 'description'):
            _require_nonempty_text(slide[field], f'Product overlay homepage slide.{field}')

    if not isinstance(homepage['statistics'], list):
        raise ValueError('Product overlay homepage.statistics must be a list')
    for statistic in homepage['statistics']:
        _require_exact_fields(statistic, {'value', 'label'}, 'Product overlay homepage statistic')
        for field in ('value', 'label'):
            _require_nonempty_text(statistic[field], f'Product overlay homepage statistic.{field}')
    _validate_text_list(homepage['partners'], 'Product overlay homepage.partners', minimum=0)

    if not isinstance(homepage['news'], list):
        raise ValueError('Product overlay homepage.news must be a list')
    news_ids = set()
    for article in homepage['news']:
        _require_exact_fields(article, {'id', 'title', 'description'}, 'Product overlay homepage news item')
        for field in ('id', 'title', 'description'):
            _require_nonempty_text(article[field], f'Product overlay homepage news item.{field}')
        if not PRODUCT_PAGE_ID_PATTERN.fullmatch(article['id']) or article['id'] in news_ids:
            raise ValueError('Product overlay homepage news ids must be unique lowercase slugs')
        news_ids.add(article['id'])

    services = overlay['services']
    if not isinstance(services, dict) or frozenset(services) not in {
        frozenset(PRODUCT_SERVICES_FIELDS), frozenset(PRODUCT_SERVICES_COLLECTION_FIELDS)
    }:
        raise ValueError('Product overlay services fields do not match the contract')
    for field in PRODUCT_SERVICES_FIELDS - {'records'}:
        _require_nonempty_text(services[field], f'Product overlay services.{field}')
    if 'collection' in services:
        if not re.fullmatch(r'[a-z][a-z0-9-]*\.json', services['collection']):
            raise ValueError('Product overlay services.collection must be a safe JSON filename')
    else:
        _validate_product_service_records(services['records'])

    return overlay


def _validate_product_service_records(records):
    if not isinstance(records, list) or not records:
        raise ValueError('Product overlay services.records must be a nonempty list')
    service_ids = set()
    for service in records:
        _require_exact_fields(service, PRODUCT_SERVICE_RECORD_FIELDS, 'Product overlay service record')
        for field in PRODUCT_SERVICE_RECORD_FIELDS - {
            'audiences', 'steps', 'requirements', 'documents', 'faq',
            'related_service_ids', 'program_ids', 'regulation_ids', 'resource_ids',
        }:
            _require_nonempty_text(service[field], f'Product overlay service record.{field}')
        if not PRODUCT_PAGE_ID_PATTERN.fullmatch(service['id']) or service['id'] in service_ids:
            raise ValueError('Product overlay service ids must be unique lowercase slugs')
        service_ids.add(service['id'])
        for field in ('audiences', 'steps', 'requirements', 'documents'):
            _validate_text_list(service[field], f'Product overlay service record.{field}')
        for field in ('related_service_ids', 'program_ids', 'regulation_ids', 'resource_ids'):
            values = service[field]
            if (
                not isinstance(values, list) or len(values) != len(set(values))
                or any(not isinstance(value, str) or not PRODUCT_PAGE_ID_PATTERN.fullmatch(value) for value in values)
            ):
                raise ValueError(f'Product overlay service record.{field} must contain unique ids')
        if not isinstance(service['faq'], list) or not service['faq']:
            raise ValueError('Product overlay service record.faq must be a nonempty list')
        for item in service['faq']:
            _require_exact_fields(item, {'question', 'answer'}, 'Product overlay service FAQ item')
            for field in ('question', 'answer'):
                _require_nonempty_text(item[field], f'Product overlay service FAQ item.{field}')

def apply_product_overlay(data, overlay):
    """Apply the fixed A01 overlay contract to known data slots only."""
    identity = overlay['identity']
    homepage = overlay['homepage']
    services = overlay['services']
    data.update(identity)
    data['home'] = {
        field: homepage[field]
        for field in PRODUCT_HOMEPAGE_FIELDS
        if field not in {'title', 'eyebrow', 'description', 'news'}
    }
    data['news'] = homepage['news']
    data['services_heading'] = services['heading']
    data['services_description'] = services['description']
    data['details_heading'] = services['details_heading']
    data['services'] = services['records']

    pages_by_path = {page.get('path'): page for page in data.get('pages', [])}
    for route, values in (
        ('index.html', {
            'title': homepage['title'],
            'eyebrow': homepage['eyebrow'],
            'description': homepage['description'],
        }),
        ('services.html', {
            'title': services['page_title'],
            'eyebrow': services['page_eyebrow'],
            'description': services['page_description'],
        }),
    ):
        if route not in pages_by_path:
            raise ValueError(f'Product config overlay requires the shared {route} baseline')
        pages_by_path[route].update(values)
    return data


def _resolve_content_reference(content_root, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Product page requires a nonempty content reference')
    content_root = content_root.resolve()
    path = (content_root / value).resolve()
    if path != content_root and content_root not in path.parents:
        raise ValueError('Product content reference must stay inside demo_content')
    if path.suffix != '.json':
        raise ValueError('Product content reference must target a JSON file')
    if not path.is_file():
        raise ValueError(f'Product content reference does not exist: {value}')
    return path


def _resolve_page_reference(page_root, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Product page registry requires nonempty page references')
    page_root = page_root.resolve()
    path = (page_root / value).resolve()
    if path != page_root and page_root not in path.parents:
        raise ValueError('Product page reference must stay inside the pages directory')
    if path.suffix != '.json':
        raise ValueError('Product page reference must target a JSON file')
    if not path.is_file():
        raise ValueError(f'Product page reference does not exist: {value}')
    return path


def load_page_registry(registry_path, content_root, renderer_registry=None):
    """Load product page definitions and dispatch registered renderer IDs."""
    renderer_registry = REGISTERED_PAGE_RENDERERS if renderer_registry is None else renderer_registry
    registry_path = Path(registry_path)
    registry = _load_json_object(registry_path, 'Product page registry')
    if set(registry) != {'schema_version', 'pages'} or registry['schema_version'] != 1:
        raise ValueError('Product page registry must use schema_version 1 and define pages')
    if not isinstance(registry['pages'], list):
        raise ValueError('Product page registry pages must be a list')

    pages = []
    page_ids = set()
    routes = set()
    required = {'id', 'route', 'renderer', 'content'}
    reserved_content = {
        'path', 'route', 'renderer', 'renderer_id', 'sections', 'template',
        'template_id',
    }
    page_references = set()
    for reference in registry['pages']:
        page_path = _resolve_page_reference(registry_path.parent, reference)
        if page_path in page_references:
            raise ValueError(f'Duplicate product page reference: {reference}')
        page_references.add(page_path)
        entry = _load_json_object(page_path, f'Product page definition {reference}')
        if set(entry) != required:
            raise ValueError('Product page entries require only id, route, renderer and content')
        page_id = entry['id']
        route = entry['route']
        renderer_id = entry['renderer']
        if not isinstance(page_id, str) or not PRODUCT_PAGE_ID_PATTERN.fullmatch(page_id):
            raise ValueError('Product page id must be a lowercase slug')
        if page_id in page_ids:
            raise ValueError(f'Duplicate product page id: {page_id}')
        if not isinstance(route, str) or not PRODUCT_PAGE_ROUTE_PATTERN.fullmatch(route):
            raise ValueError('Product page route must be a safe flat HTML filename')
        if route in routes:
            raise ValueError(f'Duplicate product page route: {route}')
        if not isinstance(renderer_id, str) or renderer_id not in renderer_registry:
            raise ValueError(f'Unknown product page renderer: {renderer_id}')

        content_path = _resolve_content_reference(Path(content_root), entry['content'])
        content = _load_json_object(content_path, f'Product page content {entry["content"]}')
        overlap = reserved_content & set(content)
        if overlap:
            raise ValueError('Product page content cannot define execution fields: ' + ', '.join(sorted(overlap)))
        pages.append({**content, 'path': route, 'sections': list(renderer_registry[renderer_id])})
        page_ids.add(page_id)
        routes.add(route)
    return pages


def _merge_registered_pages(transitional_pages, registered_pages):
    pages = list(transitional_pages)
    positions = {page['path']: index for index, page in enumerate(pages)}
    for page in registered_pages:
        if page['path'] in positions:
            pages[positions[page['path']]] = page
        else:
            positions[page['path']] = len(pages)
            pages.append(page)
    return pages


def _apply_product_data_adapters(product_id, paths, data):
    """Run only code-owned product adapters from the trusted Python registry."""
    template_root = paths['templates'].resolve()
    for index, relative in enumerate(PRODUCT_DATA_ADAPTER_REGISTRY.get(product_id, ())):
        module_path = (template_root / relative).resolve()
        if template_root not in module_path.parents or not module_path.is_file() or module_path.suffix != '.py':
            raise ValueError('Product data adapter is missing or unsafe')
        specification = importlib.util.spec_from_file_location(
            f'{product_id}_data_adapter_{index}', module_path
        )
        if specification is None or specification.loader is None:
            raise ValueError('Product data adapter cannot be loaded')
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        if not callable(getattr(module, 'apply', None)):
            raise ValueError('Product data adapter must expose apply')
        data = module.apply(data, paths['demo_content'])
        if not isinstance(data, dict):
            raise ValueError('Product data adapter must return site data')
    return data


def product_output_path(product_id):
    if not isinstance(product_id, str) or not PRODUCT_ID_PATTERN.fullmatch(product_id):
        raise ValueError('Invalid product id; use a lowercase slug such as ministry')
    return ROOT / 'dist' / 'products' / product_id


def load_product(product_id):
    """Resolve a product manifest and normalize its transitional site data."""
    output = product_output_path(product_id)
    product_root = (PRODUCTS_ROOT / product_id).resolve()
    products_root = PRODUCTS_ROOT.resolve()
    if product_root == products_root or products_root not in product_root.parents:
        raise ValueError('Product directory must stay inside products')
    manifest_path = product_root / 'product.json'
    if not manifest_path.is_file():
        raise ValueError(f'Unknown product: {product_id}')

    manifest = _load_json_object(manifest_path, 'Product manifest')
    manifest_fields = set(manifest)
    allowed_manifest_fields = PRODUCT_MANIFEST_REQUIRED_FIELDS | PRODUCT_MANIFEST_OPTIONAL_FIELDS
    if not PRODUCT_MANIFEST_REQUIRED_FIELDS.issubset(manifest_fields) or not manifest_fields.issubset(allowed_manifest_fields):
        raise ValueError('Product manifest contains missing or unsupported fields')
    if manifest.get('schema_version') != 1:
        raise ValueError('Product manifest schema_version must be 1')
    if manifest.get('id') != product_id:
        raise ValueError('Product manifest id must match the selected product')
    if not isinstance(manifest.get('name'), str) or not manifest['name'].strip():
        raise ValueError('Product manifest requires a nonempty name')

    paths = {
        key: _resolve_product_path(product_root, manifest.get(key), key, kind)
        for key, kind in PRODUCT_PATHS.items()
    }
    if 'config_overlay' in manifest:
        paths['config_overlay'] = _resolve_product_path(
            product_root, manifest['config_overlay'], 'config_overlay', 'file'
        )
    source_value = manifest.get('source_config')
    if not isinstance(source_value, str) or not source_value.strip():
        raise ValueError('Product manifest requires a nonempty source_config path')
    source_config = (product_root / source_value).resolve()
    if source_config != ROOT and ROOT not in source_config.parents:
        raise ValueError('Product source_config must stay inside the repository')
    if source_config.suffix != '.json':
        raise ValueError('Product source_config must target a JSON file')
    if products_root in source_config.parents and product_root not in source_config.parents:
        raise ValueError('Product source_config cannot depend on another product')
    if not source_config.is_file():
        raise ValueError(f'Product source_config does not exist: {source_value}')

    navigation = _load_json_object(paths['navigation'], 'Product navigation')
    footer = _load_json_object(paths['footer'], 'Product footer')
    navigation_fields = set(navigation)
    if navigation_fields not in ({'navigation_label', 'navigation'}, {'navigation_label', 'navigation', 'search_route'}) or not isinstance(navigation['navigation'], list):
        raise ValueError('Product navigation must define navigation_label, navigation and optional search_route')
    if 'search_route' in navigation and (
        not isinstance(navigation['search_route'], str)
        or not PRODUCT_PAGE_ROUTE_PATTERN.fullmatch(navigation['search_route'])
    ):
        raise ValueError('Product search_route must be a safe flat HTML filename')
    required_footer = {'footer_navigation_label', 'footer_note', 'footer_groups', 'footer_tools'}
    if not required_footer.issubset(footer) or set(footer)-required_footer-{'footer_legal_links'} or not all(isinstance(footer[key], list) for key in ('footer_groups', 'footer_tools')):
        raise ValueError('Product footer must define footer label, note, groups and tools')
    if 'footer_legal_links' in footer and not isinstance(footer['footer_legal_links'], list):
        raise ValueError('Product footer legal links must be a list')

    data = _load_json_object(source_config, 'Product source configuration')
    if 'config_overlay' in paths:
        overlay = load_product_overlay(paths['config_overlay'])
        service_config = overlay['services']
        if 'collection' in service_config:
            collection_path = _resolve_content_reference(paths['demo_content'], service_config['collection'])
            collection = _load_json_object(collection_path, 'Product services collection')
            if set(collection) != {'schema_version', 'services'} or collection['schema_version'] != 1:
                raise ValueError('Product services collection must use schema_version 1 and define services')
            _validate_product_service_records(collection['services'])
            overlay['services'] = {
                **{key: value for key, value in service_config.items() if key != 'collection'},
                'records': collection['services'],
            }
            paths['services'] = collection_path
        data = apply_product_overlay(data, overlay)
    data.update(navigation)
    data.update(footer)
    renderer_registry = dict(REGISTERED_PAGE_RENDERERS)
    renderer_registry.update({
        renderer_id: specification['sections']
        for renderer_id, specification in PRODUCT_RENDERER_REGISTRY.get(product_id, {}).items()
    })
    registered_pages = load_page_registry(paths['pages'], paths['demo_content'], renderer_registry)
    data['pages'] = registered_pages if product_id in PRODUCT_EXCLUSIVE_PAGE_REGISTRY else _merge_registered_pages(data.get('pages', []), registered_pages)
    data = _apply_product_data_adapters(product_id, paths, data)
    return {
        'manifest': manifest,
        'root': product_root,
        'paths': paths,
        'source_config': source_config,
        'output': output,
        'data': data,
        'registered_pages': registered_pages,
    }


def _load_product_renderer_handlers(product_id, paths):
    handlers = {}
    template_root = paths['templates'].resolve()
    for renderer_id, specification in PRODUCT_RENDERER_REGISTRY.get(product_id, {}).items():
        module_path = (template_root / specification['module']).resolve()
        if template_root not in module_path.parents or not module_path.is_file():
            raise ValueError(f'Product renderer module is missing or unsafe: {renderer_id}')
        module_spec = importlib.util.spec_from_file_location(
            f'{product_id}_{renderer_id.replace("-", "_")}_renderer',
            module_path,
        )
        if module_spec is None or module_spec.loader is None:
            raise ValueError(f'Product renderer module cannot be loaded: {renderer_id}')
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        if not callable(getattr(module, 'validate', None)) or not callable(getattr(module, 'render', None)):
            raise ValueError(f'Product renderer must expose validate and render: {renderer_id}')

        style_sources = []
        style_hrefs = []
        for relative in specification.get('styles', ()):
            source = (template_root / relative).resolve()
            if template_root not in source.parents or not source.is_file() or source.suffix != '.css':
                raise ValueError(f'Product renderer stylesheet is missing or unsafe: {renderer_id}')
            destination = Path('assets') / 'products' / product_id / relative
            style_sources.append((source, destination))
            style_hrefs.append(destination.as_posix())

        asset_root = paths['assets']
        asset_prefix = f'assets/products/{product_id}/'
        handlers[renderer_id] = {
            'validate': lambda page, validator=module.validate: validator(page, asset_root),
            'render': lambda page, render_markup, renderer=module.render: renderer(
                page, render_markup, asset_root, asset_prefix
            ),
            'styles': tuple(style_hrefs),
            'style_sources': tuple(style_sources),
        }
    return handlers


def page_styles(page, product_renderers=None):
    sections = set(page['sections'])
    styles = [asset for asset in ASSETS if asset not in STYLE_SECTIONS or sections & STYLE_SECTIONS[asset]]
    for section in page['sections']:
        if product_renderers and section in product_renderers:
            styles.extend(product_renderers[section]['styles'])
    return styles


def page_scripts(page):
    sections = set(page['sections'])
    scripts = []
    if 'contact' in sections:
        scripts += ['components/file-upload/file-upload.js', 'templates/contact/contact.js']
    if 'form-template' in sections:
        scripts += ['components/progress-indicator/progress-indicator.js', 'templates/form/form.js']
    if sections & {'service-overview', 'service-catalog'}:
        if 'service-overview' in sections:
            scripts.append('components/tab/tab.js')
        scripts.append('templates/service/service.js')
    if 'search-results' in sections:
        scripts.append('sections/search-results/search-results.js')
    if sections & {'portfolio-listing', 'resource-listing', 'regulatory-listing'}:
        scripts.append('styles/composites/content-collections.js')
    return scripts


def render(name, values, slots=()):
    if name == 'components/breadcrumb/two-level.html':
        values = {'breadcrumb_markup': render_two_level(values, render)}
        slots = ('breadcrumb_markup',)
    source = (ROOT / name).read_text()
    def replace(match):
        key = match[1]
        value = str(values[key])
        return value if key in slots else html.escape(value, quote=True)
    return re.sub(r'\{\{([a-z_]+)\}\}', replace, source)


def validate_record_relationships(data):
    """Resolve cross-collection IDs after all code-owned adapters have run."""
    collections=('portfolio_records','resource_records','editorial_records','regulatory_records')
    if not all(key in data for key in collections):
        return
    services={x['id'] for x in data['services']}
    portfolio={x['id'] for x in data['portfolio_records']}
    resources={x['id'] for x in data['resource_records']}
    news={x['id'] for x in data['editorial_records']}
    regulations={x['id'] for x in data['regulatory_records']}
    for service in data['services']:
        for field,targets in (('program_ids',portfolio),('resource_ids',resources),('regulation_ids',regulations),('related_service_ids',services)):
            if any(value not in targets for value in service.get(field,[])):
                raise ValueError('Service relationship does not resolve: '+field)
    for item in data['portfolio_records']:
        for field,targets in (('service_ids',services),('resource_ids',resources),('news_ids',news)):
            if any(value not in targets for value in item[field]):
                raise ValueError('Portfolio relationship does not resolve: '+field)
    for item in data['regulatory_records']:
        if any(value not in resources for value in item['resource_ids']) or any(value not in services for value in item['service_ids']):
            raise ValueError('Regulatory relationship does not resolve')


def validate(data, product_renderers=None):
    product_renderers = product_renderers or {}
    known_product_sections = set(product_renderers)
    for registry in PRODUCT_RENDERER_REGISTRY.values():
        known_product_sections.update(registry)
    validate_stamp(data.get('digital_stamp', {}))
    if data['dir'] not in ('rtl', 'ltr') or not re.fullmatch(r'[a-z]{2,3}(?:-[A-Za-z0-9]+)*', data['lang']):
        raise ValueError('Invalid language or direction')
    paths = [page['path'] for page in data['pages']]
    if len(set(paths)) != len(paths) or any(not re.fullmatch(r'[a-z][a-z0-9-]*\.html', p) for p in paths):
        raise ValueError('Page paths must be unique flat HTML filenames')
    if not {'index.html', 'services.html'}.issubset(paths):
        raise ValueError('This archetype requires index.html and services.html')
    if data.get('search_route') and data['search_route'] not in paths:
        raise ValueError('Product search_route must target a generated page')
    validate_services(data['services'])
    if data.get('editorial_records') is not None:
        validate_editorial_records(data['editorial_records'])
    if data.get('portfolio_records') is not None:
        validate_portfolio_records(data['portfolio_records'], data['services'])
    if data.get('resource_records') is not None:
        validate_resource_records(data['resource_records'])
    validate_record_relationships(data)
    for contact_page_data in (page for page in data['pages'] if 'contact' in page['sections']):
        validate_contact(contact_page_data.get('contact', data.get('contact')))
    ids = [service['id'] for service in data['services']]
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r'[a-z][a-z0-9-]*', i) for i in ids):
        raise ValueError('Service IDs must be unique slugs')
    generated = [detail_url(service) for service in data['services']]
    if set(generated) & set(paths):
        raise ValueError('Service paths collide with configured pages')
    if any(item['href'].partition('#')[0] not in paths for item in data['navigation'] + [child for item in data['navigation'] for child in item.get('children', [])] + [link for group in data['footer_groups'] + data.get('footer_tools', []) for link in group['links']] + data.get('footer_legal_links', [])):
        raise ValueError('Navigation must target generated pages')
    for page in data['pages']:
        sections = page['sections']
        for section in sections:
            if section in product_renderers:
                product_renderers[section]['validate'](page)
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
        if 'organization' in sections:
            validate_organization(page)
        if 'search-results' in sections:
            validate_search_results(page)
        if 'editorial-listing' in sections or 'editorial-detail' in sections:
            if not isinstance(page.get('records') if 'editorial-listing' in sections else page.get('record'), (list, dict)):
                raise ValueError('Editorial pages require registered records')
        if 'portfolio-listing' in sections or 'portfolio-detail' in sections:
            if not isinstance(page.get('records') if 'portfolio-listing' in sections else page.get('record'), (list, dict)):
                raise ValueError('Portfolio pages require registered records')
        if 'resource-listing' in sections or 'resource-detail' in sections:
            if not isinstance(page.get('records') if 'resource-listing' in sections else page.get('record'), (list, dict)):
                raise ValueError('Resource pages require registered records')
        if page.get('robots') not in (None, 'noindex,follow'):
            raise ValueError('Unsupported robots directive')
        intro_sections = ('page-intro', 'hero', 'contact', 'heavy-content', 'form-template', 'error-state', 'organization', 'search-results', 'editorial-listing', 'editorial-detail', 'portfolio-listing', 'portfolio-detail', 'resource-listing', 'resource-detail', *known_product_sections)
        if sum(sections.count(name) for name in intro_sections) != 1 or len(set(sections)) != len(sections):
            raise ValueError('Exactly one intro and no duplicate sections are allowed')
        if 'services' in sections and 'home-services' in sections:
            raise ValueError('Only one services presentation is allowed per page')
        if set(sections) - ({'page-intro', 'services', 'service-details', 'hero', 'about', 'home-services', 'news', 'partners', 'feedback', 'content', 'service-catalog', 'contact', 'faq', 'contact-cta', 'heavy-content', 'form-template', 'error-state', 'organization', 'search-results', 'editorial-listing', 'editorial-detail', 'portfolio-listing', 'portfolio-detail', 'resource-listing', 'resource-detail'} | known_product_sections):
            raise ValueError('Unknown section')


def build(config, output, product_renderers=None):
    product_renderers = product_renderers or {}
    data = config if isinstance(config, dict) else json.loads(Path(config).read_text())
    validate(data, product_renderers)
    output = Path(output)
    pages = {}
    service_pages = [dict(path=detail_url(service), title=service['title'], description=service['description'], sections=['service-overview','feedback'], service_id=service['id'], feedback_statistics=service.get('feedback_statistics')) for service in data['services']]
    for page in data['pages'] + service_pages:
        section_routes = {'editorial-detail':'news.html','portfolio-detail':'programs.html','resource-detail':'knowledge.html','regulatory-detail':'regulations.html'}
        current_path = 'services.html' if page.get('service_id') else next((route for section,route in section_routes.items() if section in page['sections']), page['path'])
        navigation_items = []
        for index, item in enumerate(data['navigation']):
            if item.get('children'):
                children = [dict(label=item['label'], href=item['href']), *item['children']]
                submenu = ''.join(render('components/navigation-header/submenu-item.html', {**child, 'current': ' aria-current="page"' if child['href'] == page['path'] else ''}, ('current',)) for child in children)
                navigation_items.append(render('components/navigation-header/dropdown.html', {'label': item['label'], 'panel_id': f'primary-submenu-{index}', 'current_section': str(any(child['href'].partition('#')[0] == current_path for child in children)).lower(), 'items': submenu, 'chevron': render('components/navigation-header/icon.html', {'class_name': 'nav-header__chevron', 'asset_prefix': 'components/navigation-header/assets/', 'default_asset': 'menu-imgElements7.svg', 'white_asset': 'menu-imgElements1.svg', 'disabled_asset': 'menu-imgElements4.svg'})}, ('items', 'chevron')))
            else:
                navigation_items.append(render('components/navigation-header/item.html', {**item, 'current': ' aria-current="page"' if item['href'] == current_path else ''}, ('current',)))
        navigation = '\n'.join(navigation_items)
        search_links = ''.join('<li><a class="link link--inline" href="{}">{}</a></li>'.format(html.escape(detail_url(service)), html.escape(service['title'])) for service in data['services'])
        if data.get('search_route'):
            search_action = '<a class="nav-header__action" href="{}" aria-label="البحث في الموقع"><svg class="nav-header__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/></svg><span class="nav-header__label">البحث</span></a>'.format(html.escape(data['search_route'], quote=True))
            search_dialog = ''
        else:
            search_action = '<button class="nav-header__action site-search-trigger" type="button" aria-haspopup="dialog" aria-expanded="false" aria-label="البحث" hidden><svg class="nav-header__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="10" cy="10" r="7"/><path d="m15 15 6 6"/></svg><span class="nav-header__label">البحث</span></button>'
            search_dialog = render('partials/site-header/search-dialog.html', {'search_links': search_links}, ('search_links',))
        footer_component = render_footer({
            'theme': 'dark', 'groups': data['footer_groups'],
            'tools': data.get('footer_tools', []),
            'legal_links': data.get('footer_legal_links', [{'label': 'الخصوصية وشروط الاستخدام', 'href': 'about.html#privacy'}, {'label': 'إمكانية الوصول', 'href': 'about.html#accessibility'}]),
            'copyright': data['footer_note'], 'updated': 'آخر تحديث للقالب: ' + data['updated'],
            'logos': [{'label': data['site_name']}],
        }, render)
        common = {**data, 'navigation': navigation, 'search_action': search_action, 'search_dialog': search_dialog, 'footer_component': footer_component}
        sections = []
        for section in page['sections']:
            if section == 'contact':
                sections.append(contact_page(page.get('contact', data['contact']), render))
            elif section == 'service-catalog':
                sections.append(catalogue(data['services'], render))
            elif section == 'service-overview':
                service = next(s for s in data['services'] if s['id'] == page['service_id'])
                portfolio={x['id']:{'title':x['title'],'route':('program-' if x['kind']=='program' else 'initiative-')+x['id']+'.html'} for x in data.get('portfolio_records',[])}
                regulatory={x['id']:{'title':x['title'],'route':'regulation-'+x['id']+'.html'} for x in data.get('regulatory_records',[])}
                resources={x['id']:{'title':x['title'],'route':'resource-'+x['id']+'.html'} for x in data.get('resource_records',[])}
                sections.append(overview(service, data['services'], render, 'contact.html' if any(p['path']=='contact.html' for p in data['pages']) else None, {'portfolio':portfolio,'regulatory':regulatory,'resources':resources}))
            elif section == 'heavy-content':
                sections.append(render_heavy_content(page, render))
            elif section == 'form-template':
                sections.append(render_form_template(page, render))
            elif section == 'error-state':
                sections.append(render_error_state(page, render))
            elif section == 'organization':
                sections.append(render_organization(page, render))
            elif section == 'search-results':
                sections.append(render_search_results(page, render))
            elif section == 'editorial-listing':
                sections.append(render_editorial_listing(page, render))
            elif section == 'editorial-detail':
                sections.append(render_editorial_detail(page, render))
            elif section == 'portfolio-listing':
                sections.append(render_portfolio_listing(page, render))
            elif section == 'portfolio-detail':
                sections.append(render_portfolio_detail(page, render))
            elif section == 'resource-listing':
                sections.append(render_resource_listing(page, render))
            elif section == 'resource-detail':
                sections.append(render_resource_detail(page, render))
            elif section == 'page-intro':
                sections.append(render_page_intro(page, render))
            elif section in product_renderers:
                sections.append(product_renderers[section]['render'](page, render))
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
                sections.append(render('sections/feedback/template.html', {'updated': page.get('updated', data['updated']), 'component': render_feedback('service' if page.get('service_id') else 'page', page.get('service_id', page['path']), render, page.get('feedback_statistics'))}, ('component',)))
            elif section == 'content':
                items = ''.join(render('sections/content/item.html', item) for item in page['items'])
                sections.append(render('sections/content/template.html', {'items': items}, ('items',)))
        metadata = []
        if page.get('robots'):
            metadata.append('<meta name="robots" content="{}">'.format(html.escape(page['robots'], quote=True)))
        if page.get('canonical'):
            metadata.append('<link rel="canonical" href="{}">'.format(html.escape(page['canonical'], quote=True)))
        values = {**data, **page,
                  'head_metadata': '\n  '.join(metadata),
                  'digital_stamp': render_stamp(data.get('digital_stamp', {}), render, data['dir']),
                  'header': render('partials/site-header/template.html', common, ('navigation', 'search_action', 'search_dialog', 'footer_groups')),
                  'footer': render('partials/site-footer/template.html', common, ('footer_component',)),
                  'content': '\n'.join(sections),
                  'styles': '\n'.join(f'  <link rel="stylesheet" href="{asset}">' for asset in page_styles(page, product_renderers)),
                  'scripts': '\n'.join(f'<script src="{asset}" defer></script>' for asset in page_scripts(page))}
        pages[page['path']] = render('templates/government/page.html', values, ('head_metadata', 'digital_stamp', 'header', 'footer', 'content', 'styles', 'scripts'))
    output.mkdir(parents=True, exist_ok=True)
    for asset in dict.fromkeys(ASSETS + SUPPORT_ASSETS + [str(p.relative_to(ROOT)) for component in ('navigation-header', 'footer', 'digital-stamp', 'service-card', 'service-rating', 'page-feedback', 'select') for p in (ROOT / 'components' / component / 'assets').glob('*.svg')] + [str(p.relative_to(ROOT)) for folder in ('service', 'contact', 'error') for p in (ROOT / 'templates' / folder / 'assets').glob('*') if p.suffix in ('.svg', '.png')]):
        target = output / asset
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / asset, target)
    core = (ROOT / 'scripts/core/index.js').read_text().replace('export function initCore', 'function initCore')
    (output / 'sections/faq/faq.runtime.js').write_text('(function () {\n' + core + '\n' + (ROOT / 'sections/faq/faq.js').read_text() + '\n})();\n')
    # ES module source remains canonical; this generated IIFE supports file:// previews.
    for component, initializer in [('navigation-header', 'initNavigationHeaders'), ('digital-stamp', 'initDigitalStamps')]:
        source = (ROOT / 'components' / component / (component + '.js')).read_text()
        runtime = '(function () {\n' + source.replace('export function ' + initializer, 'function ' + initializer) + '\n' + initializer + '();\n})();\n'
        (output / 'components' / component / (component + '.runtime.js')).write_text(runtime)
    for name, content in pages.items():
        (output / name).write_text(content)
    return list(pages)


def build_product(product_id, output=None):
    """Build a selected product through the existing shared rendering pipeline."""
    product = load_product(product_id)
    output = Path(output) if output is not None else product['output']
    product_renderers = _load_product_renderer_handlers(product_id, product['paths'])
    pages = build(product['data'], output, product_renderers)
    for handler in product_renderers.values():
        for source, destination in handler['style_sources']:
            target = output / destination
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    asset_root = product['paths']['assets']
    for source in asset_root.rglob('*'):
        if not source.is_file() or source.name.startswith('.'):
            continue
        relative = source.relative_to(asset_root)
        target = output / 'assets' / 'products' / product_id / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    return pages


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument('--product', help='Product id from products/<id>/product.json')
    source.add_argument('--config', type=Path, help='Existing single-site JSON configuration')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.product:
        try:
            pages = build_product(args.product, args.output)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            parser.error(str(error))
    else:
        config = args.config or ROOT / 'site/government.json'
        output = args.output or ROOT / 'dist/government'
        pages = build(config, output)
    print('Built: ' + ', '.join(pages))
