import json

from urllib3 import connection_from_url
from urllib import urlencode


class APIClient(object):
    BASE_URL = 'http://localhost:5000/'

    def __init__(self, rate_limit_lock=None):
        self.rate_limit_lock = rate_limit_lock
        self.connection_pool = self._make_connection_pool(self.BASE_URL)

    def _make_connection_pool(self, url):
        return connection_from_url(url)

    def _compose_url(self, method, url, fields=None):
        return (method, self.BASE_URL + path, fields)

    def _handle_response(self, response):
        return json.loads(response.data)

    def _request(self, method, path, fields=None):
        self.rate_limit_lock and self.rate_limit_lock.acquire()
        r = self.connection_pool.request(*self._compose_url(method, path, fields))

        return self._handle_response(r)

    def call(self, path, **fields):
        return self._request('GET', path, fields=fields)


class APIClient_SharedSecret(APIClient):
    API_KEY_PARAM = 'key'

    def __init__(self, api_key=None, *args, **kw):
        super(APIClient_SharedSecret, self).__init__(*args, **kw)
        self.api_key = api_key

    def _compose_url(self, method, path, fields=None):
        p = {}
        if self.api_key is not None:
            p[self.API_KEY_PARAM] = self.api_key

        if fields:
            p.update(fields)

        return (method, self.BASE_URL + path, p)
