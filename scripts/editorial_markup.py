"""Shared editorial records and list/detail composition."""
import html
import re
from datetime import date
try:
    from scripts.content_markup import validate_content_blocks, render_content_blocks
    from scripts.page_intro_markup import render_page_intro
except ImportError:
    from content_markup import validate_content_blocks, render_content_blocks
    from page_intro_markup import render_page_intro

SLUG = re.compile(r'[a-z][a-z0-9-]*')
FIELDS = {'id','title','summary','published','updated','category','tags','featured','image','image_alt','body','related_ids'}

def route(record): return 'news-' + record['id'] + '.html'

def _iso(value, label):
    try: date.fromisoformat(value)
    except (TypeError, ValueError): raise ValueError(label + ' must be an ISO date')

def validate_editorial_records(records):
    if not isinstance(records, list) or not records: raise ValueError('Editorial records must be nonempty')
    ids=[]
    for item in records:
        if not isinstance(item,dict) or set(item)!=FIELDS: raise ValueError('Editorial record fields do not match contract')
        if not SLUG.fullmatch(item.get('id','')): raise ValueError('Editorial IDs must be slugs')
        ids.append(item['id'])
        for key in ('title','summary','category'):
            if not isinstance(item[key],str) or not item[key].strip(): raise ValueError('Editorial text is required: '+key)
        _iso(item['published'],'Editorial published'); _iso(item['updated'],'Editorial updated')
        if not isinstance(item['featured'],bool): raise ValueError('Editorial featured must be boolean')
        if not isinstance(item['tags'],list) or any(not isinstance(x,str) or not x for x in item['tags']): raise ValueError('Editorial tags must be text')
        if (item['image'] is None)!=(item['image_alt'] is None): raise ValueError('Editorial image and alt must be paired')
        validate_content_blocks(item['body'])
        if not isinstance(item['related_ids'],list) or len(item['related_ids'])!=len(set(item['related_ids'])): raise ValueError('Editorial related IDs must be unique')
    if len(ids)!=len(set(ids)): raise ValueError('Editorial IDs and routes must be unique')
    if any(target not in ids or target==item['id'] for item in records for target in item['related_ids']): raise ValueError('Editorial related IDs must resolve without self links')

def _card(item):
    return '<article class="card record-card" data-record><p class="record-card__meta"><span class="tag tag--sm">{}</span> <time datetime="{}">{}</time></p><h2 class="card__title"><a class="link link--inline" href="{}">{}</a></h2><p>{}</p></article>'.format(html.escape(item['category']),item['published'],item['published'],route(item),html.escape(item['title']),html.escape(item['summary']))

def render_editorial_listing(page, render):
    records=sorted(page['records'],key=lambda x:x['published'],reverse=True)
    intro=render_page_intro(page,render)
    cards=''.join(_card(item) for item in records)
    return render('sections/editorial-listing/template.html',{'page_intro':intro,'cards':cards},('page_intro','cards'))

def render_editorial_detail(page, render):
    item=page['record']; intro=render_page_intro(page,render,breadcrumb_items=[{'label':'الرئيسية','href':'index.html'},{'label':'أخبار الهيئة','href':'news.html'},{'label':item['title'],'current':True}])
    tags=''.join('<span class="tag tag--sm">{}</span>'.format(html.escape(x)) for x in item['tags'])
    return render('sections/editorial-detail/template.html',{'page_intro':intro,'published':item['published'],'category':item['category'],'tags':tags,'body':render_content_blocks(item['body'])},('page_intro','tags','body'))
