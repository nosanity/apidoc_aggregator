import logging
from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.utils import timezone

import requests


def parse_docs(service):
    if not service.docs_url:
        return
    try:
        resp = requests.get(service.docs_url, timeout=settings.CONNECTION_TIMEOUT)
        assert resp.ok, '{} returned {}'.format(service.docs_url, resp.status_code)
        data = resp.json()
        service.json_data = data
        service.last_update = timezone.now()
        service.save(update_fields=['json_data', 'last_update'])
    except Exception:
        logging.exception('Failed to parse documentation at %s', service.docs_url)
        return False
    return service


def transform_documentation(service, request):
    """
    преобразование документации с заменой урлов и сокрытием внутренних ручек апи
    """
    data = service.json_data
    gateway_url = urlparse(settings.API_GATEWAY_URL)
    base_path = data.get('basePath')
    if base_path == '/':
        base_path = None
    data.update({
        'basePath': '/',
        'info': {
            'title': 'Api',
        },
        'host': gateway_url.netloc,
        'schemes': [gateway_url.scheme]
    })
    security_definitions = data.get('securityDefinitions') or {}
    security_overrides = service.security_overrides or {}
    security_definitions = {k: security_overrides.get(k, v) for k, v in security_definitions.items()}
    paths = {}
    service_paths = data.get('paths') or {}
    for path, values in service_paths.items():
        if values.pop('swaggerInnerApi', False) and not user_can_see_service_docs(service, request.user):
            continue
        paths.update(get_paths(path, values, base_path, service))
    data.update({
        'securityDefinitions': security_definitions,
        'paths': paths,
    })
    return data


def user_can_see_service_docs(service, user):
    """
    может ли пользователь видеть документацию к внутренним ручкам апи
    """
    if user.is_authenticated and user.is_staff:
        return True
    return False


def get_paths(url, data, base_api_path, service):
    http_methods = ('get', 'post', 'put', 'patch', 'delete', 'head', 'options')
    base_path = list(urlparse(url))
    base_path[0] = ''
    base_path[1] = ''
    base_data = {k: v for k, v in data.items() if k not in http_methods}
    paths = {}
    for method, method_data in data.items():
        if method not in http_methods:
            continue
        security = get_security_keys(method_data.get('security'))
        names = sorted(set(security) & set(service.prefixes.keys() if service.prefixes else []))
        service_prefixes = service.prefixes or {}
        if names:
            service_prefix = service_prefixes[names[0]]
        else:
            service_prefix = service_prefixes.get('', '')
        path = base_path[:]
        ends_with_slash = path[2].endswith('/')
        path[2] = '/'.join(map(lambda x: x.strip('/'), filter(None, [service_prefix, base_api_path, path[2]])))
        path[2] = '/{}{}'.format(path[2], '/' if ends_with_slash else '')
        path = urlunparse(path)
        if path not in paths:
            paths[path] = base_data.copy()
        paths[path][method] = method_data
    return paths


def get_security_keys(data):
    return [list(i.keys())[0] for i in data or []]
