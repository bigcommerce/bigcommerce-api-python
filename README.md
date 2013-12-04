BigCommerce API V2 - Python Client
==================================

This module provides a lightweight object-oriented wrapper around the BigCommerce V2 API
for use in Python projects or via the Python shell. 

### Requirements

- Python 2.6+
- requests : `pip install requests`

The test also requires vcrpy : `pip install vcrpy`

For a given user, a valid API key is required to authenticate requests. To grant 
API access for user, go to Control Panel > Users > Edit User and make sure that the
'Enable the API' checkbox is ticked.

### Usage

The API focuses on the subclasses of Resource and ResourceSet. They all share the same functionality
(except concerning sub-resources, explained later), so the examples below should be applicable to all
resources.

See http://developer.bigcommerce.com/docs/api/v2/resources for all resources.
The options/filters for some requests can be passed in as a dictionary (see 'Retrieving').

#### Setup
Modules
```
from bigcommerce import *

# the above is equivalent to:
from bigcommerce.connection import Connection 
from bigcommerce.httpexception import *
from bigcommerce.resource import *
from bigcommerce.subresource import *
```

Set-up connection:
```
Connection.host = YOUR_STORE    # eg. 'mystore.bigcommerce.com
Connection.user = USER          # eg. 'admin'
Connection.api_key = API_KEY    # eg. 'a2e777fbb2d98fd04461d700463a8ed71782e475'
```

Proxies can also be defined by doing:
```
Connection.proxies = {"http": "http://10.10.1.10:3128",
                      "https": "http://10.10.1.10:1080"}
```

#### Retrieving
(and count)
```
num_products = Products.count()

products = Products.get({'limit' : 10'})
for p in products:
    print "\t({}): {}, price: {}".format(p.id, p.name, p.price)
```

Use ```Products.get_by_id(some_id)``` for specific resources. 

#### Updating
```
speakers = Products.get_by_id(32)
print "\t({}): {}, price: {}".format(speakers.id, speakers.name, speakers.price)
  
speakers.name = "Logitech Pure-Fi Speakers"
speakers.price = 999.95
speakers.description = "This is a description"
speakers.update()
```

#### Creating
```
new_c = Coupons.create({'name' : "70% off order total", 
                        'amount' : 70.00, 
                        'code' : "HT75", 
                        'type' : "percentage_discount", 
                        'applies_to' : {'entity' : "products", 'ids' : [32]}})
```
The create method saves the resource to the store server (equivalent to a POST request), and
returns the corresponding resource object (Coupon in this case)

#### Deleting
```
Coupons.delete_from_id(new_c.id)
```
or:
```
new_c.delete()
```

#### Sub-Resources

Some resources are defined as a ```ParentResource```. These objects hold a bunch of class methods for handling
sub-resources independently from specific parent resources. The operations not independent of specific
instances are handled by a ```SubResourceManager```, accessible through a ParentResource 
instance's ```subresources``` field.

For these operations to work, they either take a SubResource class, or a specific instance of a SubResource.

Otherwise, much of the interface and behaviour of sub-resource related functionality is the same as the
rest of the client.

Some random sample code:

Getting states:
```
print ">> Fetching Country 226:"
murrica = Countries.get_by_id(226)

print ">> it has {} states, showing 5 of them:".format(murrica.subresources.count(CountryState))
for state in murrica.subresources.get(CountryState, {'limit':5}):
    print "\t({}): {} - {}".format(state.id, state.state_abbreviation, state.state)
```

Getting images, and some manipulation:
```
print "\n >>Looking at images of product 33"
something = Products.get_by_id(33)
for i in something.subresources.get(ProductImage):
    print "\t({}): product_id: {}, image_file: {}, desc: {}".format(i.id, i.product_id, i.image_file, i.description)
    img = i # last image found

print ">> Changing description"
img_data = {'image_file' : "http://upload.wikimedia.org/wikipedia/commons/6/61/SandstoneUSGOV.jpg",
            'is_thumbnail' : img.is_thumbnail,
            'sort_order' : img.sort_order,
            'description' : "dont worry im a doctor"}
img.description = "NOPE"
img.update()

# print them out
for i in something.subresources.get(ProductImage):
    print "\t({}): product_id: {}, image_file: {}, desc: {}".format(i.id, i.product_id, i.image_file, i.description)

print ">> Changing it back"
img.description = img_data['description'] or "ItDoesntLikeNullValues"
something.subresources.update(img) # img.update() works too

# Deletion and creation

print ">> Delete it!"
something.subresources.delete(img) # img.delete() works as well

print ">> Make it again!"
something.subresources.create(ProductImage, img_data)
for i in speakers.subresources.get(ProductImage):
    print "\t({}): product_id: {}, image_file: {}, desc: {}".format(i.id, i.product_id, i.image_file, i.description)
```

#### Exception Handling
The client defines HttpException, which acts as a direct analogue to http errors by holding headers
and content of errors encountered as fields.
It is subclassed by RedirectionException, ClientRequestException, and ServerException, corresponding
to 3xx, 4xx, 5xx status codes respectively.

```
try:
    c = Coupons.get_by_id(999999)
except ClientRequestException as e:
    print "Exception caught successfully. Headers: ", e.headers
    print "\tcontent: ", e.content
```

To handle more specific exceptions, users should examine contents for the status code using: ```e.content['status']```

Information about the API request limit (number of requests the client can make until blocked) can 
be accessed as part of the header: ```e.headers['x-bc-apilimit-remaining']```
