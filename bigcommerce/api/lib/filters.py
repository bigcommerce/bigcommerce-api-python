"""
Filter Classes

    Defines classes that control filtering.  A ResourceObject that is 
filter-able must have a filter_set instance method, that will
return a FilterSet.  A FilterSet will consist of a number of
FilterBase's.

    A FilterBase, is a mapping that contains meta-data about the
filter (ex: info, description, constraints, etc) and a value for the filter.
When a filter is set, it is active and will be used to filter the results.  

**NOTE: Since both are derived from Mappings, a FilterSet is essentially 
        a dict of dict, where the keys of the FilterSet are the names of
        the parameters that can be filtered on (ex: min_id)

"""
from mapping import Mapping
from datetime import datetime, date


class FilterSet(Mapping):
    """
    FilterSet's contain a set of FilterBase's (aka Mappings).  Essentially this is
    a dict of dicts.  
    """
    
    def query_dict(self):
        """
        For all active Filters (ie, has a "value" set), create a dictionary of
        active filter names and values  
        """
        return dict((k,v["value"]) for (k, v) in self.iteritems() if v.has_key("value"))
        


class FilterBase(Mapping):
    """
    Base Filter Class
    """
    def set(self, value):
        self.value = value


class StringFilter(FilterBase):
    """
    StringFilter handles setting and type checking the value
    """
    pass


class NumberFilter(FilterBase):
    """
    NumberFilter will type check the value to make sure it's a number
    """
    
    def set(self, value):
        if isinstance(value, (int, float)):
            self.value = value
        elif isinstance(value, basestring):
            try:
                self.value = int(value)
            except:
                self.value = float(value)
    


class DateFilter(FilterBase):
    """
    DateFilter will ensure the value is represented correctly as a date string
    accepted
    """
    format = "%m/%d/%Y %H:%M:%S"
    
    def set(self, value):
        if isinstance(value, (datetime, date)):
            self.value = value.strftime("%a, %d %b %Y %H:%M:%S +0000")
            
        elif isinstance(value, basestring):
            try:
                self.value = datetime.strptime(value, DateFilter.format).strftime("%a, %d %b %Y %H:%M:%S +0000")
            except:
                raise AttributeError("Unable to use date value - check the format (use: %s)" % DateFilter.format)
    


class BoolFilter(FilterBase):
    """
    BoolFilter will ensure the value assed is set to a boolean type
    """
    
    def set(self, value):
        if isinstance(value, bool):
            self.value = value
        else:
            if value.lower() == "true":
                self.value = True
            elif value.lower() == "false":
                self.value = False
            else:
                raise AttributeError("Unable to cast %s to a Boolean type" % value)