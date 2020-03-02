from uuid import uuid4

from typing import List, Tuple


class Product:
    def __init__(self, name: str):
        self.name = name
        self.sku = uuid4()


class Customer:
    def __init__(self, name: str):
        self.name = name


class OrderLine:
    def __init__(self, product: Product, qty: int):
        self.product = product
        self.qty = qty
        self.id = uuid4()

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False


class Order:
    def __init__(self, customer: Customer, order_lines: List[OrderLine]):
        self.customer = customer
        self.order_lines = order_lines
