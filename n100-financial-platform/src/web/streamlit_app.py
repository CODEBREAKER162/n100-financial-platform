import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
from src.screener.pdf_generator import generate_pdf_report
from src.screener.engine import screen_stocks, generate_insights, cluster_stocks

st.set_page_config(
    page_title="N100 Financial Intelligence Platform",
    page_icon="📈",
    layout="wide"
)

st.title("📈 N100 Financial Intelligence Platform")
st.markdown("Filter, analyze, and screen Nifty 100 stocks with custom metrics and peer insights.")

tab1, tab2 = st.tabs(["📊 Screener & Analysis", "🤖 AI Peer Clustering"])

with tab1:
    st.sidebar.header("Screener Filters")

    show_all = st.sidebar.checkbox("Show All Stocks (Ignore Filters)", value=False)
    pe_max = st.sidebar.slider("Max P/E Ratio", min_value=5.0, max_value=100.0, value=50.0, step=1.0)
    roe_min = st.sidebar.slider("Min ROE (%)", min_value=0.0, max_value=50.0, value=10.0, step=1.0)
    preset = st.sidebar.selectbox("Preset Strategy", options=["None", "quality_compounder", "value_play"])

    filter_data = {}
    if not show_all:
        filter_data["max_pe"] = pe_max
        filter_data["min_roe"] = roe_min
        if preset != "None":
            filter_data["preset"] = preset

    st.subheader("Screening Results")

    try:
        results = screen_stocks(filter_data)

        if results:
            df = pd.DataFrame(results)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.success(f"Total Records Found: {len(df)}")
            with col2:
                csv_data = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📄 Export CSV",
                    data=csv_data,
                    file_name="nifty100_screened_results.csv",
                    mime="text/csv"
                )
            with col3:
                pdf_bytes = generate_pdf_report(df)
                st.download_button(
                    label="📕 Export PDF",
                    data=pdf_bytes,
                    file_name="nifty100_screening_report.pdf",
                    mime="application/pdf"
                )

            st.table(df, width="stretch")

            st.subheader("💡 Qualitative Insights & Pros/Cons")
            selected_symbol = st.selectbox("Select a stock for deep dive", df["symbol"].tolist())
            selected_stock = next(s for s in results if s["symbol"] == selected_symbol)
            
            insights = generate_insights(selected_stock)
            
            p_col, c_col = st.columns(2)
            with p_col:
                st.markdown("### ✅ Strengths")
                for pro in insights["pros"]:
                    st.write(f"- {pro}")
            with c_col:
                st.markdown("### ⚠️ Concerns")
                for con in insights["cons"]:
                    st.write(f"- {con}")

        else:
            st.warning("`screen_stocks()` returned no results. Check your filters or set 'Show All Stocks'.")

    except Exception as e:
        st.error(f"Error executing screen_stocks(): {e}")

with tab2:
    st.subheader("🤖 Stock Clustering Engine (K-Means Peer Grouping)")
    st.markdown("Groups stocks dynamically based on Valuation (P/E) and Profitability (ROE) metrics.")
    
    clusters_count = st.slider("Select Number of Clusters", min_value=2, max_value=5, value=3)
    clustered_df = cluster_stocks(n_clusters=clusters_count)
    
    st.markdown(clustered_df[["symbol", "company", "sector", "pe_ratio", "roe", "cluster_label"]].to_html(index=False), unsafe_allow_html=True)
    
    st.scatter_chart(
        clustered_df,
        x="pe_ratio",
        y="roe",
        color="cluster_label",
        size=None
    )
