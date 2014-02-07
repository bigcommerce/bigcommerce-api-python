from base import *

class OptionSets(ListableApiResource, CreateableApiResource, UpdateableApiResource, DeleteableApiResource):
    resource_name = 'option_sets'

    def options(self, id=None):
        if id:
            return OptionSetOptions.get(self.id, id)
        else:
            return OptionSetOptions.all(self.id)

class OptionSetOptions(ListableApiSubResource, CreateableApiSubResource, UpdateableApiSubResource, DeleteableApiSubResource):
    resource_name = 'options'
    parent_resource = 'option_sets'

