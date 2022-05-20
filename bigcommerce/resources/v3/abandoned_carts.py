from ..base import *


class AbandonedCarts(ListableApiResource):
    resource_version = 'v3'
    resource_name = 'abandoned-carts'

#TODO 
"""
GET         /stores/{store_hash}/v3/abandoned-carts/settings
PUT         /stores/{store_hash}/v3/abandoned-carts/settings
GET         /stores/{store_hash}/v3/abandoned-carts/settings/channels/{channel_id}
PUT         /stores/{store_hash}/v3/abandoned-carts/settings/channels/{channel_id}
GET         /stores/{store_hash}/v3/abandoned-carts/{token}
"""