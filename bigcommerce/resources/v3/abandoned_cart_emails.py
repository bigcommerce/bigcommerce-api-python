from ..base import *


class AbandonedCartEmails(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'marketing/email-templates/abandoned_cart_email'

    def default(self):
        return AbandonedCartEmailsDefault.all(connection=self._connection)


class AbandonedCartEmailsDefault(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'marketing/abandoned-cart-emails/default'
