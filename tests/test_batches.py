from datetime import date

from copy import deepcopy
import pytest

from cosmic.model import Batch, OrderLine


def make_batch_and_line(sku: str, batch_qty: int, line_qty: int):
    return (
        Batch("batch-001", sku, qty=batch_qty, eta=date.today()),
        OrderLine("order123", sku, qty=line_qty),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    # given
    batch, line = make_batch_and_line("SMALL-TABLE", batch_qty=20, line_qty=2)

    # when
    batch.allocate(line)

    # then
    assert batch.available_quantity == 18


@pytest.mark.parametrize(
    "batch_qty,line_qty,expected",
    [(20, 2, True), (2, 20, False), (2, 2, True)],
)
def test_can_allocate_if_available_greater_than_required(
    batch_qty, line_qty, expected
):
    # given
    large_batch, small_line = make_batch_and_line(
        sku="ELEGANT-LAMP", batch_qty=batch_qty, line_qty=line_qty
    )

    # then
    assert large_batch.can_allocate(small_line) == expected


def test_cannot_allocate_if_skus_do_not_match():
    # given
    batch = Batch("batch-001", "UNCOMFORTABLE-CHAIR", qty=100, eta=None)
    different_sku_line = OrderLine("order123", "EXPENSIVE-TOASTER", qty=10)

    # then
    assert batch.can_allocate(different_sku_line) is False


def test_deallocate_previously_allocated_line():
    """We can deallocate an OrderLine after having it previously allocated
    to a Batch.
    """
    # given
    batch, line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)
    batch.allocate(line)
    assert batch.available_quantity == 18

    # when
    batch.deallocate(line)

    # then
    assert batch.available_quantity == 20


def test_can_only_deallocate_allocated_lines():
    """We can't deallocate an OrderLine that was not previously allocated to
    the Batch.
    """
    # given
    batch, unallocated_line = make_batch_and_line("DECORATIVE-TRINKET", 20, 2)

    # when
    batch.deallocate(unallocated_line)

    # then
    assert batch.available_quantity == 20


def test_allocation_is_idempotent():
    """We can only deallocate a OrderLine that was previously allocated to a
    Batch once.
    """
    # given
    batch, line = make_batch_and_line("ANGULAR-DESK", 20, 2)
    batch.allocate(line)

    batch.allocate(line)
    assert batch.available_quantity == 18


def test_identity_equality():
    """A Batch is an entity, which means that it has identity equality. As
    long as the `reference` in the two Batches is the same, we say that they
    the same thing.
    """
    # given
    batch, line = make_batch_and_line(
        sku="LARGE-TELEVISION", batch_qty=10, line_qty=2
    )
    copy = deepcopy(batch)  # NOTE: this is just a hack to prove our point

    # when
    batch.allocate(line)

    # then
    assert batch == copy
    assert batch.available_quantity == 8
    assert copy.available_quantity == 10


def test_batch_hash():
    # given
    reference = "order174"
    batch = Batch(ref=reference, sku="LOUD-STEREO", qty=19, eta=date.today())

    # when
    actual = hash(batch)

    # then
    assert actual == hash(reference)
