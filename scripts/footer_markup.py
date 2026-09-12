"""Compose Footer's canonical fragments; all text and attributes pass through render escaping."""
import html


def render_footer(data, render, asset_prefix='components/footer/assets/'):
    dark = data.get('theme', 'default') == 'dark'
    link_theme = 'link--on-color' if dark else 'link--neutral'

    def links(items, inline=False):
        return ''.join(render('components/footer/link.html', {**item, 'link_theme': link_theme, 'inline_class': 'link--inline' if inline else ''}) for item in items)

    groups = ''.join(render('components/footer/group.html', {'title': group['title'], 'links': links(group['links'])}, ('links',)) for group in data.get('groups', []))
    tools = []
    for group in data.get('tools', []):
        controls = ''.join(render('components/footer/control.html', {**item, 'asset': asset_prefix + ('dark' if dark else 'rtl') + '-imgElements.svg', 'button_theme': 'btn--secondary-outline-on-color' if dark else 'btn--secondary-outline'}) for item in group['links'])
        if controls:
            tools.append('<div class="ds-footer__tool-group"><h2 class="ds-footer__heading">'+html.escape(group['title'])+'</h2><div class="ds-footer__controls">'+controls+'</div></div>')
    if tools:
        groups += '<div class="ds-footer__group ds-footer__tools">'+''.join(tools)+'</div>'
    navigation = '<nav class="ds-footer__navigation" aria-label="'+html.escape(data.get('navigation_label','روابط التذييل'), quote=True)+'">'+groups+'</nav>' if groups and data.get('nav_links', True) else ''
    logos = ''.join('<span class="ds-footer__logo">'+('<img src="'+html.escape(logo['src'], quote=True)+'" alt="">' if logo.get('src') else '')+html.escape(logo['label'])+'</span>' for logo in data.get('logos', []))
    legal = links(data.get('legal_links', []), True)
    extra = links(data.get('extra_links', []))
    updated = '<p class="ds-footer__updated">'+html.escape(data['updated'])+'</p>' if data.get('updated') else ''
    return render('components/footer/template.html', {
        'theme_class': 'ds-footer--dark' if dark else '', 'navigation': navigation,
        'legal_links': '<ul class="ds-footer__legal-links">'+legal+'</ul>' if legal else '',
        'extra_links': '<ul class="ds-footer__legal-links">'+extra+'</ul>' if extra else '',
        'copyright': data['copyright'], 'updated': updated, 'logos': logos,
    }, ('navigation','legal_links','extra_links','updated','logos'))
