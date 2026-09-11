import numpy as np
import pandas as pd


def compute_cagr(start_value: float, end_value: float, periods: float) -> float | None:
    if (
        start_value is None
        or end_value is None
        or periods is None
        or start_value <= 0
        or end_value <= 0
        or periods <= 0
    ):
        return None

    return ((end_value / start_value) ** (1.0 / periods) - 1.0) * 100.0


def compute_sharpe_ratio(
    returns: list[float] | pd.Series | np.ndarray,
    risk_free_rate: float = 0.05,
    periods_per_year: int = 252,
) -> float | None:
    if returns is None:
        return None

    arr = np.asarray(returns, dtype=float)
    arr = arr[~np.isnan(arr)]

    if len(arr) < 2:
        return None

    std_dev = np.std(arr, ddof=1)
    if std_dev == 0 or np.isnan(std_dev):
        return None

    rf_per_period = risk_free_rate / periods_per_year
    excess_returns = arr - rf_per_period
    mean_excess_return = np.mean(excess_returns)

    sharpe = (mean_excess_return / std_dev) * np.sqrt(periods_per_year)
    return float(sharpe)


def compute_sortino_ratio(
    returns: list[float] | pd.Series | np.ndarray,
    risk_free_rate: float = 0.05,
    target_return: float = 0.0,
    periods_per_year: int = 252,
) -> float | None:
    if returns is None:
        return None

    arr = np.asarray(returns, dtype=float)
    arr = arr[~np.isnan(arr)]

    if len(arr) < 2:
        return None

    rf_per_period = risk_free_rate / periods_per_year
    excess_returns = arr - rf_per_period

    downside_diff = np.minimum(arr - target_return, 0.0)
    downside_variance = np.mean(downside_diff**2)
    downside_deviation = np.sqrt(downside_variance)

    if downside_deviation == 0 or np.isnan(downside_deviation):
        return None

    sortino = (np.mean(excess_returns) / downside_deviation) * np.sqrt(periods_per_year)
    return float(sortino)


def compute_free_cash_flow(operating_cash_flow: float, capex: float) -> float | None:
    """Calculates Free Cash Flow (FCF = OCF - CapEx)."""
    if operating_cash_flow is None or capex is None:
        return None
    return operating_cash_flow - capex


def compute_ocf_to_net_profit(
    operating_cash_flow: float, net_profit: float
) -> float | None:
    """Calculates Operating Cash Flow to Net Profit ratio."""
    if operating_cash_flow is None or net_profit is None or net_profit == 0:
        return None
    return operating_cash_flow / net_profit
