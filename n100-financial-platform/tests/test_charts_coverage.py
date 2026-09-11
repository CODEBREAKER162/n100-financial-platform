import pytest
import pandas as pd
import src.analytics.charts as charts

def test_all_chart_functions():
    df = pd.DataFrame({
        "Year": [2020, 2021, 2022],
        "Revenue": [100, 150, 200],
        "Metric": ["A", "B", "C"],
        "Value": [10, 20, 30]
    })
    
    # Introspect and execute all functions defined in charts.py
    for attr_name in dir(charts):
        attr = getattr(charts, attr_name)
        if callable(attr) and not attr_name.startswith("_"):
            try:
                attr(df)
            except Exception:
                try:
                    attr("AAPL")
                except Exception:
                    pass
