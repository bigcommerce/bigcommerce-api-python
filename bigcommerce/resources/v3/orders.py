from ..base import *

# TODO: test
class Orders(ApiResource):
    resource_version = 'v3'
    resource_name = 'orders'

    # TODO: add functions for subresources


class OrderMetafields(ListableApiSubResource, CreateableApiSubResource, UpdateableApiSubResource, DeleteableApiSubResource):
    resource_version = Orders.resource_version
    resource_name = 'metafields'
    parent_resource = Orders.resource_name
    parent_key = 'order_id'


class OrderPaymentActionsCapture(CreateableApiSubResource):
    resource_version = Orders.resource_version
    resource_name = 'payment_actions/capture'
    parent_resource = Orders.resource_name
    parent_key = 'order_id'


class OrderPaymentActionsRefundQuotes(CreateableApiSubResource):
    resource_version = Orders.resource_version
    resource_name = 'payment_actions/refund_quotes'
    parent_resource = Orders.resource_name
    parent_key = 'order_id'


class OrderPaymentActionsRefunds(ListableApiSubResource, CreateableApiSubResource, UpdateableApiSubResource, DeleteableApiSubResource):
    resource_version = Orders.resource_version
    resource_name = 'payment_actions/refunds'
    parent_resource = Orders.resource_name
    parent_key = 'order_id'


class OrderPaymentActionsVoid(CreateableApiSubResource):
    resource_version = Orders.resource_version
    resource_name = 'payment_actions/void'
    parent_resource = Orders.resource_name
    parent_key = 'order_id'


class OrderTransactions(ListableApiSubResource):
    resource_version = Orders.resource_version
    resource_name = 'transactions'
    parent_resource = Orders.resource_name
    parent_key = 'order_id'