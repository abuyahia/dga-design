"""Load the fixed Authority resource collection and register its routes."""
import json
from pathlib import Path
try:
    from scripts.resource_markup import validate_resource_records, route
except ImportError:
    from resource_markup import validate_resource_records, route

def apply(data, content_root):
    root=Path(content_root).resolve(); path=(root/'resources.json').resolve()
    if root not in path.parents: raise ValueError('Resource collection escaped demo content')
    payload=json.loads(path.read_text())
    if set(payload)!={'schema_version','resources'} or payload['schema_version']!=1: raise ValueError('Resource collection schema is invalid')
    records=payload['resources']; validate_resource_records(records)
    asset_root=root.parents[1]/'assets'; prefix='assets/products/authority/'
    for item in records:
        if item['destination'].startswith(prefix):
            source=(asset_root/item['destination'][len(prefix):]).resolve()
            if asset_root.resolve() not in source.parents or not source.is_file(): raise ValueError('Resource local destination does not exist')
    data['resource_records']=records
    listing=next((x for x in data['pages'] if x['path']=='knowledge.html'),None)
    if listing is None: raise ValueError('Resource listing must be registered')
    listing['records']=records
    for item in records:
        data['pages'].append({'path':route(item),'title':item['title'],'description':item['summary'],'updated':item['updated'],'canonical':route(item),'sections':['resource-detail','feedback'],'record':item})
    return data
