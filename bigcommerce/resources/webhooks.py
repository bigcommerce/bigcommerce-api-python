from .base import *


class Webhooks(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_name = 'hooks'

    @classmethod
    def delete_all(self, connection=None):
        raise NotImplementedError("The webhook resource does not have delete_all endpoint")
