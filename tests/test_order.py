import pytest

from uuid import UUID
from cosmic.base import Customer, Order, OrderLine, Product


def test_customer_place_order(customer_one, product_one, product_two):
    """An order is identified by an order reference, and comprises multiple
    order lines, where each line has a SKU and a quantity.
    """
    # given
    order_line_one = OrderLine(product=product_one, qty=10)
    order_line_two = OrderLine(product=product_two, qty=1)

    # when
    order = Order(
        customer=customer_one, order_lines=[order_line_one, order_line_two]
    )

    # then
    assert len(order.order_lines) == 2
    assert order.order_lines[0] == order_line_one
    assert order.order_lines[1] == order_line_two


def test_batch_of_stock():
    """The purchasing department orders small batches of stock. A batch of
    stock has a unique ID called a reference, a SKU and a quantity.
    """
