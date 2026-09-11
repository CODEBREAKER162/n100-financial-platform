import pandas as pd


def validate_financial_record(record: dict) -> bool:
    """Validates an individual financial record dictionary."""
    if not isinstance(record, dict) or "amount" not in record:
        return False

    amount = record["amount"]
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        return False

    return amount >= 0.0


def validate_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validates raw financial dataframe and drops fully empty rows/columns."""
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        return pd.DataFrame()

    return df.dropna(how="all")


validate_raw_records = validate_financial_data
