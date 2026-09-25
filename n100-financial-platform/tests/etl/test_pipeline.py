import pytest
import pandas as pd
from src.etl.pipeline import process_financial_pipeline, run_etl_job


def test_process_financial_pipeline_empty():
    df = pd.DataFrame()
    result = process_financial_pipeline(df)
    assert result.empty


def test_process_financial_pipeline_full():
    data = {
        "Price": [100.0],
        "EPS": [5.0],
        "Book Value": [20.0],
        "Net Income": [50.0],
        "Shareholder Equity": [200.0],
        "Operating Cash Flow": [60.0],
        "Capex": [10.0],
    }
    df = pd.DataFrame(data)
    result = process_financial_pipeline(df)
    assert "pe_ratio" in result.columns
    assert "pb_ratio" in result.columns
    assert "roe" in result.columns
    assert "free_cash_flow" in result.columns
    assert "ocf_to_net_profit" in result.columns


def test_run_etl_job_success(tmp_path):
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text("Price,EPS\n100,5")
    df = run_etl_job(str(csv_file))
    assert not df.empty
    assert "pe_ratio" in df.columns


def test_run_etl_job_unsupported_format():
    with pytest.raises(ValueError, match="Unsupported file format"):
        run_etl_job("invalid_file.txt")
