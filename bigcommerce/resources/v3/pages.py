from ..base import *


# TODO: test
# TODO: add CollectionUpdateableApiResource
class Pages(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource, CollectionDeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'content/pages'