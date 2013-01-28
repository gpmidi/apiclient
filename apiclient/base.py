import warnings

from urllib3 import connection_from_url
from urllib import urlencode

from .serializers import get_serializer


class APIClient(object):
    BASE_URL = 'http://localhost:5000/'
    TIMEOUT = 1
    
    def __init__(self, rate_limit_lock = None, cache = None):
        self.cache = cache
        self.rate_limit_lock = rate_limit_lock
        self.connection_pool = self._make_connection_pool(self.BASE_URL, self.TIMEOUT)

    def __getstate__(self):
        # ConnectionPool is not pickeable, so we remove it
        state = self.__dict__.copy()
        del state['connection_pool']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.connection_pool = self._make_connection_pool(self.BASE_URL, self.TIMEOUT)

    def _make_connection_pool(self, url, timeout = 1):
        return connection_from_url(url, timeout = timeout)

    def _compose_url(self, method, path, fields = None):
        return (method, self.BASE_URL + path, fields)

    def _handle_response(self, response):
        serializer = get_serializer(response.headers.get('content-type'))
        return serializer.loads(response.data)

    def _create_keys(self, method, url, fields = {}):
        fields = fields.items()
        fields.sort(lambda a, b: cmp(a[0], b[0]))
        return [
                url,
                ] + map(
                        lambda x: "-".join(x),
                        fields
                        )

    def _request(self, method, path, fields = None, useCache = False):
        request_args = self._compose_url(method, path, fields)
        
        if self.cache and useCache:
            r = self.cache.get(
                               keys = self._create_keys(
                                                        method = request_args[0],
                                                        url = request_args[1],
                                                        fields = request_args[2],
                                                        ),
                               )
            if r is not None:
                return r

        self.rate_limit_lock and self.rate_limit_lock.acquire()
        r = self.connection_pool.request(*request_args)

        return self._handle_response(r)

    def call(self, path, **fields):
        warnings.warn('APIClient call() is deprecated; use get() instead.',
                      PendingDeprecationWarning)
        return self.get(path, **fields)

    def delete(self, path, **fields):
        return self._request('DELETE', path, fields = fields)

    def get(self, path, **fields):
        return self._request('GET', path, fields = fields, useCache = True)
    
    def getNoCache(self, path, **fields):
        return self._request('GET', path, fields = fields, useCache = False)

    def patch(self, path, **fields):
        return self._request('PATCH', path, fields = fields)

    def post(self, path, **fields):
        return self._request('POST', path, fields = fields)

    def put(self, path, **fields):
        return self._request('PUT', path, fields = fields)


class APIClient_SharedSecret(APIClient):
    API_KEY_PARAM = 'key'

    def __init__(self, api_key = None, *args, **kwargs):
        super(APIClient_SharedSecret, self).__init__(*args, **kwargs)
        self.api_key = api_key

    def _compose_url(self, method, path, fields = None):
        p = {}
        if self.api_key is not None:
            p[self.API_KEY_PARAM] = self.api_key

        if fields:
            p.update(fields)

        return (method, self.BASE_URL + path, p)
