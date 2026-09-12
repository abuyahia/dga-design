"""Render the DGA form-page example from validated, escaped configuration."""
import html
try:
    from scripts.page_intro_markup import render_page_intro
except ImportError:
    from page_intro_markup import render_page_intro


VARIANTS = {'default', 'icon', 'prefix', 'suffix', 'helper', 'error', 'disabled'}


def validate_form_template(page):
    data = page.get('form_template')
    if not isinstance(data, dict):
        raise ValueError('Form template data must be an object')
    steps = data.get('steps')
    if not isinstance(steps, list) or not 2 <= len(steps) <= 8:
        raise ValueError('Form template requires two to eight steps')
    if any(not isinstance(step, dict) or any(not isinstance(step.get(key), str) or not step[key].strip() for key in ('title', 'description')) for step in steps):
        raise ValueError('Every form step requires a title and description')
    current = data.get('current_step')
    if not isinstance(current, int) or isinstance(current, bool) or not 1 <= current <= len(steps):
        raise ValueError('Current form step is outside the configured steps')
    variants = data.get('variants')
    if not isinstance(variants, list) or not variants or len(variants) != len(set(variants)) or set(variants) - VARIANTS:
        raise ValueError('Form field variants must be unique supported values')
    if not isinstance(data.get('required_note'), str) or not data['required_note'].strip():
        raise ValueError('Form required-note text is required')


def _icon(kind):
    if kind == 'search':
        return '<svg class="text-input__icon" aria-hidden="true" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="1.5"/><path d="m16 16 4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
    return '<svg aria-hidden="true" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="6" stroke="currentColor"/><path d="M8 7.2V11M8 4.8v.1" stroke="currentColor" stroke-linecap="round"/></svg>'


def _field(variant, required):
    suffix = 'required' if required else 'optional'
    field_id = f'form-{variant}-{suffix}'
    label = 'إدخال النص الإلزامي' if required else 'إدخال النص الاختياري'
    mark = ' <span class="contact-required" aria-hidden="true">*</span>' if required else ''
    root_classes = ['text-input']
    attributes = []
    support = ''
    describedby = ''
    if variant == 'error':
        root_classes.append('text-input--error')
        attributes.append('aria-invalid="true"')
        describedby = f' aria-describedby="{field_id}-support"'
        support = f'<p class="form-template__support" id="{field_id}-support">{_icon("info")}<span>نص مساعد</span></p>'
    elif variant == 'helper':
        describedby = f' aria-describedby="{field_id}-support"'
        support = f'<p class="form-template__support" id="{field_id}-support">{_icon("info")}<span>نص مساعد</span></p>'
    elif variant == 'disabled':
        root_classes.append('text-input--disabled')
        attributes.append('disabled')
    if required:
        attributes.extend(('required', 'aria-required="true"'))
    inner = '<div class="text-input__inner"><input class="text-input__input" type="text" id="{}" name="{}" placeholder="نص تلميحي"{} {}>{}</div>'.format(field_id, field_id, describedby, ' '.join(attributes), _icon('search') if variant == 'icon' else '')
    affix = '<div class="input-affix input-affix--text input-affix--solid" aria-hidden="true"><span class="input-affix__text">نص</span></div>'
    if variant == 'prefix':
        field = inner + affix
    elif variant == 'suffix':
        field = affix + inner
    else:
        field = inner
    return '<div class="{}" data-field="{}"><label class="text-input__label" for="{}">{}{}</label><div class="text-input__field">{}</div>{}</div>'.format(' '.join(root_classes), html.escape(field_id, quote=True), html.escape(field_id, quote=True), html.escape(label), mark, field, support)


def render_form_template(page, render):
    validate_form_template(page)
    data = page['form_template']
    current = data['current_step']
    items = []
    for index, step in enumerate(data['steps'], 1):
        state = 'is-complete' if index < current else 'is-current' if index == current else ''
        items.append(render('components/progress-indicator/item.html', {
            'state_class': state, 'index': index, 'title': step['title'], 'description': step['description'],
            'current_attribute': ' aria-current="step"' if index == current else '',
        }, ('current_attribute',)))
    active = data['steps'][current - 1]
    progress = render('components/progress-indicator/template.html', {
        'items': ''.join(items), 'current_index': current, 'total': len(data['steps']),
        'current_title': active['title'], 'current_description': active['description'],
    }, ('items',))
    rows = ''.join('<div class="form-template__row" data-field-variant="{}">{}{}</div>'.format(html.escape(variant, quote=True), _field(variant, True), _field(variant, False)) for variant in data['variants'])
    required_note = '<p class="form-page__required-note"><span aria-hidden="true">*</span> {}</p>'.format(html.escape(data['required_note']))
    page_intro = render_page_intro(page, render, variant='featured', extra_content_markup=required_note)
    return render('sections/form/template.html', {
        'page_intro': page_intro, 'progress': progress, 'current_index': current, 'fields': rows,
        'status': f'الخطوة {current} من {len(data["steps"])}: {active["title"]}',
    }, ('page_intro', 'progress', 'fields'))
