from .base import *


class Options(ListableApiResource, CreateableApiResource,
              UpdateableApiResource, DeleteableApiResource,
              CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'options'

    def values(self, id=None):
        if id:
            return OptionValues.get(self.id, id, connection=self._connection)
        else:
            return OptionValues.all(self.id, connection=self._connection)


class OptionValues(ListableApiSubResource, CreateableApiSubResource,
                   UpdateableApiSubResource, DeleteableApiSubResource,
                   CollectionDeleteableApiSubResource):
    resource_name = 'values'
    parent_resource = 'options'
    parent_key = 'option_id'
