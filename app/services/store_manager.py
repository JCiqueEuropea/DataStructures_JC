from typing import List

from app.models import ProductResponse, OrderResponse
from app.models.structures import BSTNode, ListNode


class DataStore:
    def __init__(self):
        self.products_root: BSTNode | None = None
        self.orders_head: ListNode | None = None

    def insert_product(self, product: ProductResponse):
        if not self.products_root:
            self.products_root = BSTNode(product)
        else:
            self._insert_bst_recursive(self.products_root, product)

    def _insert_bst_recursive(self, node: BSTNode, product: ProductResponse):
        if product.id < node.product.id:
            if node.left is None:
                node.left = BSTNode(product)
            else:
                self._insert_bst_recursive(node.left, product)
        else:
            if node.right is None:
                node.right = BSTNode(product)
            else:
                self._insert_bst_recursive(node.right, product)

    def find_product(self, product_id: int) -> ProductResponse | None:
        return self._search_bst(self.products_root, product_id)

    def _search_bst(self, node: BSTNode, product_id: int):
        if node is None or node.product.id == product_id:
            return node.product if node else None
        if product_id < node.product.id:
            return self._search_bst(node.left, product_id)
        return self._search_bst(node.right, product_id)

    def add_order(self, order: OrderResponse):
        if self.update_order_node(order):
            return

        new_node = ListNode(order)
        if not self.orders_head:
            self.orders_head = new_node
        else:
            current = self.orders_head
            while current.next:
                current = current.next
            current.next = new_node

    def get_order(self, order_id: int) -> OrderResponse | None:
        current = self.orders_head
        while current:
            if current.order.id == order_id:
                return current.order
            current = current.next
        return None

    def get_all_orders(self) -> List[OrderResponse]:
        orders = []
        current = self.orders_head
        while current:
            orders.append(current.order)
            current = current.next
        return orders

    def remove_order(self, order_id: int) -> bool:
        current = self.orders_head
        prev = None
        while current:
            if current.order.id == order_id:
                if prev:
                    prev.next = current.next
                else:
                    self.orders_head = current.next
                return True
            prev = current
            current = current.next
        return False

    def update_order_node(self, updated_order: OrderResponse) -> bool:
        current = self.orders_head
        while current:
            if current.order.id == updated_order.id:
                current.order = updated_order
                return True
            current = current.next
        return False


store = DataStore()
