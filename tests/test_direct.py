from bigcommerce import *

import unittest
import vcr
from nose.plugins.attrib import attr

my_vcr = vcr.VCR(match_on = ['url', 'method', 'body']) # headers too?

@attr('broken')
class TestDirectCalls(unittest.TestCase):
    """
    Test using direct calls through Connection
    """
    
    def setUp(self):
        host = 'somethingequallycreative-jackie-huynh.dev1.syd1bc.bigcommerce.net'
        user = 'admin'
        api_key = 'a2e777fbb2d98fd04461d700463a8ed71782e475'
        self.connection = Connection(host, '/api/v2', (user, api_key))
    
    def test_get_products(self):
        with my_vcr.use_cassette('vcr/test_direct/get_products.yaml'):
            products = self.connection.get('/products', {'limit':5})
            self.assertTrue(len(products) == 5)
            
            expected = [(32, "Logitech Pure-Fi Speakers"),
                        (33, "[Sample] Anna, multi-colored bangles"),
                        (34, "[Sample] Harper, tan leather woven belt"),
                        (35, "[Sample] Anna, bright single bangles")]
            for i, vals in enumerate(expected):
                self.assertTrue(products[i]['id'] == vals[0], "{} {}".format(products[i]['id'], vals[0]))
                self.assertTrue(products[i]['name'] == vals[1])
            
            speakers = self.connection.get('/products/32')
              
            new_price = float(speakers['price']) * 0.8
            new_desc = speakers['description'] + " v2"
            updates = {'price' : new_price,
                       'description' : new_desc
                       }
            self.connection.update('/products/32', updates)
            
            speakers = self.connection.get('/products/32')
            self.assertTrue(float(speakers['price']) == round(new_price, 4))
            self.assertTrue(speakers['description'] == new_desc)
#             
#     def test_manip_coupons(self):
#         with my_vcr.use_cassette('vcr/test1.yaml'):
#             coupons = self.connection.get('/coupons')
#             expected = [(1, "5% off order total"),
#                         (2, "10% off order total"),
#                         (3, "Free shipping"),
#                         (4, "$5 off shipping")]
#             for i, val in enumerate(expected):
#                 self.assertTrue(coupons[i]['id'] == val[0])
#                 self.assertTrue(coupons[i]['name'] == val[1])
#                  
#             new_c = self.connection.create('/coupons', {'name' : "70% off order total", 
#                                                       'amount' : 70.00, 
#                                                       'code' : "HT75", 
#                                                       'type' : "percentage_discount", 
#                                                       'applies_to' : {'entity' : "products", 'ids' : [32]}})
#             new_c1 = self.connection.create('/coupons', {'name' : "60% off order total", 
#                                                       'amount' : 60.00, 
#                                                       'code' : "HT85", 
#                                                       'type' : "percentage_discount", 
#                                                       'applies_to' : {'entity' : "products", 'ids' : [32]}})
#             coupons = self.connection.get('/coupons')
#             expected.append((132, "70% off order total"))
#             expected.append((133, "60% off order total"))
#             for i, val in enumerate(expected):
#                 self.assertTrue(coupons[i]['id'] == val[0])
#                 self.assertTrue(coupons[i]['name'] == val[1])
#              
#             self.connection.delete('/coupons/{}'.format(new_c['id']))
#             self.connection.delete('/coupons/{}'.format(new_c1['id']))
#              
#             coupons = self.connection.get('/coupons')
#             expected.pop()
#             expected.pop()
#             for i, val in enumerate(expected):
#                 self.assertTrue(coupons[i]['id'] == val[0])
#                 self.assertTrue(coupons[i]['name'] == val[1])
#                  
#             try:
#                 c = self.connection.get('/coupons/999999')
#                 self.assertTrue(False, "didn't catch exception")
#             except ClientRequestException as e:
#                 self.assertTrue(True)
#                  
#     def test_subresources(self):
#         with my_vcr.use_cassette('vcr/test3.yaml'):
#             countries = self.connection.get('/countries', {'limit':2, 'page':3})
#             expected = [(5, "AND", "Andorra"),
#                         (6, "AGO", "Angola")]
#             self.assertTrue(len(countries) == 2)
#             for i, val in enumerate(expected):
#                 self.assertTrue(countries[i]['id'] == val[0])
#                 self.assertTrue(countries[i]['country_iso3'] == val[1])
#                 self.assertTrue(countries[i]['country'] == val[2])
#              
#             murrica = self.connection.get('/countries/226')
#             self.assertTrue(murrica['country_iso3'] == "USA", "{}".format(murrica['country_iso3']))
#              
#             expected = [(1, "AL", "Alabama"),
#                         (2, "AL", "Alaska"),
#                         (3, "AS", "American Samoa"),
#                         (4, "AZ", "Arizona"),
#                         (5, "AR", "Arkansas")]
#             states = self.connection.get('/countries/226/states', {'limit':5})
#             self.assertTrue(len(states) == 5)
#             for i, val in enumerate(expected):
#                 self.assertTrue(states[i]['id'] == val[0])
#              
#     def test_subresources2(self):
#         with my_vcr.use_cassette('vcr/test4.yaml'):
#             something = self.connection.get('/products/33')
#              
#             expected = [(239, 33, "sample_images/cocolee_anna_92851__19446.jpg", None),
#                         (240, 33, "sample_images/cocolee_anna_92852__63752.jpg", None),
#                         (270, 33, "j/603/SandstoneUSGOV__36595.jpg", "dont worry im a doctor")]
#             imgs = self.connection.get('/products/{}/images'.format(something['id']))            
#              
#             for i, val in enumerate(expected):
#                 self.assertTrue(imgs[i]['id'] == val[0])
#                 self.assertTrue(imgs[i]['product_id'] == val[1])
#                 self.assertTrue(imgs[i]['image_file'] == val[2])
#                 self.assertTrue(imgs[i]['description'] == val[3])
#              
#             img = imgs[len(imgs) -1]
#             img_data = {'image_file' : "http://upload.wikimedia.org/wikipedia/commons/6/61/SandstoneUSGOV.jpg",
#                         'is_thumbnail' : img['is_thumbnail'],
#                         'sort_order' : img['sort_order'],
#                         'description' : "dont worry im a doctor"}
#             self.connection.update('/products/images/{}'.format(img['id']), {'description' : "NOPE"})
#              
#             imgs = self.connection.get('/products/33/images') 
#             expected[len(imgs) -1] = (270, 33, "j/603/SandstoneUSGOV__36595.jpg", "NOPE")
#             for i, val in enumerate(expected):
#                 self.assertTrue(imgs[i]['id'] == val[0])
#                 self.assertTrue(imgs[i]['product_id'] == val[1])
#                 self.assertTrue(imgs[i]['image_file'] == val[2])
#                 self.assertTrue(imgs[i]['description'] == val[3])
#               
#             self.connection.update('/products/33/images/{}'.format(img['id']),
#                            {'description' : img_data['description'] or "itdoesntlikenullvalues"})
#             imgs = self.connection.get('/products/33/images')
#             expected[len(imgs) -1] = (270, 33, "j/603/SandstoneUSGOV__36595.jpg", "dont worry im a doctor")    
#             for i, val in enumerate(expected):
#                 self.assertTrue(imgs[i]['id'] == val[0])
#                 self.assertTrue(imgs[i]['product_id'] == val[1])
#                 self.assertTrue(imgs[i]['image_file'] == val[2])
#                 self.assertTrue(imgs[i]['description'] == val[3])
#              
#             self.connection.delete('/products/33/images/{}'.format(img['id']))
#             imgs = self.connection.get('/products/33/images')
#             expected.pop()
#             self.assertTrue(len(imgs) == 2)
#             for i, val in enumerate(expected):
#                 self.assertTrue(imgs[i]['id'] == val[0])
#                 self.assertTrue(imgs[i]['product_id'] == val[1])
#                 self.assertTrue(imgs[i]['image_file'] == val[2])
#                 self.assertTrue(imgs[i]['description'] == val[3])
#                   
#             self.connection.create('/products/{}/images'.format(something['id']), img_data)
#             imgs = self.connection.get('/products/33/images')
#             expected.append((271, 33, "k/069/SandstoneUSGOV__85011.jpg", "dont worry im a doctor"))
#             for i, val in enumerate(expected):
#                 self.assertTrue(imgs[i]['id'] == val[0])
#                 self.assertTrue(imgs[i]['product_id'] == val[1])
#                 self.assertTrue(imgs[i]['image_file'] == val[2])
#                 self.assertTrue(imgs[i]['description'] == val[3])
