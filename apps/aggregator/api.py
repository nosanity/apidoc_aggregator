import logging
from django.conf import settings
import requests


class ApiError(Exception):
    pass


class BadApiResponse(ApiError):
    pass


class BaseApi:
    name = ''
    base_url = ''
    authorization = {}
    verify = True

    def update_kwargs(self, kwargs):
        """
        добавление параметров авторизации в запрос
        """
        self._populate_kwargs(kwargs, self.authorization)

    def _populate_kwargs(self, kwargs, upd_dict):
        for key, item in upd_dict.items():
            if key in kwargs and isinstance(kwargs[key], dict):
                kwargs[key].update(item)
            else:
                kwargs[key] = item

    def request(self, url, method='GET', **kwargs):
        if not url.startswith(('http://', 'https://')):
            url = '{}{}'.format(self.base_url, url)
        kwargs.setdefault('timeout', settings.CONNECTION_TIMEOUT)
        self.update_kwargs(kwargs)
        if not self.verify:
            kwargs.setdefault('verify', False)
        try:
            return_json = kwargs.pop('return_json', True)
            resp = requests.request(method, url, **kwargs)
            assert resp.ok, 'status_code %s' % resp.status_code
            if return_json:
                return resp.json()
            return resp.content
        except (ValueError, TypeError, AssertionError):
            logging.exception('Unexpected %s response for url %s' % (self.name, url))
            raise BadApiResponse
        except Exception:
            logging.exception('%s connection error' % self.name)
            raise ApiError


class SSOApi(BaseApi):
    name = 'sso'
    base_url = settings.SSO_UNTI_URL.rstrip('/')
    authorization = {'headers': {'x-sso-api-key': settings.SSO_API_KEY}}

    def check_oauth_client(self, redirect_uri):
        return self.request('/api/register-oauth-client/', params={'redirect_uri': redirect_uri})

    def create_oauth_client(self, redirect_uri, email):
        return self.request('/api/register-oauth-client/', method='POST', json={
            'redirect_uri': redirect_uri,
            'email': email,
        }, return_json=False)
