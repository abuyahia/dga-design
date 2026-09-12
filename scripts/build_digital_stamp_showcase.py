"""Build Digital Stamp samples from the same canonical fragments as the site."""
from pathlib import Path
try:
    from .build_site import render
    from .digital_stamp_markup import render_stamp, DOMAINS
except ImportError:
    from build_site import render
    from digital_stamp_markup import render_stamp, DOMAINS

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'components/digital-stamp/showcases'


def page(body, direction='rtl'):
    styles=['../../../token.css','../../../styles/base/global.css','../../../assets/fonts/fonts.css','../../link/link.css','../digital-stamp.css','showcase.css']
    return '<!doctype html><html lang="'+('ar' if direction=='rtl' else 'en')+'" dir="'+direction+'"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Digital Stamp — Figma</title>'+''.join('<link rel="stylesheet" href="'+s+'">' for s in styles)+'<body>'+body+'<p id="reference-registration" tabindex="-1" class="stamp-reference-note">معاينة من ملف Figma؛ الرقم الظاهر بيانات نموذجية وليس تسجيلًا لهذا القالب.</p><script src="../../../dist/government/components/digital-stamp/digital-stamp.runtime.js" defer></script></body></html>'


def build():
    BASE.mkdir(parents=True,exist_ok=True)
    body=['<main><h1>Digital Stamp — الختم الرقمي</h1><p>معاينة التصميم الأصلي ببيانات Figma النموذجية. افتح «كيف تتحقق؟» بلوحة المفاتيح أو بالنقر؛ يتغير التخطيط مع عرض الشاشة.</p>']
    for direction in ['rtl','ltr']:
        for opened in [False,True]:
            markup=render_stamp({'opened':opened},render,direction,'../assets/',reference=True)
            name=direction+('-open' if opened else '-closed')
            (BASE/(name+'.html')).write_text(page(markup,direction))
            body.append('<section dir="'+direction+'"><h2>'+name+'</h2>'+markup+'</section>')
    body.append('<h2>امتدادات النطاق — RTL</h2>')
    for extension in DOMAINS:
        body.append('<section><h3>'+extension+'</h3>'+render_stamp({'extension':extension,'opened':True},render,'rtl','../assets/',reference=True)+'</section>')
    body.append('<h2>وضع القالب التجريبي</h2>'+render_stamp({},render,'rtl','../assets/')+'</main>')
    (BASE/'index.html').write_text(page('\n'.join(body)))

if __name__=='__main__':build()
