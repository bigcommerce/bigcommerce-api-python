Bigcommerce API V2 - Python Client
==================================

Wrapper over the `requests` library for communicating with the Bigcommerce v2 API.

Install with `pip install bigcommerce` or `easy_install bigcommerce`. Tested with
python 2.7 and 3.3, and only requires `requests` and `streql`.

## Usage

### Connecting

```python
import bigcommerce

# OAuth2-based connection
# Access_token is optional, if you don't have one you can use oauth_fetch_token (see below)
api = bigcommerce.api.BigcommerceApi(client_id='', store_hash='', access_token='')

# Legacy Basic authentication
api = bigcommerce.api.BigcommerceApi(host='store.mybigcommerce.com', basic_auth=('username', 'api token'))
```

`BigcommerceApi` also provides two helper methods for connection with OAuth2:

* `api.oauth_fetch_token(client_secret, client_secret, code, context, scope, redirect_uri)` -- fetches and
  returns an access token for your application. As a side effect, configures `api` to be ready for use.

* `BigcommerceApi.oauth_verify_payload(signed_payload, client_secret)` -- Returns user data from a signed
  payload.

### Accessing and objects

The `api` object provides access to each API resource, each of which provides CRUD operations,
depending on capabilities of the resource:

```python
api.Products.all()                         # GET /products
api.Products.get(1)                        # GET /products/1
api.Products.create(name='', type='', ...) # POST /products
api.Products.get(1).update(price='199.90') # PUT /products/1
api.Products.delete_all()                  # DELETE /products
api.Products.get(1).delete()               # DELETE /products/1
```

The client provides full access to subresources, both as independent resources:

```
api.ProductOptions.get(1)                  # GET /products/1/options
api.ProductOptions.get(1, 2)               # GET /products/1/options/2
```

And as helper methods on the parent resoource:

```
api.Products.get(1).options()              # GET /products/1/options
api.Products.get(1).options(1)             # GET /products/1/options/1
```

These subresources implement CRUD methods in exactly the same way as regular resources:
```
api.Products.get(1).options(1).delete()
```

### Filters

Filters can be applied to `all` methods as keyword arguments:

```python
customer = api.Customers.all(first_name='John', last_name='Smith')[0]
orders = api.Orders.all(customer_id=customer.id)
```

### Error handling

Minimal validation of data is performed by the client, instead deferring this to the server.
A `HttpException` will be raised for any unusual status code: 

* 3xx status code: `RedirectionException`
* 4xx status code: `ClientRequestException`
* 5xx status code: `ServerException`

## The low level API

The high level API provided by `bigcommerce.api.BigcommerceApi` is a wrapper around a lower level
api in `bigcommerce.connection`. This can be accessed through `api.connection`, and provides helper
methods for get/post/put/delete operations.

## Further documentation

Full documentation of the API is available at
[developer.bigcommerce.com](http://developer.bigcommerce.com)

## To do

* Count endpoints
* Automatic enumeration of multiple page responses
