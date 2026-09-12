"""Generate reusable Footer reference fixtures in both directions and surfaces."""
from pathlib import Path
try:
    from .build_site import render
    from .footer_markup import render_footer
except ImportError:
    from build_site import render
    from footer_markup import render_footer

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'components/footer/showcases'


def sample(direction, theme, nav_links=True, mobile=False):
    rtl = direction == 'rtl'
    link = {'href': '#example-content', 'label': 'رابط الجزء السفلي' if rtl else 'Footer Link'}
    return {
        'theme': theme, 'nav_links': nav_links,
        'navigation_label': 'روابط التذييل' if rtl else 'Footer navigation',
        'groups': [{'title': 'عنوان مجموعة' if rtl else 'Group Label', 'links': [link]*5} for _ in range(5)],
        'tools': [{'title': 'تواصل معنا' if rtl else 'Social Media', 'links': [{'href': '#example-content', 'label': ('رابط تواصل نموذجي ' if rtl else 'Example social link ')+str(i+1)} for i in range(4)]}, {'title': 'أدوات الاتاحة والوصول' if rtl else 'Accessibility Tools', 'links': [{'href': '#example-content', 'label': ('رابط وصول نموذجي ' if rtl else 'Example accessibility link ')+str(i+1)} for i in range(3)]}],
        'legal_links': [link] * (5 if mobile else 8),
        'extra_links': [{'href': '#example-content', 'label': 'الشروط والأحكام' if rtl else 'Terms and Conditions'}, {'href': '#example-content', 'label': 'سياسة الخصوصية' if rtl else 'Privacy Policy'}],
        'copyright': 'جميع الحقوق محفوظة لهيئة الحكومة الرقمية © 2024' if rtl else 'All Right Reserved For Digital Government Authority © 2024',
        'logos': [{'src': '../assets/rtl-imgPalmSwords.svg', 'label': 'شعار المنصة' if rtl else 'Platform Logo'}] * 2,
    }


def page(body, direction='rtl', title='Footer — Figma'):
    styles = ['../../../token.css', '../../../styles/base/global.css', '../../../assets/fonts/fonts.css', '../../link/link.css', '../../button/button.css', '../footer.css', 'showcase.css']
    return '<!doctype html><html lang="'+('ar' if direction=='rtl' else 'en')+'" dir="'+direction+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+title+'</title>'+''.join('<link rel="stylesheet" href="'+s+'">' for s in styles)+'</head><body>'+body+'<div id="example-content" tabindex="-1" class="footer-example-target">محتوى المثال / Example destination</div></body></html>'


def build():
    BASE.mkdir(parents=True, exist_ok=True)
    gallery = ['<main><h1>Footer — حالات Figma</h1><p>الأسهم والشعارات النموذجية من الملف الأصلي. الروابط في هذه المعاينة تقود إلى محتوى المثال. يتبدل التخطيط تلقائيًا تحت 600px.</p>']
    for direction in ['rtl', 'ltr']:
        for theme in ['default', 'dark']:
            for mobile in [False, True]:
                name = direction+'-'+theme+('-mobile' if mobile else '')
                markup = render_footer(sample(direction, theme, mobile=mobile), render, '../assets/')
                (BASE/(name+'.html')).write_text(page(markup, direction))
                gallery.append('<p><a href="'+name+'.html">'+name+'</a></p>')
            gallery.append('<section dir="'+direction+'"><h2>'+direction.upper()+' / '+theme+'</h2>'+render_footer(sample(direction, theme), render, '../assets/')+'</section>')
    gallery.append('<section><h2>Nav links = false</h2>'+render_footer(sample('rtl','default',False), render, '../assets/')+'</section></main>')
    (BASE/'index.html').write_text(page('\n'.join(gallery)))


if __name__ == '__main__': build()
