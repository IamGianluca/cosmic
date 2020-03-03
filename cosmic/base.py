from typing import List, Tuple
from uuid import uuid4


class Product:
    def __init__(self, name: str):
        self.name = name
        self.sku = uuid4()

    def __eq__(self, other):
        return all([self.name == other.name, self.sku == other.sku])


class Customer:
    def __init__(self, name: str):
        self.name = name


class OrderLine:
    def __init__(self, product: Product, qty: int):
        self.product = product
        self.qty = qty
        self.id = uuid4()

    def __eq__(self, other):
        return all(
            [
                self.id == other.id,
                self.qty == other.qty,
                self.product == other.product,
            ]
        )


class Order:
    def __init__(self, customer: Customer, order_lines: List[OrderLine]):
        self.order_reference = uuid4()
        self.customer = customer
        self.order_lines = order_lines
