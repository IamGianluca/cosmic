from datetime import date, timedelta

import pytest

from cosmic.model import Batch, OrderLine, OutOfStock, allocate

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=2)


def test_prefers_current_stock_batches_to_shipments():
    # given
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    line = OrderLine("oref", "RETRO-CLOCK", 10)

    # when
    allocate(line, [in_stock_batch, shipment_batch])

    # then
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    # given
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = OrderLine("order1", "MINIMALIST-SPOON", 10)

    # when
    allocate(line, [medium, earliest, latest])

    # then
    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch(
        "in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=None
    )
    shipment_batch = Batch(
        "in-stock-batch-ref", "HIGHBROW-POSTER", 100, eta=tomorrow
    )
    line = OrderLine("oref", "HIGHBROW-POSTER", 10)

    # when
    allocation = allocate(line, [in_stock_batch, shipment_batch])

    # then
    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    # given
    batch = Batch("batch1", "SMALL-FORK", 10, eta=today)
    allocate(OrderLine("order1", "SMALL-FORK", 10), [batch])

    # when / then
    with pytest.raises(OutOfStock, match="SMALL-FORK"):
        allocate(OrderLine("order2", "SMALL-FORK", 1), [batch])
