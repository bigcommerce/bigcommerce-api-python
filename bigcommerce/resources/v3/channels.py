from ..base import *


class Channels(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource,
               CollectionDeleteableApiResource, CountableApiResource):
    resource_version = 'v3'
    resource_name = 'channels'


# TODO: channels/{channel_id}/active-theme
# channels/currency-assignments
# channels/{channel_id}/listings