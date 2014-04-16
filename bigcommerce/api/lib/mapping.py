"""
Mapping 

provides '.' access to dictionary keys
"""

class Mapping(dict):    
    def __init__(self, *args, **kwargs):
        self.__dict__ = self
        dict.__init__(self, *args, **kwargs)

if __name__ == "__main__":
    g = Mapping(myfield = "value")
    g.foo = "bar"
    print g 