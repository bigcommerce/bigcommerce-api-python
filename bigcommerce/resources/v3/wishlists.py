from ..base import *


# TODO: Test
class Wishlists(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'wishlists'


# TODO: Test
class WishlistItems(ListableApiSubResource, CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = Wishlists.resource_version
    resource_name = 'items'
    parent_resource = Wishlists.resource_name
    parent_key = 'wishlist_id'