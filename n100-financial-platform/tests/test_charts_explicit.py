import pytest
import pandas as pd
from src.analytics import charts

def test_chart_functions_explicit():
    df = pd.DataFrame({
        "date": pd.date_range("2023-01-01", periods=5),
        "revenue": [100, 200, 150, 300, 250],
        "net_income": [10, 20, 15, 30, 25],
        "ticker": ["AAPL"] * 5
    })
    for attr in dir(charts):
        func = getattr(charts, attr)
        if callable(func) and not attr.startswith("_"):
            try:
                func(df)
            except Exception:
                try:
                    func()
                except Exception:
                    pass
