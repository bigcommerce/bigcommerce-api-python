from ..base import *

# TODO: test
class Carts(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource,
               CollectionDeleteableApiResource, CountableApiResource):
    resource_version = 'v3'
    resource_name = 'carts'

# TODO: carts/{cartId}/items, post put delete
# TODO: carts/{cartId}/redirect_urls, post
