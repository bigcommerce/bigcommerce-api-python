import bigcommerce.api

bigcommerce.api.auth.oauth_configure('client_id', 'store_hash', 'access_token')

products = bigcommerce.api.Products.all(is_visible=True)

custom = bigcommerce.api.ProductCustomFields.create(products[0].id, name="Manufactured in", text="Australia")

custom.update(text="Manufactured in", name="USA")

print bigcommerce.api.ProductCustomFields.get(products[0].id, custom.id)

print products[0].custom_fields(custom.id).delete()

print bigcommerce.api.Countries.all(country="Australia")[0].states()[0].parent_id()