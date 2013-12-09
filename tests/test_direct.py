from bigcommerce import *

import unittest
import vcr

class TestDirectCalls(unittest.TestCase):
    """
    Almost exactly the same as TestGeneralCRUD, but uses direct 
    (through Connection) calls.
    """
    
    def setUp(self):
        Connection.host = 'somethingequallycreative-jackie-huynh.dev1.syd1bc.bigcommerce.net'
        Connection.user = 'admin'
        Connection.api_key = 'a2e777fbb2d98fd04461d700463a8ed71782e475'
    
    def test_get_products(self):
        with vcr.use_cassette('vcr/test0.yaml'):
            products = Connection.get('/products.json', limit=20)
            self.assertTrue(len(products) == 20)
            
            expected = [(32, "Logitech Pure-Fi Speakers"),
                        (33, "[Sample] Anna, multi-colored bangles"),
                        (34, "[Sample] Harper, tan leather woven belt"),
                        (35, "[Sample] Anna, bright single bangles")]
            for i, vals in enumerate(expected):
                self.assertTrue(products[i]['id'] == vals[0], "{} {}".format(products[i]['id'], vals[0]))
                self.assertTrue(products[i]['name'] == vals[1])
            
            speakers = Connection.get('/products/32.json')
            self.assertTrue(speakers['price'] == "300.9500")
              
            updates = {'name' : "Logitech Pure-Fi Speakers",
                       'price' : 200.95,
                       'description' : "This is a description"
                       }
            Connection.put('/products/32.json', updates)
            
            speakers = Connection.get('/products/32.json')
            self.assertTrue(speakers['price'] == "200.9500")
            
    def test_manip_coupons(self):
        with vcr.use_cassette('vcr/test1.yaml'):
            coupons = Connection.get('/coupons.json')
            expected = [(1, "5% off order total"),
                        (2, "10% off order total"),
                        (3, "Free shipping"),
                        (4, "$5 off shipping")]
            for i, val in enumerate(expected):
                self.assertTrue(coupons[i]['id'] == val[0])
                self.assertTrue(coupons[i]['name'] == val[1])
                
            new_c = Connection.post('/coupons.json', {'name' : "70% off order total", 
                                                      'amount' : 70.00, 
                                                      'code' : "HT75", 
                                                      'type' : "percentage_discount", 
                                                      'applies_to' : {'entity' : "products", 'ids' : [32]}})
            new_c1 = Connection.post('/coupons.json', {'name' : "60% off order total", 
                                                      'amount' : 60.00, 
                                                      'code' : "HT85", 
                                                      'type' : "percentage_discount", 
                                                      'applies_to' : {'entity' : "products", 'ids' : [32]}})
            coupons = Connection.get('/coupons.json')
            expected.append((132, "70% off order total"))
            expected.append((133, "60% off order total"))
            for i, val in enumerate(expected):
                self.assertTrue(coupons[i]['id'] == val[0])
                self.assertTrue(coupons[i]['name'] == val[1])
            
            Connection.delete('/coupons/{}.json'.format(new_c['id']))
            Connection.delete('/coupons/{}.json'.format(new_c1['id']))
            
            coupons = Connection.get('/coupons.json')
            expected.pop()
            expected.pop()
            for i, val in enumerate(expected):
                self.assertTrue(coupons[i]['id'] == val[0])
                self.assertTrue(coupons[i]['name'] == val[1])
                
            try:
                c = Connection.get('/coupons/999999.json')
                self.assertTrue(False, "didn't catch exception")
            except ClientRequestException as e:
                self.assertTrue(True)
                
    def test_subresources(self):
        with vcr.use_cassette('vcr/test3.yaml'):
            countries = Connection.get('/countries.json', limit=2, page=3)
            expected = [(5, "AND", "Andorra"),
                        (6, "AGO", "Angola")]
            self.assertTrue(len(countries) == 2)
            for i, val in enumerate(expected):
                self.assertTrue(countries[i]['id'] == val[0])
                self.assertTrue(countries[i]['country_iso3'] == val[1])
                self.assertTrue(countries[i]['country'] == val[2])
            
            murrica = Connection.get('/countries/226.json')
            self.assertTrue(murrica['country_iso3'] == "USA", "{}".format(murrica['country_iso3']))
            
            expected = [(1, "AL", "Alabama"),
                        (2, "AL", "Alaska"),
                        (3, "AS", "American Samoa"),
                        (4, "AZ", "Arizona"),
                        (5, "AR", "Arkansas")]
            states = Connection.get('/countries/226/states.json', limit=5)
            self.assertTrue(len(states) == 5)
            for i, val in enumerate(expected):
                self.assertTrue(states[i]['id'] == val[0])
            
    def test_subresources2(self):
        with vcr.use_cassette('vcr/test4.yaml'):
            something = Connection.get('/products/33.json')
            
            expected = [(239, 33, "sample_images/cocolee_anna_92851__19446.jpg", None),
                        (240, 33, "sample_images/cocolee_anna_92852__63752.jpg", None),
                        (270, 33, "j/603/SandstoneUSGOV__36595.jpg", "dont worry im a doctor")]
            imgs = Connection.get('/products/{}/images.json'.format(something['id']))            
            
            for i, val in enumerate(expected):
                self.assertTrue(imgs[i]['id'] == val[0])
                self.assertTrue(imgs[i]['product_id'] == val[1])
                self.assertTrue(imgs[i]['image_file'] == val[2])
                self.assertTrue(imgs[i]['description'] == val[3])
            
            img = imgs[len(imgs) -1]
            img_data = {'image_file' : "http://upload.wikimedia.org/wikipedia/commons/6/61/SandstoneUSGOV.jpg",
                        'is_thumbnail' : img['is_thumbnail'],
                        'sort_order' : img['sort_order'],
                        'description' : "dont worry im a doctor"}
            Connection.put('/products/images/{}.json'.format(img['id']), {'description' : "NOPE"})
            
            imgs = Connection.get('/products/33/images.json') 
            expected[len(imgs) -1] = (270, 33, "j/603/SandstoneUSGOV__36595.jpg", "NOPE")
            for i, val in enumerate(expected):
                self.assertTrue(imgs[i]['id'] == val[0])
                self.assertTrue(imgs[i]['product_id'] == val[1])
                self.assertTrue(imgs[i]['image_file'] == val[2])
                self.assertTrue(imgs[i]['description'] == val[3])
             
            Connection.put('/products/33/images/{}.json'.format(img['id']),
                           {'description' : img_data['description'] or "itdoesntlikenullvalues"})
            imgs = Connection.get('/products/33/images.json')
            expected[len(imgs) -1] = (270, 33, "j/603/SandstoneUSGOV__36595.jpg", "dont worry im a doctor")    
            for i, val in enumerate(expected):
                self.assertTrue(imgs[i]['id'] == val[0])
                self.assertTrue(imgs[i]['product_id'] == val[1])
                self.assertTrue(imgs[i]['image_file'] == val[2])
                self.assertTrue(imgs[i]['description'] == val[3])
            
            Connection.delete('/products/33/images/{}.json'.format(img['id']))
            imgs = Connection.get('/products/33/images.json')
            expected.pop()
            self.assertTrue(len(imgs) == 2)
            for i, val in enumerate(expected):
                self.assertTrue(imgs[i]['id'] == val[0])
                self.assertTrue(imgs[i]['product_id'] == val[1])
                self.assertTrue(imgs[i]['image_file'] == val[2])
                self.assertTrue(imgs[i]['description'] == val[3])
                 
            Connection.post('/products/{}/images.json'.format(something['id']), img_data)
            imgs = Connection.get('/products/33/images.json')
            expected.append((271, 33, "k/069/SandstoneUSGOV__85011.jpg", "dont worry im a doctor"))
            for i, val in enumerate(expected):
                self.assertTrue(imgs[i]['id'] == val[0])
                self.assertTrue(imgs[i]['product_id'] == val[1])
                self.assertTrue(imgs[i]['image_file'] == val[2])
                self.assertTrue(imgs[i]['description'] == val[3])
                
    #TODO: write one using XML
                
suite = unittest.TestLoader().loadTestsFromTestCase(TestDirectCalls)

unittest.TextTestRunner(verbosity=2).run(suite)