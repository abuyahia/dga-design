import copy
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
PRODUCT=ROOT/'products/authority'
SPEC=importlib.util.spec_from_file_location('authority_v1_builder',ROOT/'scripts/build_site.py')
BUILDER=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(BUILDER)

class Document(HTMLParser):
    def __init__(self): super().__init__(); self.h1=0; self.ids=set(); self.hrefs=[]; self.articles=0
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        if tag=='h1': self.h1+=1
        if tag=='article': self.articles+=1
        if values.get('id'): self.ids.add(values['id'])
        if values.get('href'): self.hrefs.append(values['href'])

class AuthorityV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(); cls.output=Path(cls.temp.name)/'authority'
        cls.pages=BUILDER.build_product('authority',cls.output); cls.product=BUILDER.load_product('authority')['data']
    @classmethod
    def tearDownClass(cls): cls.temp.cleanup()

    def test_a11_a13_services_have_one_source_catalogue_and_five_details(self):
        services=self.product['services']; self.assertEqual(5,len(services)); self.assertEqual(5,len({x['id'] for x in services}))
        overlay=(PRODUCT/'content/demo/product-overlay.json').read_text(); self.assertIn('"collection": "services.json"',overlay); self.assertNotIn('"records"',overlay)
        catalogue=(self.output/'services.html').read_text(); self.assertEqual(5,catalogue.count('data-service-card')); self.assertIn('catalog-category',catalogue); self.assertIn('data-catalog-empty',catalogue)
        for item in services:
            path='service-'+item['id']+'.html'; markup=(self.output/path).read_text(); doc=Document(); doc.feed(markup)
            self.assertEqual(1,doc.h1); self.assertIn('هذه معاينة',markup); self.assertIn('service-faq',doc.ids); self.assertIn(path,self.pages)

    def test_a14_a16_editorial_one_collection_drives_list_and_details(self):
        records=self.product['editorial_records']; self.assertEqual(4,len(records))
        listing=(self.output/'news.html').read_text(); positions=[listing.index(x['title']) for x in sorted(records,key=lambda x:x['published'],reverse=True)]; self.assertEqual(positions,sorted(positions))
        for item in records:
            markup=(self.output/('news-'+item['id']+'.html')).read_text(); self.assertIn('<article class="record-detail editorial-detail">',markup); self.assertIn('<time datetime="'+item['published']+'">',markup); self.assertIn('rel="canonical"',markup)

    def test_a17_a22_portfolio_and_resources_cover_routes_filters_and_downloads(self):
        self.assertEqual(4,len(self.product['portfolio_records'])); self.assertEqual(5,len(self.product['resource_records']))
        programs=(self.output/'programs.html').read_text(); knowledge=(self.output/'knowledge.html').read_text()
        self.assertIn('data-filter-kind',programs); self.assertIn('data-filter-status',programs); self.assertIn('data-filter-empty',programs)
        self.assertIn('data-filter-query',knowledge); self.assertIn('data-filter-topic',knowledge); self.assertIn('data-filter-empty',knowledge)
        for item in self.product['portfolio_records']:
            route=('program-' if item['kind']=='program' else 'initiative-')+item['id']+'.html'; self.assertIn(route,self.pages)
        for item in self.product['resource_records']:
            self.assertIn('resource-'+item['id']+'.html',self.pages); self.assertTrue((self.output/item['destination']).is_file())

    def test_a23_a25_regulatory_contract_status_and_routes(self):
        records=self.product['regulatory_records']; self.assertEqual(3,len(records)); listing=(self.output/'regulations.html').read_text()
        self.assertIn('مسودة عرض غير نافذة',listing); self.assertIn('سارية داخل المعاينة فقط',listing); self.assertIn('value="obsolete"',listing)
        for item in records:
            markup=(self.output/('regulation-'+item['id']+'.html')).read_text(); self.assertIn(item['disclaimer'],markup); self.assertIn('<bdi>'+item['number']+'</bdi>',markup); self.assertIn('rel="canonical"',markup)
        path=PRODUCT/'templates/regulatory/validator.py'; spec=importlib.util.spec_from_file_location('regulatory_contract_test',path); validator=importlib.util.module_from_spec(spec); spec.loader.exec_module(validator)
        cyclic=copy.deepcopy(records[:2]); cyclic[0]['id']='version-a'; cyclic[1]['id']='version-b'; cyclic[0]['supersedes_id']='version-b'; cyclic[1]['supersedes_id']='version-a'
        with self.assertRaisesRegex(ValueError,'cycle'): validator.validate_records(cyclic)

    def test_a26_home_is_record_driven_and_profiles_share_one_renderer(self):
        markup=(self.output/'index.html').read_text(); doc=Document(); doc.feed(markup); self.assertEqual(1,doc.h1)
        order=[markup.index('id="home-'+x+'"') for x in ('regulations','resources','portfolio','news')]; self.assertEqual(order,sorted(order))
        path=PRODUCT/'templates/home/renderer.py'; spec=importlib.util.spec_from_file_location('home_policy',path); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        self.assertEqual('hero',module.section_order('regulatory')[0]); self.assertIn('portfolio',module.section_order('enablement')); self.assertEqual('portfolio',module.section_order('development')[1])
        product=BUILDER.load_product('authority'); handlers=BUILDER._load_product_renderer_handlers('authority',product['paths']); home=next(x for x in product['data']['pages'] if x['path']=='index.html')
        for profile,expected in (('enablement',('id="services"','id="home-portfolio"')),('development',('id="home-portfolio"','توجهات الاستراتيجية'))):
            fixture=copy.deepcopy(home); fixture['profile']=profile; rendered=handlers['authority-home']['render'](fixture,BUILDER.render)
            self.assertLess(rendered.index(expected[0]),rendered.index(expected[1]))

    def test_a27_relationships_resolve_and_generated_link_graph_is_closed(self):
        invalid=copy.deepcopy(self.product); invalid['services'][0]['resource_ids']=['missing-resource']
        with self.assertRaisesRegex(ValueError,'does not resolve'): BUILDER.validate_record_relationships(invalid)
        html_paths={x.name for x in self.output.glob('*.html')}
        for path in self.output.glob('*.html'):
            doc=Document(); doc.feed(path.read_text()); self.assertEqual(1,doc.h1,path.name)
            for href in doc.hrefs:
                if href.startswith(('https://','mailto:','tel:')): continue
                target,_,fragment=href.partition('#'); target_name=target or path.name
                if target_name.startswith('assets/') or not target_name.endswith('.html'):
                    self.assertTrue((self.output/target_name).is_file(),(path.name,href)); continue
                self.assertIn(target_name,html_paths,(path.name,href))
                if fragment:
                    target_doc=Document(); target_doc.feed((self.output/target_name).read_text()); self.assertIn(fragment,target_doc.ids,(path.name,href))

    def test_no_ministry_runtime_dependency_or_json_selected_python(self):
        files=[*PRODUCT.rglob('*.py'),*PRODUCT.rglob('*.json')]
        source='\n'.join(path.read_text() for path in files)
        self.assertNotIn('products/ministry/',source); self.assertNotIn('../ministry',source)
        def keys(value):
            if isinstance(value,dict):
                for key,item in value.items(): yield key; yield from keys(item)
            elif isinstance(value,list):
                for item in value: yield from keys(item)
        for path in PRODUCT.rglob('*.json'):
            names=set(keys(json.loads(path.read_text())))
            self.assertNotIn('module',names); self.assertNotIn('executable',names)

if __name__=='__main__': unittest.main()
