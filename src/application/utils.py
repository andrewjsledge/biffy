from application import app
import re

us_phone_number_re = re.compile(r'^(?:1-?)?(\d{3})[-\.]?(\d{3})[-\.]?(\d{4})$')

def register_application_web_route(view, endpoint, url, view_args={}, pk='id',
                                   pk_type='int'):
    view_func = view.as_view(endpoint, **view_args)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func,
        methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
        methods=['GET', 'POST'])

def register_application_api_route(view, endpoint, url, view_args={}, pk='id',
                           pk_type='int'):
    view_func = view.as_view(endpoint, **view_args)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func,
        methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
        methods=['GET', 'PUT', 'DELETE'])

def register_module_web_route(module, view, endpoint, url, view_args={}, pk='id',
                              pk_type='int'):
    view_func = view.as_view(endpoint, **view_args)
    module.add_url_rule(url, defaults={pk: None}, view_func=view_func,
        methods=['GET',])
    module.add_url_rule(url, view_func=view_func, methods=['POST',])
    module.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
        methods=['GET', 'POST'])

def register_module_api_route(module, view, endpoint, url, view_args={},
                             pk='id', pk_type='int'):
    view_func = view.as_view(endpoint, **view_args)
    module.add_url_rule(url, defaults={pk: None}, view_func=view_func,
        methods=['GET',])
    module.add_url_rule(url, view_func=view_func, methods=['POST',])
    module.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
        methods=['GET', 'PUT', 'DELETE'])

def is_us_phone_number(phone_text):
    return us_phone_number_re.search(phone_text)