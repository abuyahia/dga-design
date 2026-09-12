"""Validate and render the reusable error-state section."""


def validate_error_state(page, paths):
    data = page.get('error_state')
    if not isinstance(data, dict):
        raise ValueError('Error state data must be an object')
    for key in ('code', 'title', 'description', 'action_href', 'action_label'):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f'Error state requires nonempty {key}')
    if not data['code'].isdigit() or len(data['code']) != 3:
        raise ValueError('Error state code must contain three digits')
    if data['action_href'].partition('#')[0] not in paths:
        raise ValueError('Error state action must target a generated page')


def render_error_state(page, render):
    data = page['error_state']
    error_state_markup = render('sections/error-state/template.html', {
        'code': data['code'],
        'error_title': data['title'],
        'error_description': data['description'],
        'action_href': data['action_href'],
        'action_label': data['action_label'],
    })
    return render('templates/error/template.html', {
        'error_state_markup': error_state_markup,
    }, ('error_state_markup',))
