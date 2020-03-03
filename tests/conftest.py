import pytest

from cosmic.base import Product, Customer


@pytest.fixture
def product_one():
    return Product(name="RED-CHAIR")


@pytest.fixture
def product_two():
    return Product(name="TASTELESS-LAMP")


@pytest.fixture
def customer_one():
    return Customer(name="luca")
