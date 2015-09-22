from .base import *


class GiftCertificates(ListableApiResource, CreateableApiResource,
              UpdateableApiResource, DeleteableApiResource,
              CollectionDeleteableApiResource):
    resource_name = 'gift_certificates'
