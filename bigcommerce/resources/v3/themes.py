from ..base import *

# TODO: Test

class Themes(ListableApiResource, CreateableApiResource,
               UpdateableApiResource, DeleteableApiResource):
    resource_version = 'v3'
    resource_name = 'themes'


class ThemeActions(CreateableApiSubResource):
    resource_version = Themes.resource_version
    resource_name = 'actions'
    parent_resource = Themes.resource_name
    key = 'theme_uuid'


# TODO: Test
class ThemeActionsDownload(CreateableApiSubResource):
    resource_version = Themes.resource_version
    resource_name = 'actions/download'
    parent_resource = Themes.resource_name
    key = 'theme_uuid'


# TODO: Test
class ThemeActionsActivate(CreateableApiSubResource):
    resource_version = Themes.resource_version
    resource_name = 'actions/activate'
    parent_resource = Themes.resource_name
    key = 'theme_uuid'