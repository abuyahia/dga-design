"""Render configurable Contact Us composition; do not invent operational contact data."""
import html
from urllib.parse import urlsplit

def validate_contact(data):
    if not isinstance(data,dict): raise ValueError('Contact data must be an object')
    for item in data.get('channels',[]) + data.get('socials',[]) + data.get('help_links',[]):
        href=item.get('href')
        if href:
            u=urlsplit(href)
            if u.scheme not in ('https','mailto','tel','sms') and (u.scheme or u.netloc or not href.startswith(('services.html','about.html','contact.html'))): raise ValueError('Invalid contact destination')
            if u.scheme=='https' and (not u.hostname or u.username): raise ValueError('Invalid HTTPS contact destination')
            if any(c in href for c in ['\n','\r']): raise ValueError('Invalid contact destination')
    if not data.get('categories') or any(not isinstance(c,str) or not c.strip() for c in data['categories']): raise ValueError('Contact categories are required')

def contact_page(data, render):
    validate_contact(data)
    fields=[]
    for name,label,typ,placeholder,autocomplete,maxlength,required in [
        ('first_name','الاسم الأول','text','أدخل الاسم الأول','given-name',80,True),
        ('last_name','الاسم الأخير','text','أدخل الاسم الأخير','family-name',80,True),
        ('email','البريد الإلكتروني','email','name@example.com','email',254,True),
        ('phone','رقم الجوال','tel','05XXXXXXXX','tel',20,True),
        ('subject','الموضوع','text','اكتب موضوع رسالتك','off',150,False)]:
        fields.append(render('sections/contact/input.html',{'name':name,'id':'contact-'+name,'label':label,'type':typ,'placeholder':placeholder,'autocomplete':autocomplete,'maxlength':maxlength,'attributes':(' required' if required else '')+(' dir="ltr"' if typ in ('email','tel') else ''),'required_mark':' <span class="contact-required" aria-hidden="true">*</span>' if required else ''},('attributes','required_mark')))
    options='<option value="">اختر الفئة</option>'+''.join('<option value="'+html.escape(c,quote=True)+'">'+html.escape(c)+'</option>' for c in data['categories'])
    fields.append(render('components/select/template.html',dict(name='category',id='contact-category',label='الفئة (اختياري)',options=options),('options',)))
    fields.append(render('components/textarea/template.html',dict(name='message',id='contact-message',label='كيف يمكننا مساعدتك؟ (مطلوب)',placeholder='اكتب رسالتك',attributes=' required'),('attributes',)))
    fields.append(render('sections/contact/upload.html',{}))
    assets={'phone':'3','sms':'4','email':'5','fax':'5','location':'7'}
    channels=[]
    for row in data.get('channels',[]):
        icon=assets.get(row.get('kind'),'5')
        value=html.escape(row['value'])
        if row.get('href'): value='<a class="link link--inline" href="'+html.escape(row['href'],quote=True)+'"><bdi>'+value+'</bdi></a>'
        channels.append('<div class="contact-card__channel"><img src="templates/contact/assets/desktop-imgElements'+icon+'.svg" width="24" height="24" alt=""><div><dt>'+html.escape(row['label'])+'</dt><dd>'+value+'</dd></div></div>')
    socials=''
    if data.get('socials'):
        icons={'x':'8','linkedin':'9','instagram':'10'}
        links=[]
        for row in data['socials']:
            if row.get('kind') not in icons: raise ValueError('Unknown contact social icon')
            links.append('<a class="btn btn--subtle btn--md btn--icon-only" aria-label="'+html.escape(row['label'],quote=True)+'" href="'+html.escape(row['href'],quote=True)+'"><img width="20" height="20" alt="" src="templates/contact/assets/desktop-imgElements'+icons[row['kind']]+'.svg"></a>')
        socials='<div><h2>تابعنا على</h2><div class="contact-card__socials">'+''.join(links)+'</div></div>'
    links=''.join('<li><a class="link link--inline" href="'+html.escape(row['href'],quote=True)+'">'+html.escape(row['label'])+'</a></li>' for row in data.get('help_links',[]))
    return render('sections/contact/template.html',dict(description=data['description'],card_title=data['card_title'],fields=''.join(fields).replace('class="text-input ', 'class="text-input text-input--disabled '),channels=''.join(channels),socials=socials,help_links=links),('fields','channels','socials','help_links'))
