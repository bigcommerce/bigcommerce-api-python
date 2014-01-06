import unittest
import vcr

import bigcommerce as api


class TestOAuthConnection(unittest.TestCase):

    def test_registration(self):
        """Fetch token, then use it to make a request."""
        with vcr.use_cassette('fixtures/vcr/register_request.yml', match_on=['method', 'url', 'headers', 'body']):
            # info from registration, etc
            code = '9tqwwadit8bc3h2lj37kmiv2bq0804v'
            client_id = 'iu4mk0piq5r664w687c1d6lv84mz1s9'
            redirect_uri = 'https://61798136.ngrok.com/auth/callback'
            context = 'stores/65j86n8y'
            scope = 'store_v2_orders store_v2_products store_v2_customers store_v2_content ' \
                    'store_v2_marketing store_v2_information_read_only ' \
                    'store_v2_shipping_read_only users_basic_information'
            client_secret = 'ntb1kcxa1do55wf0h25ps7h94fnsoi6'

            conn = api.OAuthConnection(client_id,
                                       context.split('/')[1])
            token = conn.fetch_token(client_secret, code, context, scope, redirect_uri,
                                     'https://login-dev.bigcommerceapp.com/oauth2/token')
            # token has been received and parsed correctly
            expected_token = '1qntu1f1fpyqw20prl3spstolfjpisk'
            self.assertTrue(token['access_token'] == expected_token)
            self.assertTrue(token['user']['id'] == 72)
            # session headers updated properly
            self.assertTrue(conn._session.headers.get('X-Auth-Client') == client_id)
            self.assertTrue(conn._session.headers.get('X-Auth-Token') == token['access_token'])
            # send our request and check the response
            conn.host = '18828145.ngrok.com'  # since we made the request locally
            products = conn.get('products', limit=5)
            expected = [(32, '[Sample] Tomorrow is today, Red printed scarf', '89.0000'),
                        (33, u'[Sample] Anna, multi-colored bangles', u'59.0000'),
                        (34, u'[Sample] Harper, tan leather woven belt', u'49.0000'),
                        (35, u'[Sample] Anna, bright single bangles', u'29.0000'),
                        (36, u'[Sample] Benjamin Button, red petty coat', u'110.0000')]
            self.assertTrue(len(products) == len(expected))
            for i, data in enumerate(expected):
                self.assertTrue(products[i].id == data[0])
                self.assertTrue(products[i].name == data[1])
                self.assertTrue(products[i].price == data[2])

    def test_verify(self):
        """Decode and verify signed payload."""
        payload = "eyJ1c2VyIjp7ImlkIjo3MiwiZW1haWwiOiJqYWNraWUuaHV5bmh" \
                  "AYmlnY29tbWVyY2UuY29tIn0sInN0b3JlX2hhc2giOiJsY3R2aD" \
                  "V3bSIsInRpbWVzdGFtcCI6MTM4OTA1MDMyNy42NTc5NjI2fQ==." \
                  "ZTViYzAzNTM2MGFjM2M2YTVkZjFmNzFlYTk4NTY1ODZiMzkxODZmZDExZTdjZGFmOGEzN2E3YTEzNGQ0MmExYw=="
        client_secret = 'ntb1kcxa1do55wf0h25ps7h94fnsoi6'
        user_data = api.OAuthConnection.verify_payload(payload, client_secret)
        self.assertTrue(user_data != False)
        self.assertTrue(user_data['user']['id'] == 72)
        self.assertTrue(user_data['user']['email'] == "jackie.huynh@bigcommerce.com")
