from mapping import Mapping
from pprint import pprint

class FilterSet(Mapping):
    
    def query_dict(self):
        return dict((k,v["value"]) for (k, v) in self.iteritems() if v.has_key("value"))
        


class FilterBase(Mapping):
    def set(self, value):
        self.value = value

    
    

class StringFilter(FilterBase):
    pass

class NumberFilter(FilterBase):
    pass

class DateFilter(FilterBase):
    pass

class BoolFilter(FilterBase):
    pass
