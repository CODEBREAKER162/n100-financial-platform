import streamlit as st
import pandas as pd
import plotly.express as px
from src.dashboard.utils.db import get_companies, get_ratios

st.title("01 — Executive Overview")

companies_df = get_companies()
ratios_df = get_ratios()

if companies_df.empty or ratios_df.empty:
    st.warning("Database contains no entries or is disconnected.")
    st.stop()

merged_df = pd.merge(ratios_df, companies_df, on='company_id', how='left')

# High-Level Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tracked Universe", f"{len(companies_df)} Stocks")
col2.metric("Avg Universe ROE", f"{ratios_df['roe_pct'].mean():.2f}%")
col3.metric("Avg Universe ROCE", f"{ratios_df['roce_pct'].mean():.2f}%")
col4.metric("Avg Universe P/E", f"{ratios_df['pe_ratio'].mean():.2f}x")

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top Fund Scorecards")
    top_stocks = merged_df.sort_values(by='composite_score', ascending=False).head(5)
    st.dataframe(
        top_stocks[['company_id', 'company_name', 'broad_sector', 'composite_score']],
        width='stretch'
    )

with col_right:
    st.subheader("Sector Breakdown")
    sector_counts = companies_df['broad_sector'].value_counts().reset_index()
    sector_counts.columns = ['Broad Sector', 'Count']
    fig = px.pie(sector_counts, names='Broad Sector', values='Count', hole=0.4)
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, width='stretch')
