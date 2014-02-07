from base import *

class Countries(ListableApiResource):
    resource_name = 'countries'

    def states(self, id=None):
        if id:
            return CountryStates.get(self.id, id)
        else:
            return CountryStates.all(self.id)

class CountryStates(ListableApiSubResource):
    resource_name = 'states'
    parent_resource = 'countries'

