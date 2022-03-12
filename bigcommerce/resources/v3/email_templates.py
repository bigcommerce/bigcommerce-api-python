from ..base import *


# TODO: test
class EmailTemplates(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'marketing/email-templates'