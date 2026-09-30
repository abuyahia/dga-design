"""Record-driven Authority Home composition with profile ordering policy."""
import html
try:
    from scripts.service_markup import service_card
except ImportError:
    from service_markup import service_card

PROFILES={
 'regulatory':('hero','services','regulations','resources','portfolio','news','about','contact'),
 'enablement':('hero','services','portfolio','resources','news','about','contact'),
 'development':('hero','portfolio','strategy','resources','services','news','about','contact'),
}
COLLECTIONS={'services':('services_records','featured_service_ids'),'regulations':('regulatory_records','featured_regulation_ids'),'resources':('resource_records','featured_resource_ids'),'portfolio':('portfolio_records','featured_portfolio_ids'),'news':('editorial_records','featured_news_ids')}

def section_order(profile):
    if profile not in PROFILES: raise ValueError('Authority Home profile is unsupported')
    return PROFILES[profile]
def _resolve(page,section):
    records_key,ids_key=COLLECTIONS[section]; records={x['id']:x for x in page[records_key]}; ids=page[ids_key]
    if len(ids)!=len(set(ids)) or any(x not in records for x in ids): raise ValueError('Authority Home featured IDs must be unique and resolve')
    return [records[x] for x in ids]
def validate(page,asset_root):
    required={'title','description','updated','profile','featured_service_ids','featured_regulation_ids','featured_resource_ids','featured_portfolio_ids','featured_news_ids','about_title','about_summary',*{x for pair in COLLECTIONS.values() for x in pair[:1]}}
    if any(key not in page for key in required): raise ValueError('Authority Home fields are incomplete')
    section_order(page['profile'])
    for section in COLLECTIONS:_resolve(page,section)
def _route(section,item):
    if section=='regulations':return 'regulation-'+item['id']+'.html'
    if section=='resources':return 'resource-'+item['id']+'.html'
    if section=='portfolio':return ('program-' if item['kind']=='program' else 'initiative-')+item['id']+'.html'
    return 'news-'+item['id']+'.html'
def _record_section(section,title,listing,items):
    cards=''.join('<article class="card"><h3 class="card__title"><a class="link link--inline" href="{}">{}</a></h3><p>{}</p></article>'.format(_route(section,x),html.escape(x['title']),html.escape(x.get('summary',''))) for x in items)
    return '<section class="home-section" id="home-{}"><div class="ds-container ds-stack"><div class="section-heading"><h2>{}</h2><a class="btn btn--secondary-outline" href="{}">عرض الكل</a></div><div class="ds-grid">{}</div></div></section>'.format(section,title,listing,cards)
def render(page,render_markup,asset_root,asset_prefix):
    validate(page,asset_root); pieces={}
    pieces['hero']=render_markup('sections/hero/template.html',{**page,'dots':''},('dots',))
    service_cards=''.join(service_card(x,render_markup,'home-') for x in _resolve(page,'services'))
    pieces['services']=render_markup('sections/home-services/template.html',{'heading':'خدمات مميزة','description':'مسارات تجريبية غير تشغيلية من سجل الخدمات الموحد.','cards':service_cards},('cards',))
    pieces['regulations']=_record_section('regulations','أحدث التنظيمات التجريبية','regulations.html',_resolve(page,'regulations'))
    pieces['resources']=_record_section('resources','الأدلة والمعرفة','knowledge.html',_resolve(page,'resources'))
    pieces['portfolio']=_record_section('portfolio','البرامج والمبادرات','programs.html',_resolve(page,'portfolio'))
    pieces['news']=_record_section('news','أخبار العرض التجريبي','news.html',_resolve(page,'news'))
    pieces['strategy']='<section class="home-section"><div class="ds-container"><h2>توجهات الاستراتيجية</h2><p>التمكين، والوضوح، والقياس المسؤول ضمن سيناريو العرض.</p><a class="link" href="strategy.html">عرض الاستراتيجية</a></div></section>'
    pieces['about']=render_markup('sections/about/template.html',{'heading':page['about_title'],'description':page['about_summary'],'statistics':''},('statistics',))
    pieces['contact']=render_markup('sections/contact-cta/template.html',{'title':'هل تحتاج إلى توضيح؟','description':'تواصل عبر نموذج العرض الذي لا يرسل بيانات.','href':'contact.html','label':'تواصل معنا'})
    return '\n'.join(pieces[x] for x in section_order(page['profile']))
