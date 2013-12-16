from bigcommerce.api.resource import ResourceObject

# TODO: why is this in its own module rather than being in subresources?

class OptionSetOptions(ResourceObject):
    can_update = True
    read_only = ["id"]

    def __repr__(self):
        return "%s- %s" % (self.id, self.display_name)