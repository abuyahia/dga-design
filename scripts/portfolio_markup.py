"""Shared portfolio contract and program/initiative compositions."""
import html
import re
from datetime import date
try:
    from scripts.content_markup import validate_content_blocks, render_content_blocks
    from scripts.page_intro_markup import render_page_intro
except ImportError:
    from content_markup import validate_content_blocks, render_content_blocks
    from page_intro_markup import render_page_intro

SLUG=re.compile(r'[a-z][a-z0-9-]*')
KINDS={'program':'برنامج','initiative':'مبادرة'}
STATUSES={'active':'جارٍ في سياق العرض','pilot':'مرحلة تجريبية','planned':'مخطط','complete':'مكتمل تجريبيًا'}
FIELDS={'id','kind','title','summary','status','owner','start_date','end_date','updated','objectives','outputs','body','metrics','service_ids','resource_ids','news_ids'}
def route(item): return ('program-' if item['kind']=='program' else 'initiative-')+item['id']+'.html'

def validate_portfolio_records(records, services=()):
    if not isinstance(records,list) or not records: raise ValueError('Portfolio records must be nonempty')
    ids=[]; service_ids={x['id'] for x in services}
    for item in records:
        if not isinstance(item,dict) or set(item)!=FIELDS: raise ValueError('Portfolio fields do not match contract')
        if not SLUG.fullmatch(item.get('id','')): raise ValueError('Portfolio IDs must be slugs')
        ids.append(item['id'])
        if item['kind'] not in KINDS or item['status'] not in STATUSES: raise ValueError('Portfolio kind/status is unsupported')
        for key in ('title','summary','owner'):
            if not isinstance(item[key],str) or not item[key].strip(): raise ValueError('Portfolio text is required: '+key)
        for key in ('start_date','end_date','updated'):
            if item[key] is not None:
                try: date.fromisoformat(item[key])
                except (TypeError,ValueError): raise ValueError('Portfolio dates must be ISO dates')
        if item['start_date'] and item['end_date'] and item['start_date']>item['end_date']: raise ValueError('Portfolio dates are out of order')
        for key in ('objectives','outputs'):
            if not isinstance(item[key],list) or not item[key] or any(not isinstance(x,str) or not x for x in item[key]): raise ValueError('Portfolio lists are required')
        validate_content_blocks(item['body'])
        if not isinstance(item['metrics'],list): raise ValueError('Portfolio metrics must be a list')
        for metric in item['metrics']:
            if set(metric)!={'label','value','source','date'} or not all(isinstance(metric[x],str) and metric[x] for x in metric): raise ValueError('Portfolio metrics require label/value/source/date')
            try: date.fromisoformat(metric['date'])
            except ValueError: raise ValueError('Portfolio metric dates must be ISO')
        for key in ('service_ids','resource_ids','news_ids'):
            if not isinstance(item[key],list) or len(item[key])!=len(set(item[key])) or any(not SLUG.fullmatch(x) for x in item[key]): raise ValueError('Portfolio relations must be unique slug lists')
        if any(x not in service_ids for x in item['service_ids']): raise ValueError('Portfolio service IDs must resolve')
    if len(ids)!=len(set(ids)): raise ValueError('Portfolio IDs/routes must be unique')

def _card(item):
    return '<article class="card record-card" data-record data-kind="{}" data-status="{}"><p><span class="tag tag--sm">{}</span> <span>{}</span></p><h2 class="card__title"><a class="link link--inline" href="{}">{}</a></h2><p>{}</p></article>'.format(item['kind'],item['status'],KINDS[item['kind']],STATUSES[item['status']],route(item),html.escape(item['title']),html.escape(item['summary']))

def render_portfolio_listing(page,render):
    intro=render_page_intro(page,render); cards=''.join(_card(x) for x in page['records'])
    options_kind=''.join('<option value="{}">{}</option>'.format(k,v) for k,v in KINDS.items()); options_status=''.join('<option value="{}">{}</option>'.format(k,v) for k,v in STATUSES.items())
    controls='<div class="record-collection__controls" hidden><label>النوع <select data-filter-kind><option value="">الكل</option>{}</select></label><label>الحالة <select data-filter-status><option value="">الكل</option>{}</select></label><label>الترتيب <select data-sort><option value="default">الافتراضي</option><option value="alpha">أبجديًا</option></select></label></div>'.format(options_kind,options_status)
    return render('sections/portfolio-listing/template.html',{'page_intro':intro,'controls':controls,'count':len(page['records']),'cards':cards},('page_intro','controls','cards'))

def render_portfolio_detail(page,render):
    item=page['record']; intro=render_page_intro(page,render,breadcrumb_items=[{'label':'الرئيسية','href':'index.html'},{'label':'البرامج والمبادرات','href':'programs.html'},{'label':item['title'],'current':True}])
    listing=lambda xs,ordered=False:'<{} class="list">{}</{}>'.format('ol' if ordered else 'ul',''.join('<li>{}</li>'.format(html.escape(x)) for x in xs),'ol' if ordered else 'ul')
    metrics=''.join('<div><dt>{}</dt><dd><bdi>{}</bdi><small>المصدر: {} — {}</small></dd></div>'.format(html.escape(m['label']),html.escape(m['value']),html.escape(m['source']),m['date']) for m in item['metrics'])
    metrics_section='<section><h2>نتائج موثقة في العرض</h2><dl class="record-detail__metadata">{}</dl></section>'.format(metrics) if metrics else ''
    relation_specs=(('service_ids','service-','خدمات مرتبطة'),('resource_ids','resource-','موارد مرتبطة'),('news_ids','news-','أخبار مرتبطة'))
    relation_groups=[]
    for field,prefix,label in relation_specs:
        if item[field]: relation_groups.append('<section><h2>{}</h2><ul>{}</ul></section>'.format(label,''.join('<li><a class="link" href="{}{}.html">{}</a></li>'.format(prefix,x,html.escape(x)) for x in item[field])))
    return render('sections/portfolio-detail/template.html',{'page_intro':intro,'kind':KINDS[item['kind']],'status':STATUSES[item['status']],'owner':item['owner'],'updated':item['updated'],'objectives':listing(item['objectives']),'outputs':listing(item['outputs']),'body':render_content_blocks(item['body']),'metrics':metrics_section,'relations':''.join(relation_groups)},('page_intro','objectives','outputs','body','metrics','relations'))
