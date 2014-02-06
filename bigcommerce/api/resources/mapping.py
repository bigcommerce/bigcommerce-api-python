"""
Mapping 

provides '.' access to dictionary keys
"""

class Mapping(dict):    
    def __init__(self, *args, **kwargs):
        self.__dict__ = self
        dict.__init__(self, *args, **kwargs)