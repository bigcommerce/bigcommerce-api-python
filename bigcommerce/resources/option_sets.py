from .base import *


class OptionSets(ListableApiResource, CreateableApiResource,
                 UpdateableApiResource, DeleteableApiResource,
                 CollectionDeleteableApiResource, CountableApiResource):
    resource_name = 'option_sets'

    def options(self, id=None):
        if id:
            return OptionSetOptions.get(self.id, id, connection=self._connection)
        else:
            return OptionSetOptions.all(self.id, connection=self._connection)


class OptionSetOptions(ListableApiSubResource, CreateableApiSubResource,
                       UpdateableApiSubResource, DeleteableApiSubResource,
                       CollectionDeleteableApiSubResource):
    resource_name = 'options'
    parent_resource = 'option_sets'
    parent_key = 'option_set_id'
