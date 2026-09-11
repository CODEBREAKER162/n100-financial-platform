import pandas as pd

PRESETS = {
    "value_stocks": lambda df: df[df["pe_ratio"] < 15] if "pe_ratio" in df.columns else df
}

def screen_stocks(*args, **kwargs):
    return []

def filter_financial_ratios(df, **kwargs):
    if df is None or df.empty:
        return pd.DataFrame()
    filtered = df.copy()
    for col, val in kwargs.items():
        if col in filtered.columns and val is not None:
            filtered = filtered[filtered[col] >= val]
    return filtered

def apply_preset_screener(df, preset_key):
    if df is None or df.empty:
        return pd.DataFrame()
    if preset_key not in PRESETS:
        return df
    return PRESETS[preset_key](df)

class ScreenerEngine:
    def __init__(self, data_filepath=None):
        self.data_filepath = data_filepath

    def run_preset(self, preset_key, df=None):
        if df is None:
            return []
        return apply_preset_screener(df, preset_key)
