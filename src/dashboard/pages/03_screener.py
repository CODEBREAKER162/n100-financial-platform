import streamlit as st
import pandas as pd
from src.dashboard.utils.db import get_companies, get_ratios

st.title("03 — Quantitative Stock Screener")

companies_df = get_companies()
ratios_df = get_ratios()

if companies_df.empty or ratios_df.empty:
    st.warning("No data available for screening.")
    st.stop()

# Merge ratios with company profile details
df = pd.merge(ratios_df, companies_df, on='company_id', how='left')

# Sidebar Filters
st.sidebar.header("Filter Criteria")

# Sector Filter
sectors = ["All"] + sorted(df['broad_sector'].dropna().unique().tolist())
selected_sector = st.sidebar.selectbox("Broad Sector", sectors)

# Score & Ratio Sliders
min_score, max_score = float(df['composite_score'].min()), float(df['composite_score'].max())
score_range = st.sidebar.slider("Composite Score Range", min_score, max_score, (min_score, max_score))

min_pe, max_pe = float(df['pe_ratio'].min()), float(df['pe_ratio'].max())
pe_range = st.sidebar.slider("P/E Ratio Range", min_pe, max_pe, (min_pe, max_pe))

min_roe = float(df['roe_pct'].min())
roe_filter = st.sidebar.slider("Minimum ROE (%)", min_roe, 50.0, 10.0)

max_de = st.sidebar.slider("Maximum Debt-to-Equity", 0.0, 5.0, 1.5)

# Apply Filters
filtered_df = df[
    (df['composite_score'] >= score_range[0]) & (df['composite_score'] <= score_range[1]) &
    (df['pe_ratio'] >= pe_range[0]) & (df['pe_ratio'] <= pe_range[1]) &
    (df['roe_pct'] >= roe_filter) &
    (df['debt_to_equity'] <= max_de)
]

if selected_sector != "All":
    filtered_df = filtered_df[filtered_df['broad_sector'] == selected_sector]

# Display Results
st.subheader(f"Screening Results ({len(filtered_df)} Companies Match)")

display_cols = [
    'company_id', 'company_name', 'broad_sector', 
    'composite_score', 'pe_ratio', 'roe_pct', 'roce_pct', 'debt_to_equity'
]

st.dataframe(
    filtered_df[display_cols].sort_values(by='composite_score', ascending=False),
    width='stretch'
)

# Export Functionality
csv_data = filtered_df[display_cols].to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Export Screened Results as CSV",
    data=csv_data,
    file_name="screened_stocks.csv",
    mime="text/csv"
)
