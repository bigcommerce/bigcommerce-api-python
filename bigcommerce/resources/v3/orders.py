from ..base import *

# TODO: test
class OrderMetafields(ListableApiSubResource, CreateableApiSubResource, UpdateableApiSubResource, DeleteableApiSubResource):
    resource_version = 'v3'
    resource_name = 'metafields'
    parent_resource = 'orders'
    parent_key = 'order_id'


class OrderPaymentActionsCapture(CreateableApiSubResource):
    resource_version = 'v3'
    resource_name = 'payment_actions/capture'
    parent_resource = 'orders'
    parent_key = 'order_id'


class OrderPaymentActionsRefundQuotes(CollectionCreatableApiSubResource):
    resource_version = 'v3'
    resource_name = 'payment_actions/refund_quotes'
    parent_resource = 'orders'
    parent_key = 'order_id'


class OrderPaymentActionsRefunds(ListableApiSubResource, CreateableApiSubResource, UpdateableApiSubResource, DeleteableApiSubResource):
    resource_version = 'v3'
    resource_name = 'payment_actions/refunds'
    parent_resource = 'orders'
    parent_key = 'order_id'


class OrderPaymentActionsVoid(CreateableApiSubResource):
    resource_version = 'v3'
    resource_name = 'payment_actions/void'
    parent_resource = 'orders'
    parent_key = 'order_id'


class OrderTransactions(ListableApiSubResource):
    resource_version = 'v3'
    resource_name = 'transactions'
    parent_resource = 'orders'
    parent_key = 'order_id'