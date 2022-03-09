from ..base import *


class AbandonedCartEmails(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/marketing/abandoned-cart-emails'

    def default(self):
        return AbandonedCartEmailsDefault.all(connection=self._connection)

class AbandonedCartEmailsDefault(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/marketing/abandoned-cart-emails/defaults'
