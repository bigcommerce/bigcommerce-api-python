from __future__ import print_function
import bigcommerce.api

__author__ = 'tim'

api = bigcommerce.api.BigcommerceApi(client_id='id', store_hash='hash', access_token='token')

print(repr(api.Time.all()))
