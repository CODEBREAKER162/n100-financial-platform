import pytest
import pandas as pd
from src.screener.engine import filter_financial_ratios, apply_preset_screener, ScreenerEngine

@pytest.fixture
def sample_screener_df():
    return pd.DataFrame([
        {"ticker": "AAPL", "roe": 25.0, "debt_to_equity": 0.4, "pe_ratio": 12.0, "sector": "Technology"},
        {"ticker": "JPM", "roe": 18.0, "debt_to_equity": 2.5, "pe_ratio": 10.0, "sector": "Banking"},
        {"ticker": "XYZ", "roe": -5.0, "debt_to_equity": 0.1, "pe_ratio": -8.0, "sector": "Industrial"},
    ])

def test_filter_negative_thresholds(sample_screener_df):
    res = filter_financial_ratios(sample_screener_df, min_roe=-10.0)
    assert len(res) == 3

def test_filter_empty_dataframe():
    empty_df = pd.DataFrame()
    res = filter_financial_ratios(empty_df, min_roe=15.0)
    assert res.empty

def test_apply_preset_unknown_key(sample_screener_df):
    res = apply_preset_screener(sample_screener_df, preset_key="non_existent_preset")
    assert len(res) == len(sample_screener_df)

def test_screener_engine_missing_file():
    engine = ScreenerEngine(data_filepath="non_existent_path.csv")
    results = engine.run_preset(preset_key="quality_compounder")
    assert results == []
