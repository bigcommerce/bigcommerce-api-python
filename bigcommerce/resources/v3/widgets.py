from ..base import *


class Widgets(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'content/widgets'


class WidgetTemplates(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'content/widget-templates'


class WidgetRegions(ListableApiResource):
    resource_version = 'v3'
    resource_name = 'content/regions'


class WidgetPlacements(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'content/placements'