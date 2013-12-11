from . import ResourceObject


class Brands(ResourceObject):
    """
    
    """
    can_update = True
    read_only = ["id"]
    
    def __repr__(self):
        return "%s- %s" % (self.id, self.name)
    
    
    
    