from ..base import *


class Redirects(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'storefront/redirects'