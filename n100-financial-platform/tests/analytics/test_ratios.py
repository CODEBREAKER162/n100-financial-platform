import pytest
from src.analytics.ratios import (
    calculate_quick_ratio,
    compute_pb_ratio,
    compute_roe,
    compute_pe_ratio,
)


def test_calculate_quick_ratio():
    assert calculate_quick_ratio(1000, 500, 200, 400) == 4.25


def test_calculate_quick_ratio_zero_liabilities():
    with pytest.raises(ValueError, match="Current liabilities cannot be zero"):
        calculate_quick_ratio(1000, 500, 500, 0)


def test_compute_pe_ratio():
    assert compute_pe_ratio(100, 5) == 20.0


def test_compute_pe_ratio_zero_eps():
    with pytest.raises(ValueError):
        compute_pe_ratio(100, 0)


def test_compute_pe_ratio_negative_eps():
    with pytest.raises(ValueError):
        compute_pe_ratio(100, -5)


def test_compute_pb_ratio():
    assert compute_pb_ratio(100, 50) == 2.0


def test_compute_pb_ratio_zero_book_value():
    with pytest.raises(ValueError):
        compute_pb_ratio(100, 0)


def test_compute_pb_ratio_negative_book_value():
    with pytest.raises(ValueError):
        compute_pb_ratio(100, -50)


def test_compute_roe():
    assert compute_roe(100, 500) == 20.0


def test_compute_roe_zero_equity():
    with pytest.raises(ValueError):
        compute_roe(100, 0)


def test_compute_roe_negative_equity():
    with pytest.raises(ValueError):
        compute_roe(100, -500)
