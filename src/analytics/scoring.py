import pandas as pd
import numpy as np

def compute_composite_score(roe_pct, roce_pct, pe_ratio, debt_to_equity, net_margin_pct):
    """
    Computes a normalized Composite Fund Score (0 to 100) based on key financial metrics.
    """
    # 1. Profitability Score (Max 30 pts)
    roe_score = min(max(roe_pct / 20.0 * 15, 0), 15) if pd.notnull(roe_pct) else 0
    roce_score = min(max(roce_pct / 20.0 * 15, 0), 15) if pd.notnull(roce_pct) else 0
    profitability = roe_score + roce_score

    # 2. Valuation Score (Max 25 pts) - Lower P/E is better (within reasonable bounds)
    if pd.notnull(pe_ratio) and pe_ratio > 0:
        if pe_ratio <= 15:
            valuation = 25.0
        elif pe_ratio <= 35:
            valuation = 25.0 - ((pe_ratio - 15) / 20.0 * 15.0)
        else:
            valuation = max(10.0 - ((pe_ratio - 35) / 50.0 * 10.0), 2.0)
    else:
        valuation = 5.0

    # 3. Financial Health & Risk (Max 25 pts) - Lower Debt-to-Equity is better
    if pd.notnull(debt_to_equity):
        if debt_to_equity <= 0.5:
            health = 25.0
        elif debt_to_equity <= 1.5:
            health = 25.0 - ((debt_to_equity - 0.5) * 15.0)
        else:
            health = max(10.0 - ((debt_to_equity - 1.5) * 5.0), 0.0)
    else:
        health = 10.0

    # 4. Margin Quality (Max 20 pts)
    margin_score = min(max(net_margin_pct / 15.0 * 20, 0), 20) if pd.notnull(net_margin_pct) else 0

    total_score = profitability + valuation + health + margin_score
    return round(total_score, 2)
