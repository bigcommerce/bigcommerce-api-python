from .base import *


class Countries(ListableApiResource):
    resource_name = 'countries'

    def states(self, id=None):
        if id:
            return CountryStates.get(self.id, id, connection=self._connection)
        else:
            return CountryStates.all(self.id, connection=self._connection)


class CountryStates(ListableApiSubResource):
    resource_name = 'states'
    parent_resource = 'countries'
    parent_key = 'country_id'
