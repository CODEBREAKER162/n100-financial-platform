import pytest
import sqlite3
from unittest.mock import patch
import pandas as pd
from src.etl.loader import load_financial_records, load_raw_data


def test_load_financial_records(tmp_path):
    db_file = str(tmp_path / "test_finance.db")
    records = [
        {"amount": 150.50, "vendor": "Acme Corp"},
        {"amount": 99.99, "vendor": "Beta LLC"},
    ]
    inserted_count = load_financial_records(records, db_file)
    assert inserted_count == 2

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT amount, vendor FROM financial_transactions")
    rows = cursor.fetchall()
    conn.close()
    assert len(rows) == 2


def test_load_financial_records_empty(tmp_path):
    db_file = str(tmp_path / "test_empty.db")
    inserted = load_financial_records([], db_file)
    assert inserted == 0


def test_load_raw_data_csv(tmp_path):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("amount,vendor\n100,Acme\n200,Beta")
    df = load_raw_data(str(csv_file))
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


@patch("pandas.read_excel")
def test_load_raw_data_excel(mock_read_excel):
    mock_read_excel.return_value = pd.DataFrame([{"amount": 100, "vendor": "Acme"}])
    df = load_raw_data("data.xlsx")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    mock_read_excel.assert_called_once_with("data.xlsx")


def test_load_raw_data_invalid_format():
    with pytest.raises(ValueError, match="Unsupported file format"):
        load_raw_data("data.txt")


def test_load_raw_data_non_string():
    df = load_raw_data(123)
    assert df.empty
