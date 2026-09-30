"""Authority Regulatory Document Detail renderer."""
import html, importlib.util
from pathlib import Path
try:
    from scripts.page_intro_markup import render_page_intro
    from scripts.content_markup import render_content_blocks
except ImportError:
    from page_intro_markup import render_page_intro
    from content_markup import render_content_blocks

TEMPLATE='products/authority/templates/regulatory/detail-template.html'
def _validator():
    path=Path(__file__).with_name('validator.py'); spec=importlib.util.spec_from_file_location('authority_regulatory_validator_detail',path); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
def validate(page,asset_root): _validator().validate_page(page,True)
def render(page,render_markup,asset_root,asset_prefix):
    validator=_validator(); item=page['record']; status=validator.STATUSES[item['status']]
    intro=render_page_intro(page,render_markup,breadcrumb_items=[{'label':'الرئيسية','href':'index.html'},{'label':'الأنظمة واللوائح والقرارات','href':'regulations.html'},{'label':item['title'],'current':True}])
    alert='<div class="inline-alert inline-alert--{} inline-alert--color-bg" role="alert"><div class="inline-alert__header"><div class="inline-alert__content"><p class="inline-alert__title">{}</p><p class="inline-alert__body">{}</p></div></div></div>'.format('warning' if item['status']!='demo-active' else 'info',html.escape(status),html.escape(item['disclaimer']))
    values=[('نوع الوثيقة',validator.TYPES[item['type']]),('الجهة المصدرة',item['authority']),('الرقم',item['number']),('الإصدار',item['version']),('تاريخ الاعتماد',item['adoption_date'] or 'غير معتمد'),('تاريخ النفاذ',item['effective_date'] or 'غير نافذ')]
    metadata=''.join('<div><dt>{}</dt><dd><bdi>{}</bdi></dd></div>'.format(html.escape(k),html.escape(v)) for k,v in values)
    links=[]
    if page.get('previous_record'): links.append('<a class="link" href="{}">النسخة السابقة: {}</a>'.format(validator.route(page['previous_record']),html.escape(page['previous_record']['title'])))
    if page.get('next_record'): links.append('<a class="link" href="{}">النسخة الأحدث: {}</a>'.format(validator.route(page['next_record']),html.escape(page['next_record']['title'])))
    links.extend('<a class="link" href="resource-{}.html">مورد مرتبط: {}</a>'.format(x,html.escape(x)) for x in item['resource_ids'])
    links.extend('<a class="link" href="service-{}.html">خدمة مرتبطة: {}</a>'.format(x,html.escape(x)) for x in item['service_ids'])
    relations='<nav class="regulatory-detail__relations" aria-label="علاقات النسخ">{}</nav>'.format(''.join(links)) if links else ''
    return render_markup(TEMPLATE,{'page_intro':intro,'alert':alert,'metadata':metadata,'body':render_content_blocks(item['body']),'file':item['file'],'download_label':'فتح ملف العرض — '+item['title'],'relations':relations},('page_intro','alert','metadata','body','relations'))
