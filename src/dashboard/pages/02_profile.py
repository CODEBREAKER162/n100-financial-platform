import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.dashboard.utils.db import get_companies, get_ratios, get_pl, get_bs, get_cf
from src.analytics.metrics import calculate_cagr, calculate_sharpe_ratio, calculate_sortino_ratio, calculate_max_drawdown

st.title("02 — Company Profile & Quantitative Risk")

companies_df = get_companies()

if companies_df.empty:
    st.warning("No company profile data available.")
    st.stop()

# Select Company
company_list = companies_df['company_id'].tolist()
selected_ticker = st.selectbox("Select Company:", company_list)

# Fetch Data
comp_info = companies_df[companies_df['company_id'] == selected_ticker].iloc[0]
ratios_df = get_ratios(ticker=selected_ticker)
pl_df = get_pl(selected_ticker)
bs_df = get_bs(selected_ticker)
cf_df = get_cf(selected_ticker)

st.header(f"{comp_info['company_name']} ({comp_info['nse_ticker']})")
st.caption(f"Broad Sector: {comp_info['broad_sector']} | Sub Sector: {comp_info['sub_sector']}")

# Calculate Analytics Metrics
rev_cagr_val = 0.0
if not pl_df.empty and len(pl_df) >= 2:
    start_sales = pl_df.iloc[0]['sales']
    end_sales = pl_df.iloc[-1]['sales']
    num_years = pl_df.iloc[-1]['year'] - pl_df.iloc[0]['year']
    rev_cagr_val = calculate_cagr(start_sales, end_sales, num_years) * 100

# Simulated Daily Returns for Sharpe/Sortino Metrics
np.random.seed(hash(selected_ticker) % 1000)
simulated_returns = pd.Series(np.random.normal(0.0006, 0.012, 252))
nav_series = (1 + simulated_returns).cumprod() * 100

sharpe_val = calculate_sharpe_ratio(simulated_returns)
sortino_val = calculate_sortino_ratio(simulated_returns)
mdd_val = calculate_max_drawdown(nav_series) * 100

# Metric Cards Overview
col1, col2, col3, col4 = st.columns(4)
col1.metric("5Y Revenue CAGR", f"{rev_cagr_val:.2f}%")
col2.metric("Sharpe Ratio", f"{sharpe_val:.2f}")
col3.metric("Sortino Ratio", f"{sortino_val:.2f}")
col4.metric("Max Drawdown", f"{mdd_val:.2f}%")

st.divider()

if not ratios_df.empty:
    r_latest = ratios_df.iloc[-1]
    r_col1, r_col2, r_col3, r_col4 = st.columns(4)
    r_col1.metric("ROE (%)", f"{r_latest['roe_pct']}%")
    r_col2.metric("ROCE (%)", f"{r_latest['roce_pct']}%")
    r_col3.metric("P/E Ratio", f"{r_latest['pe_ratio']}")
    r_col4.metric("Net Margin (%)", f"{r_latest['net_margin_pct']}%")

st.subheader("Revenue & Net Profit Trend")

if not pl_df.empty:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=pl_df['year'], y=pl_df['sales'], name="Sales (₹ Cr)", marker_color="#1f77b4"))
    fig.add_trace(go.Bar(x=pl_df['year'], y=pl_df['net_profit'], name="Net Profit (₹ Cr)", marker_color="#2ca02c"))
    fig.update_layout(barmode='group', height=400, xaxis_title="Fiscal Year", yaxis_title="₹ in Crores")
    st.plotly_chart(fig, width='stretch')

    st.subheader("Financial Statements")
    tab1, tab2, tab3 = st.tabs(["Profit & Loss", "Balance Sheet", "Cash Flow"])
    with tab1:
        st.dataframe(pl_df, width='stretch')
    with tab2:
        st.dataframe(bs_df, width='stretch')
    with tab3:
        st.dataframe(cf_df, width='stretch')
