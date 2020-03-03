import pytest

from cosmic.base import Customer


@pytest.mark.parametrize(
    "customer_name", (("brig"), ("al")),
)
def test_customer(customer_name):
    """A customer has a name."""
    # when
    c = Customer(name=customer_name)

    # then
    assert c.name == customer_name
