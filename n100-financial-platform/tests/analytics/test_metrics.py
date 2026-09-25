import pytest
from src.analytics.metrics import (
    compute_cagr,
    compute_sharpe_ratio,
    compute_sortino_ratio,
    compute_free_cash_flow,
    compute_ocf_to_net_profit,
)


def test_compute_cagr_valid():
    cagr = compute_cagr(100.0, 200.0, 3)
    assert pytest.approx(cagr, 0.01) == 25.99


def test_compute_cagr_invalid_inputs():
    assert compute_cagr(None, 100.0, 3) is None
    assert compute_cagr(100.0, None, 3) is None
    assert compute_cagr(100.0, 200.0, 0) is None
    assert compute_cagr(0.0, 200.0, 3) is None
    assert compute_cagr(-100.0, 200.0, 3) is None


def test_compute_sharpe_ratio_valid():
    returns = [0.01, 0.02, -0.005, 0.015, 0.03, -0.01]
    sharpe = compute_sharpe_ratio(returns, risk_free_rate=0.05, periods_per_year=252)
    assert sharpe is not None
    assert isinstance(sharpe, float)


def test_compute_sharpe_ratio_zero_std():
    returns = [0.01, 0.01, 0.01, 0.01]
    assert compute_sharpe_ratio(returns) is None


def test_compute_sharpe_ratio_edge_cases():
    assert compute_sharpe_ratio(None) is None
    assert compute_sharpe_ratio([0.01]) is None
    assert compute_sharpe_ratio([]) is None


def test_compute_sortino_ratio_valid():
    returns = [0.02, 0.01, -0.015, 0.03, -0.02, 0.015]
    sortino = compute_sortino_ratio(
        returns, risk_free_rate=0.05, target_return=0.0, periods_per_year=252
    )
    assert sortino is not None
    assert isinstance(sortino, float)


def test_compute_sortino_ratio_no_downside():
    returns = [0.01, 0.02, 0.03, 0.04]
    assert compute_sortino_ratio(returns, target_return=0.0) is None


def test_compute_sortino_ratio_edge_cases():
    assert compute_sortino_ratio(None) is None
    assert compute_sortino_ratio([0.01]) is None


def test_compute_free_cash_flow():
    assert compute_free_cash_flow(150.0, 50.0) == 100.0
    assert compute_free_cash_flow(None, 50.0) is None
    assert compute_free_cash_flow(150.0, None) is None


def test_compute_ocf_to_net_profit():
    assert compute_ocf_to_net_profit(120.0, 100.0) == 1.2
    assert compute_ocf_to_net_profit(120.0, 0.0) is None
    assert compute_ocf_to_net_profit(None, 100.0) is None
    assert compute_ocf_to_net_profit(120.0, None) is None
