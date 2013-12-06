from bigcommerce import *

import vcr

HOST = 'yourstore'
USER = 'admin'
KEY = 'yourkey'

HOST = 'somethingequallycreative-jackie-huynh.dev1.syd1bc.bigcommerce.net'
USER = 'admin'
KEY = 'a2e777fbb2d98fd04461d700463a8ed71782e475'

Connection.host = HOST
Connection.user = USER
Connection.api_key = KEY

with vcr.use_cassette('vcr/example.yaml'):
    
    print ">> Showing the first 20 products"
    products = Products.get(limit=20)
    for p in products:
        print "\t({}): {}, price: {}".format(p.id, p.name, p.price)
     
    prod = Products.get_by_id(32)
    print "\n>> Showing and updating product 32"
    print "\t({}): {}, price: {}".format(prod.id, prod.name, prod.price)
    
    prod.price = float(prod.price) * 1.5
    prod.description = "Tomorrow is most certainly not today."
    prod.update()
    print ">> new product"
    prod = Products.get_by_id(32)
    print "\t({}): {}, price: {}".format(prod.id, prod.name, prod.price)
    
    coupons = Coupons.get()
    print "\n>> Showing all coupons"
    for c in coupons:
        print "\t({}): {}".format(c.id, c.name)
    print ">> Make a new coupon:"
    new_c = Coupons.create({'name' : "70% off order total v2", 
                            'amount' : 70.00, 
                            'code' : "HT99", 
                            'type' : "percentage_discount", 
                            'applies_to' : {'entity' : "products", 'ids' : [32]}})
    print "\tnew coupon: ({}): {}".format(new_c.id, new_c.name)
    new_c1 = Coupons.create({'name' : "60% off order total v2", 'amount' : 60.00, 'code' : "HT89", 'type' : "percentage_discount", 'applies_to' : {'entity' : "products", 'ids' : [32]}})
    print "\tanother new coupon: ({}): {}".format(new_c1.id, new_c1.name)
    
    coupons = Coupons.get()
    print ">> all coupons now:"
    for c in coupons:
        print "\t({}): {}".format(c.id, c.name)
    
    print ">> deleting the new coupons"
    Coupons.delete_from_id(new_c.id)
    new_c1.delete()
    
    coupons = Coupons.get()
    print ">> all coupons now:"
    for c in coupons:
        print "\t({}): {}".format(c.id, c.name)
        
    print "\n>> Fetching coupon with id 999999"
    try:
        c = Coupons.get_by_id(999999)
    except ClientRequestException as e:
        print "Exception caught successfully. Headers: ", e.headers
        print "\tcontent: ", e.content
        
    print "\n>> Fetching 2 countries from page 3"
    countries = Countries.get(limit=2, page=3)
    for c in countries:
        print "\t({}): {} - {}".format(c.id, c.country_iso3, c.country)
    print ">> Fetching Country 226:"
    murrica = Countries.get_by_id(226)
    print ">> it has {} states, showing 5 of them:".format(murrica.subresources.count(CountryState))
    for state in murrica.subresources.get(CountryState, limit=5):
        print "\t({}): {} - {}".format(state.id, state.state_abbreviation, state.state)
        
    print "\n >>Looking at images of product 33"
    prod = Products.get_by_id(33)
    for i in prod.subresources.get(ProductImage):
        print "\t({}): product_id: {}, image_file: {}, desc: {}".format(i.id, i.product_id, i.image_file, i.description)
        img = i
    
    print ">> Changing description"
    img_data = {'image_file' : "http://upload.wikimedia.org/wikipedia/commons/6/61/SandstoneUSGOV.jpg",
                'is_thumbnail' : img.is_thumbnail,
                'sort_order' : img.sort_order,
                'description' : "dont worry im a doctor"}
    img.description = "NOPE"
    img.update()
    print ">> Images of 33 are now:"
    for i in prod.subresources.get(ProductImage):
        print "\t({}): product_id: {}, image_file: {}, desc: {}".format(i.id, i.product_id, i.image_file, i.description)
    print ">> Changing it back"
    img.description = img_data['description'] or "itdoesntlikenullvalues"
    prod.subresources.update(img)
    for i in prod.subresources.get(ProductImage):
        print "\t({}): product_id: {}, image_file: {}, desc: {}".format(i.id, i.product_id, i.image_file, i.description)
        
    print ">> Delete it!"
    prod.subresources.delete(img)
    for i in prod.subresources.get(ProductImage):
        print "\t({}): product_id: {}, image_file: {}, desc: {}".format(i.id, i.product_id, i.image_file, i.description)
    print ">> Make it again!"
    prod.subresources.create(ProductImage, img_data)
    for i in prod.subresources.get(ProductImage):
        print "\t({}): product_id: {}, image_file: {}, desc: {}".format(i.id, i.product_id, i.image_file, i.description)
