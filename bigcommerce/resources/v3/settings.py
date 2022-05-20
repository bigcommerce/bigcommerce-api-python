from ..base import *

class SettingsAnalytics(ListableApiResource, UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/analytics'


class SettingsEmailStatuses(UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/email-statuses'


class SettingsFaviconImage(CreateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/favicon/image'

class SettingsCatalog(UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/catalog'


class SettingsInventoryNotifications(UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/inventory/notifications'


class SettingsLogo(UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/logo'


class SettingsLogoImage(CreateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/logo/image'


class SettingsStorefrontProduct(UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/storefront/product'


class SettingsSearchFilters(ListableApiResource,
               CollectionUpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/search/filters'


class SettingsSearchFiltersAvailable(ListableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/search/filters/available'


class SettingsSearchFiltersContexts(ListableApiResource, UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/search/filters/contexts'


class SettingsStoreLocale(UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/store/locale'


class SettingsStorefrontCategory(UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/storefront/category'


class SettingsStorefrontRobotstxt(UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/storefront/robotstxt'


class SettingsStorefrontSearch(UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/storefront/search'


class SettingsStorefrontSecurity(UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/storefront/security'


class SettingsStorefrontSeo(UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/storefront/seo'


class SettingsStorefrontStatus(UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/storefront/status'


class SettingsStoreProfile(UpdateableApiResource):
    resource_version = 'v3'
    resource_name = 'settings/store/profile'