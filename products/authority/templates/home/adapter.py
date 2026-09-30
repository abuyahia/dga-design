"""Attach resolved records to the registered Authority Home page."""
def apply(data,content_root):
    page=next((x for x in data['pages'] if x['path']=='index.html'),None)
    if page is None: raise ValueError('Authority Home must be registered')
    page['services_records']=data['services']; page['regulatory_records']=data['regulatory_records']; page['resource_records']=data['resource_records']; page['portfolio_records']=data['portfolio_records']; page['editorial_records']=data['editorial_records']
    return data
