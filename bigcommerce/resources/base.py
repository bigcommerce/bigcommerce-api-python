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

        mapping = mapping or {}

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
        if response and not isinstance(response, dict):
            return [cls(obj, _connection=connection) for obj in response]
        else:
            return cls(response, _connection=connection)

    @classmethod
    def _make_request(cls, method, url, connection, data=None, params=None, headers=None):
        return connection.make_request(method, url, data, params, headers)

    @classmethod
    def _get_path(cls, id):
        return "%s/%s" % (cls.resource_name, id)

    @classmethod
    def get(cls, id, connection=None, **params):
        response = cls._make_request('GET', cls._get_path(id), connection, params=params)
        return cls._create_object(response, connection=connection)


class ApiSubResource(ApiResource):
    parent_resource = ""
    parent_key = ""

    @classmethod
    def _get_path(cls, id, parentid):
        return "%s/%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name, id)

    @classmethod
    def get(cls, parentid, id, connection=None, **params):
        response = cls._make_request('GET', cls._get_path(id, parentid), connection, params=params)
        return cls._create_object(response, connection=connection)

    def parent_id(self):
        return self[self.parent_key]


class CreateableApiResource(ApiResource):
    @classmethod
    def _create_path(cls):
        return cls.resource_name

    @classmethod
    def create(cls, connection=None, **params):
        response = cls._make_request('POST', cls._create_path(), connection, data=params)
        return cls._create_object(response, connection=connection)


class CreateableApiSubResource(ApiSubResource):
    @classmethod
    def _create_path(cls, parentid):
        return "%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name)

    @classmethod
    def create(cls, parentid, connection=None, **params):
        response = cls._make_request('POST', cls._create_path(parentid), connection, data=params)
        return cls._create_object(response, connection=connection)


class ListableApiResource(ApiResource):
    @classmethod
    def _get_all_path(cls):
        return cls.resource_name

    @classmethod
    def all(cls, connection=None, **params):
        """
            Returns first page if no params passed in as a list.
        """

        request = cls._make_request('GET', cls._get_all_path(), connection, params=params)
        return cls._create_object(request, connection=connection)

    @classmethod
    def iterall(cls, connection=None, **kwargs):
        """
            Returns a autopaging generator that yields each object returned one by one.
        """

        try:
            limit = kwargs['limit']
        except KeyError:
            limit = None

        try:
            page = kwargs['page']
        except KeyError:
            page = None

        def _all_responses():
            page = 1  # one based
            params = kwargs.copy()

            while True:
                params.update(page=page, limit=250)
                rsp = cls._make_request('GET', cls._get_all_path(), connection, params=params)
                if rsp:
                    yield rsp
                    page += 1
                else:
                    yield []  # needed for case where there is no objects
                    break

        if not (limit or page):
            for rsp in _all_responses():
                for obj in rsp:
                    yield cls._create_object(obj, connection=connection)

        else:
            response = cls._make_request('GET', cls._get_all_path(), connection, params=kwargs)
            for obj in cls._create_object(response, connection=connection):
                yield obj


class ListableApiSubResource(ApiSubResource):
    @classmethod
    def _get_all_path(cls, parentid=None):
        # Not all sub resources require a parent id.  Eg: /api/v2/products/skus?sku=<value>
        if (parentid):
            return "%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name)
        else: 
            return "%s/%s" % (cls.parent_resource, cls.resource_name)

    @classmethod
    def all(cls, parentid=None, connection=None, **params):
        response = cls._make_request('GET', cls._get_all_path(parentid), connection, params=params)
        return cls._create_object(response, connection=connection)


class UpdateableApiResource(ApiResource):
    def _update_path(self):
        return "%s/%s" % (self.resource_name, self.id)

    def update(self, **updates):
        response = self._make_request('PUT', self._update_path(), self._connection, data=updates)
        return self._create_object(response, connection=self._connection)


class UpdateableApiSubResource(ApiSubResource):
    def _update_path(self):
        return "%s/%s/%s/%s" % (self.parent_resource, self.parent_id(), self.resource_name, self.id)

    def update(self, **updates):
        response = self._make_request('PUT', self._update_path(), self._connection, data=updates)
        return self._create_object(response, connection=self._connection)


class DeleteableApiResource(ApiResource):
    def _delete_path(self):
        return "%s/%s" % (self.resource_name, self.id)

    def delete(self):
        return self._make_request('DELETE', self._delete_path(), self._connection)


class DeleteableApiSubResource(ApiSubResource):
    def _delete_path(self):
        return "%s/%s/%s/%s" % (self.parent_resource, self.parent_id(), self.resource_name, self.id)

    def delete(self):
        return self._make_request('DELETE', self._delete_path(), self._connection)


class CollectionDeleteableApiResource(ApiResource):
    @classmethod
    def _delete_all_path(cls):
        return cls.resource_name

    @classmethod
    def delete_all(cls, connection=None):
        return cls._make_request('DELETE', cls._delete_all_path(), connection)


class CollectionDeleteableApiSubResource(ApiSubResource):
    @classmethod
    def _delete_all_path(cls, parentid):
        return "%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name)

    @classmethod
    def delete_all(cls, parentid, connection=None):
        return cls._make_request('DELETE', cls._delete_all_path(parentid), connection)


class CountableApiResource(ApiResource):
    @classmethod
    def _count_path(cls):
        return "%s/count" % (cls.resource_name)

    @classmethod
    def count(cls, connection=None, **params):
        response = cls._make_request('GET', cls._count_path(), connection, params=params)
        return response['count']


class CountableApiSubResource(ApiSubResource):
    # Account for the fairly common case where the count path doesn't include the parent id
    count_resource = None

    @classmethod
    def _count_path(cls, parentid=None):
        if parentid is not None:
            return "%s/%s/%s/count" % (cls.parent_resource, parentid, cls.resource_name)
        elif cls.count_resource is not None:
            return "%s/count" % (cls.count_resource)
        else:
            # misconfiguration
            raise NotImplementedError('Count not implemented for this resource.')

    @classmethod
    def count(cls, parentid=None, connection=None, **params):
        response = cls._make_request('GET', cls._count_path(parentid), connection, params=params)
        return response['count']
