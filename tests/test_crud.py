from bigcommerce import *

import unittest
import vcr

my_vcr = vcr.VCR(match_on = ['url', 'method', 'body']) # headers too?

class TestGeneralCRUD(unittest.TestCase):
    """
    Test CRUD operations through Client
    """
    
    def setUp(self):
        host = 'somethingequallycreative-jackie-huynh.dev1.syd1bc.bigcommerce.net'
        user = 'admin'
        api_key = 'a2e777fbb2d98fd04461d700463a8ed71782e475'
        self.client = Client(host, api_key, user)
    
    def test_get_products(self):
        # get, update
        with my_vcr.use_cassette('vcr/test_crud/test_get_products.yaml'):
            products = list(self.client.Products.get_all(limit=20))
            self.assertTrue(len(products) == 20)
            
            expected = [(32, "Logitech Pure-Fi Speakers"),
                        (33, "[Sample] Anna, multi-colored bangles"),
                        (34, "[Sample] Harper, tan leather woven belt"),
                        (35, "[Sample] Anna, bright single bangles")]
            for i, vals in enumerate(expected):
                self.assertTrue(products[i].id == vals[0], "{} {}".format(products[i].id, vals[0]))
                self.assertTrue(products[i].name == vals[1])
            
            speakers = self.client.Products.get(32)
            self.assertTrue(speakers.price == "572.2367")
              
            new_price = float(speakers.price) * 0.5
            speakers.name = "Logitech Pure-Fi Speakers"
            speakers.price = new_price
            speakers.description = "This is a description"
            speakers.get_url()
            speakers.update()

            self.assertTrue(speakers.id == 32)
            new_price = round(new_price, 4)
            self.assertTrue(float(speakers.price) == new_price, "{} {}".format(speakers.price, new_price))
            
            speakers = self.client.Products.get(32)
            self.assertTrue(float(speakers.price) == new_price)
            
    def test_manip_coupons(self):
        # get, create, delete
        with my_vcr.use_cassette('vcr/test_crud/test_manip_coupons.yaml'):
            coupons = list(self.client.Coupons.get_all())
            expected = [(1, "5% off order total"),
                        (2, "10% off order total"),
                        (3, "Free shipping"),
                        (4, "$5 off shipping")]
            
            for i, val in enumerate(expected):
                self.assertTrue(coupons[i].id == val[0])
                self.assertTrue(coupons[i].name == val[1])
                
            new_c = self.client.Coupons.create({'name' : "20% off order total v2", 
                                                'amount' : 20.00, 
                                                'code' : "AZ21", 
                                                'type' : "percentage_discount", 
                                                'applies_to' : {'entity' : "products", 'ids' : [32]}})
            new_c1 = self.client.Coupons.create({'name' : "30% off order total v2", 'amount' : 30.00, 'code' : "AZ31", 'type' : "percentage_discount", 'applies_to' : {'entity' : "products", 'ids' : [32]}})

            coupons = list(self.client.Coupons.get_all())
            expected.append((146, "20% off order total v2"))
            expected.append((147, "30% off order total v2"))
            for i, val in enumerate(expected):
                self.assertTrue(coupons[i].id == val[0])
                self.assertTrue(coupons[i].name == val[1])
            
            self.client.Coupons.delete_from_id(new_c.id)
            new_c1.delete()
            
            coupons = list(self.client.Coupons.get_all())
            expected.pop()
            expected.pop()
            for i, val in enumerate(expected):
                self.assertTrue(coupons[i].id == val[0])
                self.assertTrue(coupons[i].name == val[1])
                
            try: # TODO: do we want this to throw an exception when not found, or None? currently None
                c = self.client.Coupons.get(999999)
                self.assertTrue(False, "didn't catch exception")
            except ClientRequestException as e:
                self.assertTrue(True)
                
    def test_subresources(self):
        # get
        with my_vcr.use_cassette('vcr/test_crud/test_subresources.yaml'):
            countries = list(self.client.Countries.get_all(start=5, limit=2))
            expected = [(5, "AND", "Andorra"),
                        (6, "AGO", "Angola")]
            self.assertTrue(len(countries) == 2)
            for i, val in enumerate(expected):
                self.assertTrue(countries[i].id == val[0])
                self.assertTrue(countries[i].country_iso3 == val[1])
                self.assertTrue(countries[i].country == val[2])
              
            murrica = self.client.Countries.get(226)
            self.assertTrue(murrica.country_iso3 == "USA", "{}".format(murrica.country_iso3))
              
            expected = [(1, "AL", "Alabama"),
                        (2, "AL", "Alaska"),
                        (3, "AS", "American Samoa"),
                        (4, "AZ", "Arizona"),
                        (5, "AR", "Arkansas")]
            states = murrica.states[:5]
            self.assertTrue(len(states) == 5)
            for i, val in enumerate(expected):
                self.assertTrue(states[i].id == val[0])
#             
#     def test_subresources2(self):
#         # get, update, update, delete, create
#         with my_vcr.use_cassette('vcr/test4.yaml'):
#             something = Products.get_by_id(33)
#             expected = [(239, 33, "sample_images/cocolee_anna_92851__19446.jpg", None),
#                         (240, 33, "sample_images/cocolee_anna_92852__63752.jpg", None),
#                         (270, 33, "j/603/SandstoneUSGOV__36595.jpg", "dont worry im a doctor")]
#             
#             imgs = something.subresources.get(ProductImage)
#             img = imgs[len(imgs) -1]
#             for i, val in enumerate(expected):
#                 self.assertTrue(imgs[i].id == val[0], "{} {}".format(imgs[i].id, val[0]))
#                 self.assertTrue(imgs[i].product_id == val[1])
#                 self.assertTrue(imgs[i].image_file == val[2])
#                 self.assertTrue(imgs[i].description == val[3])
#             
#             img_data = {'image_file' : "http://upload.wikimedia.org/wikipedia/commons/6/61/SandstoneUSGOV.jpg",
#                         'is_thumbnail' : img.is_thumbnail,
#                         'sort_order' : img.sort_order,
#                         'description' : "dont worry im a doctor"}
#             img.description = "NOPE"
#             img.update()
#             
#             imgs = something.subresources.get(ProductImage)
#             expected[len(imgs) -1] = (270, 33, "j/603/SandstoneUSGOV__36595.jpg", "NOPE")
#             for i, val in enumerate(expected):
#                 self.assertTrue(imgs[i].id == val[0], "{} {}".format(imgs[i].id, val[0]))
#                 self.assertTrue(imgs[i].product_id == val[1])
#                 self.assertTrue(imgs[i].image_file == val[2])
#                 self.assertTrue(imgs[i].description == val[3])
#             
#             img.description = img_data['description'] or "itdoesntlikenullvalues"
#             something.subresources.update(img)
#             imgs = something.subresources.get(ProductImage)
#             expected[len(imgs) -1] = (270, 33, "j/603/SandstoneUSGOV__36595.jpg", "dont worry im a doctor")    
#             for i, val in enumerate(expected):
#                 self.assertTrue(imgs[i].id == val[0], "{} {}".format(imgs[i].id, val[0]))
#                 self.assertTrue(imgs[i].product_id == val[1])
#                 self.assertTrue(imgs[i].image_file == val[2])
#                 self.assertTrue(imgs[i].description == val[3], "{} {}".format(imgs[i].description, val[3]))
#             
#             something.subresources.delete(img)
#             imgs = something.subresources.get(ProductImage)
#             expected.pop()
#             self.assertTrue(len(imgs) == 2)
#             for i, val in enumerate(expected):
#                 self.assertTrue(imgs[i].id == val[0], "{} {}".format(imgs[i].id, val[0]))
#                 self.assertTrue(imgs[i].product_id == val[1])
#                 self.assertTrue(imgs[i].image_file == val[2])
#                 self.assertTrue(imgs[i].description == val[3])
#                 
#             something.subresources.create(ProductImage, img_data)
#             imgs = something.subresources.get(ProductImage)
#             expected.append((271, 33, "k/069/SandstoneUSGOV__85011.jpg", "dont worry im a doctor"))
#             for i, val in enumerate(expected):
#                 self.assertTrue(imgs[i].id == val[0], "{} {}".format(imgs[i].id, val[0]))
#                 self.assertTrue(imgs[i].product_id == val[1])
#                 self.assertTrue(imgs[i].image_file == val[2])
#                 self.assertTrue(imgs[i].description == val[3])
