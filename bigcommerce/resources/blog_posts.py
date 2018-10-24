from .base import *


class BlogPosts(ListableApiResource, CreateableApiResource,
              UpdateableApiResource, DeleteableApiResource,
              CountableApiResource, CollectionDeleteableApiResource):
    resource_name = 'blog/posts'
