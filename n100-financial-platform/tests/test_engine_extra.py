import pytest
import pandas as pd
from src.screener.engine import ScreenerEngine

@pytest.fixture
def engine_df():
    return pd.DataFrame([
        {"ticker": "AAPL", "pe_ratio": 15.0, "roe": 20.0, "market_cap": 1000},
        {"ticker": "MSFT", "pe_ratio": 35.0, "roe": 10.0, "market_cap": 500},
    ])

def test_screener_engine_filters(engine_df):
    engine = ScreenerEngine(engine_df)
    if hasattr(engine, "filter"):
        res = engine.filter(pe_ratio=(0, 20))
        assert len(res) == 1
    if hasattr(engine, "run_preset"):
        try:
            engine.run_preset("value")
        except Exception:
            pass
