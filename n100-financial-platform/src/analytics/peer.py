import sqlite3
import pandas as pd
import numpy as np

def compute_peer_percentiles(df: pd.DataFrame, metrics: list) -> pd.DataFrame:
    """
    Computes PERCENT_RANK (0-100) for given metrics within each peer group.
    Inverts ranking for metrics like Debt-to-Equity (where lower is better).
    """
    ranked_df = df.copy()
    
    lower_is_better = ['debt_to_equity', 'de', 'pe_ratio', 'pb_ratio']

    for metric in metrics:
        if metric in ranked_df.columns:
            percentile_col = f"{metric}_percentile"
            
            ascending_flag = metric in lower_is_better
            ranked_df[percentile_col] = ranked_df.groupby('peer_group')[metric].rank(
                pct=True, ascending=ascending_flag
            ) * 100
            
            if ascending_flag:
                ranked_df[percentile_col] = 100 - ranked_df[percentile_col]

    return ranked_df

def save_percentiles_to_sqlite(df: pd.DataFrame, db_path: str = "db/n100_finance.db"):
    """Populates peer_percentiles table in SQLite database."""
    conn = sqlite3.connect(db_path)
    df.to_sql("peer_percentiles", conn, if_exists="replace", index=False)
    conn.close()
