from bigcommerce.api import connection
from bigcommerce.api.exception import NotLoggedInException


class Mapping(dict):
    """
    Mapping

    provides '.' access to dictionary keys
    """
    def __init__(self, mapping, *args, **kwargs):
        filter_args = {k: mapping[k] for k in mapping if k not in dir(self)}
        self.__dict__ = self
        dict.__init__(self, filter_args, *args, **kwargs)

class ApiResource(Mapping):
    resource_name = ""

    @classmethod
    def _create_object(cls, response):
        if isinstance(response, list):
            return [cls._create_object(obj) for obj in response]
        else:
            return cls(response)

    @classmethod
    def _make_request(cls, method, url, data=None, params={}, headers={}):
        if connection.client:
            return connection.client.make_request(method, url, data, params, headers)
        else:
            raise NotLoggedInException()

    @classmethod
    def get(cls, id, **params):
        return cls._create_object(cls._make_request('GET', "%s/%s" % (cls.resource_name, id), params=params))


class ApiSubResource(ApiResource):
    parent_resource = ""

    @classmethod
    def get(cls, parentid, id, **params):
        path = "%s/%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name, id)
        return cls._create_object(cls._make_request('GET', path, params=params))


class CreateableApiResource(ApiResource):
    pass


class CreateableApiSubResource(ApiSubResource):
    pass


class ListableApiResource(ApiResource):
    @classmethod
    def all(cls, **params):
        return cls._create_object(cls._make_request('GET', cls.resource_name, params=params))


class ListableApiSubResource(ApiSubResource):
    @classmethod
    def all(cls, parentid, **params):
        path = "%s/%s/%s" % (cls.parent_resource, parentid, cls.resource_name)
        return cls._create_object(cls._make_request('GET', path, params=params))


class UpdateableApiResource(ApiResource):
    pass


class UpdateableApiSubResource(ApiResource):
    pass


class DeleteableApiResource(ApiResource):
    pass


class DeleteableApiSubResource(ApiResource):
    pass