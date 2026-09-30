"""Load the fixed Authority editorial collection and register its routes."""
import json
from pathlib import Path
try:
    from scripts.editorial_markup import validate_editorial_records, route
except ImportError:
    from editorial_markup import validate_editorial_records, route

def apply(data, content_root):
    root=Path(content_root).resolve(); path=(root/'news.json').resolve()
    if root not in path.parents: raise ValueError('Editorial collection escaped demo content')
    payload=json.loads(path.read_text())
    if set(payload)!={'schema_version','news'} or payload['schema_version']!=1: raise ValueError('Editorial collection schema is invalid')
    records=payload['news']; validate_editorial_records(records); data['editorial_records']=records
    listing=next((x for x in data['pages'] if x['path']=='news.html'),None)
    if listing is None: raise ValueError('Editorial listing must be registered')
    listing['records']=records
    for item in records:
        data['pages'].append({'path':route(item),'title':item['title'],'description':item['summary'],'updated':item['updated'],'canonical':route(item),'sections':['editorial-detail','feedback'],'record':item})
    return data
