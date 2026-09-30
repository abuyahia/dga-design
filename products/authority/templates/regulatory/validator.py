"""Strict Authority regulatory-record contract."""
import re
from datetime import date
from urllib.parse import urlsplit
try:
    from scripts.content_markup import validate_content_blocks
except ImportError:
    from content_markup import validate_content_blocks

SLUG=re.compile(r'[a-z][a-z0-9-]*')
TYPES={'guidance-framework':'إطار استرشادي','internal-rules':'قواعد داخلية','demo-policy':'سياسة تجريبية'}
STATUSES={'draft':'مسودة عرض غير نافذة','demo-active':'سارية داخل المعاينة فقط','obsolete':'ملغاة داخل المعاينة'}
FIELDS={'id','type','title','authority','number','adoption_date','effective_date','status','version','updated','summary','topics','file','disclaimer','supersedes_id','resource_ids','service_ids','body'}

def route(item): return 'regulation-'+item['id']+'.html'
def _date(value, nullable=False):
    if nullable and value is None:return
    try: date.fromisoformat(value)
    except (TypeError,ValueError): raise ValueError('Regulatory dates must be ISO dates or allowed null')
def _safe_file(value):
    parsed=urlsplit(value)
    return (parsed.scheme=='https' and bool(parsed.netloc) and parsed.username is None) or bool(re.fullmatch(r'assets/products/authority/downloads/[a-z0-9-]+\.(?:html|pdf)',value))

def validate_records(records, resource_ids=(), service_ids=()):
    if not isinstance(records,list) or not records: raise ValueError('Regulatory records must be nonempty')
    ids=[]
    for item in records:
        if not isinstance(item,dict) or set(item)!=FIELDS: raise ValueError('Regulatory fields do not match contract')
        if not SLUG.fullmatch(item.get('id','')): raise ValueError('Regulatory IDs must be slugs')
        ids.append(item['id'])
        if item['type'] not in TYPES or item['status'] not in STATUSES: raise ValueError('Regulatory type/status is unsupported')
        for key in ('title','authority','number','version','summary','disclaimer'):
            if not isinstance(item[key],str) or not item[key].strip(): raise ValueError('Regulatory text is required: '+key)
        if 'تجريب' not in item['disclaimer'] and 'عرض' not in item['disclaimer']: raise ValueError('Regulatory demo disclaimer is mandatory')
        _date(item['adoption_date'],True); _date(item['effective_date'],True); _date(item['updated'])
        if item['status']=='draft' and item['adoption_date'] is not None: raise ValueError('Draft regulatory records cannot claim adoption')
        if not _safe_file(item['file']): raise ValueError('Regulatory file destination is unsafe')
        if not isinstance(item['topics'],list) or not item['topics']: raise ValueError('Regulatory topics are required')
        for key in ('resource_ids','service_ids'):
            if not isinstance(item[key],list) or len(item[key])!=len(set(item[key])) or any(not SLUG.fullmatch(x) for x in item[key]): raise ValueError('Regulatory relations must be unique slug lists')
        validate_content_blocks(item['body'])
    if len(ids)!=len(set(ids)): raise ValueError('Regulatory IDs/routes must be unique')
    for item in records:
        if item['supersedes_id'] is not None and (item['supersedes_id'] not in ids or item['supersedes_id']==item['id']): raise ValueError('Regulatory supersedes target must resolve without self link')
        if resource_ids and any(x not in resource_ids for x in item['resource_ids']): raise ValueError('Regulatory resource IDs must resolve')
        if service_ids and any(x not in service_ids for x in item['service_ids']): raise ValueError('Regulatory service IDs must resolve')
    graph={x['id']:x['supersedes_id'] for x in records}
    for start in graph:
        seen=set(); current=start
        while graph[current] is not None:
            current=graph[current]
            if current in seen: raise ValueError('Regulatory supersedes graph contains a cycle')
            seen.add(current)

def validate_page(page, detail=False):
    value=page.get('record') if detail else page.get('records')
    if detail:
        if not isinstance(value,dict): raise ValueError('Regulatory detail requires a record')
        isolated=dict(value); isolated['supersedes_id']=None
        validate_records([isolated])
    elif not isinstance(value,list): raise ValueError('Regulatory listing requires records')
