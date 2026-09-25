import os
import pandas as pd

def export_screener_results(preset_results: dict, output_path: str = "output/screener_output.xlsx"):
    """Exports preset screener results into multi-sheet Excel file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for preset_name, df in preset_results.items():
            df.to_excel(writer, sheet_name=preset_name[:31], index=False)

def export_peer_comparison(peer_results: dict, output_path: str = "output/peer_comparison.xlsx"):
    """Exports peer comparison percentiles into 11 peer-group sheets."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for group_name, df in peer_results.items():
            df.to_excel(writer, sheet_name=group_name[:31], index=False)
