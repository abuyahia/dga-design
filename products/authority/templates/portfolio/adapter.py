"""Load the fixed Authority portfolio collection and register its routes."""
import json
from pathlib import Path
try:
    from scripts.portfolio_markup import validate_portfolio_records, route
except ImportError:
    from portfolio_markup import validate_portfolio_records, route

def apply(data, content_root):
    root=Path(content_root).resolve(); path=(root/'portfolio.json').resolve()
    if root not in path.parents: raise ValueError('Portfolio collection escaped demo content')
    payload=json.loads(path.read_text())
    if set(payload)!={'schema_version','portfolio'} or payload['schema_version']!=1: raise ValueError('Portfolio collection schema is invalid')
    records=payload['portfolio']; validate_portfolio_records(records,data['services']); data['portfolio_records']=records
    listing=next((x for x in data['pages'] if x['path']=='programs.html'),None)
    if listing is None: raise ValueError('Portfolio listing must be registered')
    listing['records']=records
    for item in records:
        data['pages'].append({'path':route(item),'title':item['title'],'description':item['summary'],'updated':item['updated'],'canonical':route(item),'sections':['portfolio-detail','feedback'],'record':item})
    return data
