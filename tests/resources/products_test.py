from bigcommerce import *

import unittest
import vcr

class TestProducts(unittest.TestCase):
    
    def setUp(self):
        STORE_HOST = 'store-1r2j4mfe.bcapp.dev'
        STORE_TOKEN = 'e49b7ab884b2ed5069a687ff08f5bb23'
        STORE_USERID = 'admin'
        self.client = Client(STORE_HOST, STORE_TOKEN, STORE_USERID)
    
    def test_get_products(self):
        with vcr.use_cassette('vcr/test0.yaml'):

            filters = self.client.Products.filters()

            for product in self.client.Products.enumerate(start=10, limit=10, query=filters):
                print product.images

            # products = Products.enumerate(limit=20)
            # self.assertTrue(len(products) == 20)
            
            # expected = [(32, "Logitech Pure-Fi Speakers"),
            #             (33, "[Sample] Anna, multi-colored bangles"),
            #             (34, "[Sample] Harper, tan leather woven belt"),
            #             (35, "[Sample] Anna, bright single bangles")]
            # for i, vals in products:
            #     self.assertTrue(products[i].id == vals[0], "{} {}".format(products[i].id, vals[0]))
            #     self.assertTrue(products[i].name == vals[1])
            
            # speakers = Products.get_by_id(32)
            # self.assertTrue(speakers.price == "300.9500")
              
            # speakers.name = "Logitech Pure-Fi Speakers"
            # speakers.price = 200.95
            # speakers.description = "This is a description"
            # speakers.update()

            # self.assertTrue(speakers.id == 32)
            # self.assertTrue(speakers.price == "200.9500")
            # speakers = Products.get_by_id(32)
            # self.assertTrue(speakers.price == "200.9500")
