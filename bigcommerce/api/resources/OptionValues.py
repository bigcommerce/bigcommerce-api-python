from bigcommerce.api.resource import ResourceObject


class OptionValues(ResourceObject):
    """
    
    """
    can_update = True
    read_only = ["id", "option_id"]
    
    def __repr__(self):
        return "%s- %s -> %s" % (self.id, self.label, self.value)