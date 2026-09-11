import pytest
from src.etl.validator import validate_financial_record


@pytest.mark.parametrize(
    "record, expected_valid",
    [
        ({"amount": 150.50}, True),
        ({"amount": 0.0}, True),
        ({"amount": -50.0}, False),
        ({"amount": "150.50"}, False),  # Uncleaned string format
        ({"vendor": "Acme Corp"}, False),  # Missing amount key
    ],
)
def test_validate_financial_record(record, expected_valid):
    assert validate_financial_record(record) == expected_valid
