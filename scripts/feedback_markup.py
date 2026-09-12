"""Reusable feedback composition. Statistics are optional, never fabricated."""
import html
import re
from pathlib import Path
from math import isfinite

def render_feedback(kind, subject, render, stats=None, prefix=None):
    if kind not in ('page', 'service'):
        raise ValueError('Unknown feedback kind')
    ident = prefix or kind + '-feedback'
    statistics = ''
    if stats is not None:
        count = stats.get('count')
        if type(count) is not int or count < 0:
            raise ValueError('Feedback count must be a nonnegative integer')
        value = stats.get('average' if kind == 'service' else 'percentage')
        if type(value) not in (float, int) or not isfinite(value) or not 0 <= value <= (5 if kind == 'service' else 100):
            raise ValueError('Invalid feedback statistic')
        if count:
            statistics = ('<p>تم تقييم هذه الخدمة بمتوسط <strong>' + str(value) + '</strong></p>' + display_stars(value) + '<p class="feedback-statistics">' + str(count) + ' تقييم</p>') if kind == 'service' else '<p class="feedback-statistics">' + str(value) + '% من المستخدمين قالوا نعم من ' + str(count) + ' تعليقًا.</p>'
    if not statistics and kind == 'service':
        statistics = '<p>شاركنا تقييمك لهذه الخدمة</p>' + display_stars(0)
    yes=['وجدت الصفحة مفيدة وواضحة','تمكنت من الوصول للمعلومات بسهولة','صياغة المحتوى متقنة في هذه الصفحة','تصفح الصفحة مريح وسهل','سبب آخر']
    no=['المحتوى غير مفهوم','لم أتمكن من إيجاد المعلومات المطلوبة','واجهتني مشكلة تقنية','وجدت صعوبة في القراءة عند تصفح هذه الصفحة','سبب آخر']
    checkbox_source = (Path(__file__).resolve().parents[1] / 'components/checkbox/template.html').read_text()
    checkbox = re.search(r'<label class="checkbox checkbox--md checkbox--primary">(.*?)</label>', checkbox_source, re.S)[1]
    def reason_control(i):
        return '<span class="checkbox checkbox--sm checkbox--primary">' + re.sub(r'<input[^>]+>', '<input type="checkbox" class="checkbox__input" name="reason" value="'+str(i)+'" disabled>', checkbox) + '</span>'
    reasons=''.join('<label class="feedback-reason" data-reason-group="'+group+'">'+reason_control(i)+'<span>'+html.escape(label)+'</span></label>' for group,labels in [('yes',yes),('no',no)] for i,label in enumerate(labels))
    gender_options = ''.join(render('components/radio/template.html', {'name':'gender', 'value':value, 'label':label, 'attributes':' checked' if value=='unspecified' else ''}, ('attributes',)) for value,label in [('male','ذكر'),('female','أنثى'),('unspecified','أفضّل ألا أقول')])
    stars=''.join('<label class="rating__star"><input type="radio" name="score" value="'+str(i)+'" aria-label="'+str(i)+' من 5" required><img class="rating__star-icon" src="components/service-rating/assets/default-imgSizeMediumStateNormalStyleBrand.svg" width="32" height="32" alt=""></label>' for i in range(1,6))
    return render('components/'+('service-rating' if kind=='service' else 'page-feedback')+'/template.html', {'id':ident,'subject':subject,'statistics':statistics,'reasons':reasons,'gender_options':gender_options,'stars':stars,'comment_label':'أخبرنا عن تجربتك في هذه الخدمة' if kind=='service' else 'تعليق'}, ('statistics','reasons','stars','gender_options'))

def display_stars(value):
    names=['Selected' if value>=i else 'Half' if value>=i-0.5 else 'Normal' for i in range(1,6)]
    return '<span class="rating rating--md rating--brand" dir="ltr" aria-hidden="true">'+''.join('<span class="rating__star"><img class="rating__star-icon" width="32" height="32" alt="" src="components/service-rating/assets/'+('default-imgRatingStar.svg' if name=='Half' else 'default-imgSizeMediumState'+name+'StyleBrand.svg')+'"></span>' for name in names)+'</span>'
