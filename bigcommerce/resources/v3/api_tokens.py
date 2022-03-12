from ..base import *


class ApiToken(CreateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'storefront/api-token'


class ApiTokenCustomerImpersonation(CreateableApiResource):
    resource_version = 'v3'
    resource_name = 'storefront/api-token-customer-impersonation'
