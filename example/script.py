from bigcommerce import *

HOST = 'somestore.bigcommerce.com'
USER = 'admin'
KEY = 'asdfhahahahauehauheau'

Connection.host = HOST
Connection.user = USER
Connection.api_key = KEY

print ">> Showing the first 20 products"
products = Products.get({'limit' : 20})
for p in products:
    print "\t({}): {}, price: {}".format(p.id, p.name, p.price)
 
speakers = Products.get_by_id(32)
print "\n>> Showing and updating product 32"
print "\t({}): {}, price: {}".format(speakers.id, speakers.name, speakers.price)
# for f in speakers._fields:
#     print ">>>", f, ":", speakers._fields[f]
# print
  
speakers.name = "Logitech Pure-Fi Speakers"
speakers.price = random.randint(1, 1000)
speakers.description = "This is a description"
speakers.update()
print ">> new product"
speakers = Products.get_by_id(32)
print "\t({}): {}, price: {}".format(speakers.id, speakers.name, speakers.price)

coupons = Coupons.get()
print "\n>> Showing all coupons"
for c in coupons:
    print "\t({}): {}".format(c.id, c.name)
print ">> Make a new coupon:"
new_c = Coupons.create({'name' : "70% off order total", 
                        'amount' : 70.00, 
                        'code' : "HT75", 
                        'type' : "percentage_discount", 
                        'applies_to' : {'entity' : "products", 'ids' : [32]}})
print "\tnew coupon: ({}): {}".format(new_c.id, new_c.name)
new_c1 = Coupons.create({'name' : "60% off order total", 'amount' : 60.00, 'code' : "HT85", 'type' : "percentage_discount", 'applies_to' : {'entity' : "products", 'ids' : [32]}})
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
countries = Countries.get({'limit' : 2, 'page' : 3})
for c in countries:
    print "\t({}): {} - {}".format(c.id, c.country_iso3, c.country)
print ">> Fetching Country 226:"
murrica = Countries.get_by_id(226)
print ">> it has {} states, showing 5 of them:".format(murrica.subresources.count(CountryState))
for state in murrica.subresources.get(CountryState, {'limit':5}):
    print "\t({}): {} - {}".format(state.id, state.state_abbreviation, state.state)
    
print "\n >>Looking at images of product 33"
speakers = Products.get_by_id(33) # obviously this isnt speakers
for i in speakers.subresources.get(ProductImage):
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
for i in speakers.subresources.get(ProductImage):
    print "\t({}): product_id: {}, image_file: {}, desc: {}".format(i.id, i.product_id, i.image_file, i.description)
print ">> Changing it back"
img.description = img_data['description'] or "itdoesntlikenullvalues"
speakers.subresources.update(img)
for i in speakers.subresources.get(ProductImage):
    print "\t({}): product_id: {}, image_file: {}, desc: {}".format(i.id, i.product_id, i.image_file, i.description)
    
print ">> Delete it!"
speakers.subresources.delete(img)
for i in speakers.subresources.get(ProductImage):
    print "\t({}): product_id: {}, image_file: {}, desc: {}".format(i.id, i.product_id, i.image_file, i.description)
print ">> Make it again!"
speakers.subresources.create(ProductImage, img_data)
for i in speakers.subresources.get(ProductImage):
    print "\t({}): product_id: {}, image_file: {}, desc: {}".format(i.id, i.product_id, i.image_file, i.description)
