import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.dashboard.utils.db import get_companies, get_ratios

st.title("04 — Peer Comparison & Radar Analysis")

companies_df = get_companies()
ratios_df = get_ratios()

if companies_df.empty or ratios_df.empty:
    st.warning("No data found in database.")
    st.stop()

available_tickers = companies_df['nse_ticker'].tolist()
selected_tickers = st.multiselect(
    "Select Companies to Compare:",
    options=available_tickers,
    default=available_tickers[:2] if len(available_tickers) >= 2 else available_tickers
)

if not selected_tickers:
    st.info("Please select at least one company to display analysis.")
    st.stop()

filtered_ratios = ratios_df[ratios_df['ticker'].isin(selected_tickers)]

st.subheader("Metric Comparison Table")
st.dataframe(filtered_ratios, width='stretch')

st.subheader("Radar Comparison")

radar_metrics = ['roe_pct', 'roce_pct', 'net_margin_pct', 'revenue_cagr_5yr', 'composite_score']
labels = ['ROE %', 'ROCE %', 'Net Margin %', '5Y Rev CAGR', 'Composite Score']

fig = go.Figure()

for ticker in selected_tickers:
    comp_data = filtered_ratios[filtered_ratios['ticker'] == ticker]
    if not comp_data.empty:
        values = [comp_data[m].values[0] if m in comp_data.columns else 0 for m in radar_metrics]
        values.append(values[0])
        radar_labels = labels + [labels[0]]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=radar_labels,
            fill='toself',
            name=ticker
        ))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=True,
    height=500
)

st.plotly_chart(fig, width='stretch')
