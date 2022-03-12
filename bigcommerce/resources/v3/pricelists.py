from ..base import *


# TODO: test
class Pricelists(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'pricelists'


# TODO: test
class PricelistAssignments(ListableApiResource, CreateableApiResource, DeleteableApiResource):
    resource_version = Pricelists.resource_version
    resource_name = 'assignments'
    parent_resource = Pricelists.resource_name
    parent_key = 'pricelist_id'


# TODO: test
class PricelistRecords(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = Pricelists.resource_version
    resource_name = 'records'
    parent_resource = Pricelists.resource_name
    parent_key = 'pricelist_id'

    # TODO: get by variant
    # TODO: get by currency