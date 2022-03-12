from ..base import *

# TODO: Test
class CustomTemplateAssociations(CreateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'storefront/custom-template-associations'