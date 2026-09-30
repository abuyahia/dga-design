"""Register Authority regulatory list/detail pages from one collection."""
import importlib.util, json
from pathlib import Path

def _validator():
    path=Path(__file__).with_name('validator.py'); spec=importlib.util.spec_from_file_location('authority_regulatory_validator_adapter',path); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

def apply(data,content_root):
    root=Path(content_root).resolve(); path=(root/'regulations.json').resolve()
    if root not in path.parents: raise ValueError('Regulatory collection escaped demo content')
    payload=json.loads(path.read_text())
    if set(payload)!={'schema_version','regulations'} or payload['schema_version']!=1: raise ValueError('Regulatory collection schema is invalid')
    validator=_validator(); records=payload['regulations']; validator.validate_records(records,{x['id'] for x in data['resource_records']},{x['id'] for x in data['services']})
    asset_root=root.parents[1]/'assets'; prefix='assets/products/authority/'
    for item in records:
        if item['file'].startswith(prefix):
            source=(asset_root/item['file'][len(prefix):]).resolve()
            if asset_root.resolve() not in source.parents or not source.is_file(): raise ValueError('Regulatory local file does not exist')
    data['regulatory_records']=records
    listing=next((x for x in data['pages'] if x['path']=='regulations.html'),None)
    if listing is None: raise ValueError('Regulatory listing must be registered')
    listing['records']=records
    next_by_previous={x['supersedes_id']:x for x in records if x['supersedes_id']}
    by_id={x['id']:x for x in records}
    for item in records:
        data['pages'].append({'path':validator.route(item),'title':item['title'],'description':item['summary'],'updated':item['updated'],'canonical':validator.route(item),'sections':['regulatory-detail','feedback'],'record':item,'previous_record':by_id.get(item['supersedes_id']),'next_record':next_by_previous.get(item['id'])})
    return data
