from ..base import *

# TODO: Test
class CustomTemplateAssociations(DeleteableApiResource, CollectionDeleteableApiResource, CollectionUpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'storefront/custom-template-associations'