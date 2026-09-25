import pandas as pd
from src.analytics.metrics import (
    compute_free_cash_flow,
    compute_ocf_to_net_profit,
)
from src.analytics.ratios import (
    compute_pe_ratio,
    compute_pb_ratio,
    compute_roe,
)
from src.etl.loader import load_raw_data
from src.etl.normaliser import normalise_financial_data
from src.etl.validator import validate_financial_data


def process_financial_pipeline(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Executes validation, normalization, and analytical enrichments on raw dataset."""
    cleaned_df = validate_financial_data(raw_df)
    norm_df = normalise_financial_data(cleaned_df)

    if norm_df.empty:
        return norm_df

    # Calculate valuation and cash flow metrics if required columns exist
    if "price" in norm_df.columns and "eps" in norm_df.columns:
        norm_df["pe_ratio"] = norm_df.apply(
            lambda r: compute_pe_ratio(r["price"], r["eps"]), axis=1
        )

    if "price" in norm_df.columns and "book_value" in norm_df.columns:
        norm_df["pb_ratio"] = norm_df.apply(
            lambda r: compute_pb_ratio(r["price"], r["book_value"]), axis=1
        )

    if "net_income" in norm_df.columns and "shareholder_equity" in norm_df.columns:
        norm_df["roe"] = norm_df.apply(
            lambda r: compute_roe(r["net_income"], r["shareholder_equity"]),
            axis=1,
        )

    if "operating_cash_flow" in norm_df.columns and "capex" in norm_df.columns:
        norm_df["free_cash_flow"] = norm_df.apply(
            lambda r: compute_free_cash_flow(r["operating_cash_flow"], r["capex"]),
            axis=1,
        )

    if "operating_cash_flow" in norm_df.columns and "net_income" in norm_df.columns:
        norm_df["ocf_to_net_profit"] = norm_df.apply(
            lambda r: compute_ocf_to_net_profit(
                r["operating_cash_flow"], r["net_income"]
            ),
            axis=1,
        )

    return norm_df


def run_etl_job(input_path: str) -> pd.DataFrame:
    """End-to-end execution helper."""
    raw_df = load_raw_data(input_path)
    return process_financial_pipeline(raw_df)
