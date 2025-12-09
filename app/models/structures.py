from typing import Optional

from app.models.orders import OrderResponse
from app.models.products import ProductResponse


class BSTNode:
    def __init__(self, product: ProductResponse):
        self.product = product
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None


class ListNode:
    def __init__(self, order: OrderResponse):
        self.order = order
        self.next: Optional['ListNode'] = None
