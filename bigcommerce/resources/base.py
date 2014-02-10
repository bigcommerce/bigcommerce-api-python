class Mapping(dict):
    """
    Mapping

    provides '.' access to dictionary keys
    """
    def __init__(self, mapping, *args, **kwargs):
        """
        Create a new mapping. Filters the mapping argument
        to remove any elements that are already methods on the
        object.

        For example, Orders retains its `coupons` method, instead
        of being replaced by the dict describing the coupons endpoint
        """
        filter_args = {k: mapping[k] for k in mapping if k not in dir(self)}
        self.__dict__ = self
        dict.__init__(self, filter_args, *args, **kwargs)

    def __str__(self):
        """
        Display as a normal dict, but filter out underscored items first
        """
        return str({k: self.__dict__[k] for k in self.__dict__ if not k.startswith("_")})

    def __repr__(self):
        return "<%s at %s, %s>" % (type(self).__name__, hex(id(self)), str(self))


class ApiResource(Mapping):
    resource_name = ""  # The identifier which describes this resource in urls

    @classmethod
    def _create_object(cls, response, connection=None):
        if isinstance(response, list):
            return [cls._create_object(obj, connection) for obj in response]
        else:
            return cls(response, _connection=connection)

    @classmethod
    def _make_request(cls, method, url, connection, data=None, params={}, headers={}):
        return connection.make_request(method, url, data, params, headers)

    @classmethod
    def get(cls, id, connection=None, **params):
        response = cls._make_request('GET', "%s/%s" % (cls.resource_name, id), connection, params=params)
        return cls._create_object(response, connection=connection)


class ApiSubResource(ApiResource):
    parent_resource = ""
    parent_key = ""

    @classmethod
    def get(cls, parentid, id, connection=None, **params):
        path = "%s/%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name, id)
        response = cls._make_request('GET', path, connection, params=params)
        return cls._create_object(response, connection=connection)

    def parent_id(self):
        return self[self.parent_key]


class CreateableApiResource(ApiResource):
    @classmethod
    def create(cls, connection=None, **params):
        response = cls._make_request('POST', cls.resource_name, connection, data=params)
        return cls._create_object(response, connection=connection)


class CreateableApiSubResource(ApiSubResource):
    @classmethod
    def create(cls, parentid, connection=None, **params):
        path = "%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name)
        response = cls._make_request('POST', path, connection, data=params)
        return cls._create_object(response, connection=connection)


class ListableApiResource(ApiResource):
    @classmethod
    def all(cls, connection=None, **params):
        request = cls._make_request('GET', cls.resource_name, connection, params=params)
        return cls._create_object(request, connection=connection)


class ListableApiSubResource(ApiSubResource):
    @classmethod
    def all(cls, parentid, connection=None, **params):
        path = "%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name)
        response = cls._make_request('GET', path, connection, params=params)
        return cls._create_object(response, connection=connection)


class UpdateableApiResource(ApiResource):
    def update(self, **updates):
        path = "%s/%s" % (self.resource_name, self.id)
        response = self._make_request('PUT', path, self._connection, data=updates)
        return self._create_object(response, connection=self._connection)


class UpdateableApiSubResource(ApiSubResource):
    def update(self, **updates):
        path = "%s/%s/%s/%s" % (self.parent_resource, self.parent_id(), self.resource_name, self.id)
        response = self._make_request('PUT', path, self._connection, data=updates)
        return self._create_object(response, connection=self._connection)


class DeleteableApiResource(ApiResource):
    def delete(self):
        path = "%s/%s" % (self.resource_name, self.id)
        return self._make_request('DELETE', path, self._connection)

    @classmethod
    def delete_all(cls, connection=None):
        return cls._make_request('DELETE', cls.resource_name, connection)


class DeleteableApiSubResource(ApiSubResource):
    def delete(self):
        parent_id = self.parent_id()
        path = "%s/%s/%s/%s" % (self.parent_resource, parent_id, self.resource_name, self.id)
        return self._make_request('DELETE', path, self._connection)

    @classmethod
    def delete_all(cls, parentid, connection=None):
        path = "%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name)
        return cls._make_request('DELETE', path, connection)