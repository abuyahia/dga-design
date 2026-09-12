"""Digital Stamp composition; site registration data is explicit, never inferred."""
import html
import re
from urllib.parse import urlsplit

DOMAINS = {
 'gov.sa': ('روابط المواقع الإلكترونية الرسمية الحكومية تنتهي بـ', 'جميع روابط المواقع الرسمية التابعة للجهات الحكومية في المملكة العربية السعودية تنتهي بـ .gov.sa'),
 'edu.sa': ('روابط المواقع الإلكترونية الرسمية التعليمية السعودية تنتهي بـ', 'جميع روابط المواقع الرسمية التعليمية في المملكة العربية السعودية تنتهي بـ sch.sa أو edu.sa'),
 'med.sa': ('روابط المواقع الإلكترونية الرسمية الطبية السعودية تنتهي بـ', 'جميع روابط المواقع الرسمية الطبية في المملكة العربية السعودية تنتهي بـ med.sa'),
 'org.sa': ('روابط المواقع الإلكترونية الرسمية للمؤسسات غير الربحية السعودية تنتهي بـ', 'جميع روابط المواقع الرسمية للمؤسسات غير الربحية في المملكة العربية السعودية تنتهي بـ org.sa'),
 'sch.sa': ('روابط المواقع الإلكترونية الرسمية التعليمية السعودية تنتهي بـ', 'جميع روابط المواقع الرسمية التعليمية في المملكة العربية السعودية تنتهي بـ sch.sa أو edu.sa'),
 '.sa': ('روابط المواقع الإلكترونية الرسمية للأنشطة والمبادرات السعودية تنتهي بـ', 'جميع روابط المواقع الرسمية للأنشطة والمبادرات في المملكة العربية السعودية تنتهي بـ sa.'),
}


def validate_stamp(data):
    if data.get('extension', 'gov.sa') not in DOMAINS:
        raise ValueError('Unsupported Digital Stamp extension')
    if data.get('mode', 'preview') not in ('preview', 'registered'):
        raise ValueError('Digital Stamp mode must be preview or registered')
    if data.get('mode') == 'registered':
        if not re.fullmatch(r'[0-9]{6,20}', str(data.get('registration_number', ''))):
            raise ValueError('Digital Stamp needs a registration number')
        url = urlsplit(data.get('registration_url', ''))
        if url.scheme != 'https' or url.hostname != 'raqmi.dga.gov.sa' or url.username or url.password or url.port not in (None,443):
            raise ValueError('Digital Stamp registration must link to the DGA registry over HTTPS')


def render_stamp(data, render, direction='rtl', asset_prefix='components/digital-stamp/assets/', reference=False):
    validate_stamp(data)
    ar = direction == 'rtl'
    extension = data.get('extension','gov.sa')
    heading, description = DOMAINS[extension]
    mobile_heading = 'روابط المواقع الإلكترونية الرسمية السعودية تنتهي بـ' if extension=='gov.sa' else heading
    if not ar:
        kind={'gov.sa':'Government', 'edu.sa':'Educational', 'sch.sa':'Educational', 'med.sa':'Medical', 'org.sa':'Nonprofit', '.sa':'Activities and Initiatives'}[extension]
        heading = mobile_heading = 'Official Saudi '+kind+' websites URL ends with'
        description = 'Website belongs to an official government organization in the Kingdom of Saudi Arabia always ends with .gov.sa .' if extension=='gov.sa' else 'Official Saudi '+kind.lower()+' websites use '+extension+' domains.'
    registered = reference or data.get('mode')=='registered'
    caption = ('موقع حكومي مسجل لدى هيئة الحكومة الرقمية' if ar else 'A government website registered with the Digital Government Authority.') if registered else ('معاينة الختم الرقمي — قالب تجريبي' if ar else 'Digital Stamp preview — demonstration template')
    label = ('مسجل لدى هيئة الحكومة الرقمية برقم:' if ar else 'Registered on Digital Government Authority:') if registered else ('بيانات التسجيل الفعلية' if ar else 'Actual registration data')
    if registered:
        number = '20230103200' if reference else str(data['registration_number'])
        href = '#reference-registration' if reference else data['registration_url']
        registration = '<a class="link link--md link--inline" dir="ltr" href="'+html.escape(href,quote=True)+'">'+html.escape(number)+'</a>'
    else:
        registration = '<span>'+('تُضاف عند تخصيص القالب للجهة' if ar else 'Provided when configuring the owning entity')+'</span>'
    return render('components/digital-stamp/template.html', {
        'open_attribute': 'open' if data.get('opened',False) else '', 'asset_prefix': asset_prefix,
        'caption': caption, 'toggle_label': 'كيف تتحقق؟' if ar else 'How you know?',
        'domain_heading': heading, 'mobile_domain_heading': mobile_heading, 'domain_description': description,
        'extension': extension if ar or extension.startswith('.') else '.'+extension,
        'security_heading': 'المواقع الإلكترونية الحكومية الموثوقة تستخدم بروتوكول' if ar else 'Official Reliable websites use',
        'security_description': 'تحقق من أن الموقع يستخدم بروتوكول HTTPS' if ar else 'Ensure the website is using the HTTPS protocol.',
        'registration_label': label, 'registration': registration,
        'authority_label': 'هيئة الحكومة الرقمية' if ar else 'Digital Government Authority',
    }, ('open_attribute','registration'))
