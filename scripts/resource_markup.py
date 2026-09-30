"""Shared knowledge-resource contract and library/detail composition."""
import html
import re
from datetime import date
from urllib.parse import urlsplit
try:
    from scripts.content_markup import validate_content_blocks, render_content_blocks
    from scripts.page_intro_markup import render_page_intro
except ImportError:
    from content_markup import validate_content_blocks, render_content_blocks
    from page_intro_markup import render_page_intro

SLUG=re.compile(r'[a-z][a-z0-9-]*')
KINDS={'guide':'دليل','report':'تقرير','template':'قالب','dataset':'بيانات'}
FORMATS={'HTML','PDF','XLSX','CSV'}
FIELDS={'id','kind','title','summary','published','updated','format','size','language','topic','audiences','version','owner','destination','cover','cover_alt','body','related_ids'}
def route(item): return 'resource-'+item['id']+'.html'
def _safe_destination(value):
    parsed=urlsplit(value)
    if parsed.scheme: return parsed.scheme=='https' and bool(parsed.netloc) and parsed.username is None
    return bool(re.fullmatch(r'assets/products/authority/downloads/[a-z0-9-]+\.(?:pdf|xlsx|csv|html)',value))

def validate_resource_records(records):
    if not isinstance(records,list) or not records: raise ValueError('Resource records must be nonempty')
    ids=[]
    for item in records:
        if not isinstance(item,dict) or set(item)!=FIELDS: raise ValueError('Resource fields do not match contract')
        if not SLUG.fullmatch(item.get('id','')): raise ValueError('Resource IDs must be slugs')
        ids.append(item['id'])
        if item['kind'] not in KINDS or item['format'] not in FORMATS: raise ValueError('Resource kind/format is unsupported')
        for key in ('title','summary','size','language','topic','version','owner'):
            if not isinstance(item[key],str) or not item[key].strip(): raise ValueError('Resource text is required: '+key)
        for key in ('published','updated'):
            try: date.fromisoformat(item[key])
            except (TypeError,ValueError): raise ValueError('Resource dates must be ISO')
        if not isinstance(item['audiences'],list) or not item['audiences'] or any(not isinstance(x,str) or not x for x in item['audiences']): raise ValueError('Resource audiences are required')
        if not _safe_destination(item['destination']): raise ValueError('Resource destination must be safe local or HTTPS')
        if (item['cover'] is None)!=(item['cover_alt'] is None): raise ValueError('Resource cover and alt must be paired')
        validate_content_blocks(item['body'])
        if not isinstance(item['related_ids'],list) or len(item['related_ids'])!=len(set(item['related_ids'])): raise ValueError('Resource related IDs must be unique')
    if len(ids)!=len(set(ids)): raise ValueError('Resource IDs/routes must be unique')
    if any(target not in ids or target==item['id'] for item in records for target in item['related_ids']): raise ValueError('Resource related IDs must resolve')

def _card(item):
    return '<article class="card record-card" data-record data-kind="{}" data-topic="{}" data-search="{}"><p><span class="tag tag--sm">{}</span> <bdi>{} · {}</bdi></p><h2 class="card__title"><a class="link link--inline" href="{}">{}</a></h2><p>{}</p></article>'.format(item['kind'],html.escape(item['topic'],quote=True),html.escape(item['title']+' '+item['summary'],quote=True),KINDS[item['kind']],item['format'],html.escape(item['size']),route(item),html.escape(item['title']),html.escape(item['summary']))

def render_resource_listing(page,render):
    records=sorted(page['records'],key=lambda x:x['published'],reverse=True); intro=render_page_intro(page,render)
    kinds=''.join('<option value="{}">{}</option>'.format(k,v) for k,v in KINDS.items()); topics=''.join('<option value="{}">{}</option>'.format(html.escape(x,quote=True),html.escape(x)) for x in dict.fromkeys(r['topic'] for r in records))
    controls='<div class="record-collection__controls" hidden><label>بحث <input type="search" data-filter-query></label><label>النوع <select data-filter-kind><option value="">الكل</option>{}</select></label><label>الموضوع <select data-filter-topic><option value="">الكل</option>{}</select></label><button class="btn btn--secondary-outline" type="button" data-filter-reset>مسح</button></div>'.format(kinds,topics)
    return render('sections/resource-listing/template.html',{'page_intro':intro,'controls':controls,'count':len(records),'cards':''.join(_card(x) for x in records)},('page_intro','controls','cards'))

def render_resource_detail(page,render):
    item=page['record']; intro=render_page_intro(page,render,breadcrumb_items=[{'label':'الرئيسية','href':'index.html'},{'label':'مكتبة المعرفة','href':'knowledge.html'},{'label':item['title'],'current':True}])
    label='تنزيل {}، {}، {}'.format(item['title'],item['format'],item['size'])
    related='<section><h2>موارد مرتبطة</h2><ul>{}</ul></section>'.format(''.join('<li><a class="link" href="resource-{}.html">{}</a></li>'.format(x,html.escape(x)) for x in item['related_ids'])) if item['related_ids'] else ''
    return render('sections/resource-detail/template.html',{'page_intro':intro,'kind':KINDS[item['kind']],'version':item['version'],'format':item['format'],'size':item['size'],'language':item['language'],'body':render_content_blocks(item['body']),'destination':item['destination'],'download_label':label,'related':related},('page_intro','body','related'))
