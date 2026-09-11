import sqlite3
import pandas as pd


def load_financial_records(records: list, db_path: str) -> int:
    """Inserts a list of record dictionaries into an SQLite database."""
    if not records:
        return 0

    conn = sqlite3.connect(db_path)
    df = pd.DataFrame(records)
    df.to_sql("financial_transactions", conn, if_exists="append", index=False)
    inserted_count = len(df)
    conn.close()
    return inserted_count


def load_raw_data(file_path: str, *args, **kwargs) -> pd.DataFrame:
    """Loads raw financial dataset from CSV or Excel file."""
    if not isinstance(file_path, str):
        return pd.DataFrame()

    if file_path.endswith(".csv"):
        return pd.read_csv(file_path, *args, **kwargs)
    elif file_path.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_path, *args, **kwargs)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
