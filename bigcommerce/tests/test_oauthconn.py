import unittest
import vcr

import bigcommerce as api


myvcr = vcr.VCR(match_on=['method', 'path', 'headers', 'body'])


class TestOAuthConnection(unittest.TestCase):
    """Test the OAuth helper methods"""

    def test_registration(self):
        """Fetch token, then use it to make a request."""
        with myvcr.use_cassette('fixtures/vcr/register_request.yml'):
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
            # (ignore this)  = 18828145  # since we made the request locally
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
        self.assertTrue(user_data != False)  # otherwise verification has failed
        self.assertTrue(user_data['user']['id'] == 72)
        self.assertTrue(user_data['user']['email'] == "jackie.huynh@bigcommerce.com")


class TestOAuthCRUD(unittest.TestCase):
    """Test CRUD operations with oauth connection"""

    def setUp(self):
        cid = "iu4mk0piq5r664w687c1d6lv84mz1s9"
        store_hash = "lctvh5wm"
        token = "7ij6bj9q78g0hu8xusumgj5dss70t8b"
        self.conn = api.OAuthConnection(cid, store_hash, token, host='18828145.ngrok.com')

    def test_get(self):
        """Retrieving resources with filters, getting specific resources."""
        with myvcr.use_cassette('fixtures/vcr/test_get.yaml'):
            products = [(p.id, p.name, p.price) for p in self.conn.get('products', limit=4, page=2)]
            expected = [(36, '[Sample] Benjamin Button, red petty coat', 110),
                        (37, "[Sample] Levi's, blue denim womens shirt", 29),
                        (38, '[Sample] Maccas, colorful cardigans', 39),
                        (39, '[Sample] Burberry, Fuschia knitted sweater', 189)]
            self.assertTrue(len(products) == len(expected))
            for i, data in enumerate(expected):
                self.assertTrue(products[i][0] == data[0])
                self.assertTrue(products[i][1] == data[1])
                self.assertTrue(float(products[i][2]) == data[2])

            products = [(p.id, p.name, p.price) for p in self.conn.get('products', limit=4, min_price=100.90)]
            expected = [(36, '[Sample] Benjamin Button, red petty coat', '110.0000'),
                        (39, '[Sample] Burberry, Fuschia knitted sweater', '189.0000'),
                        (47, '[Sample] Ben Sherman, BW striped long sleeve tee', '110.0000'),
                        (48, '[Sample] Marcs, power to the paisley mens shirt', '112.0000')]
            self.assertTrue(len(products) == len(expected))
            for i, data in enumerate(expected):
                self.assertTrue(products[i][0] == data[0])
                self.assertTrue(products[i][1] == data[1])
                self.assertTrue(products[i][2] == data[2])
                self.assertTrue(float(data[2]) >= 100.90)

            p = self.conn.get('products', 37)
            expected = (37, "[Sample] Levi's, blue denim womens shirt", 29.0)
            self.assertTrue(p.id == expected[0])
            self.assertTrue(p.name == expected[1])
            self.assertTrue(float(p.price) == expected[2])

    def test_update(self):
        """Updating resources"""
        with myvcr.use_cassette('fixtures/vcr/test_update.yaml'):
            p = self.conn.get('products', 45)
            expected = (45, "Something Completely Different", 29.0)
            self.assertTrue(expected[0] == p.id)
            self.assertTrue(expected[1] == p.name)
            self.assertTrue(expected[2] == float(p.price))

            different_p = self.conn.update('products', p.id,
                                           {'name': "Something Cool"})  # returns new res
            expected = (45, "Something Cool", 29.0)
            self.assertTrue(expected[0] == different_p.id)
            self.assertTrue(expected[1] == different_p.name)
            self.assertTrue(expected[2] == float(different_p.price))

            different_p = self.conn.get('products', 45)  # retrieve again to prove it has changed
            self.assertTrue(different_p.name != p.name)
            self.assertTrue(expected[0] == different_p.id)
            self.assertTrue(expected[1] == different_p.name)
            self.assertTrue(expected[2] == float(different_p.price))

            old_p = self.conn.update('products', p.id, {'name': p.name})  # haven't bound p to anything - local dict
            expected = (45, "Something Completely Different", 29.0)
            self.assertTrue(expected[0] == old_p.id)
            self.assertTrue(expected[1] == old_p.name)
            self.assertTrue(expected[2] == float(old_p.price))
            self.assertTrue(old_p.name != different_p.name)
            self.assertTrue(old_p.name == p.name)

            old_p = self.conn.get('products', 45)  # retrieve again, just in case
            self.assertTrue(expected[0] == old_p.id)
            self.assertTrue(expected[1] == old_p.name)
            self.assertTrue(expected[2] == float(old_p.price))

    def test_create_delete(self):
        """Creating a resource, then deleting it."""
        with vcr.use_cassette('fixtures/vcr/test_create_delete.yaml'):
            expected = [{'amount': '5.0000',
                         'code': '3E13CB68AAAEBE5',
                         'name': '5% off order total'},
                        {'amount': u'10.0000',
                         'code': u'9DB19A3F921355C',
                         'name': u'10% off order total'},
                        {'amount': u'0.0000',
                         'code': u'FCA407528841E55',
                         'name': u'Free shipping'},
                        {'amount': u'5.0000',
                         'code': u'CFF623E6B5219CA',
                         'name': u'$5 off shipping'}]
            coupons = self.conn.get('coupons')
            for i, data in enumerate(expected):
                self.assertTrue(coupons[i].amount == data['amount'])
                self.assertTrue(coupons[i].code == data['code'])
                self.assertTrue(coupons[i].name == data['name'])
            new_data = {'amount': 11.0,
                        'code': "SOMETHINGRANDOM1234",
                        'name': "Hi Im Coupon",
                        'type': "percentage_discount",
                        'applies_to': {'entity': "products", 'ids': [37]}}
            self.conn.create('coupons', new_data)
            new_data['amount'] = "11.0000"
            expected.append(new_data)
            coupons = self.conn.get('coupons')
            for i, data in enumerate(expected):
                self.assertTrue(coupons[i].amount == data['amount'])
                self.assertTrue(coupons[i].code == data['code'])
                self.assertTrue(coupons[i].name == data['name'])
            c = self.conn.get('coupons', code=new_data['code'])[0]
            self.conn.delete('coupons/{}'.format(c.id))
            expected.pop()
            coupons = self.conn.get('coupons')
            for i, data in enumerate(expected):
                self.assertTrue(coupons[i].amount == data['amount'])
                self.assertTrue(coupons[i].code == data['code'])
                self.assertTrue(coupons[i].name == data['name'])