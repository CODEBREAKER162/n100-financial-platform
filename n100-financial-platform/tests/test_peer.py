import pytest
import sqlite3
import pandas as pd
from src.analytics.peer import compute_peer_percentiles, save_percentiles_to_sqlite

@pytest.fixture
def sample_peer_df():
    return pd.DataFrame([
        {"ticker": "AAPL", "peer_group": "Tech", "pe_ratio": 25.0, "debt_to_equity": 1.2},
        {"ticker": "MSFT", "peer_group": "Tech", "pe_ratio": 30.0, "debt_to_equity": 0.8},
        {"ticker": "NVDA", "peer_group": "Tech", "pe_ratio": 45.0, "debt_to_equity": 0.5},
    ])

def test_compute_peer_percentiles(sample_peer_df):
    metrics = ["pe_ratio", "debt_to_equity"]
    result_df = compute_peer_percentiles(sample_peer_df, metrics)
    
    assert "pe_ratio_percentile" in result_df.columns
    assert "debt_to_equity_percentile" in result_df.columns
    # Lower pe_ratio gets a higher percentile because lower is better
    assert result_df.loc[result_df["ticker"] == "AAPL", "pe_ratio_percentile"].values[0] > result_df.loc[result_df["ticker"] == "NVDA", "pe_ratio_percentile"].values[0]

def test_save_percentiles_to_sqlite(sample_peer_df, tmp_path):
    db_file = tmp_path / "test_n100.db"
    save_percentiles_to_sqlite(sample_peer_df, str(db_file))
    
    conn = sqlite3.connect(db_file)
    df_db = pd.read_sql("SELECT * FROM peer_percentiles", conn)
    conn.close()
    
    assert len(df_db) == 3
