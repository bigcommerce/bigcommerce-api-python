from resource import ResourceObject
import subresource
from bigcommerce.api.filters import FilterSet, StringFilter, NumberFilter, DateFilter, BoolFilter

class Countries(ResourceObject):
    sub_resources = Mapping(states = Mapping(klass = subresource.States))
    
    @classmethod
    def filter_set(cls):
        return FilterSet(country = StringFilter(),
                      country_iso2 = StringFilter(),
                      country_iso3 = StringFilter(),
                      ) 
        
    def __repr__(self):
        return "%s- %s" % (self.id, self.country)