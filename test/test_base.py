import unittest

from apiclient import APIClient, APIClient_SharedSecret, RateLimiter


class TestAPIClient(unittest.TestCase):
    class FacebookAPI(APIClient):
        BASE_URL = 'https://graph.facebook.com/'

    class FacebookAPI_SharedSecret(APIClient_SharedSecret):
        BASE_URL = 'https://graph.facebook.com/'
        API_KEY_PARAM = 'metadata'

    def test_facebook_client(self):
        api = self.FacebookAPI()
        r = api.call('/facebook')
        self.assertTrue('username' in r)

    def test_facebook_client_share_secret(self):
        api = self.FacebookAPI_SharedSecret('true')
        r = api.call('/facebook', fields='username')
        self.assertTrue('username' in r)

    def test_facebook_client_rate_limit(self):
        rate = RateLimiter(max_messages=1, every_seconds=2)
        api = self.FacebookAPI(rate_limit_lock=rate)
        r = api.call('/facebook')
        self.assertTrue('username' in r)

        # Blocks for 2 sec
        r = api.call('/facebook')
        self.assertTrue('username' in r)