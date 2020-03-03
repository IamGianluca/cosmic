import pytest
from uuid import UUID

from cosmic.base import Product


@pytest.mark.parametrize(
    "product_name", (("one"), ("two")),
)
def test_product(product_name):
    """A product is identified by a SKU, pronounced "skew," which is short
    for stock keeping unit.
    """
    # when
    product = Product(name=product_name)

    # then
    assert product.name == product_name
    assert isinstance(product.sku, UUID)
