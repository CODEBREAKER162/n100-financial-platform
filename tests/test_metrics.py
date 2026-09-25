import pytest
import pandas as pd
import numpy as np
from src.analytics.metrics import calculate_cagr, calculate_sharpe_ratio, calculate_sortino_ratio, calculate_max_drawdown, calculate_beta_ols

def test_calculate_cagr():
    assert round(calculate_cagr(100, 200, 5), 4) == 0.1487
    assert calculate_cagr(0, 100, 5) == 0.0
    assert calculate_cagr(100, 200, 0) == 0.0

def test_calculate_sharpe_ratio():
    returns = pd.Series([0.01, 0.02, -0.01, 0.015, 0.005])
    sharpe = calculate_sharpe_ratio(returns)
    assert isinstance(sharpe, float)

def test_calculate_sortino_ratio():
    returns = pd.Series([0.01, -0.02, 0.015, -0.005, 0.02])
    sortino = calculate_sortino_ratio(returns)
    assert isinstance(sortino, float)

def test_calculate_max_drawdown():
    nav = pd.Series([100, 110, 105, 95, 120])
    mdd = calculate_max_drawdown(nav)
    assert round(mdd, 4) == -0.1364

def test_calculate_beta_ols():
    stock_returns = pd.Series([0.01, 0.02, 0.015, -0.01, 0.005])
    benchmark_returns = pd.Series([0.008, 0.015, 0.01, -0.008, 0.004])
    beta = calculate_beta_ols(stock_returns, benchmark_returns)
    assert isinstance(beta, float)
    assert beta > 0

from src.analytics.scoring import compute_composite_score

def test_compute_composite_score():
    score = compute_composite_score(roe_pct=18.5, roce_pct=22.0, pe_ratio=24.5, debt_to_equity=0.3, net_margin_pct=14.2)
    assert isinstance(score, float)
    assert 0 <= score <= 100
