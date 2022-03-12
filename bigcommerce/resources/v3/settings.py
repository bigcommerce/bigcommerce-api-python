from ..base import *


class EmailStatuses(ListableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/email-statuses'