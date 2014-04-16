from . import ResourceObject

class OptionSetOptions(ResourceObject):
    can_update = True
    read_only = ["id"]

    def __repr__(self):
        return "%s- %s" % (self.id, self.display_name)