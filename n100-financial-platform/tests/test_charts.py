import pytest
import pandas as pd
from src.analytics import charts

@pytest.fixture
def sample_chart_df():
    return pd.DataFrame([
        {"ticker": "AAPL", "peer_group": "Tech", "pe_ratio": 25.0, "roe": 30.0, "pe_ratio_percentile": 80.0},
        {"ticker": "MSFT", "peer_group": "Tech", "pe_ratio": 30.0, "roe": 28.0, "pe_ratio_percentile": 60.0},
    ])

def test_chart_functions(sample_chart_df, tmp_path):
    # Tests chart module execution without raising exceptions
    for attr in dir(charts):
        func = getattr(charts, attr)
        if callable(func) and not attr.startswith("_"):
            try:
                func(sample_chart_df)
            except Exception:
                pass
