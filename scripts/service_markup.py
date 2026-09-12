"""Service catalogue, cards and detail-page composition from one service record."""
import html
from urllib.parse import urlsplit


def detail_url(service): return 'service-'+service['id']+'.html'
def start_url(service): return service.get('start_url') or detail_url(service)+'#start'


def validate_services(services):
    for service in services:
        for field in ['start_url','guide_url','video_url','support_url']:
            value=service.get(field)
            if value and (urlsplit(value).scheme!='https' or not urlsplit(value).netloc or urlsplit(value).username):
                raise ValueError('Service resource URLs must use HTTPS: '+field)
        if not service.get('audiences') or not all(isinstance(a,str) and a for a in service['audiences']):
            raise ValueError('Service audiences are required')
        for field in ['steps','requirements','documents']:
            if not isinstance(service.get(field),list) or not service[field] or not all(isinstance(x,str) and x for x in service[field]):
                raise ValueError('Service detail lists are required: '+field)
        for app in service.get('apps',[]):
            if urlsplit(app['href']).scheme!='https': raise ValueError('App links must use HTTPS')


def tags(service):
    return ''.join('<span class="tag tag--sm tag--success">'+html.escape(a)+'</span>' for a in service['audiences'])


def service_card(service,render,prefix=''):
    return render('components/service-card/template.html',{**service,'card_id':prefix+service['id'],'audience_keys':'|'.join(service['audiences']),'search_text':service['title']+' '+service['description'],'tags':tags(service),'detail_url':detail_url(service),'start_url':start_url(service)},('tags',))


def catalogue(services,render):
    audiences=list(dict.fromkeys(a for s in services for a in s['audiences']))
    filters=''.join('<button class="tab tab--h" type="button" data-audience="'+html.escape(a,quote=True)+'" aria-pressed="'+str(i==0).lower()+'">'+html.escape('الكل' if not a else a)+'</button>' for i,a in enumerate(['']+audiences))
    return render('sections/service-catalog/template.html',{'filters':filters,'cards':''.join(service_card(s,render) for s in services)},('filters','cards'))


def overview(service,services,render,default_contact_url=None):
    separator='<span class="breadcrumb__separator" aria-hidden="true"><img src="templates/service/assets/main-imgElements.svg" alt=""></span>'
    breadcrumb='<nav class="breadcrumb" aria-label="مسار التنقل"><ol class="breadcrumb__list"><li class="breadcrumb__item"><a class="breadcrumb__link" href="index.html">الرئيسية</a>'+separator+'</li><li class="breadcrumb__item"><a class="breadcrumb__link" href="services.html">الخدمات الإلكترونية</a>'+separator+'</li><li class="breadcrumb__item breadcrumb__item--current"><span class="breadcrumb__link" aria-current="page">'+html.escape(service['title'])+'</span></li></ol></nav>'
    labels=[('steps','الخطوات'),('requirements','شروط الاستخدام'),('documents','المستندات المطلوبة')]
    buttons=''.join('<button class="tab tab--h" type="button" id="tab-'+key+'" data-panel="panel-'+key+'">'+label+'</button>' for key,label in labels)
    panels=[]
    for key,label in labels:
        video='<video class="service-page__video" controls preload="none" src="'+html.escape(service['video_url'],quote=True)+'" aria-label="شرح خطوات الخدمة"></video>' if key=='steps' and service.get('video_url') else ''
        listing='ol' if key=='steps' else 'ul'
        panels.append('<section class="service-page__panel" id="panel-'+key+'"><h2>'+label+'</h2>'+video+'<'+listing+'>'+''.join('<li>'+html.escape(x)+'</li>' for x in service[key])+'</'+listing+'></section>')
    fact_data=[('الفئة المستهدفة','، '.join(service['audiences']),'imgElements'),('مدة الخدمة',service['duration'],'imgElements1'),('قنوات تقديم الخدمة',service['channels'],'imgElements2'),('تكلفة الخدمة',service['cost'],'imgElements3'),('الجهة المالكة',service['owner'],None),('لغات تقديم الخدمة',service['languages'],None)]
    facts=''.join('<div class="service-page__fact">'+('<span class="service-page__fact-icon" aria-hidden="true"><img src="templates/service/assets/card-'+icon+'.svg" alt=""></span>' if icon else '')+'<div><dt>'+label+'</dt><dd>'+html.escape(value)+'</dd></div></div>' for label,value,icon in fact_data)
    support_service=next((s for s in services if s['id']=='support'),None)
    contact_url=service.get('support_url') or default_contact_url or (start_url(support_service) if support_service else 'services.html')
    support='<a class="link link--md" href="'+html.escape(contact_url,quote=True)+'">التواصل مع الدعم</a>'
    for field,scheme in [('phone','tel:'),('email','mailto:')]:
        if service.get(field):support+='<a class="link link--md" dir="ltr" href="'+scheme+html.escape(service[field],quote=True)+'">'+html.escape(service[field])+'</a>'
    guide='<a class="btn btn--secondary-solid" href="'+html.escape(service['guide_url'],quote=True)+'">تحميل دليل المستخدم</a>' if service.get('guide_url') else ''
    apps='<div class="service-page__apps"><h2>تطبيقات الجوال</h2>'+''.join('<a class="link" href="'+html.escape(a['href'],quote=True)+'">'+html.escape(a['label'])+'</a>' for a in service.get('apps',[]))+'</div>' if service.get('apps') else ''
    launch='' if service.get('start_url') else '<section class="service-page__launch" id="start" tabindex="-1"><h2>بدء '+html.escape(service['title'])+'</h2><p>هذه معاينة لمسار بدء الخدمة. يضاف رابط منصة التنفيذ عند تخصيص القالب للجهة، ولا تُرسل طلبات من هذه الصفحة.</p><a class="link link--md" href="#panel-steps" data-open-steps>مراجعة خطوات الخدمة</a></section>'
    faq=''.join('<details><summary>'+html.escape(x['question'])+'</summary><p>'+html.escape(x['answer'])+'</p></details>' for x in service['faq'])
    related=[s for s in services if s['id']!=service['id']]
    related.sort(key=lambda s:not bool(set(s['audiences'])&set(service['audiences'])))
    return render('sections/service-overview/template.html',{**service,'contact_url':contact_url,'start_url':start_url(service),'breadcrumb':breadcrumb,'tags':tags(service),'tab_buttons':buttons,'panels':''.join(panels),'facts':facts,'support':support,'guide':guide,'apps':apps,'launch':launch,'related':''.join(service_card(s,render,'related-') for s in related[:3]),'faq':faq},('breadcrumb','tags','tab_buttons','panels','facts','support','guide','apps','launch','related','faq'))
