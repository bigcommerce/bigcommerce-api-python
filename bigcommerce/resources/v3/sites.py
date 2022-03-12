from ..base import *


# TODO: test
class Sites(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'sites'

    # TODO: add subresource function


# TODO: test
class SiteRoutes(ListableApiSubResource, CreateableApiSubResource, DeleteableApiSubResource):
    resource_version = Sites.resource_version
    resource_name = 'routes'
    parent_resource = Sites.resource_name
    parent_key = 'site_id'
