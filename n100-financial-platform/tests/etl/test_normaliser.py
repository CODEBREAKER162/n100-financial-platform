import pytest
import pandas as pd
from src.etl.normaliser import clean_financial_data, normalise_financial_data


def test_clean_financial_data_valid():
    assert clean_financial_data("$1,234.56") == 1234.56
    assert clean_financial_data({"amount": "150.0"}) == 150.0
    assert clean_financial_data(100) == 100.0


def test_clean_financial_data_missing_key():
    assert clean_financial_data({}) is None


def test_clean_financial_data_invalid_string():
    with pytest.raises(ValueError):
        clean_financial_data("invalid_amount")


def test_clean_financial_data_complex_type():
    with pytest.raises(TypeError):
        clean_financial_data(1 + 2j)


def test_clean_financial_data_unsupported_type():
    with pytest.raises(TypeError, match="Unsupported data type"):
        clean_financial_data([1, 2, 3])


def test_normalise_financial_data_empty():
    assert normalise_financial_data(None).empty
    assert normalise_financial_data(pd.DataFrame()).empty

