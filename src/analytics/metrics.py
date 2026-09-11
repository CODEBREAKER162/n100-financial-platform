import numpy as np
import pandas as pd
import statsmodels.api as sm

def calculate_cagr(start_value, end_value, num_years):
    """Calculate Compound Annual Growth Rate (CAGR)."""
    if start_value <= 0 or num_years <= 0:
        return 0.0
    return ((end_value / start_value) ** (1 / num_years)) - 1

def calculate_sharpe_ratio(returns, risk_free_rate=0.06):
    """Calculate annualized Sharpe Ratio given daily returns."""
    if len(returns) == 0 or returns.std() == 0:
        return 0.0
    excess_returns = returns - (risk_free_rate / 252)
    return np.sqrt(252) * (excess_returns.mean() / returns.std())

def calculate_sortino_ratio(returns, risk_free_rate=0.06):
    """Calculate annualized Sortino Ratio given daily returns."""
    if len(returns) == 0:
        return 0.0
    downside_returns = returns[returns < 0]
    if len(downside_returns) == 0 or downside_returns.std() == 0:
        return 0.0
    excess_returns = returns - (risk_free_rate / 252)
    return np.sqrt(252) * (excess_returns.mean() / downside_returns.std())

def calculate_max_drawdown(nav_series):
    """Calculate Maximum Drawdown from a series of NAVs or Prices."""
    if len(nav_series) == 0:
        return 0.0
    rolling_max = nav_series.cummax()
    drawdown = (nav_series - rolling_max) / rolling_max
    return float(drawdown.min())

def calculate_beta_ols(stock_returns, benchmark_returns):
    """Calculate Stock Beta relative to Benchmark using OLS Regression."""
    if len(stock_returns) != len(benchmark_returns) or len(stock_returns) == 0:
        return 1.0
    
    df = pd.DataFrame({'stock': stock_returns, 'benchmark': benchmark_returns}).dropna()
    X = sm.add_constant(df['benchmark'])
    model = sm.OLS(df['stock'], X).fit()
    return float(model.params['benchmark'])
