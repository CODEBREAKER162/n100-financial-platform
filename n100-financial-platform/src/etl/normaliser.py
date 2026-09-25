import pandas as pd


def clean_financial_data(data):
    """Cleans currency strings into floats or handles raw dictionary records."""
    if isinstance(data, (complex)):
        raise TypeError("Invalid data type for financial normalization.")

    if isinstance(data, str):
        cleaned_str = data.strip().replace("$", "").replace(",", "")
        try:
            return float(cleaned_str)
        except ValueError:
            raise ValueError(f"Cannot parse amount string: {data}")

    if isinstance(data, dict):
        if "amount" not in data:
            return None
        return clean_financial_data(data["amount"])

    if isinstance(data, (int, float)):
        return float(data)

    raise TypeError(f"Unsupported data type: {type(data)}")


def normalise_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalizes financial column names and formats for DataFrames."""
    if df is None or getattr(df, "empty", False):
        return pd.DataFrame() if df is None else df.copy()

    df_clean = df.copy()
    df_clean.columns = [
        str(c).strip().lower().replace(" ", "_") for c in df_clean.columns
    ]
    return df_clean


normalize_financial_data = normalise_financial_data
