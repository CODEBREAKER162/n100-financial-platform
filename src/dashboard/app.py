import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Nifty 100 Financial Intelligence Platform")
st.sidebar.success("Select a screen above.")

st.write("""
Welcome to the N100 Financial Intelligence Platform. Use the sidebar to navigate across the 8 dashboard screens:
- **01 Home**: Summary KPI tiles and Sector Breakdown
- **02 Profile**: Detailed Company Financial Health
- **03 Screener**: Multi-metric Custom Screener & Presets
- **04 Peers**: Peer Comparison & Radar Charts
- **05 Trends**: 10-Year Metric Trend Overlays
- **06 Sectors**: Sector Performance & Bubble Analysis
- **07 Capital**: Capital Allocation Treemap
- **08 Reports**: Annual Reports & Links
""")
