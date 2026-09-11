import os
import pytest
import pandas as pd
from src.screener.exporter import export_screener_results, export_peer_comparison

@pytest.fixture
def sample_export_data():
    return {
        "Tech": pd.DataFrame([{"ticker": "AAPL", "roe": 25.0}]),
        "Banking": pd.DataFrame([{"ticker": "JPM", "roe": 15.0}])
    }

def test_export_screener_results(sample_export_data, tmp_path):
    output_file = tmp_path / "screener.xlsx"
    export_screener_results(sample_export_data, str(output_file))
    assert os.path.exists(output_file)

def test_export_peer_comparison(sample_export_data, tmp_path):
    output_file = tmp_path / "peers.xlsx"
    export_peer_comparison(sample_export_data, str(output_file))
    assert os.path.exists(output_file)
