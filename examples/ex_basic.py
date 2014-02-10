from __future__ import print_function
import bigcommerce.api

api = bigcommerce.api.BigcommerceApi(client_id='id', store_hash='hash', access_token='token')

products = api.Products.all(is_visible=True)

custom = api.ProductCustomFields.create(products[0].id, name="Manufactured in", text="Australia")

custom.update(text="USA", name="Manufactured in")

print(api.ProductCustomFields.get(products[0].id, custom.id))

print(products[0].custom_fields(custom.id).delete())

print(api.Countries.all(country="Australia")[0].states()[0].parent_id())
