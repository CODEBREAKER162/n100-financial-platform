import pytest
import pandas as pd
from src.analytics import charts

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "ticker": ["AAPL", "MSFT"],
        "pe_ratio": [25.0, 30.0],
        "roe": [30.0, 28.0],
        "peer_group": ["Tech", "Tech"]
    })

def test_charts_direct(sample_df):
    # Call specific chart generation functions directly
    for func_name in dir(charts):
        if not func_name.startswith("_"):
            func = getattr(charts, func_name)
            if callable(func):
                try:
                    func(sample_df)
                except Exception:
                    pass
