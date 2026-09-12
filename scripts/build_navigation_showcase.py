"""Generate the Figma variant matrix from reusable navigation markup and exact assets."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'components/navigation-header'
STATES = ['default', 'hovered', 'pressed', 'focused', 'disabled']


def icon(kind='login', prefix='../assets/', on_color=False, boxed=False):
    files = {
        'login': ['action-imgElements2.svg', 'action-imgElements.svg', 'action-imgElements1.svg'],
        'chevron': ['menu-imgElements7.svg', 'menu-imgElements1.svg', 'menu-imgElements4.svg'],
        'check': ['item-icon-imgElements.svg' if boxed else 'submenu-imgElements.svg', 'submenu-imgElements1.svg', 'submenu-imgElements.svg'],
    }[kind]
    klass = 'nav-header__chevron' if kind == 'chevron' else 'nav-header__icon'
    markup = '<span class="'+klass+'" aria-hidden="true">'+''.join('<img class="nav-header__glyph--'+state+'" src="'+prefix+file+'" alt="">' for state,file in zip(['default','white','disabled'],files))+'</span>'
    if kind == 'check':
        markup = '<span class="nav-header__item-icon'+(' nav-header__item-icon--boxed' if boxed else '')+(' nav-header__item-icon--on-color' if on_color else '')+'">'+markup+'</span>'
    return markup


def control(part, state, selected, direction, layout='inline'):
    label = ('تبويب' if direction == 'rtl' else 'Link') if part=='item' else ('إجراء' if direction=='rtl' else 'Action')
    classes = 'nav-header__'+part + (' nav-header__action--stacked' if layout=='stacked' else '') + (' nav-header__action--icon-only' if layout=='icon-only' else '')
    body = ('' if layout=='text' else icon()) + ('' if layout=='icon-only' else '<span class="nav-header__label">'+label+'</span>') + (icon('chevron') if part=='item' else '')
    return '<button type="button" class="'+classes+'" data-part="'+part+'" data-layout="'+layout+'" data-selected="'+str(selected).lower()+'" data-preview-state="'+state+'" aria-label="'+label+'"'+(' disabled' if state=='disabled' else '')+'>'+body+'</button>'


def submenu(direction, state, on_color=False, boxed=False, helper=True, prefix='../assets/'):
    label, desc = ('عنوان عنصر القائمة','محتوى مساند لعنصر الوصول') if direction=='rtl' else ('Menu Item Label','Menu item helper text')
    return '<a href="#example-content" class="nav-header__submenu-item'+(' nav-header__submenu-item--on-color' if on_color else '')+'" data-preview-state="'+state+'">'+icon('check', prefix, on_color, boxed)+'<span class="nav-header__submenu-content"><span class="nav-header__submenu-title">'+label+'</span>'+('<span class="nav-header__submenu-description">'+desc+'</span>' if helper else '')+'</span></a>'


def build():
    parts=['<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Navigation Header — Figma states</title>']
    for href in ['../../../token.css','../../../styles/base/global.css','../../../styles/base/accessibility.css','../../../styles/base/layout.css','../../../assets/fonts/fonts.css','../../tag/tag.css','../navigation-header.css','showcase.css']:
        parts.append('<link rel="stylesheet" href="'+href+'">')
    parts.append('<body><main class="nav-showcase"><h1>Navigation Header — الحالات الأصلية من Figma</h1><p>مرجع القياسات: UI Shell / Nav Header. الحالات التالية ثابتة للمقارنة؛ مثال التنقل الحي أسفل الصفحة.</p>')
    for part,layouts in [('item',['inline']),('action',['inline','stacked','icon-only','text'])]:
        parts.append('<h2>'+('Header Menu Item' if part=='item' else 'Header Action')+'</h2>')
        for direction in ['ltr','rtl']:
            for layout in layouts:
                for selected in [True,False]:
                    parts.append('<section class="state-group" dir="'+direction+'"><h3>'+direction.upper()+' · '+layout+' · Selected='+str(selected)+'</h3><div class="state-row">')
                    for state in STATES:
                        parts.append('<figure>'+control(part,state,selected,direction,layout)+'<figcaption>'+state+'</figcaption></figure>')
                    parts.append('</div></section>')
    parts.append('<h2>Header Sub-menu Item</h2>')
    for on_color in [False,True]:
        parts.append('<div class="submenu-board'+(' on-color' if on_color else '')+'">')
        for direction in ['ltr','rtl']:
            parts.append('<div dir="'+direction+'">')
            for state in STATES[:-1]:parts.append(submenu(direction,state,on_color))
            parts.append('</div>')
        parts.append('</div>')
    parts.append('<h2>Header Menu — Opened / Closed</h2><div class="state-row">')
    for opened in [False,True]:
        for state in STATES[:-1]:
            parts.append('<figure><button class="nav-header__toggle nav-showcase__toggle" type="button" data-preview-state="'+state+'" aria-expanded="'+str(opened).lower()+'" aria-label="القائمة"><span class="nav-header__toggle-face"><span class="nav-header__icon" aria-hidden="true"><img src="../assets/toggle-imgElements.svg" alt=""></span></span></button><figcaption>'+str(opened)+' / '+state+'</figcaption></figure>')
    parts.append('</div><h2>Item Icon</h2><div class="state-row">')
    for on_color in [False,True]:
        for boxed in [False,True]:parts.append('<figure class="'+('on-color' if on_color else '')+'">'+icon('check',on_color=on_color,boxed=boxed)+'<figcaption>Contained='+str(boxed)+' / On-color='+str(on_color)+'</figcaption></figure>')
    parts.append('</div><h2>Nav Header Sub-Menu</h2>')
    for on_color in [False,True]:
        for full in [False,True]:
            for style in ['text','simple','boxed']:
                parts.append('<h3>'+style+' · Full-width='+str(full)+' · On-color='+str(on_color)+'</h3><div class="nav-header__panel'+(' nav-header__panel--on-color' if on_color else '')+(' nav-header__panel--full-width' if full else '')+'"><div class="nav-header__panel-content">')
                for group in range(4):
                    parts.append('<div class="nav-header__group"><h4 class="nav-header__group-title">عنوان مجموعة</h4><ul class="nav-header__submenu">')
                    for index in range(3):
                        markup=submenu('rtl','default',on_color,style=='boxed',style=='boxed')
                        if style=='text':markup=re.sub(r'<span class="nav-header__item-icon.*?</span></span>', '', markup)
                        parts.append('<li>'+markup+'</li>')
                    parts.append('</ul></div>')
                parts.append('</div></div>')
    parts.append('<h2>مثال التنقل الحي</h2>'+(BASE/'template.html').read_text().replace('src="assets/', 'src="../assets/'))
    parts.append('<section id="example-content"><h2>محتوى المثال</h2></section><section id="home"><h2>الرئيسية</h2></section><section id="service"><h2>الخدمة الأولى</h2></section></main><script src="../../../dist/government/components/navigation-header/navigation-header.runtime.js" defer></script></body></html>')
    (BASE/'showcases/index.html').write_text('\n'.join(parts))

if __name__=='__main__': build()
