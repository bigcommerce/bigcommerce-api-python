from ..base import *


class Webhooks(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version='v3'
    resource_name = 'hooks'