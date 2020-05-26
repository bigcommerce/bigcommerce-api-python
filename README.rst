Bigcommerce API Python Client
==================================

|Build Status| |Package Version|

Wrapper over the ``requests`` library for communicating with the Bigcommerce v2 API.

Install with ``pip install bigcommerce`` or ``easy_install bigcommerce``. Tested with
python 2.7.7+ and 3.4, and only requires ``requests`` and ``pyjwt``.

Usage
-----

Connecting
~~~~~~~~~~

.. code:: python

    import bigcommerce

    # Public apps (OAuth)
    # Access_token is optional, if you don't have one you can use oauth_fetch_token (see below)
    # For connecting to the v2 api:
    api = bigcommerce.api.BigcommerceApi(client_id='', store_hash='', access_token='')
    For connecting to the v3 api:
    api = bigcommerce.api.BigcommerceApi(client_id='', store_hash='', access_token='', api_path='/stores/{}/v3/{}'))

    # Private apps (Basic Auth)
    api = bigcommerce.api.BigcommerceApi(host='store.mybigcommerce.com', basic_auth=('username', 'api token'))

``BigcommerceApi`` also provides two helper methods for connection with OAuth2:

-  ``api.oauth_fetch_token(client_secret, code, context, scope, redirect_uri)``
   -- fetches and returns an access token for your application. As a
   side effect, configures ``api`` to be ready for use.

-  ``BigcommerceApi.oauth_verify_payload(signed_payload, client_secret)``
   -- Returns user data from a signed payload.

Accessing and objects
~~~~~~~~~~~~~~~~~~~~~

The ``api`` object provides access to each API resource, each of which
provides CRUD operations, depending on capabilities of the resource:

.. code:: python

    api.Products.all()                         # GET /products (returns only a single page of products as a list)
    api.Products.iterall()                     # GET /products (autopaging generator that yields all
                                               #                  products from all pages product by product.)
    api.Products.get(1)                        # GET /products/1
    api.Products.create(name='', type='', ...) # POST /products
    api.Products.get(1).update(price='199.90') # PUT /products/1
    api.Products.delete_all()                  # DELETE /products
    api.Products.get(1).delete()               # DELETE /products/1
    api.Products.count()                       # GET /products/count

The client provides full access to subresources, both as independent
resources:

::

    api.ProductOptions.get(1)                  # GET /products/1/options
    api.ProductOptions.get(1, 2)               # GET /products/1/options/2

And as helper methods on the parent resource:

::

    api.Products.get(1).options()              # GET /products/1/options
    api.Products.get(1).options(1)             # GET /products/1/options/1

These subresources implement CRUD methods in exactly the same way as
regular resources:

::

    api.Products.get(1).options(1).delete()

Filters
~~~~~~~

Filters can be applied to ``all`` methods as keyword arguments:

.. code:: python

    customer = api.Customers.all(first_name='John', last_name='Smith')[0]
    orders = api.Orders.all(customer_id=customer.id)

Error handling
~~~~~~~~~~~~~~

Minimal validation of data is performed by the client, instead deferring
this to the server. A ``HttpException`` will be raised for any unusual
status code:

-  3xx status code: ``RedirectionException``
-  4xx status code: ``ClientRequestException``
-  5xx status code: ``ServerException``

The low level API
~~~~~~~~~~~~~~~~~

The high level API provided by ``bigcommerce.api.BigcommerceApi`` is a
wrapper around a lower level api in ``bigcommerce.connection``. This can
be accessed through ``api.connection``, and provides helper methods for
get/post/put/delete operations.

Managing OAuth Rate Limits
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can optionally pass a ``rate_limiting_management`` object into ``bigcommerce.api.BigcommerceApi`` or ``bigcommerce.connection.OAuthConnection`` for automatic rate limiting management, ex:

.. code:: python

    import bigcommerce

    api = bigcommerce.api.BigcommerceApi(client_id='', store_hash='', access_token=''
                                         rate_limiting_management= {'min_requests_remaining':2,
                                                                    'wait':True,
                                                                    'callback_function':None})

``min_requests_remaining`` will determine the number of requests remaining in the rate limiting window which will invoke the management function

``wait`` determines whether or not we should automatically sleep until the end of the window

``callback_function`` is a function to run when the rate limiting management function fires. It will be invoked *after* the wait, if enabled.

``callback_args`` is an optional parameter which is a dictionary passed as an argument to the callback function.

For simple applications which run API requests in serial (and aren't interacting with many different stores, or use a separate worker for each store) the simple sleep function may work well enough for most purposes. For more complex applications that may be parallelizing API requests on a given store, it's adviseable to write your own callback function for handling the rate limiting, use a ``min_requests_remaining`` higher than your concurrency, and not use the default wait function.

Further documentation
---------------------

Full documentation of the API is available on the Bigcommerce
`Developer Portal <http://developer.bigcommerce.com>`__

To do
-----

-  Automatic enumeration of multiple page responses for subresources.

.. |Build Status| image:: https://api.travis-ci.org/bigcommerce/bigcommerce-api-python.svg?branch=master
   :target: https://travis-ci.org/bigcommerce/bigcommerce-api-python
.. |Package Version| image:: https://badge.fury.io/py/bigcommerce.svg
   :target: https://pypi.python.org/pypi/bigcommerce
