from bigcommerce import *

import unittest
import vcr

# import logging, sys
# logging.basicConfig(level=logging.DEBUG, 
#                     stream=sys.stdout,
#                     format='%(asctime)s %(levelname)-8s[%(name)s] %(message)s',
#                     datefmt='%m/%d %H:%M:%S')

class TestProductsBasic(unittest.TestCase):
    
    def setUp(self):
        STORE_HOST = 'somethingequallycreative-jackie-huynh.dev1.syd1bc.bigcommerce.net' #'store-1r2j4mfe.bcapp.dev'
        STORE_TOKEN = 'a2e777fbb2d98fd04461d700463a8ed71782e475'
        STORE_USERID = 'admin'
        self.client = Client(STORE_HOST, STORE_TOKEN, STORE_USERID)
    
    def test_get_products(self):
        with vcr.use_cassette('vcr/products_test.yaml'):
            filters = self.client.Products.filters()
            for product in self.client.Products.enumerate(start=10, limit=10, query=filters):
                print product.id, product.name, product.images

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProductsBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)